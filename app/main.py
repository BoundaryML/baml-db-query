from baml_client import b
import asyncio


async def main():
    testQuestion = "What are the top 10 most popular products in the database?"
    testSchema = """
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
"""
    result = b.SelectRelevantTables(testQuestion, testSchema)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
