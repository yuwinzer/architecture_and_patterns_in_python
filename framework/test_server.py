import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8001)
server_socket.bind(server_address)
server_socket.listen(1)

while True:
    print(f'====== Server started ======\nhttp://{server_address[0]}:{server_address[1]}')
    client_connection, client_address = server_socket.accept()
    print(f'I got connection: {client_address}')
    data = client_connection.recv(1024).decode()
    print(data)
    client_connection.close()
