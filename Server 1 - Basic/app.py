from flask import Flask, request, render_template_string, render_template, url_for
from lxml import etree
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('basicchallange.html')

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
        # Return the error page
        return render_template("basicchallenge_error.html", e=e)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)