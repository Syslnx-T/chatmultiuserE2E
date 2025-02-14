import socket # Import socket module
import threading


host = 'localhost'  # Localhost
port = 12345     # Port to listen on (non-privileged ports are > 1023)
        

def handle_client(conn, usernames, clients):
    usernames[conn] = conn.recv(1024).decode("utf-8") # Receive username from client
    print(f"\n{usernames[conn]} has joined the chat room") #send message to server that a new user has joined.

    for client in clients:
        if client != conn:
            client.sendall(f"[+]{usernames[conn]} has joined the chat room".encode("utf-8")) #send message to all clients that a new user has joined.

     # Ifinite loop to receive messages from client
    while True:
        try:
            message = conn.recv(1024) # Receive message from client
            if message:
                print(f"\n{usernames[conn]}: {message.decode('utf-8')}\n") # Print message to server
                message_to_send = f"{usernames[conn]}: {message.decode('utf-8')}" # Create message to send to all clients

                for client in clients:
                    if client != conn:
                        client.sendall(message_to_send.encode("utf-8")) # Send message to all clients
        except Exception as e:
            print(f"\nError receiving message: {e}")
            clients.remove(conn)
            for client in clients:
                client.sendall(f"{usernames[conn]} has left the chat room".encode("utf-8")) # Send message to all clients that a user has left
                conn.close()
                clients.remove(conn)
                



def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #time wait socket reuse conector
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"\n[+] Server started waiting for connections...")


    clients = []
    usernames = {}

    while True:
        conn, address = server_socket.accept()
        clients.append(conn)

        print(f"\n[!] Connection has been established | {address}")
        
        conn.send(f"Welcome to the chat room!\n".encode("utf-8"))
        thread = threading.Thread(target=handle_client, args=(conn, usernames, clients))
        thread.daemon = True 
        thread.start()


    server_socket.close() # Close the socket when done



#start the server
if __name__ == '__main__':
    server_program()
