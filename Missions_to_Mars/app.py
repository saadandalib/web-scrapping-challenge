from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Define the main route, query mongo db to get mars facts, return html page - index.html via render_template
@app.route("/")
def index():
    facts = mongo.db.facts.find_one()
    return render_template("index.html", facts=facts)

# Define srcape route, call function scrape from scrape_mars.app to perform web scraping,
# update mongo db collection with found data, return to the main page index.html
@app.route("/scrape")
def scraper():
    facts = mongo.db.facts
    mars_data = scrape_mars.scrape()
    print(mars_data)
    facts.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)