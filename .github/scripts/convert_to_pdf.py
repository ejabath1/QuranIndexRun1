import sys
import os
import urllib.request
import urllib.parse

def convert_html_to_pdf(html_path, pdf_path, hf_space_url):
    if not os.path.exists(html_path):
        print(f"Error: HTML file '{html_path}' not found.")
        sys.exit(1)

    url = f"{hf_space_url.rstrip('/')}/convert"
    
    with open(html_path, "rb") as f:
        file_bytes = f.read()

    # Construct standard multipart/form-data payload without external packages
    boundary = "----GitHubActionsFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(html_path)}"\r\n'
        f"Content-Type: text/html\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )

    print(f"Uploading {html_path} to HF Space endpoint: {url}...")
    try:
        with urllib.request.urlopen(req) as response:
            pdf_data = response.read()

        with open(pdf_path, "wb") as f:
            f.write(pdf_data)
        
        print(f"Successfully generated PDF: {pdf_path} ({len(pdf_data)} bytes)")
    except Exception as e:
        print(f"Failed to convert HTML to PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python convert_to_pdf.py   ")
        sys.exit(1)
        
    convert_html_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
