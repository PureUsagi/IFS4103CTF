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
        <title>Umbra Cartel Church Portal</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #121212;
                    color: #ddd;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }
                .container {
                    width: 40%;
                    margin: 50px auto;
                    background-color: #1e1e1e;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(255, 0, 0, 0.3);
                }
                h1 {
                    color: #ff4444;
                    text-transform: uppercase;
                    font-size: 24px;
                }
                .logo {
                    width: 100px;
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                    font-weight: bold;
                    color: #ff4444;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    margin: 8px 0;
                    border: 1px solid #444;
                    background-color: #222;
                    color: #fff;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #ff4444;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                    text-transform: uppercase;
                    font-weight: bold;
                }
                input[type="submit"]:hover {
                    background-color: #cc0000;
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
                <img src="static/images/umbra_cartel_logo.png" alt="Umbra Cartel Logo" class="logo">
                <h1>Blind Error Trial</h1>
                <p>Prove your faith to the priest, hand me your best XXE payload and you shall be rewarded!</p>
                <form action="/blindAttack" method="POST">
                    <textarea name="xml_payload" rows="10" cols="50" placeholder="I am 14 and this is deep"></textarea><br>
                    <button type="submit">I pledge my faith!</button>
                </form>
            </div>
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
            response_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Message Received</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #121212;
                        color: #ddd;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                    }
                    .container {
                        width: 40%;
                        margin: 80px auto;
                        background-color: #1e1e1e;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 10px rgba(255, 0, 0, 0.3);
                    }
                    .logo {
                        width: 100px;
                        margin-bottom: 20px;
                    }
                    h1 {
                        color: #ff4444;
                        font-size: 24px;
                        text-transform: uppercase;
                        text-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
                    }
                    p {
                        font-size: 18px;
                        color: #ccc;
                        padding: 10px;
                        background-color: #222;
                        border-left: 4px solid #ff4444;
                        display: inline-block;
                    }
                </style>
            </head>
            <body>
                    <h1>Payload Received</h1>
                    <p>Thank you for your pledge, we will make sure the priest will be in touch with you.</p>
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
