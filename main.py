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
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Student API Docs | Test Interface</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f9f9f9;
                padding: 40px;
                line-height: 1.6;
                color: #2c3e50;
            }
            h1, h2 {
                color: #34495e;
            }
            .section {
                background-color: #fff;
                border-left: 5px solid #3498db;
                padding: 20px;
                margin: 30px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                border-radius: 8px;
            }
            code, textarea, input {
                background: #eef;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #ccc;
                width: 100%;
                box-sizing: border-box;
            }
            textarea {
                height: 100px;
            }
            button {
                background: #3498db;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background: #2980b9;
            }
            .response {
                white-space: pre-wrap;
                background: #eef;
                margin-top: 10px;
                padding: 10px;
                border: 1px dashed #ccc;
                font-family: monospace;
            }
            footer {
                margin-top: 60px;
                font-size: 13px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <h1>🎓 Student API Testing Interface</h1>
        <p><strong>Base URL:</strong> {{ url }}</p>

        <div class="section">
            <h2>📥 GET /students</h2>
            <button onclick="getStudents()">Fetch Students</button>
            <div id="getResponse" class="response"></div>
        </div>

        <div class="section">
            <h2>➕ POST /students</h2>
            <textarea id="postData">{ "name": "Alice", "age": 23 }</textarea>
            <button onclick="postStudent()">Create Student</button>
            <div id="postResponse" class="response"></div>
        </div>

        <div class="section">
            <h2>✏️ PUT /students/&lt;id&gt;</h2>
            <input type="text" id="putId" placeholder="Student ID">
            <textarea id="putData">{ "name": "Bob", "age": 24 }</textarea>
            <button onclick="putStudent()">Update Student</button>
            <div id="putResponse" class="response"></div>
        </div>

        <div class="section">
            <h2>🗑️ DELETE /students/&lt;id&gt;</h2>
            <input type="text" id="deleteId" placeholder="Student ID">
            <button onclick="deleteStudent()">Delete Student</button>
            <div id="deleteResponse" class="response"></div>
        </div>

        <div class="section">
            <h2>🔍 GET /students/&lt;id&gt;</h2>
            <input type="text" id="getById" placeholder="Student ID">
            <button onclick="getStudentById()">Get Student</button>
            <div id="getByIdResponse" class="response"></div>
        </div>

        <footer>
            &copy; 2025 Student API | Flask-powered RESTful Service
        </footer>

        <script>
            const base = "{{ url }}";

            function getStudents() {
                fetch(base + "/students")
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById("getResponse").innerText = JSON.stringify(data, null, 2);
                    });
            }

            function postStudent() {
                const body = document.getElementById("postData").value;
                fetch(base + "/students", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: body
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("postResponse").innerText = JSON.stringify(data, null, 2);
                });
            }

            function putStudent() {
                const id = document.getElementById("putId").value;
                const body = document.getElementById("putData").value;
                fetch(base + "/students/" + id, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: body
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("putResponse").innerText = JSON.stringify(data, null, 2);
                });
            }

            function deleteStudent() {
                const id = document.getElementById("deleteId").value;
                fetch(base + "/students/" + id, {
                    method: "DELETE"
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("deleteResponse").innerText = JSON.stringify(data, null, 2);
                });
            }

            function getStudentById() {
                const id = document.getElementById("getById").value;
                fetch(base + "/students/" + id)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById("getByIdResponse").innerText = JSON.stringify(data, null, 2);
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, url=request.host_url.rstrip('/'))



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
