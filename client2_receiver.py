# client2_receiver.py

import socket
from utils import (
    compute_even_parity,
    compute_2d_parity,
    compute_crc16_ccitt,
    compute_hamming_checkbits,
)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6001   # Server'ın Client2'ye gönderdiği port


def recompute_control(text: str, method: str):
    if method == "PARITY":
        return compute_even_parity(text)
    elif method == "CRC16":
        return compute_crc16_ccitt(text)
    elif method == "2D_PARITY":
        return compute_2d_parity(text)
    elif method == "HAMMING":
        return compute_hamming_checkbits(text)
    else:
        return None


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("Server'a (Client2 portu) bağlanıldı, paket bekleniyor...")

        packet = sock.recv(4096).decode("utf-8")
        print(f"Alınan paket: {packet}")

        try:
            data, method, incoming_control = packet.split("|")
        except ValueError:
            print("Paket formatı hatalı!")
            return

        print(f"Received Data        : {data}")
        print(f"Method               : {method}")
        print(f"Sent Check Bits      : {incoming_control}")

        computed_control = recompute_control(data, method)
        if computed_control is None:
            print(f"Bilinmeyen yöntem: {method}")
            return

        print(f"Computed Check Bits  : {computed_control}")

        if computed_control == incoming_control:
            print("Status               : DATA CORRECT")
        else:
            print("Status               : DATA CORRUPTED")


if __name__ == "__main__":
    main()
