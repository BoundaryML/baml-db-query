// At this point we know the tables and columns.
// Note that we could also give this LLM function the type of DB this is (postgres, mysql, etc) to generate different kinds of queries.

class GeneratedQuery {
  query string @description("The SQL query that answers the user's question")
  explanation string @description("Brief explanation of how the query works")
}

function GenerateSQLQuery(
  userQuestion: string, 
  schemaDescription: string
) -> GeneratedQuery {
  client GPT4o
  prompt #"
    Generate a SQL query to answer the user's question using only the provided relevant tables and columns.
    Ensure the query is efficient and follows SQL best practices.

    The schema description is provided for additional context about data types and relationships.
    Only use tables and columns that were specifically identified as relevant.

    {{ ctx.output_format }}

    User Question: {{ userQuestion }}

    Tables:
    {{ schemaDescription }}
  "#
}


test BasicQueryTest {
  functions [GenerateSQLQuery]
  args {
    userQuestion #"
      What are the top 10 most popular products in the database?
    "#
    schemaDescription #"
      {
        "products": {
          "columns": {
            "id": "unique product identifier",
            "name": "product name"
          }
        },
        "orders": {
          "columns": {
            "product_id": "reference to products table",
            "quantity": "number of items ordered"
          }
        }
      }
    "#
  }
}

