import socket
import sys
import time
import random

# Constants
TIMEOUT = 1.0  # Timeout in seconds
MAX_RETRIES = 10  # Maximum number of retransmissions

def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python client_2_with_loss.py <server_domain_name> <file_name>")
        sys.exit(1)
    
    # Get server domain name and file name from command line arguments
    server_domain = sys.argv[1]
    file_name = sys.argv[2]
    
    # Perform DNS lookup to get server's IP address
    try:
        server_ip = socket.gethostbyname(server_domain)
        print(f"Server IP address: {server_ip}")
    except socket.gaierror:
        print(f"Error: Could not resolve hostname {server_domain}")
        sys.exit(1)
    
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set socket timeout
    client_socket.settimeout(TIMEOUT)
    
    # Set server address and port
    server_address = (server_ip, 6789)
    
    print("Client started with 50% simulated packet loss...")
    
    try:
        # Open the file for reading
        with open(file_name, 'r') as file:
            # Read each line from the file
            sequence_number = 0
            
            for line in file:
                # Remove newline characters
                line = line.strip()
                
                if line:  # Skip empty lines
                    retries = 0
                    message_delivered = False
                    
                    # Format message with sequence number: "SEQ:X:MESSAGE"
                    message_with_seq = f"SEQ:{sequence_number}:{line}"
                    
                    while not message_delivered and retries < MAX_RETRIES:
                        try:
                            # Simulate packet loss (50% probability) when sending
                            rand = random.randint(1, 10)
                            if rand > 5:
                                print(f"Sending message: '{line}' (SEQ={sequence_number})")
                                
                                # Send the message to the server
                                client_socket.sendto(message_with_seq.encode('utf-8'), server_address)
                            else:
                                print(f"Simulating packet loss - did not send message (SEQ={sequence_number})")
                                # We still need to wait to simulate the packet being lost
                                time.sleep(TIMEOUT)
                                retries += 1
                                continue
                            
                            # Wait for response (ACK)
                            data, server = client_socket.recvfrom(2048)
                            response = data.decode('utf-8')
                            
                            # Parse the ACK
                            # Format: "ACK:X:RESPONSE"
                            parts = response.split(':', 2)
                            if len(parts) >= 3 and parts[0] == "ACK" and parts[1] == str(sequence_number):
                                actual_response = parts[2]
                                print(f"Received from server: '{actual_response}' (ACK={parts[1]})")
                                message_delivered = True
                                sequence_number = (sequence_number + 1) % 100  # Wrap around at 100
                            else:
                                print(f"Received invalid ACK, retransmitting...")
                                retries += 1
                            
                        except socket.timeout:
                            retries += 1
                            print(f"Timeout occurred. Retransmitting... (Attempt {retries}/{MAX_RETRIES})")
                    
                    if not message_delivered:
                        print(f"Failed to deliver message after {MAX_RETRIES} attempts. Moving to next message.")
                    
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        client_socket.close()
        print("Client socket closed")

if __name__ == "__main__":
    main()