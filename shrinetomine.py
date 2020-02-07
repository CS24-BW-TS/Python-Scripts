import requests
import random
import json
import time

token = "c1d970e90b8e3296481f21522265f9a564b57512"

def traversal(myToken):
    init = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    node = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    myToken = "c1d970e90b8e3296481f21522265f9a564b57512"
    visited = None
    with open('./mapdata.txt') as f:
        visited = json.load(f)

    print(visited)


traversal(token)
