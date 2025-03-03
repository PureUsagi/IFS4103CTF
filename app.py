from flask import Flask, request, render_template_string, render_template, url_for
from lxml import etree
import os
import blindError

app = Flask(__name__)

blindError.init_blind_routes(app)
# Get the current working directory
current_directory = os.getcwd()

# Define the filename
file_path = os.path.join(current_directory, 'test.txt')

# Create the file and write content to it
with open(file_path, 'w') as file:
    file.write("This is a test file created by the Flask app.\n")
    file.write("You can now read it with XXE injection!")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Main page with form
@app.route('/basic', methods=['GET'])
def basic_index():
    return render_template("basicchallange.html")

@app.route('/submit', methods=['POST'])
def submit():
    # Get the raw XML data from the request
    xml_data = request.data.decode('utf-8')
    
    # Process the XML data using lxml (vulnerable to XXE)
    try:
        # Create an XML parser with external entity resolution enabled
        parser = etree.XMLParser(resolve_entities=True, no_network=False, load_dtd=True)  # Enable external entities

        # Parse the XML string
        root = etree.fromstring(xml_data, parser=parser)

        # Extract the 'name' field from the XML
        location = root.find('location').text

        # Return the beautified HTML response
        return render_template("basicchallange_response.html", location=location)

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
                <p>There was an error processing the XML data: {str(e)}</p>
            </div>
        </body>
        </html>
        """
        
        # Return the error page
        return error_html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)