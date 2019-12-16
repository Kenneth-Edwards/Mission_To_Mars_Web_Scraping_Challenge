from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time

# Create an instance of Flask
app = Flask(__name__)
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.static_folder = 'static'

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database and assign it to "mars_scrape"
    mars_scrape = mongo.db.marscollection.find_one()
    # Return template and data
    return render_template("index.html", description=mars_scrape)

################################################################################

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the "scrape" function in the scrape_mars.py file
    # scrape_data = scrape_mars.scrape()
    scrape_data = scrape_mars.scrape()

    # Update the Mongo database using .update and upsert=True OR .insert()
    # mongo.db.coastacollection.update({}, scrape_data, upsert=True)
    mongo.db.marscollection.drop()
    mongo.db.marscollection.insert(scrape_data)  

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)