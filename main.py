from fetch import fetch_and_save_text_notifications
from summarise import summarize_all_txt
from config import TEXT_DIR, SUMMARY_DIR, METADATA_FILE
from emailer import load_notifications_from_txt, format_notifications_for_email, send_email
import os
import config

def main():
    fetch_and_save_text_notifications()
    summarize_all_txt(TEXT_DIR, SUMMARY_DIR)
    
    notifications = load_notifications_from_txt(SUMMARY_DIR, METADATA_FILE)
    if not notifications:
        print("No summaries to send")
        return

    html_body = format_notifications_for_email(notifications)
    subject = "RBI Notification Summary Digest"
    from_email = config.FROM_EMAIL
    to_email =  config.TO_EMAIL
    app_password = config.APP_PASSWORD

    send_email(html_body, subject, to_email, from_email, app_password)

if __name__ == "__main__":
    main()
