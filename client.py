"""
Author: Talya Gross
Game: Pop the Mole
CLIENT
"""
# import
from game import start_game
from game import win
from game import lose
import socket


class Client:
    """
        build function of the Client class.
    """
    def __init__(self, port, ip):
        print("connecting...")
        self.sock = socket.socket()
        self.sock.connect((ip, port))
        print("connected!")

    def start_client(self):
        """
            the function receives input from the user and according to that it
            starts the game or exits and closes the socket. here is all the communication
             with the server after connecting.
        """
        try:
            while True:
                start = input("enter yes to start the game, exit to quit ")
                if start == "yes":
                    self.sock.send("start".encode())
                    print("the server is looking for a teammate...")
                    answer = self.sock.recv(1024).decode()

                    if answer == "game":
                        final_time = start_game()
                        print(final_time)
                        # sending the client's time
                        # msg = "\r\n" + str(final_time) #############
                        self.sock.send(str(final_time).encode())
                    print(answer)
                    answer = self.sock.recv(1024).decode()
                    if answer == "win":
                        win()
                    if answer == "lose":
                        lose()
                if start == "exit":
                    self.sock.send("exit".encode())
                    print("exiting...")
                    break
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            self.sock.close()


def main():
    """
         the main function of the client
    """
    try:
        my_client = Client(8000, "127.0.0.1")
        my_client.start_client()
    except socket.error as err:
        print('received socket exception - ' + str(err))
        print("couldn't make a connection... try again")
    finally:
        pass  # there is no socket to close when the client wasn't able to connect.


if __name__ == "__main__":
    # Call the main handler function
    main()
