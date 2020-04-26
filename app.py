#################################################
# MongoDB and Flask Application
#################################################

# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def home():
    destination_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=destination_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    #Run the scrape function
    mars_data = scrape_mars.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)