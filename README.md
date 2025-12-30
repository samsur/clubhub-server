# Club Hub Server - Simple REST API with SQLite

A dead-simple Python REST API for managing clubs using Flask and SQLite. Perfect for hackathon projects!

## Features

- SQLite database (no setup required!)
- GET endpoint to retrieve clubs
- POST endpoint to create clubs
- CORS enabled (works with Angular/React/Vue frontends!)
- Minimal dependencies (just Flask!)
- Easy to understand code

## Installation

1. **Install Python** (if you haven't already)
   - Download from [python.org](https://python.org)
   - Make sure Python 3.7+ is installed

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Simply run:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Get All Clubs
**GET** `/clubs`

Returns all clubs in the database.

**Example:**
```bash
curl http://localhost:5000/clubs
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Coding Club",
    "description": "Learn to code together",
    "memberCount": 50,
    "image": "https://example.com/image.jpg"
  }
]
```

### 2. Get Single Club
**GET** `/clubs/<id>`

Returns a specific club by ID.

**Example:**
```bash
curl http://localhost:5000/clubs/1
```

### 3. Create a Club
**POST** `/clubs`

Creates a new club.

**Required Fields:**
- `name` (string)

**Optional Fields:**
- `description` (string)
- `memberCount` (number)
- `image` (string)

**Example (Linux/Mac):**
```bash
curl -X POST http://localhost:5000/clubs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robotics Club",
    "description": "Build awesome robots",
    "memberCount": 30,
    "image": "https://example.com/robot.jpg"
  }'
```

**Example (Windows CMD/PowerShell - single line):**
```bash
curl -X POST http://localhost:5000/clubs -H "Content-Type: application/json" -d "{\"name\": \"Robotics Club\", \"description\": \"Build awesome robots\", \"memberCount\": 30, \"image\": \"https://example.com/robot.jpg\"}"
```

**Example (Windows PowerShell - recommended):**
```powershell
Invoke-RestMethod -Uri http://localhost:5000/clubs -Method Post -ContentType "application/json" -Body '{"name": "Robotics Club", "description": "Build awesome robots", "memberCount": 30, "image": "https://example.com/robot.jpg"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Club created successfully",
  "club_id": 1
}
```

### 4. Delete a Club
**DELETE** `/clubs/<id>`

Deletes a specific club by ID.

**Example (Linux/Mac):**
```bash
curl -X DELETE http://localhost:5000/clubs/1
```

**Example (Windows PowerShell):**
```powershell
Invoke-RestMethod -Uri http://localhost:5000/clubs/1 -Method Delete
```

**Response:**
```json
{
  "success": true,
  "message": "Club deleted successfully"
}
```

**Error Response (Club not found):**
```json
{
  "success": false,
  "error": "Club not found"
}
```

## Testing with Browser

You can test the GET endpoints directly in your browser:
- Visit `http://localhost:5000/` for API info
- Visit `http://localhost:5000/clubs` to see all clubs

## Testing with Python

```python
import requests

# Create a club
response = requests.post('http://localhost:5000/clubs', json={
    'name': 'Chess Club',
    'description': 'Play chess and have fun',
    'memberCount': 25,
    'image': 'https://example.com/chess.jpg'
})
print(response.json())

# Get all clubs
response = requests.get('http://localhost:5000/clubs')
print(response.json())
```

## Database

The SQLite database file (`clubs.db`) will be automatically created when you run the app for the first time.

**Table Structure:**
```sql
CREATE TABLE club (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    memberCount INTEGER DEFAULT 0,
    image TEXT
)
```

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── clubs.db           # SQLite database (created automatically)
```

## Tips for Hackathon Students

1. **Start simple**: This code is intentionally simple. Get it working first!
2. **Test as you go**: Use `curl` or your browser to test endpoints
3. **Add features gradually**: Once this works, you can add update/delete endpoints
4. **Frontend**: Connect this to a angular frontend


## Common Issues

**Port already in use?**
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=3000)  # Change 5000 to 3000
```

**Can't install Flask?**
Try:
```bash
python -m pip install --upgrade pip
python -m pip install Flask
```

## Next Steps

Want to make it better? Try adding:
- UPDATE endpoint to modify clubs
- Search/filter functionality
- Input validation
- Error logging

## License

Free to use for your hackathon projects!

