from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import joblib
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Secret key for login sessions
app.secret_key = "heart_disease_secret"

# Load trained model
model = joblib.load("../model/model.pkl")


# -----------------------------
# DATABASE SETUP
# -----------------------------
def init_db():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()

    conn.close()


init_db()


# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = sqlite3.connect("users.db")

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = username

            return redirect(url_for('home'))

        else:

            return "Invalid username or password"

    return render_template("login.html")


# -----------------------------
# REGISTER PAGE
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        try:

            conn = sqlite3.connect("users.db")

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()

            conn.close()

            return redirect(url_for('login'))

        except:

            return "Username already exists"

    return render_template("register.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():

    session.pop('user', None)

    session.pop('report_data', None)

    return redirect(url_for('login'))


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():

    if 'user' not in session:

        return redirect(url_for('login'))

    return render_template("index.html")


# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():

    if 'user' not in session:

        return redirect(url_for('login'))

    try:

        # Basic patient details
        age = float(request.form['age'])

        sex = float(request.form['sex'])

        cp = float(request.form['cp'])

        # Blood pressure
        systolic_bp = float(request.form['systolic_bp'])

        diastolic_bp = float(request.form['diastolic_bp'])

        bp = systolic_bp

        # Cholesterol handling
        if request.form.get("unknown_chol") == "yes":

            chol = 204

        else:

            chol_value = request.form.get("chol")

            if not chol_value:

                chol = 204

            else:

                chol = float(chol_value)

        # Other features
        fbs = float(request.form['fbs'])

        restecg = float(request.form['restecg'])

        exang = float(request.form['exang'])

        thalach = float(request.form['thalach'])

        # Default oldpeak
        oldpeak = 0.0

        # ST slope
        slope = float(request.form['slope'])

        # Final model input
        features = np.array([[
            age,
            sex,
            cp,
            bp,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope
        ]])

        # Prediction
        prediction = model.predict(features)

        # Confidence score
        probability = model.predict_proba(features)[0][1]

        confidence = round(probability * 100, 2)

        # Result
        if prediction[0] == 1:

            result = "High Risk of Heart Disease"

            risk_class = "high"

        else:

            result = "Low Risk of Heart Disease"

            risk_class = "low"

        # Save report data
        session['report_data'] = {

            'age': age,

            'sex': 'Male' if sex == 1 else 'Female',

            'bp': f"{systolic_bp}/{diastolic_bp}",

            'chol': chol,

            'prediction': result,

            'confidence': confidence
        }

        return render_template(
            "result.html",
            prediction=result,
            risk_class=risk_class,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            confidence=confidence
        )

    except Exception as e:

        return str(e)


# -----------------------------
# DOWNLOAD PDF REPORT
# -----------------------------
@app.route('/download-report')
def download_report():

    if 'user' not in session:

        return redirect(url_for('login'))

    report_data = session.get('report_data')

    if not report_data:

        return "No report data found"

    filename = "heart_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # Title
    title = Paragraph(
        "Heart Disease Prediction Report",
        styles['Title']
    )

    content.append(title)

    content.append(Spacer(1, 20))

    # Timestamp
    timestamp = Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    )

    content.append(timestamp)

    content.append(Spacer(1, 20))

    # Report details
    fields = [

        ("Age", report_data['age']),

        ("Sex", report_data['sex']),

        ("Blood Pressure", report_data['bp']),

        ("Cholesterol", report_data['chol']),

        ("Prediction", report_data['prediction']),

        ("Confidence", f"{report_data['confidence']}%")
    ]

    for label, value in fields:

        text = Paragraph(
            f"<b>{label}:</b> {value}",
            styles['BodyText']
        )

        content.append(text)

        content.append(Spacer(1, 12))

    # Disclaimer
    disclaimer = Paragraph(
        "This report is for informational purposes only and does not replace professional medical advice. Please consult a qualified healthcare provider for diagnosis and treatment.",
        styles['Italic']
    )

    content.append(Spacer(1, 20))

    content.append(disclaimer)

    doc.build(content)

    return send_file(filename, as_attachment=True)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':

    app.run(debug=True)
