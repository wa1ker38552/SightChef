import threading
import json


class Database:
    def __init__(self, path: str):
        self.path: str = path
        self.lock = threading.Lock()

    # returns database as a dictionary
    def load(self) -> dict:
        with open(self.path, "r") as file:
            try:
                self.lock.acquire()
                return json.loads(file.read())
            finally:
                self.lock.release()

    # saves dictionary to database
    def save(self, data: dict, indent: int = 2):
        with open(self.path, "w") as file:
            try:
                self.lock.acquire()
                file.write(json.dumps(data, indent=indent))
            finally:
                self.lock.release()

    # gets a key or a list of keys
    def get(self, keys: str | list[str]):
        data = self.load()
        if isinstance(keys, str):
            return data[keys]
        else:
            # calling the key of a key of a key...
            # calls each key in a list of keys
            # for example, if I pass in [a, b, c] it would call data[a][b][c]
            # I made the code shorter as an eval expression so it's cleaner (the non eval version is extremely messy)
            expression = f"""data{"".join([f"['{k}']" for k in keys])}"""
            return eval(expression)

    # sets a key or a list of keys
    def set(self, keys: str | list[str], value):
        data = self.load()
        if isinstance(keys, str):
            data[keys] = value
        else:
            # see line 24
            expression = f"""data{"".join([f"['{k}']" for k in keys])} = {f"'{value}'" if isinstance(value, str) else value}"""
            exec(expression)
        self.save(data)

    # appends to the value of a key or a list of keys
    def append(self, keys: str | list[str], value):
        val = self.get(keys)
        val.append(value)
        self.set(keys, val)

    # deletes the value of a key or a list of keys
    def delete(self, keys: str | list[str]):
        data = self.load()
        deleted_data = self.get(keys)
        if isinstance(keys, str):
            del data[keys]
        else:
            # see line 24
            expression = f"""del data{"".join([f"['{k}']" for k in keys])}"""
            exec(expression)
        self.save(data)
        return deleted_data
