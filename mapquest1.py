from time import time, ctime
current_DateTime = time()
print("\nThe output of time():",current_DateTime)
print('\nToday is: ',ctime(current_DateTime))
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "pmp9aYEbDqBwX98dZIxrTDWvwL4TnWEg" #Replace with your MapQuest key

while True:
    orig = input("Lugar origen: ")
    if orig == "quit" or orig == "h":
        break
    dest = input("Destino: ")
    if dest == "quit" or dest == "h":
        break
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Direcciones de origen y destino " + (orig) + " to " + (dest))
        print("Duracion del viaje:   " + (json_data["route"]["formattedTime"]))
        print("Kilometros:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print("=============================================")
    for each in json_data["route"]["legs"][0]["maneuvers"]:
        print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
        print("=============================================\n")
