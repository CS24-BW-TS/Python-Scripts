import requests
import random
import json
import time


def get_neighbors(room, visited):
    neighbors = []
    saved = visited[room['room_id']]
    if room['exits']:
        for x in room['exits']:
            if x not in saved:
                neighbors.append(x)
    return neighbors


if __name__ == '__main__':
    init = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    node = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    myToken = "c1d970e90b8e3296481f21522265f9a564b57512"
    total = 500
    new_name = 'Chris York'
    graph = []
    visited = {}
    # with open('testfile.txt') as f:
    #     visited = json.load(f)
    rdirs = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    stack = []
    headers = {'Authorization': f'Token {myToken}'}
    r = requests.get(url=init, headers=headers)
    data = r.json()
    print(data)
    current = data
    stack.append(current)
    neighbors = None
    direction = None

    while len(visited) < total:
        if current['room_id'] not in visited: visited[current['room_id']] = {}
        neighbors = get_neighbors(current, visited)
        if len(neighbors) < 1:
            if len(stack):
                last = stack.pop()
                prev_dir = last[1]
                post_data = {'direction': rdirs[prev_dir]}
                r = requests.post(url=node, json=post_data, headers=headers)
                data = r.json()
                print(f'Backtrack: {data}')
                current = data
                time.sleep(current['cooldown'])
                continue
            else:
                neighbors = current['exits']
        direction = random.choice(neighbors)
        post_data = {'direction': direction}
        print(f'Direction: {direction}')
        r = requests.post(url=node, json=post_data, headers=headers)
        try:
            data = r.json()
        except:
            print('Failed to decode')
        if 'room_id' not in data:
            time.sleep(15)
            continue
        visited[current['room_id']][direction] = data['room_id']
        graph.append(data)
        current = data
        file = open("testfile.txt", "a")
        file.write(json.dumps(data) + ",")
        file.close()
        print(f'Visited: {visited}')
        print(f'Current Room: {current}')
        stack.append((current, direction))
        time.sleep(data['cooldown'])
        if current['room_id'] == 449:
            print('You can now mine!')
            break
