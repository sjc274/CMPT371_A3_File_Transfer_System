# CMPT371 A3 - TCP File Transfer System

## Project Description
This project is a TCP-based file transfer system implemented in Python. It follows a client-server architecture and allows a client to connect to a server, view the files available on the server, upload files to the server, download files from the server, and close the client connection safely.

The application uses TCP because file transfer requires reliable, ordered, and complete delivery of data. The server is designed to keep running and accept multiple client connections over time. Each client connection is handled independently.

## Features
- List files currently available on the server
- Upload a file from the client to the server
- Download a file from the server to the client
- Safe client disconnect using the `QUIT` command
- Chunk-based file transfer for efficiency
- Basic filename sanitization to reduce path traversal issues
- Multithreaded server support so more than one client can connect over time

## Project Structure
```text
CMPT371_A3_File_Transfer_System/
│
├── client.py
├── server.py
├── README.md
├── shared/
│   └── protocol.py
├── client_files/
└── server_files/
```

## Technologies Used
- Python 3
- TCP sockets (`socket` module)
- Threading (`threading` module)
- File and path handling (`os` module)

## Communication Protocol
The client and server communicate using newline-terminated text commands for control messages and raw bytes for file transfer.

### Supported Commands
- `LIST`  
  Requests the list of files stored on the server.

- `UPLOAD <filename> <filesize>`  
  Tells the server that the client wants to upload a file. After the server replies with `READY`, the client sends the file bytes.

- `DOWNLOAD <filename>`  
  Requests a file from the server. If the file exists, the server replies with `FILE <filename> <filesize>`, and after the client replies with `READY`, the server sends the file bytes.

- `QUIT`  
  Closes the client connection only. It does **not** shut down the server.

## Limitations
This project is a working file transfer system, but it has several limitations:

1. **Localhost by default**  
   The server is configured to run on `127.0.0.1`, so by default it only accepts connections from the same computer. To use it across multiple machines, the host/IP configuration would need to be changed.

2. **No encryption**  
   File transfers are not encrypted. This means the application is suitable for learning and local testing, but not for secure real-world deployment over untrusted networks.

3. **No authentication**  
   Any connected client can request file listings, upload files, and download files. There is no username/password system.

4. **Basic overwrite behavior**  
   Uploading a file with the same name as an existing server file may overwrite the existing file.

5. **Simple CLI interface only**  
   The application uses a command-line interface. There is no graphical interface.

6. **No resume support**  
   If a transfer is interrupted, it must be started again from the beginning.

7. **Limited command parsing**  
   The system expects commands in the correct format. Invalid input is handled with error messages, but the protocol is intentionally simple.

8. **No checksum verification**  
   The current version does not verify file integrity using hashing after transfer.

## Questions or Issues That Could Come Up
When running or testing this application, the following issues may come up:

- **"Connection refused"**  
  This usually means the server is not running yet, or the host/port in `client.py` does not match the server.

- **The client says a file does not exist**  
  For upload, the file must be placed in the `client_files/` folder. The client only uploads files from that folder.

- **The server says a file does not exist**  
  For download, the requested file must already be inside the `server_files/` folder or uploaded there first.

- **The server does not stop after the client quits**  
  This is expected. `QUIT` only disconnects the client. The server keeps running and waits for the next connection. Stop the server manually with `Ctrl + C`.

- **Port already in use**  
  Another process may already be using port `5001`. In that case, either stop the other process or change the port number in both `server.py` and `client.py`.

- **Path or filename problems**  
  Only plain filenames should be used. The program sanitizes filenames using `os.path.basename()`.

## Requirements
This project uses only Python standard library modules:
- `socket`
- `threading`
- `os`

Because of that, **no external third-party libraries are required**.

### requirements.txt
A `requirements.txt` file is **not needed** for this project because there are no external packages to install.

If your instructor strictly expects a `requirements.txt` file in every repo, it can be included as an empty file or with a comment such as:

```text
# No external dependencies required
```

## Fresh Environment Setup Guide
These instructions assume a fresh environment.

### 1. Install Python
Make sure Python 3 is installed.

Check with:

```bash
python3 --version
```

or:

```bash
python --version
```

A Python 3 version should be shown.

If Python is not installed, install Python 3 first.

### 2. Download or clone the repository
If using Git:

```bash
git clone <your-repository-url>
cd CMPT371_A3_File_Transfer_System
```

Or download the project as a ZIP and extract it, then open a terminal in the project folder.

### 3. Confirm the project structure
Make sure the following folders exist:

```text
client_files/
server_files/
shared/
```

If `client_files/` or `server_files/` are missing, create them manually:

```bash
mkdir client_files
mkdir server_files
```

On Windows Command Prompt:

```cmd
mkdir client_files
mkdir server_files
```

### 4. No package installation is needed
Since the project uses only Python standard library modules, there is no `pip install` step.

## Step-by-Step Run Guide

### Terminal 1: Start the server
Open a terminal in the project folder and run:

```bash
python3 server.py
```

If your system uses `python` instead of `python3`, run:

```bash
python server.py
```

Expected output:

```text
[STARTED] Server listening on 127.0.0.1:5001
```

Keep this terminal open. The server must stay running while clients connect.

### Terminal 2: Start one client
Open a second terminal in the same project folder and run:

```bash
python3 client.py
```

or:

```bash
python client.py
```

Expected output:

```text
[CONNECTED] Connected to server at 127.0.0.1:5001
```

The client will then show the available commands.

## Client Commands
Once the client is running, you can type the following commands:

```text
list
upload <filename>
download <filename>
quit
```

### Example Session
#### 1. View files on the server
```text
list
```

#### 2. Upload a file
First, place a file inside `client_files/`, for example:

```text
client_files/test.txt
```

Then in the client terminal:

```text
upload test.txt
```

#### 3. Download a file
```text
download test.txt
```

The downloaded file will be saved into `client_files/`.

#### 4. Quit the client
```text
quit
```

This disconnects the client only.

## Running Multiple Clients
You can open additional terminals and run more clients with the same command:

```bash
python3 client.py
```

Each client can connect to the same server while the server is running.

## How to Stop the Server
The server is designed to keep running after a client disconnects.

To stop the server, go to the server terminal and press:

```text
Ctrl + C
```

That is the expected way to terminate the server in this version.

## Example End-to-End Test
A simple full test can be done like this:

1. Start the server.
2. Start the client.
3. Put `test.txt` inside `client_files/`.
4. Run `upload test.txt`.
5. Run `list` and confirm `test.txt` appears.
6. Run `download test.txt`.
7. Run `quit`.
8. Stop the server with `Ctrl + C`.

## Notes for Marker / Instructor
- The server must be started before the client.
- The client connects to `127.0.0.1` on port `5001`.
- The application uses only Python standard library modules, so there are no external installation dependencies.
- `QUIT` disconnects the client only; it does not shut down the server.