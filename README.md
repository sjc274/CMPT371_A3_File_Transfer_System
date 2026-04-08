# CMPT371 A3 - TCP File Transfer System
**Course:** CMPT 371 - Data Communications & Networking <br>
**Instructor**: Mirza Zaeem Baig <br>
**Semester**: Spring 2026
## Group Members
| Name      | Student ID | Email                         |
|-----------|------------|-------------------------------|
| Jiachen Sun  | 301436357  | [jsa356@sfu.ca](mailto:jsa356@sfu.ca) |
| Atulya Malhan|  301607963 | [ama367@sfu.ca](mailto:ama367@sfu.ca) |

## 1. Project Description
This project is a TCP-based file transfer system implemented in Python. It follows a client-server architecture and allows a client to connect to a server, view the files available on the server, upload files to the server, download files from the server, and close the client connection safely.

The application uses TCP because file transfer requires reliable, ordered, and complete delivery of data. The server is designed to keep running and accept multiple client connections over time. Each client connection is handled independently.

## 2. Features
- List files currently available on the server
- Upload a file from the client to the server
- Download a file from the server to the client
- Safe client disconnect using the `QUIT` command
- Chunk-based file transfer for efficiency
- Basic filename sanitization to reduce path traversal issues
- Multithreaded server support so more than one client can connect over time
### Supported Commands
- `list`  
  Requests the list of files stored on the server.

- `upload <filename>`  
  Tells the server that the client wants to upload a file. After the server replies with `READY`, the client sends the file bytes.

- `download <filename>`  
  Requests a file from the server. If the file exists, the server replies with `FILE <filename> <filesize>`, and after the client replies with `READY`, the server sends the file bytes.

- `quit`  
  Closes the client connection only. It does **not** shut down the server.

## 3. Video Demo
[VIDEO DEMO HERE](https://www.loom.com/share/6477916222364835884429dd030ad781)

## 4. Technologies Used
- Python 3
- TCP sockets (`socket` module)
- Threading (`threading` module)
- File and path handling (`os` module)

***RUBRIC NOTE: No external libraries are required. Therefore, a requirements.txt file is not strictly necessary for dependency installation, though one might be included for environment completeness.***

## 5. Step-by-Step Run Guide
### 1. Start the server
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

### 2. Start one client
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

### Client Commands
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

### Running Multiple Clients
You can open additional terminals and run more clients with the same command:

```bash
python3 client.py
```

Each client can connect to the same server while the server is running.

### How to Stop the Server
The server is designed to keep running after a client disconnects.

To stop the server, go to the server terminal and press:

```text
Ctrl + C
```

That is the expected way to terminate the server in this version.

### Example End-to-End Test
A simple full test can be done like this:

1. Start the server.
2. Start the client.
3. Put `test.txt` inside `client_files/`.
4. Run `upload test.txt`.
5. Run `list` and confirm `test.txt` appears.
6. Run `download test.txt`.
7. Run `quit`.
8. Stop the server with `Ctrl + C`.

## 6. Limitations
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

## 7. Technical Protocol Details (Custom Text Protocol over TCP)
We designed a custom application-layer protocol for communication between the client and server using newline-terminated text commands over TCP, followed by raw byte streams for file data transfer.
- **Control Message Format:** Plain text, one message in a line
- **Handshake Phase:** Client connects to the server at `127.0.0.1:5001`
- **Command Phase:** Client sends command such as: `list`, `upload <filename>`
  Server responds `[STATUS] MESSAGE`

## 8. Academic Integrity & References
- #### GenAI Usage:
  - ChatGPT was used used to assist in generating the code for file directory handling including checking the existentce of required directory and downloading/uploading files from correct file path.
  - ChatGPT was used to help with `readme.md` syntax.
  - Copilot was used to help with polishing the code and write comments.
- #### References:
  - [Python `socket`](https://docs.python.org/3/library/socket.html)
  - [Python `threading`](https://docs.python.org/3/library/threading.html)
  - [Python `os`](https://docs.python.org/3/library/os.html)
