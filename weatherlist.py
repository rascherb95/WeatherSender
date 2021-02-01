import requests
import json
import ssl
import smtplib
import datetime as dt
import csv
from decouple import config

api_key = config('weather_api')
password = config('mailer_pass')

url_id = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&appid={}"

#gmail / api vars
port = 465
password = config('weather_api_pass')
context = ssl.create_default_context()
sender_email = config('sender_email')

#time vars for schedule
current_time = dt.datetime.now()
current_hour = (current_time.hour)
current_min  = (current_time.minute)


#define our CSV-import-Class
class ListRecipient:
    def __init__(self,email,city,state):
        self.email = email
        self.city = city
        self.state = state
        self.api_url = url_id.format(self.city,self.state,api_key)

    def get_recipient_url(self):
        return self.api_url

#define forecast object (stores data from api)
class Forecast:
    def __init__(self, air_temp, real_feel, recipient):
        self.air_temp=air_temp
        self.real_feel=real_feel
        self.recipient=recipient
    def formatted_forecast(self):
        return "Air Temp = {}\nReal Feel = {}".format(self.air_temp,self.real_feel)

#function to get data from api
def get_forecast_by_recipient(recipient):
    response = requests.get(recipient.get_recipient_url())
    weather_data = json.loads(response.text)
    return Forecast(weather_data['main']['temp'], weather_data['main']['feels_like'], recipient)

def send_email(forecast):
    message =("""Your lunchtime weather report for {}, {}


    It is {} degrees
    It feels like {} degress

        """.format(forecast.recipient.city,forecast.recipient.state,forecast.air_temp,forecast.real_feel))
    with smtplib.SMTP_SSL('smtp.gmail.com', port,
                            context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,forecast.recipient.email,message)
        server.quit()

#just to double check it only sends once
if current_hour == 11 and current_min == 59:
    with open('mailinglist.csv','r') as read_csv:
        reader = csv.reader(read_csv,delimiter=',')
        for row in reader:
            u = ListRecipient(*row)
            forecast=get_forecast_by_recipient(u)
            send_email(forecast)
    print('Success!')
else:
    print('Not sent, try again later')
