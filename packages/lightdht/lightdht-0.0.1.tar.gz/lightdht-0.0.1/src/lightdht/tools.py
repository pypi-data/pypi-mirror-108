from hashlib import sha1
import sqlite3
from uuid import uuid4
import os


def create_id():
    random_string = str(uuid4())
    print("Random string for hash ", random_string)
    user_hash = create_hash(random_string)
    print("Your id: " + user_hash)
    return user_hash


def create_hash(text):
    hash_obj = sha1(str.encode(text))
    hashed = hash_obj.hexdigest()
    return hashed


def init_db(db_path, user_hash, user_address):
    print("Creating database...")
    if not os.path.isdir("data"):
        os.mkdir("data")

    user_data = [user_hash, user_address, 1.0, 0]
    print("Your data: " + str(user_data))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE dht
        (hash TEXT, address TEXT, similarity REAL, isfile INT, UNIQUE(hash, address))''')
    cur.execute("INSERT INTO dht VALUES (?,?,?,?)", user_data)
    con.commit()
    cur.close()
    con.close()


def load_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT hash, address FROM dht ORDER BY similarity DESC LIMIT 1")
    user_data = list(cur.fetchone())
    cur.close()
    con.close()

    user_hash = user_data[0]
    address = user_data[1]
    address = address.rsplit(':', 1)
    ip = address[0]
    port = address[1]

    return user_hash, ip, port
