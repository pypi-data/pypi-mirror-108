import socket
import random
from .tools import *
import traceback
import sqlite3
import Levenshtein
import json


class Client:
    def __init__(self, db_path, user_hash, user_data):
        self.db_path = db_path
        self.user_hash = user_hash
        self.user_data = user_data

    def update_db(self, elements, isfile=False):
        con = sqlite3.connect(self.db_path)  # Bad code
        cur = con.cursor()
        for i in range(len(elements)):
            print(elements[i])
            element = elements[i]
            element = element.split('-')
            element_hash = element[0]
            element_address = element[1].replace('\n', '')
            print("Hash: " + element_hash)
            print("Address: " + element_address)
            similarity = Levenshtein.ratio(element_hash, self.user_hash)
            elements[i] = (element_hash, element_address, similarity, int(isfile))
        print("To insert: " + str(elements))
        cur.executemany("INSERT OR IGNORE INTO dht VALUES (?,?,?,?)", elements)
        con.commit()
        cur.close()
        con.close()

    def get_dht(self):
        con = sqlite3.connect(self.db_path)  # Bad code
        cur = con.cursor()
        cur.execute("SELECT * FROM dht ORDER BY similarity DESC")
        result = cur.fetchall()
        cur.close()
        con.close()
        return result

    def get_similarity(self, data_hash, include_files=True):
        similarities = {}
        dht = self.get_dht()

        for element in dht:
            if not include_files and element[3] == 1:
                continue

            node_hash = element[0]
            node_address = element[1]
            similarity = Levenshtein.ratio(str(data_hash), node_hash)
            print("Similarity " + str(data_hash) + " and " + node_hash + '-' + node_address + " is " + str(similarity))
            similarities[node_hash + '-' + node_address] = similarity

        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)  # Sort in descending order
        sorted_similarities = tuple(dict(sorted_similarities).keys())
        return sorted_similarities

    def put(self, filename, content):
        self.get(filename)

        content_sliced = []

        for i in range(0, len(content), 4096):
            content_sliced.append(content[i:i + 4096])
        print("Num of slices: " + str(len(content_sliced)))

        filename_hash = create_hash(filename)
        print("File upload...")
        file_similarities = list(self.get_similarity(filename_hash, include_files=False))
        file_similarities.remove(self.user_data)
        file_similarities = tuple(file_similarities)

        command = str.encode('put&' + self.user_data + '&' + filename)

        for node in file_similarities[:5]:  # The number of nodes that will receive a file
            print(node)
            node_data = node.split('-')[1]
            node_data = node_data.rsplit(':', 1)  # Get an address from the node data and split it to get an ip and port
            ip = node_data[0]
            port = int(node_data[1])

            try:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
                    s.connect((ip, port, 0, 0))
                    s.sendall(command)
                    data = s.recv(1024)

                    for i in content_sliced:
                        s.sendall(i)
            except Exception as ex:
                print(str(ex))
                pass

    def bootstrap(self):
        shuffled_dht = self.get_dht()
        shuffled_dht.pop(0)
        random.shuffle(shuffled_dht)
        print(shuffled_dht)
        # We need to shuffle the dht to distribute network load between nodes
        for node in shuffled_dht:
            if node[3] == 1:
                continue

            address = node[1].rsplit(':', 1)
            ip = address[0]
            port = int(address[1])
            try:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
                    s.connect((ip, port, 0, 0))
                    s.sendall(str.encode('bootstrap&' + self.user_data))
                    recvnodes = s.recv(4096).decode(encoding='utf-8')
                    recvnodes = json.loads(recvnodes)
                    self.update_db(recvnodes)
                break
            except Exception as ex:
                print(str(ex))
                continue

    def get(self, file_name):  # Get new nodes that are similar to file hash
        file_hash = create_hash(file_name)
        similarities = list(self.get_similarity(file_hash, include_files=False))
        print("Sorted similarities: " + str(similarities))
        similarities.remove(self.user_data)
        similarities = similarities[:5]  # Get first five nodes that have the best similarity with filename_hash
        received_nodes = []
        for node in similarities:
            print("Get node: " + str(node))
            node_address = node.split('-')[1]
            node_address = node_address.rsplit(':', 1)
            node_ip = node_address[0]
            node_port = node_address[1]
            print("Ip " + node_ip)
            print("Port " + node_port)

            try:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
                    s.connect((node_ip, int(node_port), 0, 0))
                    s.sendall(str.encode('get&' + self.user_data + '&' + file_name))
                    recvdata = bytes()
                    while True:
                        recvpart = s.recv(4096)
                        if not recvpart:
                            break
                        recvdata += recvpart
                    s.close()
                    print(str(recvdata))

                    try:
                        recvnodes = json.loads(recvdata.decode('utf-8'))

                        print("Similarities: " + str(similarities))
                        if self.user_data in str(recvnodes):
                            recvnodes.remove(self.user_data)
                        for node in recvnodes.copy():
                            if node in str(similarities):
                                recvnodes.remove(node)

                        if len(recvnodes) != 0:  # If received list contains at least one element
                            similarities.extend(recvnodes)
                            received_nodes.extend(recvnodes)
                        received_nodes = list(set(received_nodes))
                        print("Now similarities is: " + str(similarities))
                    except ValueError:
                        print(file_name + " found and saved! (recv_" + file_name + ")")
                        with open("recv_" + file_name, 'wb') as f:
                            f.write(recvdata)
                        break

            except Exception:
                traceback.print_exc()
                pass
        # print("Received nodes is: " + str(received_nodes))
        # print("Now similarities is: " + str(similarities))
        self.update_db(received_nodes)  # We need to update the database with received nodes
