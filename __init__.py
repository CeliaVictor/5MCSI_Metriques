from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #test2
  
@app.route("/contact/")
def mongraphique3():
    return render_template("contact.html")
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

# Fonction pour extraire les minutes à partir d'une date au format ISO
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Nouvelle route pour afficher les commits sous forme de graphique
@app.route('/commits/')
def get_commits():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        response = requests.get(url)

        if response.status_code != 200:
            return f"Erreur lors de la récupération des commits: {response.status_code}", 500

        commits_data = response.json()

        commits_info = []
        for commit in commits_data:
            commit_date = commit['commit']['author']['date']
            commits_info.append({'date': commit_date})

        return jsonify(commits=commits_info)

    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}", 500

# Fonction pour extraire les minutes d'un timestamp donné
def extract_minutes_from_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute

if __name__ == "__main__":
    app.run(debug=True)
