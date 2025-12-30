import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database file
DATABASE = 'clubs.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to get results as dictionaries
    return conn

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

if __name__ == '__main__':
    # Initialize database when app starts
    init_db()
    
    # Run the Flask app
    print("Starting Club Hub Server...")
    print("Visit http://localhost:5000 to see the API")
    app.run(debug=True, host='0.0.0.0', port=5000)

