import os
import socket

BUFFER_SIZE = 4096
ENCODING = "utf-8"


def send_text(sock: socket.socket, message: str) -> None:
    """
    Send a text message terminated by newline.
    """
    data = (message + "\n").encode(ENCODING)
    sock.sendall(data)


def recv_text(sock: socket.socket) -> str:
    """
    Receive a newline-terminated text message.
    """
    data = bytearray()

    while True:
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Connection closed while receiving text message.")
        if chunk == b"\n":
            break
        data.extend(chunk)

    return data.decode(ENCODING)


def send_file(sock: socket.socket, file_path: str) -> None:
    """
    Send the file contents in chunks.
    """
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)


def recv_file(sock: socket.socket, file_path: str, file_size: int) -> None:
    """
    Receive exactly file_size bytes and save them to file_path.
    """
    remaining = file_size

    with open(file_path, "wb") as file:
        while remaining > 0:
            chunk = sock.recv(min(BUFFER_SIZE, remaining))
            if not chunk:
                raise ConnectionError("Connection closed during file transfer.")
            file.write(chunk)
            remaining -= len(chunk)


def safe_filename(filename: str) -> str:
    """
    Prevent path traversal by stripping directory components.
    """
    return os.path.basename(filename)