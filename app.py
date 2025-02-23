from flask import Flask, request, render_template_string
from lxml import etree
import os

app = Flask(__name__)

# Get the current working directory
current_directory = os.getcwd()

# Define the filename
file_path = os.path.join(current_directory, 'test.txt')

# Create the file and write content to it
with open(file_path, 'w') as file:
    file.write("This is a test file created by the Flask app.\n")
    file.write("You can now read it with XXE injection!")


# Main page with form
@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTF Challenge: XXE Injection</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 50%;
                margin: 50px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin: 8px 0 20px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            .footer {
                text-align: center;
                font-size: 12px;
                color: #888;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CTF Challenge: XXE Injection</h1>
            <form action="/submit" method="POST" enctype="text/plain">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br>

                <label for="message">Message:</label>
                <input type="text" id="message" name="message" required><br>

                <input type="submit" value="Submit">
            </form>
        </div>

        <script>
            document.querySelector('form').addEventListener('submit', function(e) {
                e.preventDefault();
                const name = document.querySelector('input[name="name"]').value;
                const message = document.querySelector('input[name="message"]').value;
                const xmlData = `<root><name>${name}</name><message>${message}</message></root>`;
                fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/xml'
                    },
                    body: xmlData
                }).then(response => response.text())
                  .then(data => document.body.innerHTML = data);
            });
        </script>
    </body>
    </html>

    '''

@app.route('/submit', methods=['POST'])
def submit():
    # Get the raw XML data from the request
    xml_data = request.data.decode('utf-8')
    
    # Process the XML data using lxml (vulnerable to XXE)
    try:
        # Create an XML parser with external entity resolution enabled
        parser = etree.XMLParser(resolve_entities=True, no_network=False)  # Enable external entities

        # Parse the XML string
        root = etree.fromstring(xml_data, parser=parser)

        # Extract the 'name' field from the XML
        name = root.find('name').text

        # Build a beautified HTML response page
        response_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Message Received</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 50%;
                    margin: 50px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #4CAF50;
                }}
                p {{
                    font-size: 18px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Message Received</h1>
                <p>Thanks, {name}! Your message has been successfully received.</p>
            </div>
        </body>
        </html>
        """

        # Return the beautified HTML response
        return response_html

    except Exception as e:
        # Handle any errors that occur during XML processing and return an error page
        error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error Processing XML</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 50%;
                    margin: 50px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #f44336;
                }}
                p {{
                    font-size: 18px;
                    text-align: center;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Error Processing XML</h1>
                <p>There was an error processing the XML data: {e}</p>
            </div>
        </body>
        </html>
        """
        
        # Return the error page
        return error_html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)