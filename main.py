# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory list to store students
students = [{'id': 1, 'name': 'John', 'age': 20}]
next_id = 2

# Base URL of your Render service
BASE_URL = "https://doctor-api-1-ac1h.onrender.com"

@app.route('/')
def homepage():
    html = """
    <html>
      <head>
        <title>API Home</title>
        <style>
          body { font-family: Arial; padding: 40px; background: #f4f4f4; }
          h1 { color: #2c3e50; }
          ul { line-height: 1.8; }
          code { background: #e8e8e8; padding: 2px 5px; border-radius: 4px; }
        </style>
      </head>
      <body>
        <h1>📡 Welcome to the Student API</h1>
        <p>This is a testable Flask API hosted on Render.</p>
        <h2>🔗 Endpoints:</h2>
        <ul>
          <li><code>GET /students</code> — List all students</li>
          <li><code>POST /students</code> — Create a new student</li>
          <li><code>GET /students/&lt;id&gt;</code> — Get student by ID</li>
          <li><code>PUT /students/&lt;id&gt;</code> — Update student by ID</li>
          <li><code>DELETE /students/&lt;id&gt;</code> — Delete student by ID</li>
        </ul>
        <p>🧪 Test with: <code>curl</code>, <code>Postman</code>, or a frontend app.</p>
        <p>📍 <strong>Base URL:</strong> <code>https://your-api-name.onrender.com</code></p>
      </body>
    </html>
    """
    return html


@app.route('/students', methods=['POST'])
def create_student():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'error': 'Name and age are required.'}), 400

    student = {'id': next_id, 'name': data['name'], 'age': data['age']}
    students.append(student)
    next_id += 1
    return jsonify(student), 201

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student['name'] = data.get('name', student['name'])
    student['age'] = data.get('age', student['age'])
    return jsonify(student)

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return jsonify({'message': f'Student {student_id} deleted'}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
