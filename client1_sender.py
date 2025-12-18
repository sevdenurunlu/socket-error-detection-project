# client1_sender.py

import socket
from utils import (
    compute_even_parity,
    compute_2d_parity,
    compute_crc16_ccitt,
    compute_hamming_checkbits,
)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000   # Server'ın Client1'den dinlediği port


def select_method() -> str:
    print("Hata tespit yöntemi seçin:")
    print("1) PARITY")
    print("2) CRC16")
    print("3) 2D_PARITY")
    print("4) HAMMING")

    choice = input("Seçiminiz (1/2/3/4): ").strip()

    if choice == "2":
        return "CRC16"
    elif choice == "3":
        return "2D_PARITY"
    elif choice == "4":
        return "HAMMING"
    else:
        return "PARITY"


def generate_control_info(text: str, method: str) -> str:
    if method == "CRC16":
        return compute_crc16_ccitt(text)
    elif method == "2D_PARITY":
        return compute_2d_parity(text)
    elif method == "HAMMING":
        return compute_hamming_checkbits(text)
    else:  
        return compute_even_parity(text)


def main():
    # 1) Kullanıcıdan metin al
    text = input("Göndermek istediğiniz metni girin: ")

    # 2) Yöntem seç
    method = select_method()
    print(f"Seçilen yöntem: {method}")

    # 3) Kontrol bilgisi üret
    control_info = generate_control_info(text, method)

    # 4) Paketi oluştur: DATA|METHOD|CONTROL
    packet = f"{text}|{method}|{control_info}"
    print(f"Gönderilecek paket: {packet}")

    # 5) Server'a bağlan ve gönder
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("Server'a (Client1 portu) bağlanıldı.")
        sock.sendall(packet.encode("utf-8"))
        print("Paket server'a gönderildi.")


if __name__ == "__main__":
    main()
