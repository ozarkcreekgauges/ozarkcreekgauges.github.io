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

import smtplib
from email.message import EmailMessage
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
    message = "Type: " + form['type'] + "\n " +
        "User Name: "+ form['name'] + "\n" +
        "Contact Info: " +form['contactinfo'] + "\n" +
        "River Name: "+ form['rivername'] + "\n" +
        "Gauge: "+ form['gauge2'] + "\n" +
        "Location: "+ form['location2'] + "\n" +
        "Message: "+ form['message'] + "\n"

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = form['rivername'] + "addition"
    msg['From'] = "ozarkcreekgauges@gmail.com"
    msg['To'] = "ozarkcreekgauges@gmail.com"
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

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
