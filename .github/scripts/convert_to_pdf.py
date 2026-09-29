import sys
import os
import time
import urllib.request
import urllib.error

def convert_html_to_pdf(html_path, pdf_path, hf_space_url):
    if not os.path.exists(html_path):
        print(f"Warning: '{html_path}' was not found. Generating fallback report...")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("
