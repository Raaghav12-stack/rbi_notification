# RBI Notification Monitor & Summarizer

This project is designed to **automate the monitoring, summarization, and email delivery** of the latest notifications published on the Reserve Bank of India (RBI) Notifications page  
It extracts notification content (HTML or PDF), summarizes them using an LLM, and sends an email digest with clickable links — all with minimal manual intervention.

---

## Features

- Automatically scrapes new RBI notifications using Selenium
- Handles both HTML and PDF-based notifications
- Extracts main content and converts to plain text
- Summarizes the content using an LLM (via OpenRouter)
- Sends a formatted HTML email digest of all new summaries
- Avoids reprocessing old notifications using metadata
- Organized modular structure for easy extension and deployment

---

## Directory Structure
rbi-notifier/
├── fetch.py # Notification scraping logic
├── summarise.py # Text extraction and LLM summarization
├── emailer.py # Email formatting and delivery
├── config.py # All path and config variables
├── main.py # Orchestration of the full pipeline
├── .env # Sensitive credentials and API keys
├──notifications_data/
│ ├── extracted_text/ # Extracted .txt files from HTML
│ └── summary/ # LLM-generated summaries
├── processed_notifications.json # Metadata of seen notifications
└── seen_notifications.json # List of IDs already processed

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/your-username/rbi-notifier.git
cd rbi-notifier

### 2. Set Up Python Virtual Environment
python -m venv venv
source venv/bin/activate

### 3. Install Required Packages
pip install -r requirements.txt

### 4. Create .env File with Your Secrets
FROM_EMAIL=your_sender_email@gmail.com
TO_EMAIL=recipient_email@example.com
APP_PASSWORD=your_app_password
OPENROUTER_API_KEY=your_openrouter_key

## How to Run
python main.py
