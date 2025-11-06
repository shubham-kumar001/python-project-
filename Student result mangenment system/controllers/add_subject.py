# controllers/subject_controller.py
from flask import Blueprint, render_template, request, redirect, url_for
from util.validation import valide_subject

subject_bp = Blueprint('subject', __name__)

@subject_bp.route("/add_subject", methods=["GET", "POST"])
def add_subject_route():
    if request.method == "POST":
        name = request.form["subject_name"]
        add_subject(name)
        return redirect(url_for('subject.add_subject_route'))
    
    all_subjects = get_all_subjects()
    return render_template("add_subject.html", subjects=all_subjects)
