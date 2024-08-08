"""
Project Name: Lights On
Filename: main.py
Title: Main Flask server
Designed & Developed by
    Muhilan
    Naveen
    Raghava
GitHub: @raghavtwenty
Date Created: March 15, 2023 | Last Updated: August 7, 2024
Language: Python | Version: 3.11.9, 64-bit
"""


# Required imports
from flask import Flask, render_template
from flask import request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Environment variables
load_dotenv()
OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# Flask
app = Flask(__name__)

# API url endpoint
base_url = "http://api.openweathermap.org/data/2.5/weather?"


# Calculation 
@app.route('/result',methods = ['POST'])
def main():
    
    if city != '':
        # Make connection
        complete_url = base_url + "appid=" + OPEN_WEATHER_MAP_API_KEY + "&q=" + city
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]

            # Retrieve parameters
            current_temperature = main_data["temp"]
            current_humidity = main_data["humidity"]
            weather_description = data["weather"][0]["description"]
            visi = data['visibility']
            sun_rise = data['sys']['sunrise']
            sun_set = data['sys']['sunset']
            
            # Datetime conversion
            sun_rise = datetime.utcfromtimestamp(sun_rise)
            sun_set = datetime.utcfromtimestamp(sun_set)

            # Format datetime object to human-readable string
            sunrise_dt_con = sun_rise.strftime('%Y-%m-%d %H:%M:%S')
            sunset_dt_con = sun_set.strftime('%Y-%m-%d %H:%M:%S')

            # Decision
            if visi >= 2000 and current_temperature >= 280:
                lights = "LIGHTS ARE TURNED OFF"
            else : 
                lights = "LIGHTS ARE TURNED ON"

            # Final Show
            return render_template('result.html',
            CT = current_temperature, 
            CH = current_humidity ,
            WD = weather_description,
            S_rise = sunrise_dt_con,
            S_set = sunset_dt_con, 
            Vis = visi,
            lig = lights)
        else:
            return render_template('')
    else : 
        return render_template('')


# Default Home Route
@app.route('/')
def home():
    # User location
    global city

    city = str(request.form.get('city'))

    return render_template('index.html')


# Main
if __name__ == "__main__":
    app.run()