# P2P File Sharing System

## Overview
This project is a **Peer-to-Peer (P2P) File Sharing System** that enables fast and efficient file transfers between devices on the same WiFi network. It combines Python for the graphical user interface (GUI) and higher-level logic, while C is used for the core file transfer operations to ensure high-speed performance.

## Features
- **Peer Discovery**: Automatically detects and connects to nearby peers on the same WiFi network.
- **File Sharing**: Allows users to send and receive files seamlessly.
- **Optimized Transfer Speed**: Uses C for high-performance file transfer.
- **User-Friendly GUI**: Provides an intuitive interface for selecting files and managing transfers.
- **Built-in Chat**: Enables communication between peers.
- **Completion Animation**: Displays a "Congratulations, Share Completed" animation after successful transfers.

## How It Works
1. **Launching the Application**: Run the Python GUI, which initializes the P2P connection.
2. **Discovering Peers**: The system scans for available peers in the network.
3. **Sending a File**: The sender selects a file and initiates a transfer request.
4. **Receiving a File**: The receiver waits for incoming transfer requests and accepts them.
5. **File Transfer**: The core transfer logic, implemented in C, handles high-speed file transmission.
6. **Transfer Completion**: Once the file transfer completes, an animation is displayed to confirm success.

## Installation
### Prerequisites
- Python 3.x
- GCC Compiler (for C code)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/p2p-file-sharing.git
   cd p2p-file-sharing
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Compile the C transfer module:
   ```bash
   gcc -o file_transfer file_transfer.c
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
- **Sender**: Select a file and choose a peer to send the file.
- **Receiver**: Wait for a file transfer request and accept it.
- **Chat**: Use the built-in chat feature to communicate with peers.