

# Setting up the FastAPI project (Macbook Air M1)

## 1.  Create a virtual environment

Open you terminal and type:

```bash
python3 -m venv apienv
```

## 2. Activate the virtual environment

(Note: Once activated, your terminal prompt will change to show `(apienv)` indicating you're inside the virtual environment.)

```bash
source apienv/bin/activate
```

## 3. Install the required packages

```python
pip3 install "fastapi[all]" uvicorn sqlalchemy psycopg2-binary asyncpg
```

## 4. Run the FastAPI application

```python
uvicorn app.main:app --reload
```

# Working on the project

<aside>
💡 Tip: For a quicker start, you can combine the two commands below:

```bash
source apienv/bin/activate && uvicorn app.main:app --reload
```

</aside>

To work on the project or run the server later on, make sure you're in the correct project directory and follow these steps:

## 1. Activate the virtual environment

```bash
source apienv/bin/activate
```

## 2. Run the FastAPI application

```python
uvicorn main:app --reload
```

# Migrating database with Alembic

This is how you update the postgres database

```bash
alembic revision --autogenerate -m "Description of update"
alembic upgrade head
```