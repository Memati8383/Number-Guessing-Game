import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

while True:
    message = client_socket.recv(1024).decode()
    if not message:
        break
    print(message)
    
    guess = int(input())
    client_socket.send(str(guess).encode())
    
    result = client_socket.recv(1024).decode()
    print(result)
    if "CONGRATULATIONS" in result:
        break

client_socket.close()
