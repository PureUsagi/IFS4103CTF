#!/usr/bin/env python3
"""
License: Class 3
Contact: 995
Dependencies: Grades
"""
from flask import Flask, request, render_template_string, render_template, url_for
from lxml import etree  # Ensure lxml is imported for XML parsing
import traceback

app = Flask(__name__)

def init_blindOOB(app):
    @app.route('/blindOOB', methods=['GET'])
    def blindOOB_index():
        return render_template("blindOOB.html")

    @app.route('/blindOOBAttack', methods=['POST'])
    def blindOOBAttack():
        # Get the raw XML data from the request
        xml_data = request.data
        
        # Process the XML data using lxml (vulnerable to XXE)
        try:
            # Create an XML parser with external entity resolution enabled
            parser = etree.XMLParser(load_dtd=True, dtd_validation=False, resolve_entities=True, no_network=False, remove_blank_text=True)  # Enable external entities
            
            # Parse the XML string
            root = etree.fromstring(xml_data, parser=parser)

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
                    <h1>Press back to return to home page.</h1>
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
                    <p>There was an error processing the XML data</p>
                </div>
            </body>
            </html>
            """
            
            # Return the error page
            return error_html
