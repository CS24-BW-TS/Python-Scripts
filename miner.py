import hashlib
import json
import time
from uuid import uuid4
import requests

def hash(proof):
    raw_hash = hashlib.sha256(proof)
    hex_hash = raw_hash.hexdigest()
    return hex_hash


def valid_proof(last_proof, new_proof, difficulty):
    guess = f"{last_proof}{new_proof}".encode()
    guess_hash = str(hash(guess))
    # print(guess_hash)
    return guess_hash[:difficulty] == ("0" * difficulty)


def generate_proof(last_proof):
    # does hash(last_proof, new_proof) have n (difficulty) leading 0s
    difficulty = last_proof['difficulty']
    lproof = last_proof['proof']
    proof = 0
    while valid_proof(lproof, proof, difficulty) is False:
        proof += 1
    return proof

if __name__ == '__main__':
    token = 'c1d970e90b8e3296481f21522265f9a564b57512'
    glp_url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/'
    mine_url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/'
    headers = {'Authorization': f'Token {token}'}
    while True:
        last_proof_req = requests.get(url=glp_url, json={}, headers=headers)
        last_proof = last_proof_req.json()
        print(last_proof)
        if 'difficulty' not in last_proof:
            time.sleep(last_proof['cooldown'])
            continue
        new_proof = generate_proof(last_proof)
        print(f'New proof: {new_proof}')
        mine = requests.post(url=mine_url, json={'proof': new_proof}, headers=headers)
        mine_result = mine.json()
        print(mine_result)
        # shouldn't ever need to wait the cooldown, but we'll do it to avoid penalties
        time.sleep(mine_result['cooldown'])
