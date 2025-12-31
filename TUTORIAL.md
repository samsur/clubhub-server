# Building a REST API with Python, Flask, and SQLite - Step by Step Tutorial

Welcome! In this tutorial, you'll learn how to build a simple REST API from scratch. By the end, you'll have a working backend that can store and retrieve club data.

## What You'll Build

A REST API with these endpoints:

- GET `/clubs` - Get all clubs
- GET `/clubs/<id>` - Get a specific club
- POST `/clubs` - Create a new club
- DELETE `/clubs/<id>` - Delete a club

## Prerequisites

- Python 3.x or higher installed
- Basic understanding of Python
- A code editor (VS Code, PyCharm, etc.)
- A terminal/command prompt

## Step 1: Create Your Project Folder

First, create a folder for your project and navigate into it.

**On Windows (Command Prompt or PowerShell), Mac, or Linux:**

```bash
mkdir ClubHubServer
cd ClubHubServer
```

**Note:** The `mkdir` (make directory) and `cd` (change directory) commands work the same on all operating systems!

## Step 2: Set Up Dependencies

Create a file called `requirements.txt` with the following content:

```
Flask==3.0.0
flask-cors==4.0.0
```

**What are these?**

- **Flask**: A lightweight web framework for Python
- **flask-cors**: Enables Cross-Origin Resource Sharing (allows your frontend to talk to your backend)

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Step 3: Create Your Main Application File

Create a file called `app.py`. We'll build this step by step.

### Step 3.1: Import Required Libraries

```python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
```

**What do these imports do?**

- `sqlite3`: Built-in Python library for SQLite database
- `Flask, request, jsonify`: Core Flask components for building web APIs
- `CORS`: Handles cross-origin requests

### Step 3.2: Initialize Flask App

```python
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

### Step 3.3: Set Up Database Connection

```python
# Database file
DATABASE = 'clubs.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to get results as dictionaries
    return conn
```

**What's happening here?**

- `DATABASE`: Name of our SQLite database file
- `get_db_connection()`: Function that creates a connection to the database
- `row_factory`: Allows us to access database rows like dictionaries

### Step 3.4: Initialize the Database

```python
def init_db():
    """Initialize the database with the club table"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS club (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            memberCount INTEGER DEFAULT 0,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
```

**What does this do?**

- Creates a table called `club` with 5 fields
- `id`: Auto-incrementing unique identifier
- `name`: Required text field
- `description`, `memberCount`, `image`: Optional fields

### Step 3.5: Create GET Endpoint for All Clubs

```python
@app.route('/clubs', methods=['GET'])
def get_clubs():
    """GET endpoint to retrieve all clubs"""
    try:
        conn = get_db_connection()
        clubs = conn.execute('SELECT * FROM club').fetchall()
        conn.close()

        # Convert rows to dictionaries
        clubs_list = [dict(club) for club in clubs]

        return jsonify(clubs_list), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

**What's happening here?**

- `@app.route('/clubs', methods=['GET'])`: Decorator that defines the endpoint
- `SELECT * FROM club`: SQL query to get all clubs
- `[dict(club) for club in clubs]`: Converts database rows to dictionaries
- `jsonify()`: Converts Python data to JSON format
- `200`: HTTP status code for success
- `500`: HTTP status code for server error

### Step 3.6: Create GET Endpoint for Single Club

```python
@app.route('/clubs/<int:club_id>', methods=['GET'])
def get_club(club_id):
    """GET endpoint to retrieve a single club by ID"""
    try:
        conn = get_db_connection()
        club = conn.execute('SELECT * FROM club WHERE id = ?', (club_id,)).fetchone()
        conn.close()

        if club is None:
            return jsonify({
                'success': False,
                'error': 'Club not found'
            }), 404

        return jsonify({
            'success': True,
            'club': dict(club)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

**Key points:**

- `<int:club_id>`: URL parameter that must be an integer
- `WHERE id = ?`: SQL query with parameter (prevents SQL injection)
- `404`: HTTP status code for "not found"

### Step 3.7: Create POST Endpoint to Add Clubs

```python
@app.route('/clubs', methods=['POST'])
def create_club():
    """POST endpoint to create a new club"""
    try:
        # Get data from request body
        data = request.get_json()

        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400

        name = data.get('name')
        description = data.get('description', '')
        member_count = data.get('memberCount', 0)
        image = data.get('image', '')

        # Insert into database
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO club (name, description, memberCount, image) VALUES (?, ?, ?, ?)',
            (name, description, member_count, image)
        )
        conn.commit()
        club_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Club created successfully',
            'club_id': club_id
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

**Key points:**

- `request.get_json()`: Extracts JSON data from the request body
- `data.get('name')`: Safely gets a value from the dictionary
- `INSERT INTO`: SQL query to add new data
- `lastrowid`: Gets the ID of the newly created record
- `201`: HTTP status code for "created"
- `400`: HTTP status code for "bad request"

### Step 3.8: Create DELETE Endpoint

```python
@app.route('/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    """DELETE endpoint to delete a club by ID"""
    try:
        conn = get_db_connection()

        # Check if club exists
        club = conn.execute('SELECT * FROM club WHERE id = ?', (club_id,)).fetchone()

        if club is None:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Club not found'
            }), 404

        # Delete the club
        conn.execute('DELETE FROM club WHERE id = ?', (club_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Club deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Step 3.9: Create Home Endpoint

```python
@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'Welcome to Club Hub API!',
        'endpoints': {
            'GET /clubs': 'Get all clubs',
            'GET /clubs/<id>': 'Get a specific club by ID',
            'POST /clubs': 'Create a new club (requires: name, optional: description, memberCount, image)',
            'DELETE /clubs/<id>': 'Delete a club by ID'
        }
    })
```

### Step 3.10: Run the Application

```python
if __name__ == '__main__':
    # Initialize database when app starts
    init_db()

    # Run the Flask app
    print("Starting Club Hub Server...")
    print("Visit http://localhost:5000 to see the API")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**What does this do?**

- `if __name__ == '__main__'`: Only runs if this file is executed directly
- `init_db()`: Creates the database and table
- `app.run()`: Starts the Flask development server
- `debug=True`: Enables debug mode (auto-reload on code changes)
- `host='0.0.0.0'`: Makes server accessible from other devices
- `port=5000`: Server runs on port 5000

## Step 4: Run Your Server

In your terminal, run:

```bash
python app.py
```

You should see:

```
Database initialized successfully!
Starting Club Hub Server...
Visit http://localhost:5000 to see the API
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## Step 5: Test Your API

### Test 1: Check the Home Page

Open your browser and go to:

```
http://localhost:5000/
```

You should see a JSON response with API information.

### Test 2: Get All Clubs (Empty at First)

In your browser:

```
http://localhost:5000/clubs
```

You should see an empty array: `[]`

### Test 3: Create a Club

**Windows PowerShell:**

```powershell
Invoke-RestMethod -Uri http://localhost:5000/clubs -Method Post -ContentType "application/json" -Body '{"name": "Coding Club", "description": "Learn to code together", "memberCount": 50, "image": "https://example.com/coding.jpg"}'
```

**Linux/Mac:**

```bash
curl -X POST http://localhost:5000/clubs \
  -H "Content-Type: application/json" \
  -d '{"name": "Chess Club", "description": "Learn and play chess with fellow enthusiasts!", "memberCount": 75, "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=400&h=300&fit=crop"}'
```

You should see:

```json
{
  "success": true,
  "message": "Club created successfully",
  "club_id": 1
}
```

### Test 4: Get All Clubs Again

Refresh `http://localhost:5000/clubs` in your browser.

You should now see your club:

```json
[
  {
    "id": 1,
    "name": "Coding Club",
    "description": "Learn to code together",
    "memberCount": 50,
    "image": "https://example.com/coding.jpg"
  }
]
```

### Test 5: Get Single Club

Visit: `http://localhost:5000/clubs/1`

### Test 6: Delete a Club

**Windows PowerShell:**

```powershell
Invoke-RestMethod -Uri http://localhost:5000/clubs/1 -Method Delete
```

**Linux/Mac:**

```bash
curl -X DELETE http://localhost:5000/clubs/1
```

## Understanding Key Concepts

### 1. REST API

REST (Representational State Transfer) is a way to design APIs. It uses HTTP methods:

- **GET**: Retrieve data
- **POST**: Create new data
- **PUT/PATCH**: Update data
- **DELETE**: Delete data

### 2. HTTP Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request (client error)
- **404**: Not Found
- **500**: Internal Server Error

### 3. JSON

JavaScript Object Notation - a lightweight data format:

```json
{
  "name": "Coding Club",
  "memberCount": 50
}
```

### 4. SQLite

A lightweight database that stores data in a single file. Perfect for small projects and prototypes.

### 5. CORS

Cross-Origin Resource Sharing allows your frontend (running on port 4200) to talk to your backend (running on port 5000).

## Common Issues and Solutions

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Solution:** Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=3000)  # Changed to 3000
```

### Issue 2: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Issue 3: Database Locked

**Error:** `database is locked`

**Solution:** Make sure you're closing database connections:

```python
conn.close()  # Always close connections!
```

## Next Steps

Congratulations! You've built a working REST API. Here are some ways to extend it:

1. **Add UPDATE endpoint**: Allow users to modify club information
2. **Add validation**: Check that memberCount is a positive number
3. **Add search**: Filter clubs by name or description
4. **Add pagination**: Return clubs in pages (e.g., 10 at a time)
5. **Add authentication**: Require login to create/delete clubs
6. **Connect to a frontend**: Build an Angular/React app that uses this API
7. **Deploy it**: Put your API online using Render, Railway, or Heroku

## Complete Code

Your final `app.py` should have approximately 170 lines and contain all the functions we built above.

## Tips for Hackathons

1. **Start simple**: Get the basic CRUD (Create, Read, Update, Delete) working first
2. **Test as you go**: Don't wait until the end to test your code
3. **Use debug mode**: Flask's debug mode shows helpful error messages
4. **Read error messages**: They usually tell you exactly what's wrong
5. **Google is your friend**: Copy error messages and search for solutions
6. **Ask for help**: Don't spend hours stuck on one problem

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- REST API Tutorial: https://restfulapi.net/
- HTTP Status Codes: https://httpstatuses.com/

Good luck with your hackathon project!
