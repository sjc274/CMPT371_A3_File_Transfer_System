import os
import socket
import threading
from shared.protocol import send_text, recv_text, send_file, recv_file, safe_filename

HOST = "127.0.0.1"
PORT = 5001
SERVER_FILES_DIR = "server_files"


def ensure_server_directory() -> None:
    os.makedirs(SERVER_FILES_DIR, exist_ok=True)


def handle_list(client_socket: socket.socket) -> None:
    files = os.listdir(SERVER_FILES_DIR)
    files = [f for f in files if os.path.isfile(os.path.join(SERVER_FILES_DIR, f))]

    if not files:
        send_text(client_socket, "OK No files on server.")
        return

    file_list = " | ".join(files)
    send_text(client_socket, f"OK {file_list}")


def handle_upload(client_socket: socket.socket, filename: str, filesize_str: str) -> None:
    try:
        filename = safe_filename(filename)
        file_size = int(filesize_str)

        if file_size < 0:
            send_text(client_socket, "ERROR Invalid file size.")
            return

        file_path = os.path.join(SERVER_FILES_DIR, filename)

        send_text(client_socket, "READY")
        recv_file(client_socket, file_path, file_size)
        send_text(client_socket, "DONE")

        print(f"[UPLOAD] Received file: {filename} ({file_size} bytes)")

    except ValueError:
        send_text(client_socket, "ERROR Invalid UPLOAD command format.")
    except Exception as error:
        send_text(client_socket, f"ERROR Upload failed: {error}")


def handle_download(client_socket: socket.socket, filename: str) -> None:
    try:
        filename = safe_filename(filename)
        file_path = os.path.join(SERVER_FILES_DIR, filename)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            send_text(client_socket, "ERROR File not found.")
            return

        file_size = os.path.getsize(file_path)
        send_text(client_socket, f"FILE {filename} {file_size}")

        response = recv_text(client_socket)
        if response != "READY":
            send_text(client_socket, "ERROR Client not ready for download.")
            return

        send_file(client_socket, file_path)
        print(f"[DOWNLOAD] Sent file: {filename} ({file_size} bytes)")

    except Exception as error:
        send_text(client_socket, f"ERROR Download failed: {error}")


def handle_client(client_socket: socket.socket, client_address) -> None:
    print(f"[NEW CONNECTION] {client_address} connected.")

    try:
        while True:
            command_line = recv_text(client_socket).strip()
            if not command_line:
                continue

            print(f"[COMMAND] From {client_address}: {command_line}")
            parts = command_line.split(maxsplit=2)
            command = parts[0].upper()

            if command == "LIST":
                handle_list(client_socket)

            elif command == "UPLOAD":
                if len(parts) != 3:
                    send_text(client_socket, "ERROR Usage: UPLOAD <filename> <filesize>")
                else:
                    filename = parts[1]
                    filesize_str = parts[2]
                    handle_upload(client_socket, filename, filesize_str)

            elif command == "DOWNLOAD":
                if len(parts) != 2:
                    send_text(client_socket, "ERROR Usage: DOWNLOAD <filename>")
                else:
                    filename = parts[1]
                    handle_download(client_socket, filename)

            elif command == "QUIT":
                send_text(client_socket, "OK Goodbye.")
                print(f"[DISCONNECT] {client_address} requested quit.")
                break

            else:
                send_text(client_socket, "ERROR Unknown command.")

    except ConnectionError:
        print(f"[DISCONNECT] {client_address} disconnected unexpectedly.")
    except Exception as error:
        print(f"[ERROR] Client {client_address}: {error}")
    finally:
        client_socket.close()
        print(f"[CLOSED] Connection with {client_address} closed.")


def start_server() -> None:
    ensure_server_directory()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()