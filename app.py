from flask import Flask, request, jsonify, render_template, send_from_directory
import pymysql
import os
from PyPDF2 import PdfReader
from flask_mail import Mail, Message
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'manager',
    'database': 'resume_db',
    'port': 3306  # Change to 3307 if needed
}

# Mal configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vishnuvarshan34@gmail.com'  # Your full Gmail address
app.config['MAIL_PASSWORD'] = 'wdkp gnhe jmge lctr'  # Your generated App Password
app.config['MAIL_DEFAULT_SENDER'] = 'vishnuvarshan34@gmail.com'  # Same as your email

mail = Mail(app)


def connect_to_db():
    """Establish a connection to the MySQL database using pymysql."""
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        return conn
    except pymysql.MySQLError as e:
        print("Error connecting to MySQL:", e)
        return None

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username, password)

    conn = connect_to_db()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"}), 500

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/details', methods=['POST'])
def details():
    data = request.get_json(silent=True) or {}
    selected_filter = data.get("filter", "").strip().lower()

    conn = connect_to_db()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"}), 500

    cursor = conn.cursor()

    query = "SELECT name, email, phone, filename, score, matched_requirements FROM resumes"
    query_params = []

    if selected_filter:
        query += " WHERE LOWER(matched_requirements) LIKE %s"
        query_params.append(f"%{selected_filter}%")

    query += " ORDER BY score DESC;"

    cursor.execute(query, query_params)
    resumes = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"success": True, "resumes": resumes}) if resumes else jsonify({"success": False, "message": "No resumes found"})


def extract_name_email(resume_text, filename):
    """Extracts name and email from the resume text or filename."""
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
    email = email_match.group(0) if email_match else "Unknown"
    name = os.path.splitext(filename)[0].replace("_resume", "").replace("_cv", "").replace("-", " ")
    name = " ".join(word.capitalize() for word in name.split("_"))
    return name, email

# Function to extract phone number from extracted text
def extract_phone_number(text):
    match = re.search(r'\b\d{10}\b', text)  # Find first 10-digit number
    return match.group() if match else "Unknown"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload_resumes():
    if 'resumes' not in request.files:
        return jsonify({"success": False, "message": "No files part"}), 400

    resumes = request.files.getlist('resumes')
    filenames = []

    for resume in resumes:
        if resume.filename.endswith('.pdf'):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(filename)
            filenames.append(filename)

    if filenames:
        return jsonify({"success": True, "message": "Files uploaded successfully!"}), 200
    else:
        return jsonify({"success": False, "message": "Only PDF files are allowed!"}), 400


def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf_reader = PdfReader(f)
        text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        return text.strip()


def check_resume_quality(resume_text, company_requirements):
    return sum(1 for requirement in company_requirements if requirement.lower() in resume_text.lower())

def load_email_template():
    """Reads the email template from email.txt"""
    with open("email.txt", "r", encoding="utf-8") as file:
        return file.read()


@app.route('/process_resumes', methods=['POST'])
def process_resumes():
    print("Processing resumes...")
    company_requirements = [
        "Team Player", "Diploma", "English", "MBA", "JavaScript", 
        "3+ years", "Bachelor’s Degree", 
        "Python", "React", "AWS",
    ]
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    resume_scores = []

    conn = connect_to_db()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"}), 500

    cursor = conn.cursor()

    for filename in uploaded_files:
        if filename.endswith('.pdf'):
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_text = extract_text_from_pdf(resume_path)
            name, email = extract_name_email(resume_text, filename)
            phone = extract_phone_number(resume_text)
            matched_requirements = [req for req in company_requirements if req.lower() in resume_text.lower()]
            matched_str = ", ".join(matched_requirements)
            print(matched_str)
            score = len(matched_requirements)
            cursor.execute(
                    "INSERT INTO resumes (name, email, phone, filename, score, matched_requirements) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, phone, filename, score, matched_str)
            )
            conn.commit()

            resume_scores.append({'name': name, 'email': email, 'phone': phone, 'filename': filename, 'score': score, 'requirements': matched_requirements})

    cursor.close()
    conn.close()

    resume_scores.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"success": True, "ranked_resumes": resume_scores})


@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get("email")
    recipient_name = data.get("name")
    rank = data.get("rank")
    score = data.get("score")

    if not recipient_email:
        return jsonify({"success": False, "message": "Email is required!"})

    # Load and format the email template
    email_template = load_email_template()
    email_content = email_template.format(name=recipient_name, email=recipient_email, rank=rank, score=score)

    # Extract subject and body
    subject_line, email_body = email_content.split("\n", 1)  # Splits the first line as subject
    subject = subject_line.replace("Subject: ", "").strip()

    try:
        msg = Message(subject, recipients=[recipient_email])
        msg.body = email_body.strip()
        mail.send(msg)
        return jsonify({"success": True, "message": f"Email sent to {recipient_email}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
