

# In-memory storage
store = {}

def set_key(key: str, value: str):
    store[key] = value

def get_key(key: str):
    return store.get(key)

def delete_key(key: str):
    return store.pop(key, None)
