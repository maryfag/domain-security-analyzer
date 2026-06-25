from urllib.parse import urlparse # Add this import at the top of app.py

# Update just this section inside your scan_url() function:
@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.get_json()
    raw_url = data.get('url').strip()
    
    # Clean up the URL (adds http:// if missing so urlparse can read it properly)
    if not raw_url.startswith(('http://', 'https://')):
        clean_url = 'http://' + raw_url
    else:
        clean_url = raw_url
        
    # Extract just the main domain (e.g., "zenfy.com")
    target_domain = urlparse(clean_url).netloc
    if target_domain.startswith('www.'):
        target_domain = target_domain[4:]

    try:
        # Now pass the perfectly cleaned domain to whois
        domain_data = whois.whois(target_domain)
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