import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from dotenv import load_dotenv
load_dotenv()


def load_notifications_from_txt(summary_dir, metadata_path):
    if not os.path.exists(metadata_path):
        return []

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    link_map = {
        os.path.splitext(os.path.basename(x["text_file"]))[0]: x["pdf_link"]
        for x in metadata
    }

    notifications = []
    for fname in os.listdir(summary_dir):
        if fname.endswith("_summary.txt"):
            base = fname.replace("_summary.txt", "")
            with open(os.path.join(summary_dir, fname), "r", encoding="utf-8") as f:
                summary = f.read().strip()
            notifications.append({
                "title": base.replace("_", " "),
                "summary": summary,
                "pdf_link": link_map.get(base, "")
            })
    return notifications

def format_notifications_for_email(notifications):
    body = ""
    for n in notifications:
        bullets = "".join(f"<li>{line.strip()}</li>" for line in n["summary"].split("\n") if line.strip())
        body += f"""
        <h3>{n['title']}</h3>
        <ul>{bullets}</ul>
        <p><strong>📎 PDF:</strong> <a href="{n['pdf_link']}">{n['pdf_link']}</a></p>
        <hr>
        """
    return body

def send_email(html_body, subject, to_email , from_email , app_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    

    print(from_email, to_email, app_password)
    
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, app_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")
