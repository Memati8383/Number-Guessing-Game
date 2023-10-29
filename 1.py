import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen()

print("Waiting for connections...")

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

number = random.randint(1, 9)
chances = 0

client_socket.send("Number guessing game\n".encode())
client_socket.send("Guess a number (between 1 and 9):\n".encode())

while True:
    guess = int(client_socket.recv(1024).decode())

    if guess == number:
        result = f'CONGRATULATIONS! YOU HAVE GUESSED THE NUMBER {number} IN {chances} ATTEMPTS!'
        client_socket.send(result.encode())
        break

    elif guess < number:
        result = f"Your guess was too low: Guess a number higher than {guess}"
        client_socket.send(result.encode())

    else:
        result = f"Your guess was too high: Guess a number lower than {guess}"
        client_socket.send(result.encode())

    chances += 1

client_socket.close()
server_socket.close()
