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
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student API - Swagger Style</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                color: #333;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ccc;
                text-align: left;
            }}
            th {{
                background-color: #f0f0f0;
            }}
            .tag {{
                padding: 4px 8px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }}
            .GET {{ background-color: #4CAF50; }}
            .POST {{ background-color: #2196F3; }}
            .PUT {{ background-color: #FFC107; color: black; }}
            .DELETE {{ background-color: #F44336; }}
        </style>
    </head>
    <body>
        <h1>📘 Student API - Render Deployment</h1>
        <p>Base URL: <code>{BASE_URL}</code></p>
        <table>
            <tr>
                <th>Method</th>
                <th>Endpoint</th>
                <th>Description</th>
                <th>Full URL</th>
            </tr>
            <tr>
                <td><span class="tag GET">GET</span></td>
                <td>/students</td>
                <td>Fetch all students</td>
                <td><a href="{BASE_URL}/students">{BASE_URL}/students</a></td>
            </tr>
            <tr>
                <td><span class="tag GET">GET</span></td>
                <td>/students/&lt;id&gt;</td>
                <td>Fetch a specific student by ID</td>
                <td><code>{BASE_URL}/students/1</code></td>
            </tr>
            <tr>
                <td><span class="tag POST">POST</span></td>
                <td>/students</td>
                <td>Create a new student</td>
                <td><code>{BASE_URL}/students</code></td>
            </tr>
            <tr>
                <td><span class="tag PUT">PUT</span></td>
                <td>/students/&lt;id&gt;</td>
                <td>Update student info by ID</td>
                <td><code>{BASE_URL}/students/1</code></td>
            </tr>
            <tr>
                <td><span class="tag DELETE">DELETE</span></td>
                <td>/students/&lt;id&gt;</td>
                <td>Delete a student by ID</td>
                <td><code>{BASE_URL}/students/1</code></td>
            </tr>
        </table>
        <p>Test this API using Postman or Swagger UI. JSON format is used for all inputs and outputs.</p>
    </body>
    </html>
    """
    return render_template_string(html)

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
