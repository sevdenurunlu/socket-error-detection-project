Socket Programming Project
Data Transmission with Error Detection Methods

1. Project Overview
This project aims to demonstrate commonly used error detection methods in data
communication through a socket-based client-server architecture. Data is transmitted
from a sender to a receiver via an intermediate server that intentionally introduces errors.

2. System Architecture
The system consists of three main components:
- Client 1: Data Sender
- Server: Intermediate Node with Error Injection
- Client 2: Receiver and Error Checker

3. Packet Structure
All transmitted data follows the packet format below:
DATA|METHOD|CONTROL_INFORMATION

Example:
HELLO|CRC16|87AF

4. Implemented Error Detection Methods
The following error detection techniques are implemented in this project:
- Even Parity Bit
- Two-Dimensional (2D) Parity
- CRC-16 (CCITT-FALSE)
- Hamming Code (7,4)

5. Error Injection
The server simulates transmission errors by applying various error injection methods
to the data field of the packet, including bit flips, character substitution, insertion,
deletion, swapping, multiple bit flips, and burst errors.

6. Receiver Operation
The receiver recalculates the control information using the selected error detection
method and compares it with the received control information to determine whether
the data has been transmitted correctly.

7. Execution Order
1) server.py
2) client2_receiver.py
3) client1_sender.py
