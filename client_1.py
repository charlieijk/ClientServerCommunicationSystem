import socket
import sys

def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python client_1.py <server_domain_name> <file_name>")
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
    
    # Set server address and port
    server_address = (server_ip, 6789)
    
    try:
        # Open the file for reading
        with open(file_name, 'r') as file:
            # Read each line from the file
            for line in file:
                # Remove newline characters
                line = line.strip()
                
                if line:  # Skip empty lines
                    print(f"Sending message: {line}")
                    
                    # Send the message to the server
                    client_socket.sendto(line.encode('utf-8'), server_address)
                    
                    # Set a timeout for receiving response
                    client_socket.settimeout(5.0)
                    
                    try:
                        # Receive response from server
                        data, server = client_socket.recvfrom(2048)
                        
                        # Decode and print the response
                        response = data.decode('utf-8')
                        print(f"Received from server: {response}")
                        
                    except socket.timeout:
                        print("Error: Request timed out")
                    
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