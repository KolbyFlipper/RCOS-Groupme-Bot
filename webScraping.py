import requests, json

def getImage(imageName):

    url = "https://serpapi.com/search.json?q="
    keyword = imageName
    endOfUrl = "&tbm=isch&ijn=0"

    full_url = url+imageName+endOfUrl

    response = requests.get(full_url)
    x = response.json()
    return(x["suggested_searches"]["name"])


def getWeather(cityname):
    #credit to GeeksForGeeks.org for the basis of this function's code
    #code moderately edited by Kolby so it works with the bot
    key = "6c15d695c4ae781e55d0545f5d364b75"
    #this api key can be published, it doesn't really matter because it's only for openweathermap

    # base_url variable to store url
    url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city = cityname

    # complete url address
    complete_url = url + "appid=" + key + "&q=" + city

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
        return(" City Not Found - Syntax is \n \"Weather city\" or \n \"Weather ZipCode\"" +
          "\n Ex1: Weather Troy \n Ex2: Weather 12180")
