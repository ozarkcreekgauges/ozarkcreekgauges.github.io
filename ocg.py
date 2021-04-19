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

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "ozarkcreekgauges@gmail.com"
    password = "WeLoveBoats1!"
      
    # Create a secure SSL context
    context = ssl.create_default_context()
      
    # Try to log in to server and send email
    try:
          server = smtplib.SMTP(smtp_server,port)
          server.ehlo() # Can be omitted
          server.starttls(context=context) # Secure the connection
          server.ehlo() # Can be omitted
          server.login(sender_email, password)
          #Send email here
          server.sendmail("ozarkcreekgauges@gmail.com", "ozarkcreekgauges@gmail.com", message)
    except Exception as e:
          # Print any error messages to stdout
          print(e)
    finally:
          server.quit() 

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
