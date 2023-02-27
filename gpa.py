import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Login script")

# Define the expected arguments
parser.add_argument("-u", "--username", type=str, help="Your username")
parser.add_argument("-p", "--password", type=str, help="Your password")

# Parse the arguments from the command line
args = parser.parse_args()

# Access the values of the arguments
username = args.username
password = args.password

hostName = "http://jw.hitsz.edu.cn"

# Get lt, execution and eventId from the first request
session = requests.Session()
response = session.get(f"{hostName}/cas")
soup = BeautifulSoup(response.text, "html.parser")
cookies = response.cookies.get_dict()
lt = soup.select_one("input[name=lt]")
if lt is not None:
    lt = lt["value"]
execution = soup.select_one("input[name=execution]")
if execution is not None:
    execution = execution["value"]
eventId = soup.select_one("input[name=_eventId]")
if eventId is not None:
    eventId = eventId["value"]

# Perform second request to log in
login_url = "https://sso.hitsz.edu.cn:7002/cas/login?service=http%3A%2F%2Fjw.hitsz.edu.cn%2FcasLogin"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
payload = {
    "username": username,
    "password": password,
    "lt": lt,
    "rememberMe": "on",
    "execution": execution,
    "_eventId": eventId,
}
response = session.post(login_url, headers=headers, data=payload)
cookies.update(response.cookies.get_dict())

# Cookies variable now contains all the cookies from both requests
# You can now use the session object to make requests with the cookies
response = session.post(f"{hostName}/cjgl/grcjcx/getgpa", cookies=cookies)

# Get your percentage
rk = response.json()["PJXFJ_PM"]
total = response.json()["ZRS"]
print("%{F#EC7875}RK %{F#C4C7C5}" + f"{rk} / {total}")
