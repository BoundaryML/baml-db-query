class TableMetadata {
  // reason string @description("Brief explanation of why this table and these columns are relevant")

  tableName string @description("Name of the selected table")
  columns string[] @description("Names of relevant columns from this table")
}

template_string ChainOfThought #"
  Before you answer, add your thinking in <think> </think> tags, to help you figure out why each table and column is relevant to the question.
"#

function SelectRelevantTables(userQuestion: string, schemaDescription: string) -> TableMetadata[] {
  client GPT4o
  prompt #"
    Given a JSON description of multiple database tables and their columns, select the most relevant tables and columns that would be needed to construct a SQL query.

    Only select tables and columns that are directly relevant. Explain briefly why each selected table is relevant.

    {{ ctx.output_format }}

    {{ _.role("user") }} {{ schemaDescription }}
  "#
}

// Note: we may want to make the schema description include the type of each column (float, int, etc, just for additional context).
test BasicSchemaTest {
  functions [SelectRelevantTables]
  args {
    userQuestion #"
      What are the top 10 most popular products in the database?
    "#
    schemaDescription #"
      {
        "users": {
          "columns": {
            "id": "unique user identifier",
            "name": "user's full name",
            "email": "user's email address",
            "created_at": "timestamp of user creation"
          }
        },
        "orders": {
          "columns": {
            "id": "unique order identifier",
            "user_id": "reference to users table",
            "total_amount": "total order amount",
            "status": "order status (pending/completed)"
          }
        }
      }
    "#
  }
}

test ComplexSchemaTest {
  functions [SelectRelevantTables]
  args {
    userQuestion #"
      What is the current stock level of the top-selling products in each category?
    "#
    schemaDescription #"
      {
        "products": {
          "columns": {
            "id": "unique product identifier",
            "name": "product name",
            "price": "product price",
            "category_id": "reference to categories table"
          }
        },
        "categories": {
          "columns": {
            "id": "unique category identifier",
            "name": "category name"
          }
        },
        "inventory": {
          "columns": {
            "product_id": "reference to products table",
            "quantity": "available quantity",
            "warehouse_id": "storage location"
          }
        }
      }
    "#
  }
}