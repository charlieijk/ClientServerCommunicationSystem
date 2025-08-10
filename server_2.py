import socket
import random

def main():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the host and port
    server_address = ('', 6789)  # Empty string means listen on all available interfaces
    server_socket.bind(server_address)
    
    print(f"Server is listening on port 6789...")
    print(f"Simulating 50% packet loss...")
    
    # Enter an infinite loop to listen for client messages
    while True:
        try:
            # Receive data and client address
            data, client_address = server_socket.recvfrom(2048)
            
            # Decode the received message
            message = data.decode('utf-8')
            
            # Parse the sequence number from the message
            # Format: "SEQ:X:MESSAGE"
            parts = message.split(':', 2)
            if len(parts) < 3 or parts[0] != "SEQ":
                print(f"Invalid message format received from {client_address}")
                continue
                
            seq_num = parts[1]
            actual_message = parts[2]
            
            print(f"Received message from {client_address}: {actual_message} (SEQ={seq_num})")
            
            # Simulate packet loss (50% probability)
            rand = random.randint(1, 10)
            if rand > 5:
                # Convert message to uppercase
                uppercase_message = actual_message.upper()
                
                # Format response with acknowledgment: "ACK:X:RESPONSE"
                response = f"ACK:{seq_num}:{uppercase_message}"
                
                # Send the response back to the client
                server_socket.sendto(response.encode('utf-8'), client_address)
                print(f"Sent response to {client_address} (ACK={seq_num})")
            else:
                print(f"Simulating packet loss - did not send response (SEQ={seq_num})")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()