import os

class Persistence:
    def __init__(self, filename):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def log_set(self, key, value):
        with open(self.filename, "a") as f:
            f.write(f"SET {key} {value}\n")

    def log_delete(self, key):
        with open(self.filename, "a") as f:
            f.write(f"DEL {key}\n")

    def recover(self):
        data = {}

        if not os.path.exists(self.filename):
            return data

        with open(self.filename, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)
                if parts[0] == "SET":
                    data[parts[1]] = parts[2]
                elif parts[0] == "DEL":
                    data.pop(parts[1], None)

        return data
