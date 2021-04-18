#----------------------------
# Filename: scraper.py
# Author: Capstone Group 1
#----------------------------

import xml.etree.ElementTree as ET
import requests

def timeConvert(time):
    hours, minutes, extra, extra2 = time.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "AM"
    if hours > 12:
        setting = "PM"
        hours -= 12
    finalStandardTime = ("%02d:%02d" + setting) % (hours, minutes)
    return finalStandardTime

def scrape():
    with open('streamNumbers.txt','r') as file:
        lines = file.readlines()
        print(len(lines))

    names  = []
    times  = []
    values = []
    for i,line  in enumerate(lines):
        temp = line.split(" ")
        temp = temp[0].split('\t')
        number = temp[0]
        rest = line.replace(number,"")
        rest = rest[1:len(rest)-1]
        url = "https://waterservices.usgs.gov/nwis/iv/?format=waterml,2.0&sites="+number+"&parameterCd=00060,00065&siteStatus=all"

        resp = requests.get(url)
        root = ET.fromstring(resp.text)

        #Traverse the tree to find necessary values
        try:
            temp = root.findall('{http://www.opengis.net/waterml/2.0}observationMember')
            if len(temp) == 2:
                root = root.findall('{http://www.opengis.net/waterml/2.0}observationMember')[1]
            else:
                root = root.find('{http://www.opengis.net/waterml/2.0}observationMember')
            root = root.find('{http://www.opengis.net/om/2.0}OM_Observation')
            root = root.find('{http://www.opengis.net/om/2.0}result')
            root = root.find('{http://www.opengis.net/waterml/2.0}MeasurementTimeseries')
            root = root.find('{http://www.opengis.net/waterml/2.0}point')
            root = root.find('{http://www.opengis.net/waterml/2.0}MeasurementTVP')
            time = root.find('{http://www.opengis.net/waterml/2.0}time')
            value = root.find('{http://www.opengis.net/waterml/2.0}value')
            temp = time.text
            date, ftime = temp.split('T')
            standardTime = timeConvert(ftime)
            temp2 = standardTime + " " + date

            names.append(rest)
            times.append(temp2)
            values.append(value.text)
        except Exception as e:
            print("EXCEPTION")
            names.append(rest)
            times.append("NA")
            values.append("NA")

    return names, times, values
