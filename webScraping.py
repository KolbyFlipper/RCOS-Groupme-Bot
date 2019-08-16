import requests, json

#takes a string in any form, a single word or a full sentence or question.
#returns a LMGTFY link, which is a service that googles a phrase for you.
#useful if a user is asking questions in the chat that are exceedingly easy
#to google.
def letMeGoogleThatForYou(question):
    print(question)
    url = "https://lmgtfy.com/?q="

    wordArray = question.split()
    wordArray.pop(0)

    for word in wordArray:
        if (word.isalpha()):
            url += word
            url+= "+"
        #site ignores the extra + concatenated on, no need to strip it at the end.

    return url

def getWeather(cityname):
    #credit to GeeksForGeeks.org for the basis of this function's code
    #code moderately edited by Kolby so it works with the bot
    key = "6c15d695c4ae781e55d0545f5d364b75"
    #this api key can be published, it doesn't really matter because it's only for openweathermap

    # base_url variable to store url
    url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete url address
    complete_url = url + "appid=" + key + "&q=" + cityname

    # get method of requests module
    # return response object
    response = requests.get(complete_url)
    x = response.json()
    #could break if the site doesn't respond? not worried for now, but that's a footnote

    #check if city is found, if cod = 404 it's not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        current_temperature = y["temp"]
        current_temperature = (current_temperature - 273.15) * (9/5) +32 #temp in F
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]

        weather_description = z[0]["description"]

        # print following values
        return(" Temperature (in F) : " +
                        str(round(current_temperature,2)) +
              "\n Atmospheric pressure (in hPa) : " +
                        str(current_pressure) +
              "\n Humidity (by %) : " +
                        str(current_humidity) +
              "\n Description : " +
                        str(weather_description))

    else:
        return("City/zipcode not found! Are you sure you typed that right?")
