# BAML Demo

This repository contains demo code showcasing the BAML library. The demo demonstrates how to:

- Select relevant tables from a SQL schema based on a user query.
- Generate a SQL query based on the selected tables and columns.
- Use chain-of-thought prompts to help the model decide which tables and columns are relevant.

## Overview

There are two main components in this demo:

1. **`app/main.py`**  
   This Python script performs the following:
   - Prompts the user for a SQL-related question (with an option to use a default).
   - Uses the BAML library to select relevant tables and columns based on the given question.
   - Filters the SQL schema to include only the relevant parts.
   - Requests the model to generate an SQL query.
   - Displays the selected tables, columns, and the generated SQL query with formatted colored output.

2. **`app/baml_src/extract-tables.baml`**  
   This BAML file defines:
   - A schema for table metadata.
   - A function to select relevant tables from the provided schema based on the user's question.
   - Testing blocks to verify the selection process for different queries.

## Prerequisites

- Python 3.7 or later.
- The [BAML client library](#) installed and properly configured.
- Dependencies such as `colorama`. You can install them via pip manually or through a `requirements.txt` if available.

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BoundaryML/baml-db-query.git
   cd baml-db-query
   ```

2. **Install Dependencies**

    > consider using a virtual environment
    >
    > `python -m venv venv`
    >
    > `source venv/bin/activate`


   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the BAML**

    Convert from `*.baml` to `*.py` using the following command:

    ```bash
    baml-cli generate
    ```

    You should now see a directory called `baml_client`.

    > Alternatively, you can save any `.baml` file while you have the BAML VSCode/Cursor extension and that will run the command for you.

4. **Set Up the Environment**

   - Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.

   ```bash
   export OPENAI_API_KEY=<your-api-key>
   ```

## Running the Demo

Run the demo using the following command:

```bash
BAML_LOG=warn python app/main.py
```

## Example Output

### Default question

```bash
BAML_LOG=warn python app/main.py
Enter your question (default: 'What are the top 10 most popular products in the database?'): What are the top 10 most popular products in the database?
--------------------------------------------------
Question: What are the top 10 most popular products in the database?
--------------------------------------------------
Selecting Relevant Tables...
Table Selected: cart
  - product_id
  - quantity
Table Selected: products
  - id
  - name
--------------------------------------------------
Generating SQL Query...
Query:
SELECT p.name, SUM(c.quantity) AS total_quantity FROM products p JOIN cart c ON p.id = c.product_id GROUP BY p.id, p.name ORDER BY total_quantity DESC LIMIT 10;
--------------------------------------------------
```

### Unrelated question

```bash
BAML_LOG=warn python app/main.py
Enter your question (default: 'What are the top 10 most popular products in the database?'): how old is obama
--------------------------------------------------
Question: how old is obama
--------------------------------------------------
Selecting Relevant Tables...
Sorry, I can't help with that question.
Reason: The question is not relevant to the tables as it pertains to the age of a public figure, Barack Obama, which is not related to the database schema provided.
```

Feel free to explore and modify the demo to better understand and showcase the capabilities of BAML.