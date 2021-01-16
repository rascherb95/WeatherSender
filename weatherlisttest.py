import requests
import json
import ssl
import smtplib
import datetime
import csv
from decouple import config

api_key = '695b86f565c2d9468123e937ad407980'
#password = config('mailer_pass')

#global url inherited by each object
#note - to add functionality for more parameters. currently only city, state, apikey & defaulted fahrenheit
url_id = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&appid={}"


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
    def __init__(self, air_temp, real_feel):
        self.air_temp=air_temp
        self.real_feel=real_feel
    def formatted_forecast(self):
        return "Air Temp = {}\nReal Feel = {}".format(self.air_temp,self.real_feel)

#function to get data from api
def get_forecast_by_recipient(recipient):
    response = requests.get(recipient.get_recipient_url())
    weather_data = json.loads(response.text)
    return Forecast(weather_data['main']['temp'], weather_data['main']['feels_like'])

#create our list of Objects
object_list = []

#to convert CSV data into ListReceipient objects, then added to ObjectList
with open('mailinglist.csv','r') as read_csv:
    reader = csv.reader(read_csv,delimiter=',')
    for row in reader:
        object_list.append(ListRecipient(*row))

#to create empty lists
mailers = []
cities = []
states = []
airtemps = []  # figure out how to fill
realfeels = []  # figure out how to fill

#to create our lists of object data & API data
for x in object_list:
    forecast = get_forecast_by_recipient(x)
    mailers.append(x.email)
    cities.append(x.city)
    states.append(x.state)
    airtemps.append(forecast.air_temp)
    realfeels.append(forecast.real_feel)

#to create the dictionary of email:[data]
mailing_list = {a:[b,c,d,e] for a, b, c, d, e in zip(mailers,cities,states,airtemps,realfeels)}

print(mailing_list)
print(mailing_list.keys)
