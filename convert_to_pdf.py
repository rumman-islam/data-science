import markdown
from xhtml2pdf import pisa
import re

# Read Markdown report
with open('LAB_REPORT.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert Markdown to HTML with extensions
html_body = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'codehilite', 'toc']
)

# Custom PDF CSS styling compatible with xhtml2pdf
html_style = """
<style>
    @page {
        size: a4 portrait;
        margin: 1.5cm;
    }
    body {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.5;
        color: #222222;
    }
    h1 {
        font-size: 20pt;
        color: #1a365d;
        text-align: center;
        margin-bottom: 8px;
        padding-bottom: 5px;
    }
    h2 {
        font-size: 14pt;
        color: #2b6cb0;
        margin-top: 18px;
        margin-bottom: 8px;
        border-bottom: 1px solid #cbd5e0;
        padding-bottom: 3px;
    }
    h3 {
        font-size: 11pt;
        color: #2d3748;
        margin-top: 12px;
        margin-bottom: 6px;
    }
    p {
        margin-bottom: 8px;
        text-align: justify;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    th {
        background-color: #2b6cb0;
        color: #ffffff;
        font-weight: bold;
        padding: 6px 8px;
        text-align: left;
        font-size: 9pt;
    }
    td {
        padding: 5px 8px;
        border-bottom: 1px solid #e2e8f0;
        font-size: 9pt;
    }
    tr:nth-child(even) {
        background-color: #f7fafc;
    }
    code {
        font-family: Courier, monospace;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 2px 4px;
        font-size: 8.5pt;
    }
    pre {
        background-color: #f8fafc;
        color: #0f172a;
        border: 1px solid #cbd5e0;
        padding: 10px;
        font-size: 8pt;
        margin-bottom: 12px;
    }
    pre code {
        background-color: transparent;
        color: inherit;
        padding: 0;
    }
    img {
        max-width: 500px;
        width: 100%;
        display: block;
        margin: 12px auto;
        text-align: center;
    }
    hr {
        border: 0;
        height: 1px;
        background: #cbd5e0;
        margin: 15px 0;
    }
</style>
"""

full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{html_style}</head><body>{html_body}</body></html>"

# Convert HTML to PDF using xhtml2pdf
output_pdf_path = "LAB_REPORT.pdf"
with open(output_pdf_path, "wb") as pdf_file:
    pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)

if pisa_status.err:
    print("Error during PDF creation:", pisa_status.err)
else:
    print(f"PDF successfully created: {output_pdf_path}")
