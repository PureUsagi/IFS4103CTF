from flask import Flask, request, render_template_string
from lxml import etree
import traceback

def init_blind_routes(app):
    @app.route('/blind', methods=['GET'])
    def blind_index():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTF Challenge: Blind XXE Injection</title>
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
            <h1>Blind XXE Challenge</h1>
            <p>This challenge doesn't display the parsed data in the response (hence "blind").</p>
            <p>Try to exfiltrate server-side files or data by making the server connect to your endpoint! Get flag.txt</p>

            <form action="/blindAttack" method="POST">
                <textarea name="xml_payload" rows="10" cols="50" placeholder="Place your XML here"></textarea><br>
                <button type="submit">Submit Blind XXE Payload</button>
            </form>
        </body>
        </html>
        '''

    @app.route('/blindAttack', methods=['POST'])
    def blind_attack():
        xml_data = request.form.get('xml_payload', '')
        
        # Process the XML data using lxml (vulnerable to XXE)
        try:
            parser = etree.XMLParser(load_dtd=True, dtd_validation=False, resolve_entities=True, no_network=False)  # Enable external entities

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
                    <h1>Payload Received</h1>
                    <p>No parsed data is shown. This is a blind XXE scenario.</p>
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
                    <p>There was an error processing the XML data: {str(e)}</p>
                </div>
            </body>
            </html>
            """
            
            # Return the error page
            return error_html
