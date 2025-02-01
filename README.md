# ajackus-task1

---

# FastAPI with SQLite and spaCy

This project is a FastAPI-based web application that connects to an SQLite database, processes natural language queries, and responds based on the database content. The app also uses the spaCy library for Named Entity Recognition (NER) to extract information like departments and dates from user queries.

### Features
- **SQLite Database**: Stores data about employees and departments.
- **spaCy NLP**: Extracts departments and dates from user queries to help generate database queries.
- **FastAPI**: Used to create the API endpoints for processing user queries.
- **Jinja2 Templates**: Renders HTML frontend to interact with the app.
  
### Project Structure
```
my-fastapi-app/
├── app.py               # FastAPI application code
├── templates/           # Directory for Jinja2 templates (HTML)
│   └── index.html       # The main HTML interface
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel configuration
├── vercel-build.sh      # Script to download spaCy model on Vercel build
└── runtime.txt          # Python version configuration for Vercel
```

---

### Prerequisites

Before you start, you need to have the following installed:
- **Python** (3.9 or later)
- **pip** (Python's package manager)
- **Vercel account** (for deployment)
- **Git** (for version control and pushing to Vercel)

### Setup

Follow these steps to set up and run the FastAPI app locally or deploy it to Vercel.

---

## 1. Install Dependencies

First, install the required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install:
- `FastAPI`: The web framework.
- `uvicorn`: ASGI server to run FastAPI locally.
- `spaCy`: NLP library for natural language processing.
- `sqlite3`: SQLite database.
- `jinja2`: For rendering HTML templates.

Additionally, spaCy's `en_core_web_sm` model will be downloaded when deploying to Vercel.

---

## 2. Running the App Locally

To run the FastAPI app locally, use the following command:

```bash
uvicorn app:app --reload
```

This will start the FastAPI server at `http://127.0.0.1:8000`. Open your browser and navigate to this URL to access the app.

You can also use the `/query` endpoint to interact with the API. To make a POST request to `/query`, use tools like `curl`, Postman, or Python's `requests` library. Here's an example using `curl`:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/query' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "List all employees in the Sales department"
}'
```

---

## 3. Deployment on Vercel

### Step-by-Step Vercel Deployment

1. **Ensure Vercel CLI is Installed**

   If you haven't installed the Vercel CLI, do so by running the following command:

   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**

   Log into your Vercel account:

   ```bash
   vercel login
   ```

3. **Prepare for Deployment**

   Your project is ready for deployment once you've set up the `vercel.json` and `vercel-build.sh` files as described below:

   - **`vercel.json`**: Configures the deployment settings for Vercel, including build hooks and routing.
   - **`vercel-build.sh`**: Downloads the spaCy model (`en_core_web_sm`) during the build process on Vercel.

4. **Deploy to Vercel**

   Run the following command to deploy your app to Vercel:

   ```bash
   vercel --prod
   ```

   Follow the prompts to link your project to Vercel if you haven't done so already.

Once the deployment is complete, Vercel will provide a URL to access your deployed app.

---

## 4. Folder Structure Breakdown

### **app.py**

The main FastAPI application that contains:
- A database setup and query processing logic.
- API endpoints:
  - `/query`: Accepts user queries and returns responses based on the database.
  - `/`: Renders the HTML frontend.

### **templates/index.html**

This file contains the basic HTML interface that is rendered when the app is accessed. The frontend allows users to input queries and view the results.

### **static/**

This directory holds static files like CSS and JavaScript. You can add additional styling or functionality to the frontend here.

### **vercel.json**

Configures the Vercel deployment, specifying the use of Python, build duration, and routes.

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxDuration": 60
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.9"
  },
  "hooks": {
    "build": "sh vercel-build.sh"
  }
}
```

### **vercel-build.sh**

This script downloads the spaCy model (`en_core_web_sm`) during the build process. It is executed when the Vercel build happens to ensure the model is installed:

```bash
#!/bin/bash

# Install spaCy model
python -m spacy download en_core_web_sm
```

### **requirements.txt**

This file lists all the Python dependencies for the app, which include:
- `fastapi`
- `uvicorn`
- `spacy`
- `sqlite3`
- `jinja2`

### **runtime.txt**

Specifies the Python version to use on Vercel (e.g., `python-3.11`).

---

## 5. Common Issues & Solutions

- **spaCy model not found**: Ensure that the `vercel-build.sh` script is correctly downloading the model during the build process. If you encounter issues, check the build logs on Vercel.
- **Database errors**: SQLite might not be ideal for production deployments as Vercel is a serverless platform. You may consider moving to a cloud database service like PostgreSQL or MongoDB for larger applications.
- **FastAPI is slow**: Serverless functions can experience cold starts. If this is a concern, consider optimizing your app or moving to a different deployment platform with persistent servers.

---

## Conclusion

This FastAPI app demonstrates how to build a web service that integrates natural language processing with a database. By using spaCy for NLP and SQLite for data storage, you can process user queries and return meaningful results.


--- 
