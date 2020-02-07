import requests
import random
import sys
import json
import time


def stack_peek(stack):
    if len(stack) < 1:
        return None
    else:
        return stack[-1]


def room_peek(current, dir):
    inte = eval(current)
    coords = ""
    if dir == "n":
        coords = str((inte[0], inte[1] + 1))
    elif dir == "e":
        coords = str((inte[0], inte[1] + 1))
    elif dir == "s":
        coords = str((inte[0], inte[1] + 1))
    elif dir == "w":
        coords = str((inte[0], inte[1] + 1))
    else:
        coords = None
    return str(coords)


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    # node =  "http://127.0.0.1:8000/api/adv/move" d03b59eb374a236f6be051a6fdc0669e03278fa2
    node = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    myToken = "c1d970e90b8e3296481f21522265f9a564b57512"

    graph = {}
    idgraph = {}
    reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}
    visited = set()
    starting_room = {"room_id": 139, "title": "A misty room",
                     "description": "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.",
                     "coordinates": "(56,60)", "elevation": 0, "terrain": "NORMAL", "players": [], "items": [],
                     "exits": ["e", "w"], "cooldown": 15.0, "errors": [], "messages": ["You have walked east."]}
    stack = []  # current path
    initial = starting_room
    stack.append(initial)
    while len(visited) < 200:
        print(stack)
        current = stack_peek(stack)
        if 'coordinates' not in current:
            time.sleep(current['cooldown'])
        current_coords = current['coordinates']
        visited.add(current_coords)
        graph[current_coords] = current
        if current['room_id'] not in idgraph:
            idgraph[current['room_id']] = {"n": None, "s": None, "e": None, "w": None}
        discovered = []
        for neighbor_dir in current['exits']:
            next_coords = room_peek(current_coords, neighbor_dir)
            if next_coords not in visited:
                idgraph[current['room_id']][neighbor_dir] = -1
                discovered.append((current_coords, next_coords, neighbor_dir))

        if len(discovered) > 0:  # If there are still rooms to discover, add them to the stack
            next_move = random.choice(discovered)
            post_data = {"direction": next_move[2]}
            if next_move[1] in graph:
                known_id = graph[next_move[1]]['room_id']
                post_data = {"direction": next_move[2], "next_room_id": known_id}
            headers = {'Authorization': f'Token {myToken}'}
            r = requests.post(url=node, json=post_data, headers=headers)
            data = r.json()
            if data and data['room_id']:
                idgraph[current['room_id']][next_move[2]] = data['room_id']
                idgraph[data['room_id']] = {}
                idgraph[data['room_id']][reverse[next_move[2]]] = current['room_id']
            file = open("testfile.txt", "a")
            file.write(json.dumps(data) + ",")
            file.close()
            time.sleep(data['cooldown'])
            print("visited", visited)
            print("IDgraph", idgraph)
            print("GRAPH", graph)
            stack.append(data)
        else:  # No more discovered rooms. Pop to backtrack to last current.
            stack.pop()
            current = stack_peek(stack)