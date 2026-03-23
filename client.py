import os
import socket
from shared.protocol import send_text, recv_text, send_file, recv_file, safe_filename

HOST = "127.0.0.1"
PORT = 5001
CLIENT_FILES_DIR = "client_files"


def ensure_client_directory() -> None:
    os.makedirs(CLIENT_FILES_DIR, exist_ok=True)


def print_menu() -> None:
    print("\nAvailable commands:")
    print("  list")
    print("  upload <filename>")
    print("  download <filename>")
    print("  quit")


def handle_list(sock: socket.socket) -> None:
    send_text(sock, "LIST")
    response = recv_text(sock)
    print(f"[SERVER] {response}")


def handle_upload(sock: socket.socket, filename: str) -> None:
    filename = safe_filename(filename)
    file_path = os.path.join(CLIENT_FILES_DIR, filename)

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("[CLIENT] File does not exist in client_files.")
        return

    file_size = os.path.getsize(file_path)
    send_text(sock, f"UPLOAD {filename} {file_size}")

    response = recv_text(sock)
    if response != "READY":
        print(f"[SERVER] {response}")
        return

    send_file(sock, file_path)

    final_response = recv_text(sock)
    print(f"[SERVER] {final_response}")


def handle_download(sock: socket.socket, filename: str) -> None:
    filename = safe_filename(filename)
    send_text(sock, f"DOWNLOAD {filename}")

    response = recv_text(sock)
    if response.startswith("ERROR"):
        print(f"[SERVER] {response}")
        return

    parts = response.split(maxsplit=2)
    if len(parts) != 3 or parts[0] != "FILE":
        print(f"[CLIENT] Unexpected server response: {response}")
        return

    recv_filename = parts[1]
    file_size = int(parts[2])

    save_path = os.path.join(CLIENT_FILES_DIR, recv_filename)

    send_text(sock, "READY")
    recv_file(sock, save_path, file_size)

    print(f"[CLIENT] Download complete: {recv_filename} ({file_size} bytes)")


def start_client() -> None:
    ensure_client_directory()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")

        while True:
            print_menu()
            user_input = input("\nEnter command: ").strip()

            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()

            if command == "list":
                handle_list(client_socket)

            elif command == "upload":
                if len(parts) != 2:
                    print("[CLIENT] Usage: upload <filename>")
                    continue
                handle_upload(client_socket, parts[1])

            elif command == "download":
                if len(parts) != 2:
                    print("[CLIENT] Usage: download <filename>")
                    continue
                handle_download(client_socket, parts[1])

            elif command == "quit":
                send_text(client_socket, "QUIT")
                response = recv_text(client_socket)
                print(f"[SERVER] {response}")
                break

            else:
                print("[CLIENT] Unknown command.")

    except ConnectionRefusedError:
        print("[CLIENT] Could not connect to server. Make sure the server is running.")
    except KeyboardInterrupt:
        print("\n[CLIENT] Exiting.")
    except Exception as error:
        print(f"[CLIENT ERROR] {error}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()