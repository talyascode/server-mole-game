"""
Author: Talya Gross
Game: Pop the Mole
SERVER
"""
# import
import socket
import threading
import time


class Server:
    """
        build function of the Client class.
    """
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen()
        print("server is up")

        """
        ALL CLIENTS:
        ('127.0.0.1', 49944): socket
        ('127.0.0.1', 49942): socket

        CAN PLAY:
        ('127.0.0.1', 49944): True
        ('127.0.0.1', 49944): True

        FINAL TIMES:
        ('127.0.0.1', 49944): 9876
        ('127.0.0.1', 49942): 5567
        * in this case 49944 is the winner
        """
        self.all_clients = {}
        self.can_play = {}
        self.final_times = {}
        t = threading.Thread(target=self.check_2_ready)
        t.start()
        t_r = threading.Thread(target=self.send_final_results)
        t_r.start()
        print("check 2 ready is working")

    def wait_for_clients(self):
        """
            the function accepts new clients and calls the handle client in threading
        """
        try:
            while True:
                client_socket, client_address = self.sock.accept()
                self.all_clients[client_address] = client_socket
                self.can_play[client_address] = False
                print("all clients:")
                print(self.all_clients)
                # self.handle_client(client_address)
                t = threading.Thread(target=self.handle_client, args=[client_address])
                t.start()
                print("new thread for client:", client_address)
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            if self.all_clients:
                client_socket = list(self.all_clients.values())[0]
                client_socket.close()
                client_socket = list(self.all_clients.values())[1]
                client_socket.close()

    def handle_client(self, client_address):
        """
            the function receives data from the current client and checks what the data is and acts according
            to the protocol of the program.
        :param client_address: the address of the current client that is being handled
        """
        client_socket = self.all_clients[client_address]
        try:
            while True:
                print("listening to client:", client_address)
                data = client_socket.recv(1024).decode()
                if data == "start":
                    self.can_play[client_address] = True
                elif data == "exit":
                    #  closing current socket
                    client_socket.close()
                    # updating dictionaries
                    self.can_play[client_address] = None
                    self.can_play[client_address] = False
                else:
                    final_time = int(data)
                    self.final_times[client_address] = final_time
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            client_socket.close()

    def send_final_results(self):
        """
        the function sends a msg to the winner and the loser according to who sent the final times first.
        also resets the dictionaries can play and final times so they will be ready for another game.
        """
        try:
            while True:
                addresses = []
                times = []
                print(self.can_play)
                for addr in self.final_times:
                    addresses.append(addr)
                    times.append(self.final_times[addr])
                if len(addresses) == 2:
                    time1 = times[0]
                    time2 = times[1]
                    # send to the first address in the list(the winner) because the winner(the shortest time) will
                    # go in the dictionary first.
                    print(self.all_clients[addresses[0]])
                    print(self.all_clients[addresses[1]])
                    self.all_clients[addresses[0]].send("win".encode())
                    self.all_clients[addresses[1]].send("lose".encode())
                    # reset dictionary
                    self.can_play = {}
                    self.final_times = {}
                time.sleep(1)
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            if self.all_clients:
                client_socket = list(self.all_clients.values())[0]
                client_socket.close()
                client_socket = list(self.all_clients.values())[1]
                client_socket.close()

    def check_2_ready(self):
        """
            the function checks if there are 2 players that are ready to play according to the can play dictionary
        """
        try:
            while True:
                ready_socket = []
                ready_addr = []
                print(self.can_play)
                """
                addr1: value
                addr2: value
                addr3: value
                for addr in dict:
                    dict[addr] - false/true
                """
                for addr in self.can_play:
                    if self.can_play[addr]:
                        ready_socket.append(self.all_clients[addr])
                        ready_addr.append(addr)
                if len(ready_socket) == 2:
                    ready_socket[0].send("game".encode())
                    ready_socket[1].send("game".encode())
                    self.can_play[ready_addr[0]] = False
                    self.can_play[ready_addr[1]] = False
                time.sleep(1)
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            if self.all_clients:
                client_socket = list(self.all_clients.values())[0]
                client_socket.close()
                client_socket = list(self.all_clients.values())[1]
                client_socket.close()


def main():
    """
        the main function of the server
    """
    my_server = Server(8000)
    my_server.wait_for_clients()


if __name__ == "__main__":
    # Call the main handler function
    main()
