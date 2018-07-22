from flask import Flask, render_template, jsonify, redirect
from pymongo import MongoClient
from scrape_mars import scrape

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
	mars = db.mars.find_one()
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def mars_scraping():
	mars = db.mars
	mars_data = scrape()
	mars.update(
		{},
		mars_data,
		upsert=True
	)
	return redirect("/", code=302)

# @app.route("/test")
# def test():
# 	mars = db.mars
# 	mars_data={'weather':77}
# 	mars.insert(mars_data)

# test()

if __name__ == "__main__":
	app.run(debug=True)