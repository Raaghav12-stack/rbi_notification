import os
import json

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_text_to_file(text, title, output_dir):
    filename = title.replace(" ", "_").replace("/", "-") + ".txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to: {filepath}")

def load_seen_notifications(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_notifications(seen_set, filepath):
    with open(filepath, "w") as f:
        json.dump(sorted(list(seen_set)), f)

def save_processed_notifications(notifications, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(notifications, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata for {len(notifications)} notifications to {filename}")
