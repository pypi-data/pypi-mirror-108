"""
MIT License

Copyright (c) 2021 Sijey

Read more : https://raw.githubusercontent.com/sijey-praveen/YouTube-Music-API/Sijey/LICENSE

"""

import requests
from bs4 import BeautifulSoup as Extract_Data
from random import randint as get_results
import webbrowser as Browser
import socket
import platform

def NoInternetError():
    if "127.0.0.1" in socket.gethostbyname(socket.gethostname()):
        print("You're Offline, Please Connect To Internet!")

def AutoUpdate():
    if 200 == requests.head("https://pypi.org/project/googlesearch.py/1.2/").status_code:
        if "Windows" == platform.system():
            os.system("pip install googlesearch.py==1.2")
        elif "Darwin" == platform.system():
            os.system("pip install googlesearch.py==1.2")
        elif "Linux" == platform.system():
            os.system("pip install googlesearch.py==1.2")
            
def search(query, show=False):
    Data = []
    for link in Extract_Data(requests.get(f"https://www.google.com/search?q={query}&tbm=isch&biw=1536&bih=739").text, 'html.parser').find_all('a'):
        Data.append(f"{link.get('href')}")
    Data = Data[get_results(17,50)]
    if "/url?q=https://" in Data:
        Data = f"https://www.google.com{Data}"
    elif "/search?q=" in Data:
        Data = f"https://www.google.com/{Data}"
    if show == True:
        Browser.open(Data)
    else:
        Data = {"query": f"{query}", "result": f"{Data}"}
        return Data
            
if __name__ == "__main__":
    NoInternetError()