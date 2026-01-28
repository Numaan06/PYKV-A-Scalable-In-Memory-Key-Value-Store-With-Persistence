import requests

BASE = "http://127.0.0.1:8000"

while True:
    cmd = input("PyKV> ")
    parts = cmd.split()

    if parts[0] == "SET":
        requests.post(BASE + "/set", json={"key": parts[1], "value": parts[2]})

    elif parts[0] == "GET":
        print(requests.get(BASE + "/get/" + parts[1]).json())

    elif parts[0] == "DEL":
        requests.delete(BASE + "/delete/" + parts[1])