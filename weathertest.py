import requests
import json
import ssl
import smtplib
from decouple import config

api_key = config('weather_api')
city = 'Philadelphia'
state = 'Philadelphia'

url_id = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&appid={}".format(city,state,api_key)

#to get weather data
response = requests.get(url_id)
weather_data = json.loads(response.text)
#temperature variabls
air_temp = weather_data['main']['temp']
real_feel = weather_data['main']['feels_like']
delta = air_temp - real_feel

#email variables
sender_email = 'rascherbpythontesting@gmail.com'
receiver_email = 'rascherb95@gmail.com'

#connection to gmail
port = 465
password = config('weather_api_pass')
context = ssl.create_default_context()


#email to be sent
message = """\
Subject: Your weather report for {}, {}

It is currently  {} degrees outside
The real feel is {} degrees

Send via python""".format(city,state,air_temp,real_feel)


with smtplib.SMTP_SSL('smtp.gmail.com', port,
                        context=context) as server:
    server.login(sender_email,password)
    server.sendmail(sender_email,receiver_email,message)
