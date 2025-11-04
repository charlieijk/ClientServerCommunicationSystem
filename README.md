# Client-Server Communication System

A Python-based UDP client-server communication system demonstrating basic networking concepts and reliable data transfer protocols.

## Overview

This project contains two implementations of UDP client-server communication:

1. **Basic UDP Communication** (client_1.py / server_1.py)
2. **Reliable UDP with Packet Loss Simulation** (client_2.py / server_2.py)

## Features

### Version 1: Basic UDP Communication
- Simple UDP socket communication
- DNS hostname resolution
- File-based message sending
- Server converts messages to uppercase
- Basic error handling

### Version 2: Reliable UDP with Packet Loss
- Sequence number-based message tracking
- Acknowledgment (ACK) protocol
- 50% simulated packet loss on both client and server
- Automatic retransmission on timeout
- Configurable retry limits (default: 10 attempts)
- Demonstrates reliable data transfer over unreliable network

## Requirements

- Python 3.x
- No external dependencies (uses built-in `socket` library)

## Installation

Clone the repository:
```bash
git clone https://github.com/charlieijk/ClientServerCommunicationSystem.git
cd ClientServerCommunicationSystem
```

## Usage

### Basic UDP Communication (Version 1)

**Start the server:**
```bash
python server_1.py
```

**Run the client:**
```bash
python client_1.py <server_domain_name> <file_name>
```

Example:
```bash
python client_1.py localhost testfile.txt
```

### Reliable UDP with Packet Loss (Version 2)

**Start the server with packet loss simulation:**
```bash
python server_2.py
```

**Run the client with packet loss simulation:**
```bash
python client_2.py <server_domain_name> <file_name>
```

Example:
```bash
python client_2.py localhost testfile.txt
```

## How It Works

### Basic Version
1. Client reads messages from a text file line by line
2. Each line is sent to the server via UDP
3. Server receives the message, converts it to uppercase
4. Server sends the uppercase message back to the client
5. Client displays the response

### Reliable Version
1. Client assigns sequence numbers to each message (format: `SEQ:X:MESSAGE`)
2. Client simulates 50% packet loss when sending
3. Server simulates 50% packet loss when responding
4. Server acknowledges received messages (format: `ACK:X:RESPONSE`)
5. Client retransmits if no ACK is received within timeout (1 second)
6. Maximum 10 retransmission attempts per message
7. Sequence numbers wrap around at 100

## Protocol Specification

### Message Format (Version 2)
- **Client to Server:** `SEQ:<sequence_number>:<message>`
- **Server to Client:** `ACK:<sequence_number>:<uppercase_message>`

### Parameters
- **Port:** 6789 (UDP)
- **Buffer Size:** 2048 bytes
- **Timeout:** 1.0 seconds
- **Max Retries:** 10 attempts
- **Packet Loss Rate:** 50% (simulated)

## File Structure

```
ClientServerCommunicationSystem/
├── client_1.py          # Basic UDP client
├── server_1.py          # Basic UDP server
├── client_2.py          # Reliable UDP client with loss simulation
├── server_2.py          # Reliable UDP server with loss simulation
├── testfile.txt         # Sample input file
└── README.md            # This file
```

## Testing

Create a test file with sample messages:
```bash
echo -e "Hello World\nThis is a test\nUDP communication" > testfile.txt
```

Run the server in one terminal and the client in another to observe the communication.

## Learning Objectives

This project demonstrates:
- UDP socket programming in Python
- DNS resolution using `gethostbyname()`
- Client-server architecture
- Reliable data transfer protocols
- Sequence numbers and acknowledgments
- Timeout and retransmission mechanisms
- Packet loss simulation and handling

## Limitations

- Uses UDP (connectionless, unreliable by design)
- No congestion control
- Simple stop-and-wait protocol (not pipelined)
- Fixed timeout values
- No flow control
- Messages limited to 2048 bytes

## Future Enhancements

- Implement sliding window protocol
- Add checksums for data integrity
- Dynamic timeout adjustment
- TCP implementation for comparison
- Support for binary file transfer
- Connection establishment/teardown

## License

This project is for educational purposes.

## Author

Charlie
