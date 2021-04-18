#--------------------------------------------------------
#File Name: ocg.py
#Purpose: App router for the Ozark Creek Gauges Web App
#Author: Capstone Group 1
#Date: January 31, 2021
#Includes Templates from templated.co
#--------------------------------------------------------
from flask import Flask, request, render_template, session, redirect
import random
from scraper import scrape
import time
import threading
app = Flask(__name__,static_folder='static', static_url_path='/static')

#Global Variables for HTML placeholders
names = []
times = []
values = []
loading = ""

#Adjust necessary globals once the scraper thread is finished
def background():
      items = scrape()
      global names
      names = items[0]
      global times
      times = items[1]
      global values
      values = items[2]
      global loading
      loading = 'none'
#Takes form data as a Dictionary and appends it to file
def writeToFile(form):
    with open("additions.txt",'a+') as file:
        file.write("-----------------------------------\n")
        file.write("Type: " + form['type'])
        file.write("\n")
        file.write("User Name: "+ form['name'])
        file.write("\n")
        file.write("Contact Info: " +form['contactinfo'])
        file.write("\n")
        file.write("River Name: "+ form['rivername'])
        file.write("\n")
        file.write("Gauge: "+ form['gauge2'])
        file.write("\n")
        file.write("Location: "+ form['location2'])
        file.write("\n")
        file.write("Message: "+ form['message'])
        file.write("\n")
        file.write("\n")

#Main/Table page
@app.route('/',methods=["GET"])
@app.route('/index.html',methods=["GET"])
def index():
    t1 = threading.Thread(target=background)
    t1.start()
    return render_template('index.html',names = names, times = times, values = values, loading=loading)

#River Map
@app.route('/map.html',methods=["POST","GET"])
def map():
    return render_template('map.html')

#About Page with Changes Submission
@app.route('/about.html',methods=["POST","GET"])
def about():
    return render_template('about.html')

#For submitting changes
@app.route('/submit',methods=["POST","GET"])
def submit():
    writeToFile(request.form)
    return redirect("/about.html")


if __name__ == "__main__":
    app.run()
