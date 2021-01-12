from flask import Flask, jsonify
from flask import Response,json
# from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect

from pymongo import MongoClient
<<<<<<< HEAD
# import scrape_ranking

mongo = "MonashBootcamp"
=======
# from config import mongo
# import scrape_ranking
from selenium import webdriver
import time
from collections import defaultdict
import pandas as pd

GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
>>>>>>> 53d325092ec975ec1bca61f27b9797b56b074d49

#################################################
# Database Setup
#################################################
dbname = "Soccer_db"
client = MongoClient(f"mongodb+srv://Louis:{mongo}@cluster0.ddqv6.mongodb.net/{dbname}?retryWrites=true&w=majority")
soccer_db = client.get_database('Soccer_db')
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

<<<<<<< HEAD
@app.route("/",methods=['GET',"POST"])
=======
def scrape(league):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    if league == "England":
        url = "https://www.flashscore.com.au/football/england/epl/standings/"
    if league == "Spain":
        url = "https://www.flashscore.com.au/football/spain/laliga/standings/"
    if league == "Italy":
        url = "https://www.flashscore.com.au/football/italy/serie-a/standings/"
    #urls = [url_eng,url_es,url_it]

    table = defaultdict(list)
    #for url in urls:
    driver.get(url)
    time.sleep(1)

    col1 = driver.find_elements_by_xpath('//a[@class="rowCellParticipantName___38vskiN"]')
    col2 = driver.find_elements_by_xpath('//span[@class="  rowCell____vgDgoa cell___4WLG6Yd "]')
    
    for i in range(len(col1)):
        table["Ranking"].append(i+1)
        table["Team"].append(col1[i].text)
        if league == "England":
            table["League"].append('England')
        if league == "Spain":
            table["League"].append('Spain')
        if league == "Italy":
            table["League"].append('Italy')
    count = 0
    for i in range(len(col2)):
        if count == 0 :
            table["MP"].append(col2[i].text)
        if count == 1:
            table["W"].append(col2[i].text)
        if count == 2:
            table["D"].append(col2[i].text)
        if count == 3:
            table["L"].append(col2[i].text)
        if count == 4:
            table["Pts"].append(col2[i].text)
            count = -1
        count+=1
    table = dict(table)
    driver.close()
    # Return results
    return table

@app.route("/",methods=['GET', 'POST'])
>>>>>>> 53d325092ec975ec1bca61f27b9797b56b074d49
def home():
    select = "England"
    if request.method == 'POST':
        select = request.form.get('league')
    #get the title
    if select == "England":
        league_title = "English Premiere League"
        league_logo = "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/23.png&h=60&w=60&scale=crop&cquality=40&location=origin"
    if select == "Spain":
        league_title = "La Liga BVBA"
        league_logo = "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/15.png&h=60&w=60&scale=crop&cquality=40&location=origin"
    if select == "Italy":
        league_title = "Serie A"
        league_logo = "https://a.espncdn.com/combiner/i?img=/i/leaguelogos/soccer/500/12.png&h=60&w=60&scale=crop&cquality=40&location=origin"
    # Collect the data
    pred_col = soccer_db.predictions.find({"Country":select},{'_id': False}).sort("Predictions Final Ranking",1)
    pred_data = []
    for doc in pred_col:
        pred_data.append(doc)
    return render_template("correlation.html", pred = pred_data, title=league_title,logo = league_logo)

@app.route("/scrape",methods=['GET', 'POST'])
def scrape():
    select = "England"
    if request.method == 'POST':
<<<<<<< HEAD
        select = request.form.get('league')
        return redirect(url_for('home',select=select))
        
    # Collect the data
    ranking_data = scrape_ranking.scrape(select)
    return (jsonify(ranking_data))
=======
        select = request.form.value('league')
    else :
        select = "England"
    # Run the scrape function
    ranking_data = scrape(select)
    # for record in ranking_data:
    #     print(record["Ranking"])
    return render_template("index.html", ranking=ranking_data)
>>>>>>> 53d325092ec975ec1bca61f27b9797b56b074d49

@app.route("/financial")
def financial():
    return  render_template("financial.html")

@app.route("/correlation")
def correlation():
    return  render_template("correlation.html")

@app.route("/scatter/data", methods=["GET"])
def scatterData():
    #create connection

    team_stats_col = soccer_db.team_stats.find({},{'_id': False})
    data_scatter = []
    for doc in team_stats_col:
        data_scatter.append(doc)

    return  (jsonify(data_scatter))

@app.route("/corr/data", methods=["GET"])
def correlationData():
    #create connection
    app.config['JSON_SORT_KEYS'] = False

    corr_col = soccer_db.correlation.find({},{'_id': False})
    data_corr = []
    for doc in corr_col:
        data_corr.append(doc)

    return  (jsonify(data_corr))

@app.route("/financials/comparison/data", methods=["GET"])
def comparisonData():
   
    table = soccer_db.summary_financials.find({},{'_id': False})
    data = []
    for doc in table:
        data.append(doc)

    return  (jsonify(data))

@app.route("/financials/hero/data", methods=["GET"])
def heroData():

    table = soccer_db.transfer_summary.find({},{'_id': False})
    data = []
    for doc in table:
        data.append(doc)

    return  (jsonify(data))

@app.route("/financials/top4/data", methods=["GET"])
def top4_financialData():

    table = soccer_db.top4_financials.find({},{'_id': False})
    data = []
    for doc in table:
        data.append(doc)

    return  (jsonify(data))

@app.route("/diversity")
def diversity():

    return  render_template("z.html")

@app.route("/diversity/diversity_stats", methods=["GET"])
def summary_diversity_stats():
    #create connection
    collection = soccer_db.summary_diversity_stats.find({},{'_id': False})
    data = []
    for doc in collection:
        data.append(doc)

    return  (jsonify(data))

@app.route("/diversity/geo_data", methods=["GET"])
def geo_data():
    #create connection

    collection = soccer_db.geo_data.find({},{'_id': False})
    data = []
    for doc in collection:
        data.append(doc)
    
    return  (jsonify(data))


if __name__ == '__main__':
    app.run(debug=True)
