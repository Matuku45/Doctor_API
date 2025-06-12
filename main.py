# main.py
from flask import Flask, request, jsonify, render_template_string
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
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>🎓 Student API Testing Interface</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f4f6f8;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
            }}
            .endpoint {{
                background: #fff;
                border-left: 5px solid #2980b9;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 6px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }}
            .endpoint h2 {{
                margin-top: 0;
            }}
            input, textarea {{
                width: 100%;
                padding: 8px;
                margin: 5px 0 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: monospace;
            }}
            button {{
                background: #2980b9;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            pre {{
                background: #eef;
                padding: 10px;
                border-radius: 4px;
                overflow: auto;
            }}
        </style>
    </head>
    <body>
        <h1>🎓 Student API Testing Interface</h1>
        <p><strong>Base URL:</strong> {BASE_URL}</p>

        <div class="endpoint">
            <h2>📥 GET /students</h2>
            <button onclick="getStudents()">Fetch Students</button>
            <pre id="getResponse"></pre>
        </div>

        <div class="endpoint">
            <h2>➕ POST /students</h2>
            <textarea id="postBody">{{"name": "Alice", "age": 23}}</textarea>
            <button onclick="postStudent()">Create Student</button>
            <pre id="postResponse"></pre>
        </div>

        <div class="endpoint">
            <h2>✏️ PUT /students/&lt;id&gt;</h2>
            <input id="putId" placeholder="Student ID (e.g. 1)" />
            <textarea id="putBody">{{"name": "Bob", "age": 24}}</textarea>
            <button onclick="putStudent()">Update Student</button>
            <pre id="putResponse"></pre>
        </div>

        <div class="endpoint">
            <h2>🗑️ DELETE /students/&lt;id&gt;</h2>
            <input id="deleteId" placeholder="Student ID (e.g. 1)" />
            <button onclick="deleteStudent()">Delete Student</button>
            <pre id="deleteResponse"></pre>
        </div>

        <div class="endpoint">
            <h2>🔍 GET /students/&lt;id&gt;</h2>
            <input id="getOneId" placeholder="Student ID (e.g. 1)" />
            <button onclick="getStudent()">Get Student</button>
            <pre id="getOneResponse"></pre>
        </div>

        <script>
            const BASE = '{BASE_URL}';

            async function getStudents() {{
                const res = await fetch(`${{BASE}}/students`);
                const data = await res.json();
                document.getElementById('getResponse').textContent = JSON.stringify(data, null, 2);
            }}

            async function postStudent() {{
                const body = JSON.parse(document.getElementById('postBody').value);
                const res = await fetch(`${{BASE}}/students`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(body)
                }});
                const data = await res.json();
                document.getElementById('postResponse').textContent = JSON.stringify(data, null, 2);
            }}

            async function putStudent() {{
                const id = document.getElementById('putId').value;
                const body = JSON.parse(document.getElementById('putBody').value);
                const res = await fetch(`${{BASE}}/students/${{id}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(body)
                }});
                const data = await res.json();
                document.getElementById('putResponse').textContent = JSON.stringify(data, null, 2);
            }}

            async function deleteStudent() {{
                const id = document.getElementById('deleteId').value;
                const res = await fetch(`${{BASE}}/students/${{id}}`, {{
                    method: 'DELETE'
                }});
                const data = await res.json();
                document.getElementById('deleteResponse').textContent = JSON.stringify(data, null, 2);
            }}

            async function getStudent() {{
                const id = document.getElementById('getOneId').value;
                const res = await fetch(`${{BASE}}/students/${{id}}`);
                const data = await res.json();
                document.getElementById('getOneResponse').textContent = JSON.stringify(data, null, 2);
            }}
        </script>
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
