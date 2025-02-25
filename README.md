# Resume Ranking Automation - Flask App 📄🚀

## 📌 Overview
This project is a **Flask-based Resume Ranking System** that:
- ✅ Accepts resume submissions and evaluates them based on predefined criteria.
- ✅ Stores resume details (**name, email, score, and file**) in a **MySQL database**.
- ✅ Provides an **admin panel** to view ranked resumes.
- ✅ Allows sending **automated emails** to applicants with their ranking details.
- ✅ Uses **Flask-Mail** to send emails and allows customization via an `email.txt` template.

---

## 🛠 Features
✔ **Resume Submission & Ranking** - Stores resumes and assigns scores.  
✔ **Admin Panel** - Displays ranked resumes dynamically.  
✔ **Automated Email Notifications** - Sends rank details to candidates.  
✔ **Email Template Customization** - Modify `email.txt` to change email content.  
✔ **MySQL Database Integration** - Stores candidate data securely.  
✔ **Flask & JavaScript** - Ensures smooth frontend-backend interaction.  

---

## 📂 Folder Structure
```
Resume-Ranking/
│── static/               # Static files (CSS, JS, etc.)
│   ├── css/
│   │   ├── details.css   # Styles for the admin panel
│   ├── js/
│   │   ├── script.js     # JavaScript for fetching & displaying resumes
│── templates/            # HTML templates
│   ├── admin.html        # Admin panel for viewing resumes
│── uploads/              # Folder where resumes are stored
│── app.py                # Flask backend
│── email.txt             # Email template for notifications
│── requirements.txt      # Required dependencies
│── README.md             # Documentation
│── database.sql          # SQL schema for MySQL
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies
Ensure you have **Python 3** installed, then run:
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up MySQL Database
Create a **MySQL database** and execute `database.sql`:
```sql
CREATE DATABASE resume_ranking;
USE resume_ranking;

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    filename VARCHAR(255),
    score INT
);
```

### 3️⃣ Configure `app.py`
Update the **database credentials** in `app.py`:
```python
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "resume_ranking"
```

### 4️⃣ Set Up Email (Flask-Mail)
- Enable **Less Secure Apps** or use **App Passwords** in Gmail.
- Update the **email configuration** in `app.py`:
```python
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
```

---

## 🚀 Running the Application
Start the **Flask server**:
```bash
python app.py
```
Access the **Admin Panel** at:
🔗 **http://localhost:5000/admin**

---

## 🖥️ Admin Panel (`admin.html`)
The Admin Panel displays all resumes in ranked order:

| Rank | Name      | Email              | Score | Resume           | Action      |
|------|----------|--------------------|-------|------------------|-------------|
| 1    | John Doe | john@example.com   | 90    | [View Resume]()  | [Send Email]() |
| 2    | Jane Doe | jane@example.com   | 85    | [View Resume]()  | [Send Email]() |

🔹 Click **"Send Email"** to notify the candidate about their ranking.

---

## 📨 Customizing Email Template
Modify the `email.txt` file to change the email content:
```
Subject: Your Resume Ranking is Here!

Dear {name},

We are excited to share that your resume has been ranked!

Rank: {rank}  
Score: {score}  

Congratulations! If you have any questions, feel free to reach out.

Best Regards,  
[Your Team]
```
🔹 The placeholders **`{name}`**, **`{rank}`**, and **`{score}`** will be **automatically replaced**.

---

## 📌 API Endpoints

| Method | Endpoint            | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/upload`           | Upload resumes (PDF)        |
| POST   | `/process_resumes`  | Process & rank resumes      |
| POST   | `/details`          | Fetch ranked resume data    |
| POST   | `/send_email`       | Send email to candidates    |

---

## 💡 Troubleshooting

### ❓ Flask-Mail email not sending?
✔ Check **`MAIL_USERNAME`** and **`MAIL_PASSWORD`** in `app.py`.  
✔ Ensure **Less Secure Apps** or **App Passwords** are enabled in Gmail.  
✔ Check your **spam folder** for the emails.  

### ❓ MySQL connection error?
✔ Ensure **MySQL is running**.  
✔ Verify the **database name, username, and password**.  
✔ Run `database.sql` again if tables are missing.  

---
