from flask import Flask, request, render_template_string, render_template
from lxml import etree
import traceback

def init_blind_routes(app):
    @app.route('/blind', methods=['GET'])
    def blind_index():
        return render_template('blinderror.html')

    @app.route('/blindAttack', methods=['POST'])
    def blind_attack():
        xml_data = request.data.decode('utf-8')
        
        # Process the XML data using lxml (vulnerable to XXE)
        try:
            parser = etree.XMLParser(load_dtd=True, dtd_validation=False, resolve_entities=True, no_network=False)  # Enable external entities

            # Parse the XML string
            root = etree.fromstring(xml_data, parser=parser)
            #root sent to jesus
            return render_template('blinderror_response.html')

        except Exception as e:
            # Handle any errors that occur during XML processing and return an error page
            return render_template("blinderror_error.html", e=e)
