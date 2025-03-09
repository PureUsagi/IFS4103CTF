from flask import Flask, request

app = Flask(__name__)

EXPECTED_SOURCE_ADDR = "127.0.0.1"

@app.route('/')
def index():
    source_addr = request.remote_addr

    # Simulate detection of SSRF (e.g., Flask app sending XML payloads)
    if source_addr == EXPECTED_SOURCE_ADDR:
        return "Secret Data: The flag is CTF{XXE_SSRF_SUCCESS}"
    
    return "This is a normal service. Nothing to see here."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)