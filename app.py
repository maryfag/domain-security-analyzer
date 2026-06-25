from flask import Flask, render_template, request, jsonify
import whois

app = Flask(__name__)

# Route 1: This serves your HTML interface to your browser
@app.route('/')
def home():
    return render_template('index.html')

# Route 2: This processes the URL submitted by your frontend
@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.get_json()
    target_url = data.get('url')

    try:
        # Grab the domain data via WHOIS
        domain_data = whois.whois(target_url)
        registrar = domain_data.registrar or "Unknown Registrar"

        return jsonify({
            "status": "success",
            "message": f"Scan complete! This site is registered via: {registrar}"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Could not scan this domain. Check the spelling."
        })

if __name__ == '__main__':
    app.run(debug=True)