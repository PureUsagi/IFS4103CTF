from flask import Flask
import base64

app = Flask(__name__)

@app.route('/')
def get_flag():
    try:
        with open('/flag/flag.txt', 'rb') as f:
            encoded_flag = base64.b64encode(f.read()).decode()
        return encoded_flag  # Just return the base64 flag, like PHP
    except Exception as e:
        return "Error"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=7000, debug=True)
