from flask import Flask, request, render_template_string, render_template, url_for
from lxml import etree

app = Flask(__name__)

EXPECTED_SOURCE_ADDR = "127.0.0.1"

@app.route('/')
def index():
    source_addr = request.remote_addr

    # Simulate detection of SSRF (e.g., Flask app sending XML payloads)
    if source_addr == EXPECTED_SOURCE_ADDR:
        hidden_message = "I hope this message finds it way into the right hands. If you are reading this message, that means my cover has been blown and I'm currently in hiding." \
        "But my time in the cartel has not gone to waste, I have discovered where the cartel are keeping <insert information here>. The information is kept in 2 locations," \
        " a decommissioned server with most of its contents removed (<IP and port>), and a experimental test server for XML attacks (<IP and port>). This is all I can provide you," \
        "good luck. -A4103"
        return ""
    
    return render_template("hidden.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
