from flask import Flask, request, render_template_string, render_template, url_for
from lxml import etree

app = Flask(__name__)

EXPECTED_SOURCE_ADDR = "127.0.0.1"

@app.route('/')
def index():
    source_addr = request.remote_addr

    # Simulate detection of SSRF (e.g., Flask app sending XML payloads)
    if source_addr == EXPECTED_SOURCE_ADDR:
        return "I see that you have found me"
    
    return render_template("hidden.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
