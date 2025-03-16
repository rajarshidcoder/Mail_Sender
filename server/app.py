from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"html", "csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_files():

    if "html_file" not in request.files or "csv_file" not in request.files:
        flash("Both HTML template and CSV file are required")
        return redirect(request.url)

    html_file = request.files["html_file"]
    csv_file = request.files["csv_file"]

    if html_file.filename == "" or csv_file.filename == "":
        flash("Please select both files")
        return redirect(request.url)

    if (
        html_file
        and allowed_file(html_file.filename)
        and csv_file
        and allowed_file(csv_file.filename)
    ):

        html_path = os.path.join(
            app.config["UPLOAD_FOLDER"], secure_filename(html_file.filename)
        )
        csv_path = os.path.join(
            app.config["UPLOAD_FOLDER"], secure_filename(csv_file.filename)
        )

        html_file.save(html_path)
        csv_file.save(csv_path)

        session["html_path"] = html_path
        session["csv_path"] = csv_path

        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        csv_headers = []
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            csv_headers = next(csv_reader)

        placeholders = []
        for item in html_content.split("["):
            if "]" in item:
                placeholder = "[" + item.split("]")[0] + "]"
                if placeholder not in placeholders:
                    placeholders.append(placeholder)

        return render_template(
            "preview.html", placeholders=placeholders, csv_headers=csv_headers
        )

    flash("Invalid file type. Only HTML and CSV files are allowed.")
    return redirect(request.url)


@app.route("/send", methods=["POST"])
def send_emails():
    html_path = session.get("html_path")
    csv_path = session.get("csv_path")

    if not html_path or not csv_path:
        flash("Files not found. Please upload again.")
        return redirect(url_for("index"))

    placeholder_mappings = {}
    email_column = request.form.get("email_column")

    for key, value in request.form.items():
        if key.startswith("map_"):
            placeholder = key.replace("map_", "")
            placeholder_mappings[placeholder] = value

    sender_email = request.form.get("sender_email") or os.getenv("EMAIL")
    sender_password = request.form.get("sender_password") or os.getenv("PASS")
    email_subject = request.form.get("email_subject") or "Automated Email"

    if not sender_email or not sender_password:
        flash("Email credentials not provided")
        return redirect(url_for("index"))

    sent_count = 0
    failed_count = 0
    error_message = None

    try:

        with open(html_path, "r", encoding="utf-8") as file:
            html_template = file.read()

        csv_data = []
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)

            email_index = (
                headers.index(email_column) if email_column in headers else None
            )
            if email_index is None:
                flash(f'Email column "{email_column}" not found in CSV')
                return redirect(url_for("index"))

            for row in csv_reader:
                if row:
                    csv_data.append(row)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)

            for row in csv_data:
                if len(row) <= email_index:
                    continue

                recipient_email = row[email_index]
                if not recipient_email:
                    continue

                personalized_html = html_template

                for placeholder, column_name in placeholder_mappings.items():
                    if column_name in headers:
                        column_index = headers.index(column_name)
                        if column_index < len(row):
                            replacement_value = row[column_index]
                            personalized_html = personalized_html.replace(
                                placeholder, replacement_value
                            )

                msg = MIMEMultipart()
                msg["Subject"] = email_subject
                msg["From"] = sender_email
                msg["To"] = recipient_email
                smtp.sendmail(sender_email, recipient_email, msg.as_string())
                sent_count += 1

        flash(f"Successfully sent {sent_count} emails")
    except Exception as e:
        failed_count = len(csv_data) - sent_count
        error_message = str(e)
        flash(
            f"Error occurred: {error_message}. Sent: {sent_count}, Failed: {failed_count}"
        )

    return render_template(
        "results.html",
        sent_count=sent_count,
        failed_count=failed_count,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
