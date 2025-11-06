from flask import Flask, render_template_string, request, redirect, url_for, session, flash, get_flashed_messages
from functools import wraps
import os

# --- Configuration & Initialization ---
app = Flask(__name__)
# 1. Mandatory for using sessions (login/logout). Replace the default key in a real deployment.
app.secret_key = os.environ.get('SECRET_KEY', 'my_highly_secure_cutm_key_12345') 

# Temporary storage (Data will reset when the server restarts)
students = []

# --- Custom Decorator for Faculty Login Requirement ---
def login_required(f):
    """Decorator to restrict access to faculty (logged-in users)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the 'logged_in' session flag is True
        if session.get("logged_in") != True:
            # Using simple HTML redirect with message since we are relying on render_template_string
            return redirect(url_for("faculty_login"))
        return f(*args, **kwargs)
    return decorated_function

# --- Helper Function ---
def calculate_grade(percentage):
    """Grade calculation based on the custom CUTM scale."""
    if percentage >= 90:
        return "O"
    elif percentage >= 85:
        return "E"
    elif percentage >= 80:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 65:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"

# --- Authentication Routes ---

@app.route("/login", methods=["GET", "POST"])
def faculty_login():
    """Faculty Login Page. Checks for @cutm.ac.in domain."""
    if request.method == "POST":
        faculty_mail = request.form.get("email")
        # 2. Professional requirement: Check for the mandatory domain "@cutm.ac.in"
        if faculty_mail and faculty_mail.endswith("@cutm.ac.in"):
            session["logged_in"] = True
            session["faculty_email"] = faculty_mail
            # Flash is used to temporarily store a message to display on the next page
            flash(f"Welcome, Faculty {faculty_mail}. Login successful! Please add student data.", "success")
            # Redirect to Add Student page after successful login
            return redirect(url_for("add_student"))
        else:
            flash("Invalid credentials or email domain. Access is restricted to @cutm.ac.in faculty emails only.", "danger")
            return redirect(url_for("faculty_login")) # Redirect back to show error

    # Template for Login Page (GET request)
    
    # Correctly retrieve flash messages for display in the template string
    flashed_messages = get_flashed_messages(with_categories=True)
    flash_html = ""
    for category, message in flashed_messages:
        # Define basic styles for success and danger alerts
        style = 'background: #d4edda; color: #155724;' if category == 'success' else 'background: #f8d7da; color: #721c24;'
        flash_html += f'<div style="{style} padding: 10px; border-radius: 5px; margin-bottom: 15px; text-align: center;">{message}</div>'
        
    return render_template_string(f"""
    <html>
    <head>
        <title>Faculty Login | CUTM</title>
        <style>
            body {{ font-family: Arial, sans-serif; background:#003366; text-align:center; padding:80px; }}
            .form-box {{ background:white; padding:40px; border-radius:10px; box-shadow:0 8px 20px rgba(0,0,0,0.3); display:inline-block; text-align:left; max-width: 400px; width: 90%;}}
            h2 {{ color:#003366; text-align:center; margin-bottom: 20px; }}
            input[type=email], input[type=password] {{ width:95%; padding:12px; border-radius:5px; border:1px solid #ccc; margin-top:5px; margin-bottom: 15px; }}
            button {{ background:#ffcc00; color:black; padding:12px 20px; border:none; border-radius:5px; cursor:pointer; margin-top:15px; width:100%; font-weight: bold; }}
            button:hover {{ background:#ffaa00; }}
        </style>
    </head>
    <body>
        <div class="form-box">
            <h2>CUTM Faculty Portal Login 🔑</h2>
            {flash_html}
            <form method="POST">
                <label for="email">Faculty Email (must be @cutm.ac.in):</label>
                <input type="email" id="email" name="email" placeholder="e.g. shubham@cutm.ac.in" required>
                <label for="password">Password (Any value for demo):</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Secure Login</button>
            </form>
            <p style="text-align:center; margin-top:20px;"><a style="color: #003366;" href="/home">Back to Home</a></p>
        </div>
    </body>
    </html>
    """)

@app.route("/logout")
def faculty_logout():
    """Logout endpoint."""
    session.pop("logged_in", None)
    session.pop("faculty_email", None)
    flash("You have been securely logged out.", "info")
    return redirect(url_for("home"))

# --- Application Routes ---

# Landing Page - UPDATED: Now redirects immediately to the Home Dashboard (/home)
@app.route("/")
def start():
    """Application starting page with CUTM branding. Now redirects to Home for casual access."""
    # Bypassing the intermediate 'Enter Portal' screen as requested.
    return redirect(url_for("home"))

# Homepage
@app.route("/home")
def home():
    """Main dashboard for the portal."""
    # Determine navigation links based on login status
    login_status_html = ""
    if session.get("logged_in"):
        login_status_html = f"""
            <span style="color: #ffcc00; font-weight: normal; font-size: 14px;">(Logged in as: {session.get('faculty_email')})</span>
            <a href="/logout">Logout</a>
        """
    else:
        login_status_html = '<a href="/login">Faculty Login</a>'

    return render_template_string(f"""
    <html>
    <head>
        <title>Student Results of CUTM</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; margin: 0; background: #f4f7f8; }}
            header {{ background: #003366; color: white; padding: 20px; text-align: center; }}
            header img.logo {{ width: 60px; vertical-align: middle; margin-right: 15px; border-radius: 50%; }}
            header h1 {{ display: inline-block; vertical-align: middle; margin: 0; font-size: 28px; }}
            nav {{ margin-top: 10px; }}
            nav a {{ color: white; text-decoration: none; margin: 0 15px; font-weight: bold; padding: 5px 10px; border-radius: 5px; transition: background 0.3s; }}
            nav a:hover {{ background: #0055a5; }}
            main {{ padding: 60px 20px; text-align: center; }}
            footer {{ background: #003366; color: white; padding: 15px; text-align: center; position: fixed; width: 100%; bottom: 0; font-size: 12px; }}
            a.button {{ background: #ffcc00; color: black; padding: 12px 25px; border-radius: 5px; text-decoration: none; margin: 15px 10px; display: inline-block; font-weight: bold; transition: transform 0.2s; box-shadow: 0 4px #e6b800; }}
            a.button:hover {{ transform: translateY(-2px); box-shadow: 0 6px #e6b800; }}
            .faculty-status {{ display: block; margin-top: 15px; font-size: 16px; font-weight: bold; color: #ffcc00; }}
        </style>
    </head>
    <body>
        <header>
            <img class="logo" src="https://upload.wikimedia.org/wikipedia/en/6/62/Centurion_University_of_Technology_and_Management_Logo.svg" alt="CUTM Logo">
            <h1>Student Results Management</h1>
            <nav>
                <a href="/home">Home</a> <!-- Updated link to point to the main dashboard -->
                <a href="/add">Add Student</a>
                <a href="/results">View Results</a>
                {login_status_html}
            </nav>
        </header>
        <main>
            <h2>Centurion University of Technology And Management (CUTM)</h2>
            <p>Use the links above to securely manage and view student academic performance data.</p>
            <a class="button" href="/add">➕ Add Student Results</a>
            <a class="button" href="/results">📋 View Published Results</a>
        </main>
        <footer>
            &copy; 2025-26 CUTM University Project | Directorate of Evaluation
        </footer>
    </body>
    </html>
    """)

# Add student - first step: enter number of subjects
@app.route("/add", methods=["GET", "POST"])
@login_required # ONLY FACULTY CAN ACCESS
def add_student():
    """Route to determine number of subjects and then get student/marks data."""
    if request.method == "POST" and "num_subjects" in request.form:
        try:
            num_subjects = int(request.form["num_subjects"])
            if num_subjects <= 0:
                raise ValueError
        except ValueError:
            return "<h3>Please enter a valid positive integer for number of subjects.</h3>"
        
        # Second step: Form to enter details and subject marks
        # The core HTML is kept close to the original for format consistency
        return render_template_string(f"""
        <html>
        <head>
            <title>Add Student - Enter Subjects</title>
            <style>
                body {{ font-family: Arial, sans-serif; background:#f4f7f8; text-align:center; padding:40px; }}
                .form-box {{ background:white; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); display:inline-block; text-align:left; }}
                h2 {{ color:#003366; text-align:center; }}
                label {{ font-weight:bold; display:block; margin-top:10px; }}
                input {{ width:95%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:5px; }}
                button {{ background:#003366; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; margin-top:15px; }}
                button:hover {{ background:#0055a5; }}
                a.back {{ display:inline-block; margin-top:10px; text-decoration:none; color:#003366; }}
                a.back:hover {{ text-decoration:underline; }}
                table {{ width:100%; border-collapse: collapse; margin-top:15px; }}
                th, td {{ border:1px solid #ddd; padding:8px; text-align:center; }}
                th {{ background:#003366; color:white; }}
            </style>
        </head>
        <body>
            <div class="form-box">
                <h2>Enter Student Details & Subjects</h2>
                <form method="POST" action="/submit_student">
                    <label>Name:</label>
                    <input type="text" name="name" required>
                    <label>Roll Number:</label>
                    <input type="text" name="roll" required>
                    <label>Branch:</label>
                    <input type="text" name="branch" required>
                    <label>Section:</label>
                    <input type="text" name="section" required>
                    <label>Year:</label>
                    <input type="text" name="year" required>
                    <input type="hidden" name="num_subjects" value="{num_subjects}">
                    <table>
                        <tr>
                            <th>Sr. No.</th>
                            <th>Subject Name</th>
                            <th>Marks Obtained</th>
                            <th>Total Marks</th>
                        </tr>
                        {''.join([f"""
                        <tr>
                            <td>{i+1}</td>
                            <td><input type="text" name="subject_{i+1}" required></td>
                            <td><input type="number" name="marks_{i+1}" required></td>
                            <td><input type="number" name="total_{i+1}" required></td>
                        </tr>""" for i in range(num_subjects)])}
                    </table>
                    <button type="submit">Add Student</button>
                </form>
                <a class="back" href='/home'>⬅ Back Home</a>
            </div>
        </body>
        </html>
        """)

    # First step: user enters number of subjects manually
    return render_template_string("""
    <html>
    <head>
        <title>Add Student - Number of Subjects</title>
        <style>
            body { font-family: Arial, sans-serif; background:#f4f7f8; text-align:center; padding:40px; }
            .form-box { background:white; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); display:inline-block; text-align:left; }
            h2 { color:#003366; text-align:center; }
            input { width:100%; padding:8px; border-radius:5px; border:1px solid #ccc; margin-top:5px; }
            button { background:#003366; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; margin-top:15px; }
            button:hover { background:#0055a5; }
            a.back { display:inline-block; margin-top:10px; text-decoration:none; color:#003366; }
            a.back:hover { text-decoration:underline; }
        </style>
    </head>
    <body>
        <div class="form-box">
            <h2>Enter Number of Subjects</h2>
            <form method="POST">
                <input type="number" name="num_subjects" placeholder="Enter number of subjects" required min="1">
                <button type="submit">Next</button>
            </form>
            <a class="back" href='/home'>⬅ Back Home</a>
        </div>
    </body>
    </html>
    """)

# Submit student data
@app.route("/submit_student", methods=["POST"])
@login_required # ONLY FACULTY CAN ACCESS
def submit_student():
    """Handles the submission and calculation of marks."""
    student = {
        "name": request.form["name"],
        "roll": request.form["roll"],
        "branch": request.form["branch"],
        "section": request.form["section"],
        "year": request.form["year"],
        "subjects": []
    }
    num_subjects = int(request.form["num_subjects"])
    total_obtained = 0
    total_marks = 0
    
    # Process subject marks
    try:
        for i in range(1, num_subjects+1):
            # Input validation and type casting
            obtained = int(request.form[f"marks_{i}"])
            total = int(request.form[f"total_{i}"])
            
            if obtained < 0 or total <= 0 or obtained > total:
                 # In a professional app, you'd send an error page
                 flash("Input Error: Marks must be positive and obtained marks must not exceed total marks.", "danger")
                 return redirect(url_for("add_student"))

            student["subjects"].append({
                "name": request.form[f"subject_{i}"],
                "obtained": obtained,
                "total": total
            })
            total_obtained += obtained
            total_marks += total
    except ValueError:
        flash("Input Error: Please ensure all marks are valid numbers.", "danger")
        return redirect(url_for("add_student"))


    # Calculate percentage and grade
    student["percentage"] = round((total_obtained / total_marks) * 100, 2) if total_marks else 0
    student["grade"] = calculate_grade(student["percentage"])

    # Update or Add student record
    for idx, s in enumerate(students):
        if s["roll"] == student["roll"]:
            students[idx] = student
            flash(f"Results for Roll No. {student['roll']} updated successfully.", "success")
            break
    else:
        students.append(student)
        flash(f"New student {student['name']} added successfully.", "success")
        
    return redirect(url_for("view_results"))

# Edit student
@app.route("/edit/<roll>", methods=["GET", "POST"])
@login_required # ONLY FACULTY CAN ACCESS
def edit_student(roll):
    """Route to edit an existing student's details and marks."""
    student = next((s for s in students if s["roll"] == roll), None)
    if not student:
        flash(f"Student with Roll No. {roll} not found.", "danger")
        return redirect(url_for("view_results"))
    
    if request.method == "POST":
        # Handle form submission for editing
        try:
            student["name"] = request.form["name"]
            student["branch"] = request.form["branch"]
            student["section"] = request.form["section"]
            student["year"] = request.form["year"]
            num_subjects = len(student["subjects"]) 
            total_obtained = 0
            total_marks = 0
            student["subjects"] = []
            
            for i in range(1, num_subjects+1):
                obtained = int(request.form[f"marks_{i}"])
                total = int(request.form[f"total_{i}"])
                
                if obtained < 0 or total <= 0 or obtained > total:
                     flash("Input Error: Marks must be positive and obtained marks must not exceed total marks.", "danger")
                     return redirect(url_for("edit_student", roll=roll))

                student["subjects"].append({
                    "name": request.form[f"subject_{i}"],
                    "obtained": obtained,
                    "total": total
                })
                total_obtained += obtained
                total_marks += total

            student["percentage"] = round((total_obtained / total_marks) * 100, 2) if total_marks else 0
            student["grade"] = calculate_grade(student["percentage"])
            flash(f"Results for Roll No. {roll} updated successfully.", "success")
        except Exception as e:
            flash(f"Error updating data: {e}", "danger")
            
        return redirect(url_for("view_results"))

    # GET request: Display edit form
    subject_inputs = "".join([f"""
        <tr>
            <td>{i+1}</td>
            <td><input type="text" name="subject_{i+1}" value="{sub['name']}" required></td>
            <td><input type="number" name="marks_{i+1}" value="{sub['obtained']}" required></td>
            <td><input type="number" name="total_{i+1}" value="{sub['total']}" required></td>
        </tr>""" for i, sub in enumerate(student["subjects"])])

    return render_template_string(f"""
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body {{ font-family: Arial, sans-serif; background:#f4f7f8; text-align:center; padding:40px; }}
            .form-box {{ background:white; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); display:inline-block; text-align:left; }}
            table {{ width:100%; border-collapse: collapse; margin-top:15px; }}
            th, td {{ border:1px solid #ddd; padding:8px; text-align:center; }}
            th {{ background:#003366; color:white; }}
            button {{ background:#003366; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; margin-top:15px; }}
            button:hover {{ background:#0055a5; }}
            a.back {{ display:inline-block; margin-top:10px; text-decoration:none; color:#003366; }}
            a.back:hover {{ text-decoration:underline; }}
            input[type="text"], input[type="number"] {{ width: 80%; padding: 5px; border-radius: 3px; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <div class="form-box">
            <h2>📝 Edit Student / Marks for Roll: {student['roll']}</h2>
            <form method="POST">
                <label>Name:</label><input type="text" name="name" value="{student['name']}" required><br>
                <label>Branch:</label><input type="text" name="branch" value="{student['branch']}" required><br>
                <label>Section:</label><input type="text" name="section" value="{student['section']}" required><br>
                <label>Year:</label><input type="text" name="year" value="{student['year']}" required><br>
                <input type="hidden" name="num_subjects" value="{len(student['subjects'])}">
                <table>
                    <tr><th>Sr. No.</th><th>Subject Name</th><th>Marks Obtained</th><th>Total Marks</th></tr>
                    {subject_inputs}
                </table>
                <button type="submit">Update Student</button>
            </form>
            <a class="back" href='/results'>⬅ Back to Results</a>
        </div>
    </body>
    </html>
    """)

# Emergency restart
@app.route("/restart", methods=["POST"])
@login_required # ONLY FACULTY CAN ACCESS
def restart():
    """Clears all student data - requires faculty login."""
    students.clear()
    flash("⚠ WARNING: All student records have been cleared via Emergency Restart.", "danger")
    return redirect(url_for("view_results"))

# View results - PROTECTED
@app.route("/results")
@login_required # ONLY FACULTY CAN ACCESS
def view_results():
    """Displays the main results table. Requires faculty login."""
    table_rows = []
    
    # Process flash messages to display professional alerts
    flash_html = ""
    for category, message in session.pop('_flashes', []):
        if category == 'danger':
             flash_html += f"<div style='background:#f8d7da; color:#721c24; border:1px solid #f5c6cb; padding:10px; margin-bottom:10px; border-radius:5px; text-align:center;'>{message}</div>"
        else: # success/info
             flash_html += f"<div style='background:#d4edda; color:#155724; border:1px solid #c3e6cb; padding:10px; margin-bottom:10px; border-radius:5px; text-align:center;'>{message}</div>"
        
    for idx, s in enumerate(students, 1):
        subject_details = "<ul style='margin:0;padding-left:16px; font-size: 0.9em;'>"
        for sub in s["subjects"]:
            subject_details += f"<li>{sub['name']}: {sub['obtained']}/{sub['total']}</li>"
        subject_details += "</ul>" if s["subjects"] else "None"
        
        # Determine professional color for grade display
        grade_color = "red" if s['grade'] == 'F' else "#008000" if s['grade'] in ['O', 'E'] else "#ffaa00"

        table_rows.append(
            f"<tr><td>{idx}</td><td>{s['roll']}</td><td>{s['name']}</td><td>{subject_details}</td>"
            f"<td>{s['percentage']}% <span style='font-weight:bold; color:{grade_color};'>({s['grade']})</span><br>"
            f"<a href='/edit/{s['roll']}' style='color:#003366; font-weight:bold;'>Edit Records</a></td></tr>"
        )

    return render_template_string(f"""
<html>
<head>
    <title>Student Results - Faculty Control</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f7f8; text-align: center; padding: 20px; }}
        table {{ border-collapse: collapse; width: 95%; margin: 20px auto; background: white; box-shadow: 0 0 20px rgba(0,0,0,0.05); }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }}
        th {{ background: #003366; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        ul {{ margin: 0; padding-left: 20px; list-style-type: disc; }}
        a.button, input[type=submit] {{ background: #003366; color: white; padding: 10px 18px; border-radius: 5px; border: none; margin: 5px; text-decoration: none; cursor: pointer; display: inline-block; font-weight: bold; }}
        a.button:hover, input[type=submit]:hover {{ background: #0055a5; }}
        .emergency-btn {{ background: #cc0000 !important; }}
        .emergency-btn:hover {{ background: #990000 !important; }}
    </style>
</head>
<body>
    <h2>🔐 Faculty Control Panel: Student Results</h2>
    {flash_html}
    <form method="POST" action="/restart" onsubmit="return confirm('ARE YOU SURE? Emergency Restart will permanently delete ALL current student data.')">
        <input type="submit" value="⚠ EMERGENCY RESTART" class="emergency-btn">
    </form>
    <table>
        <tr><th>Sr. No.</th><th>Roll</th><th>Name</th><th>Subjects (Obtained/Total)</th><th>Percentage & Grade / Action</th></tr>
        {''.join(table_rows)}
    </table>
    <a class="button" href='/home'>⬅ Back Home</a>
</body>
</html>
""")

# --- Application Runner ---
if __name__ == "__main__":
    # 3. Ensures the server only runs once, preventing the "opens twice" issue.
    # We keep debug=True for convenience during development.
    app.run(debug=True, use_reloader=False)