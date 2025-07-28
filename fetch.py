import os
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from config import BASE_URL, START_URL, TEXT_DIR, SEEN_FILE, METADATA_FILE
from utils import save_text_to_file, load_seen_notifications, save_seen_notifications, save_processed_notifications

def get_selenium_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    return driver
    # return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extract_notification_links(main_html):
    soup = BeautifulSoup(main_html, "html.parser")
    return list(set(
        urljoin(BASE_URL + "/Scripts/", a['href'])
        for a in soup.find_all('a', href=True)
        if "NotificationUser.aspx?Id=" in a['href']
    ))

def extract_notification_text(html):
    soup = BeautifulSoup(html, "html.parser")
    td_candidates = soup.find_all('td')
    best_td = max(td_candidates, key=lambda td: len(td.get_text(strip=True)), default=None)
    if not best_td:
        return "No useful text found."

    lines = []
    for element in best_td.find_all(['p', 'a']):
        if element.name == 'a' and element.get('href'):
            label = element.get_text(strip=True)
            full_url = urljoin(BASE_URL, element['href'])
            lines.append(f"{label} ({full_url})")
        else:
            text = element.get_text(strip=True)
            if text:
                lines.append(text)
    return "\n".join(lines)

def extract_pdf_links(html):
    soup = BeautifulSoup(html, "html.parser")
    return list(set(
        urljoin(BASE_URL, a['href'])
        for a in soup.find_all('a', href=True)
        if a['href'].lower().endswith(".pdf") and "rbidocs.rbi.org.in/rdocs/notification/PDFs/" in a['href']
    ))

def fetch_and_save_text_notifications():
    seen = load_seen_notifications(SEEN_FILE)
    newly_seen = set()
    processed = []
    driver = get_selenium_driver()

    try:
        driver.get(START_URL)
        time.sleep(3)
        main_html = driver.page_source
        links = extract_notification_links(main_html)
        print(f"Found {len(links)} notifications.")

        for link in links:
            notif_id = link.split("Id=")[-1].split("&")[0]
            if notif_id in seen:
                print(f"Skipping ID {notif_id}")
                continue

            print(f"Processing: {link}")
            driver.get(link)
            time.sleep(2)
            detail_html = driver.page_source

            pdf_links = extract_pdf_links(detail_html)
            pdf_link = pdf_links[0] if pdf_links else None

            soup = BeautifulSoup(detail_html, "html.parser")
            title_tag = soup.find('span', {'id': 'ContentPlaceHolder1_lblTitle'}) or soup.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else f"Notification_{notif_id}"

            text = extract_notification_text(detail_html)
            if pdf_link:
                text += f"\n\n[PDF Link]({pdf_link})"

            save_text_to_file(text, title, TEXT_DIR)
            newly_seen.add(notif_id)

            processed.append({
                "title": title,
                "text": text,
                "pdf_link": pdf_link,
                "source_url": link,
                "text_file": os.path.join(TEXT_DIR, title.replace(" ", "_").replace("/", "-") + ".txt")
            })
    finally:
        driver.quit()

    save_seen_notifications(seen.union(newly_seen), SEEN_FILE)
    save_processed_notifications(processed, METADATA_FILE)
    return processed
