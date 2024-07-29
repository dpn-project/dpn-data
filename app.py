from flask import Flask, render_template, request, redirect, url_for, flash
import json
import re
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DOMAINS_FILE = 'domains.json'

def load_domains():
    if os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_domains(domains):
    with open(DOMAINS_FILE, 'w') as file:
        json.dump(domains, file, indent=4)
    print(f"[+] Domains saved: {domains}")

def is_valid_dpn_domain(dpn_domain):
    if re.match(r'^[a-zA-Z0-9.-]+$', dpn_domain) and '.' in dpn_domain:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        dpn_domain = request.form['dpn_domain']
        existing_website = request.form['existing_website']

        domains = load_domains()
        print(f"[+] Loaded domains: {domains}")

        if dpn_domain in domains:
            flash('DPN domain already exists.')
            return redirect(url_for('register'))

        if not is_valid_dpn_domain(dpn_domain):
            flash('Invalid DPN domain. It should contain only English letters, numbers, dots, and at least one dot.')
            return redirect(url_for('register'))

        domains[dpn_domain] = existing_website
        save_domains(domains)
        flash('DPN domain registered successfully.')
        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)