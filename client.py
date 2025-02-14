# Description: This file contains the client-side code for the chat room application.
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def exit_request(client_socket, username, window):
    client_socket.sendall(f"\n[+] The user {username} has left room chat\n\n".encode("utf-8"))  # Send exit message to server
    client_socket.close()  # Close the socket
    window.quit()  # Quit the Tkinter main loop
    window.destroy()  # Destroy the Tkinter window


def send_message(event, client_socket, texte_widget, entry_widget):
    message = entry_widget.get()  # Get the message from the entry widget
    if message:  # Check if the message is not empty
        client_socket.sendall(message.encode("utf-8"))  # Send the message to the server
        texte_widget.configure(state="normal")  # Enable text widget for editing
        texte_widget.insert(END, f"\nYou: {message}\n\n")  # Insert the message into the text widget
        texte_widget.configure(state="disable")  # Disable text widget for editing
        entry_widget.delete(0, END)  # Clear the entry widget

def receive_messages(client_socket, texte_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")  # Receive message from server
            if message:  # Check if the message is not empty
                texte_widget.configure(state="normal")  # Enable text widget for editing
                texte_widget.insert(END, f"{message}\n")  # Insert the message into the text widget
                texte_widget.configure(state="disable")  # Disable text widget for editing
        except Exception as e:
            print(f"Error receiving message: {e}")  # Print error message
            break  # Exit the loop on error

def client_program():
    host = 'localhost'  # The server's hostname or IP address
    port = 12345        # The port used by the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    client_socket.connect((host, port))  # Connect to the server

    username = input("Enter your username: ")  # Prompt for username
    client_socket.send(username.encode("utf-8"))  # Send username to server

    window = Tk()  # Create a Tkinter window
    window.title("Chat Room Encrypted")  # Set window title
    texte_widget = ScrolledText(window, state="disable")  # Create a ScrolledText widget for chat display
    texte_widget.pack(padx=5, pady=5)  # Add padding around the widget

    entry_widget = Entry(window, width=50)  # Create an Entry widget for user input
    entry_widget.bind("<Return>", lambda event: send_message(event, client_socket, texte_widget, entry_widget))  # Bind the Enter key to send_message function
    entry_widget.pack(padx=5, pady=5, fill=BOTH)  # Add padding around the widget

    frame_widget = Frame(window)  # Create a Frame widget
    frame_widget.pack(padx=5, pady=5, fill=BOTH)  # Add padding around the widget

    buttom_widget = Button(frame_widget, text="Send", command=lambda: send_message(None, client_socket, texte_widget, entry_widget))  # Create a Button widget to send messages
    buttom_widget.pack(side=RIGHT)  # Pack the widget to the right

    user_widget = Label(frame_widget, text=f"Logged in as: {username}")  # Create a Label widget to display username
    user_widget.pack(side=LEFT)  # Pack the widget to the left  

    exit_widget = Button(frame_widget, text="Exit", command=lambda: exit_request(client_socket, username, window))  # Create a Button widget to exit the application
    exit_widget.pack(side=RIGHT)  # Pack the widget to the right

    thread = threading.Thread(target=receive_messages, args=(client_socket, texte_widget))  # Create a thread to receive messages
    thread.daemon = True  # Set the thread as a daemon thread
    thread.start()  # Start the thread

    thread = threading.Thread(target=receive_messages, args=(client_socket, texte_widget))  # Create a thread to receive messages
    thread.daemon = True  # Set the thread as a daemon thread
    thread.start()  # Start the thread

    window.mainloop()  # Start the Tkinter main loop
    client_socket.close()  # Close the socket when done



if __name__ == "__main__":
    client_program()