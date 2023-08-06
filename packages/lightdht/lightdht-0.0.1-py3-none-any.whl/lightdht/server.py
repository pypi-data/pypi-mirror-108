import socket
import threading
from .tools import *
from .client import Client
import json


class Server(Client):
    def __init__(self, db_path, user_hash, ip, port):
        self.ip = ip
        self.port = port
        self.user_data = user_hash + '-' + self.ip + ':' + str(self.port)
        print("Your data: " + self.user_data)
        Client.__init__(self, db_path, user_hash, self.user_data)

    def __connection(self, conn, addr):
        data = conn.recv(4096).decode(encoding='utf-8')
        print("Received command is " + data)
        data = data.split('&')  # Example: put&<random_hash>-127.0.0.1:4444&file.txt
        cmd = data[0]
        address = data[1]  # Get sender's "hash-127.0.0.1:4444" from received data
        self.update_db([address])

        if cmd == 'bootstrap':
            print("Bootstrap request!")
            dht = self.get_dht()[:20]

            for element in dht.copy():

                if element[3] == 1:  # We don't need to include files
                    dht.remove(element)
                    continue

                node_hash = element[0]
                node_address = element[1]
                dht[dht.index(element)] = node_hash + '-' + node_address

            conn.sendall(json.dumps(dht).encode())
        elif cmd == 'get':
            file_name = data[2]
            file_hash = create_hash(file_name)
            closer_data = self.__get_handler(file_hash, address)
            print("Data that closer to " + file_hash + " " + str(closer_data))

            if file_hash in closer_data[0] and ':' not in closer_data[0]:
                content_sliced = []
                with open("data/" + file_hash, 'rb') as f:
                    content = f.read()
                for i in range(0, len(content), 1024):
                    content_sliced.append(content[i:i + 1024])
                for i in content_sliced:
                    conn.sendall(i)
            else:
                conn.sendall(json.dumps(closer_data).encode())

        elif cmd == 'put':
            file_name = data[2]
            file_hash = create_hash(file_name)
            conn.send("ok".encode())
            recvfile = bytes()

            while True:
                recvpart = conn.recv(4096)
                if not recvpart:
                    break
                recvfile += recvpart

            with open("data/" + file_hash, 'wb') as f:
                f.write(recvfile)
            print("File " + file_hash + " saved successfully!")

            self.update_db([file_hash + '-' + 'data/' + file_hash], isfile=True)
        else:
            conn.sendall("[wrong_command]".encode())

        conn.close()

    def __get_handler(self, file_hash, address):
        sorted_similarities = list(self.get_similarity(file_hash))
        sorted_similarities.remove(address)
        sorted_similarities = sorted_similarities[:5]

        for similarity in sorted_similarities.copy():
            if file_hash not in similarity and 'data/' in similarity:
                # If it's a file that doesn't contain the requested hash, we delete it
                sorted_similarities.remove(similarity)

        if file_hash in sorted_similarities[0] and 'data/' in sorted_similarities[0]:
            sorted_similarities = [sorted_similarities[0]]

        print("Closer data to send: " + str(sorted_similarities))
        return sorted_similarities

    def __listen_handler(self, ip, port):
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.listen()

        while True:
            conn, addr = sock.accept()
            print('Connected by', addr)
            conn_thread = threading.Thread(target=self.__connection, args=(conn, addr,))
            conn_thread.start()

    def listen(self):
        listen_thread = threading.Thread(target=self.__listen_handler, args=(self.ip, int(self.port),))
        listen_thread.start()


if __name__ == "__main__":
    print('Error')
