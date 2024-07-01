from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")


HOST = ip_address
PORT = 9999

sitename = {
    'en': "PS by Fabian_MCH",
    'de': "PS von Fabian_MCH",
    'fr': "PS par Fabian_MCH"
}
heading1 = {
    'en': "Private Storage by Fabian_MCH",
    'de': "Privater Speicher von Fabian_MCH",
    'fr': "Stockage Privé par Fabian_MCH"
}
text1 = {
    'en': "All stored things",
    'de': "Alle gespeicherten Dinge",
    'fr': "Toutes les choses stockées"
}
icon_path = "assets/icon.ico"
image_path = "assets/icon.jpg"

language_icons = {
    'en': "assets/flags/en_flag.png",
    'de': "assets/flags/de_flag.png",
    'fr': "assets/flags/fr_flag.png"
}

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/favicon.ico':
            if os.path.exists(icon_path):
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.end_headers()
                with open(icon_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return

        for lang, img_path in language_icons.items():
            if self.path == f'/{img_path}':
                if os.path.exists(img_path):
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.end_headers()
                    with open(img_path, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.end_headers()
                return

        if self.path == '/assets/icon.jpg':
            if os.path.exists(image_path):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open(image_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return

        # Determine language based on query parameter
        language = 'en'  # default language
        if '?' in self.path:
            query = self.path.split('?')[1]
            params = dict(param.split('=') for param in query.split('&'))
            if 'lang' in params and params['lang'] in ['en', 'de', 'fr']:
                language = params['lang']

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        main_background = "#0C6198"
        txt1_background = "#ecf0f1"
        box_background = "#064D7B"

        heading_color = "#9400FF"
        dropdown_background = "#D200FF"
        dropdown_textcolor = "white"
        languages_background = "#f1f1f1"
        lg_text_color = "black"



        # Construct HTML content dynamically
        html_content = f"""
        <!DOCTYPE html>
        <html lang="{language}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{sitename[language]}</title>
            <link rel="icon" href="/favicon.ico" type="image/x-icon">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: {main_background};
                    color: {txt1_background};
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }}
                .container {{
                    text-align: center;
                    padding: 20px;
                    background-color: {box_background};
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                h1 {{
                    color: {heading_color};
                }}
                p {{
                    font-size: 1.2em;
                }}
                img {{
                    margin-top: 20px;
                    max-width: 100%;
                    height: auto;
                    border-radius: 10px;
                }}
                .language-switcher {{
                    position: absolute;
                    top: 20px;
                    right: 20px;
                }}
                .dropdown {{
                    position: relative;
                    display: inline-block;
                }}
                .dropbtn {{
                    background-color: {dropdown_background};
                    color: {dropdown_textcolor};
                    padding: 10px;
                    font-size: 16px;
                    border: none;
                    cursor: pointer;
                    border-radius: 5px;
                }}
                .dropdown-content {{
                    display: none;
                    position: absolute;
                    background-color: {languages_background};
                    min-width: 160px;
                    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                    z-index: 1;
                    left: -70px; /* Show to the left */
                }}
                .dropdown-content a {{
                    color: {lg_text_color};
                    padding: 12px 16px;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                }}
                .dropdown-content a img {{
                    margin-right: 10px;
                    width: 20px;
                    height: 20px;
                }}
                .dropdown-content a:hover {{background-color: #D8D8D8}}
                .dropdown:hover .dropdown-content {{display: block;}}
                .dropdown:hover .dropbtn {{background-color: #9400FF;}}
            </style>
        </head>
        <body>
            <div class="language-switcher">
                <div class="dropdown">
                    <button class="dropbtn">Language</button>
                    <div class="dropdown-content">
                        <a href="?lang=en"><img src="/{language_icons['en']}" alt="English"> English</a>
                        <a href="?lang=de"><img src="/{language_icons['de']}" alt="German"> German</a>
                        <a href="?lang=fr"><img src="/{language_icons['fr']}" alt="French"> French</a>
                    </div>
                </div>
            </div>
            <div class="container">
                <h1>{heading1[language]}</h1>
                <p>{text1[language]}</p>
                <img src="/assets/icon.jpg" alt="Cool Picture">
            </div>
        </body>
        </html>
        """

        self.wfile.write(bytes(html_content, "utf-8"))

server = HTTPServer((HOST, PORT), NeuralHTTP)
print("Now running...")
server.serve_forever()
server.server_close()
print("Server stopped!")