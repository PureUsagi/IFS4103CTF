from flask import Flask, request, render_template
from lxml import etree

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('blindError.html')

@app.route('/submit', methods=['POST'])
def submit():

    xml_data = request.form.get('xml_payload', '')

    # Process the XML data using lxml (vulnerable to XXE)
    try:
        parser = etree.XMLParser(load_dtd=True, dtd_validation=False, resolve_entities=True, no_network=False)  # Enable external entities

    # Parse the XML string
        root = etree.fromstring(xml_data, parser=parser)

        # Return the beautified HTML response
        return render_template("blindError_response.html")

    except Exception as e:
        # Return the error page
        return render_template("blindError_error.html", e=e)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)