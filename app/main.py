import asyncio
import json
from typing import Dict, TypedDict

from colorama import Fore, Style, init
from baml_client import b
from baml_client.types import IrrelevantQuestion

# Initialize Colorama with auto-reset
init(autoreset=True)

class TableMetadata(TypedDict):
    description: str
    columns: Dict[str, str]

# Added helper function for printing a divider line
def print_divider():
    print(Fore.MAGENTA + "-" * 50 + Style.RESET_ALL)

async def main():
    default_question = "What are the top 10 most popular products in the database?"
    user_question = input(f"{Fore.CYAN}Enter your question (default: '{default_question}'): {Style.RESET_ALL}") or default_question

    schema: Dict[str, TableMetadata] = {
        "users": {
            "description": "store users and their information",
            "columns": {
                "id": "unique user identifier",
                "name": "user's full name",
                "email": "user's email address",
                "created_at": "timestamp of user creation",
            },
        },
        "orders": {
            "description": "store orders and their status",
            "columns": {
                "id": "unique order identifier",
                "user_id": "reference to users table",
                "cart_id": "reference to cart table",
                "total_amount": "total order amount",
                "status": "order status (pending/completed)",
                "created_at": "timestamp of order creation",
            },
        },
        "inventory": {
            "description": "store inventory information",
            "columns": {
                "product_id": "reference to products table",
                "quantity": "available quantity",
            },
        },
        "cart": {
            "description": "store cart information",
            "columns": {
                "id": "unique cart identifier",
                "user_id": "reference to users table",
                "product_id": "reference to products table",
                "quantity": "quantity in cart",
            },
        },
        "products": {
            "description": "store products and their information",
            "columns": {
                "id": "unique product identifier",
                "name": "product name",
                "price": "product price",
                "category_id": "reference to categories table",
            },
        },
        "categories": {
            "description": "store product categories",
            "columns": {
                "id": "unique category identifier",
                "name": "category name",
            },
        },
    }

    # Use the helper function to print dividers and update colors
    print_divider()
    print(f"{Style.DIM}{Fore.WHITE}Question:{Style.RESET_ALL}", user_question)
    print_divider()
    print(f"{Style.DIM}{Fore.WHITE}Selecting Relevant Tables...{Style.RESET_ALL}")

    # Ask the model to select the relevant tables (or identify that the question is not relevant to the tables)
    relevant_tables = b.SelectRelevantTables(user_question, json.dumps(schema))

    # Handle the case where the question is not relevant to the tables
    if isinstance(relevant_tables, IrrelevantQuestion):
        print(f"{Fore.RED}Sorry, I can't help with that question.{Style.RESET_ALL}")
        print(f"{Style.DIM}{Fore.WHITE}Reason:{Style.RESET_ALL}", relevant_tables.reason)
        return
    elif not relevant_tables:
        # Handle no tables being selected
        print(f"{Fore.RED}Sorry, I can't help with that question.{Style.RESET_ALL}")
        return

    # Display the selected tables and columns
    for table in relevant_tables:
        # Print table name in light green for better prominence
        print(f"{Style.DIM}{Fore.WHITE}Table Selected:{Style.RESET_ALL}", table.tableName)
        for column in table.columns:
            # Print each column in muted style
            print(f"{Style.DIM}{Fore.WHITE}  - {column}{Style.RESET_ALL}")

    # Filter out tables and columns that are not in the relevant_tables
    useful_tables = {
        table.tableName: {
            "columns": {
                column: schema[table.tableName]["columns"][column]
                for column in schema[table.tableName]["columns"]
                if column in table.columns
            }
        }
        for table in relevant_tables
    }

    print_divider()
    print(f"{Style.DIM}{Fore.WHITE}Generating SQL Query...{Style.RESET_ALL}")

    # Ask the model to generate the SQL query
    result = b.GenerateSQLQuery(user_question, json.dumps(useful_tables))

    # Display the generated SQL query
    print(f"{Style.DIM}{Fore.WHITE}Query:{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}{result.query}{Style.RESET_ALL}")
    print_divider()

if __name__ == "__main__":
    asyncio.run(main())
