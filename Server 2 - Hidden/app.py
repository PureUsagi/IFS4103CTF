from flask import Flask, request, render_template
from lxml import etree

app = Flask(__name__)

EXPECTED_SOURCE_ADDR = "127.0.0.1" ## Remember to change

@app.route('/')
def index():
    source_addr = request.remote_addr

    # Simulate detection of SSRF (e.g., Flask app sending XML payloads)
    if source_addr == EXPECTED_SOURCE_ADDR:
        hidden_message = "Message can be accessed at URL /static/not_sus.html of this server."
        return hidden_message
    
    return render_template("hidden.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
