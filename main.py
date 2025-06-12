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
        <title>Student API Docs | Swagger Style</title>
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
            code {
                background: #eef;
                padding: 3px 6px;
                border-radius: 4px;
            }
            ul {
                margin-top: 10px;
            }
            footer {
                margin-top: 60px;
                font-size: 13px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <h1>📘 API Testing with Swagger Style</h1>

        <p><strong>Last Updated:</strong> 28 Apr, 2025</p>

        <div class="section">
            <h2>🧠 Understanding APIs</h2>
            <p>In the realm of software, applications often need to exchange information or trigger actions between systems. <strong>APIs act as messengers</strong>, allowing smooth and structured communication.</p>
            <p><em>Example:</em> An e-commerce site may use an API to fetch product details from its database.</p>
        </div>

        <div class="section">
            <h2>🗺️ Swagger as the Map</h2>
            <p>Swagger acts like a city map for APIs — showing every route (endpoint) available, what data can be requested, and what actions can be performed.</p>
            <p>This standardized map helps developers understand and interact with the API effectively.</p>
        </div>

        <div class="section">
            <h2>🛠️ Leveraging Swagger for Testing</h2>
            <p>When testing APIs, developers simulate tasks like retrieving data, updating information, or deleting records. Swagger provides an environment to:</p>
            <ul>
                <li>Send requests (e.g., <code>GET /students</code>)</li>
                <li>Receive and verify API responses</li>
                <li>Validate that parameters and behaviors are correct</li>
            </ul>
        </div>

        <div class="section">
            <h2>✅ Example Endpoints (Base URL: <code>{{ url }}</code>)</h2>
            <ul>
                <li><code>GET /students</code> – List all students</li>
                <li><code>POST /students</code> – Add a new student</li>
                <li><code>GET /students/&lt;id&gt;</code> – Get student by ID</li>
                <li><code>PUT /students/&lt;id&gt;</code> – Update student info</li>
                <li><code>DELETE /students/&lt;id&gt;</code> – Remove a student</li>
            </ul>
        </div>

        <div class="section">
            <h2>🔍 Proactive Testing</h2>
            <p>Swagger testing identifies issues early by simulating realistic scenarios. Just like navigating with a reliable map avoids dead ends, Swagger ensures all API routes function properly before reaching users.</p>
        </div>

        <footer>
            &copy; 2025 Student API | Flask-powered RESTful Service with Swagger-style Documentation
        </footer>
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
