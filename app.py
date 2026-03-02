from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

skills_db = ["python", "java", "machine learning", "data structures", "sql", "react"]

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.lower()

@app.route("/", methods=["GET", "POST"])
def index():
    score = 0
    found_skills = []
    
    if request.method == "POST":
        file = request.files["resume"]
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)

        for skill in skills_db:
            if skill in text:
                found_skills.append(skill)
        
        score = (len(found_skills) / len(skills_db)) * 100

    return render_template("index.html", score=score, skills=found_skills)

if __name__ == "__main__":
    app.run(debug=True)
