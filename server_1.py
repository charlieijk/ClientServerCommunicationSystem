import socket

def main():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the host and port
    server_address = ('', 6789)  # Empty string means listen on all available interfaces
    server_socket.bind(server_address)
    
    print(f"Server is listening on port 6789...")
    
    # Enter an infinite loop to listen for client messages
    while True:
        try:
            # Receive data and client address
            data, client_address = server_socket.recvfrom(2048)
            
            # Decode and print the received message
            message = data.decode('utf-8')
            print(f"Received message from {client_address}: {message}")
            
            # Convert message to uppercase
            uppercase_message = message.upper()
            
            # Send the uppercase message back to the client
            server_socket.sendto(uppercase_message.encode('utf-8'), client_address)
            
            print(f"Sent uppercase message to {client_address}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()