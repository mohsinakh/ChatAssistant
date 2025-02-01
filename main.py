import sqlite3
import spacy
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

# FastAPI app instance
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load spaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Database file
db_file = "database.db"

# Create database and tables (same as before)
def create_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables with additional columns
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Salary INTEGER NOT NULL,
            Hire_Date TEXT NOT NULL,
            Email TEXT NOT NULL,
            Phone TEXT NOT NULL,
            Job_Title TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Manager TEXT NOT NULL,
            Budget INTEGER NOT NULL
        );
    """)
    
    # Insert Data (Only if no data exists to prevent duplication)
    employees = [
        (1, 'Alice', 'Sales', 50000, '2021-01-15', 'alice@sales.com', '555-1234', 'Sales Manager'),
        (2, 'Bob', 'Engineering', 70000, '2020-06-10', 'bob@eng.com', '555-5678', 'Software Engineer'),
        (3, 'Charlie', 'Marketing', 60000, '2022-03-20', 'charlie@marketing.com', '555-8765', 'Marketing Specialist'),
        (4, 'David', 'Sales', 55000, '2021-02-25', 'david@sales.com', '555-4321', 'Sales Associate'),
        (5, 'Eve', 'Engineering', 75000, '2019-11-10', 'eve@eng.com', '555-1357', 'Senior Software Engineer'),
        (6, 'Frank', 'Marketing', 65000, '2023-01-05', 'frank@marketing.com', '555-2468', 'Marketing Manager')
    ]
    
    departments = [
        (1, 'Sales', 'Alice', 200000),
        (2, 'Engineering', 'Bob', 500000),
        (3, 'Marketing', 'Charlie', 150000)
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)", employees)
    cursor.executemany("INSERT OR IGNORE INTO Departments VALUES (?, ?, ?, ?)", departments)

    conn.commit()
    conn.close()

# Call database creation function
create_database()

# Pydantic model for query
class QueryRequest(BaseModel):
    query: str

# Extract department from query
def extract_department(query: str):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
            return ent.text.capitalize()
    
    for word in ["Sales", "Engineering", "Marketing"]:
        if word.lower() in query.lower():
            return word
    return None

# Extract date from query
def extract_date(query: str):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text
    return None

# Process user query
def process_query(user_query: str):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        user_query = user_query.lower()

        # Extract department
        department = extract_department(user_query)

        if "employees" in user_query and department:
            cursor.execute("SELECT Name FROM Employees WHERE Department = ?", (department,))
            result = cursor.fetchall()
            return [row[0] for row in result] if result else "No employees found."

        elif "manager" in user_query and department:
            cursor.execute("SELECT Manager FROM Departments WHERE Name = ?", (department,))
            result = cursor.fetchone()
            return result[0] if result else "Department not found."

        elif "hired after" in user_query:
            date = extract_date(user_query)
            if date:
                cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
                result = cursor.fetchall()
                return [row[0] for row in result] if result else "No employees found."
            else:
                return "Invalid date format. Use YYYY-MM-DD."

        elif "salary expense" in user_query and department:
            cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
            result = cursor.fetchone()
            return f"Total salary expense for {department}: {result[0]}" if result and result[0] else "No data available."

        else:
            return "Unsupported query. Try another question."

    except Exception as e:
        return f"Error processing query: {str(e)}"
    finally:
        conn.close()

@app.post("/query")
async def chat_assistant(request: QueryRequest):
    response = process_query(request.query)
    return {"response": response}

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

