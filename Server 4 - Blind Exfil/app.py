from flask import Flask, request, render_template
from lxml import etree

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('blindOOB.html')

@app.route('/blindOOBAttack', methods=['POST'])
def blindOOBAttack():
    # Get the raw XML data from the request
    xml_data = request.data
    
    # Process the XML data using lxml (vulnerable to XXE)
    try:
        # Create an XML parser with external entity resolution enabled
        parser = etree.XMLParser(load_dtd=True, dtd_validation=False, resolve_entities=True, no_network=False, remove_blank_text=True, recover=True)  # Enable external entities
        
        # Parse the XML string
        root = etree.fromstring(xml_data, parser=parser)

        return render_template("blindOOB_response.html")

    except Exception as e:
        # Handle any errors that occur during XML processing and return an error page
        return render_template("blindOOB_error.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)