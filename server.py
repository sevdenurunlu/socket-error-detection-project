# server.py

import socket
import random
import string

HOST = "127.0.0.1"
PORT_CLIENT1 = 6000   
PORT_CLIENT2 = 6001  


# ---------------- HATA ENJEKSIYON METOTLARI ---------------- #

def error_bit_flip(text: str) -> str:
    data = bytearray(text.encode("utf-8"))
    if not data:
        return text
    byte_index = random.randint(0, len(data) - 1)
    bit_index = random.randint(0, 7)
    data[byte_index] ^= (1 << bit_index)
    return data.decode("utf-8", errors="replace")


def error_char_substitution(text: str) -> str:
    if not text:
        return text
    index = random.randint(0, len(text) - 1)
    new_char = random.choice(string.ascii_letters)
    return text[:index] + new_char + text[index + 1:]


def error_char_deletion(text: str) -> str:
    if len(text) <= 1:
        return text
    index = random.randint(0, len(text) - 1)
    return text[:index] + text[index + 1:]


def error_random_insertion(text: str) -> str:
    index = random.randint(0, len(text))
    new_char = random.choice(string.ascii_letters)
    return text[:index] + new_char + text[index:]


def error_char_swapping(text: str) -> str:
    if len(text) < 2:
        return text
    index = random.randint(0, len(text) - 2)
    lst = list(text)
    lst[index], lst[index + 1] = lst[index + 1], lst[index]
    return ''.join(lst)


def error_multiple_bit_flips(text: str) -> str:
    result = text
    flips = random.randint(2, 5)
    for _ in range(flips):
        result = error_bit_flip(result)
    return result


def error_burst_error(text: str) -> str:
    if len(text) < 3:
        return text
    length = random.randint(3, min(8, len(text)))
    start = random.randint(0, len(text) - length)
    burst = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return text[:start] + burst + text[start + length:]


ERROR_METHODS = [
    ("Bit Flip", error_bit_flip),
    ("Char Substitution", error_char_substitution),
    ("Char Deletion", error_char_deletion),
    ("Random Insertion", error_random_insertion),
    ("Char Swapping", error_char_swapping),
    ("Multiple Bit Flips", error_multiple_bit_flips),
    ("Burst Error", error_burst_error),
]


# ---------------- SERVER MAIN ---------------- #

def main():
    print("Server başlatılıyor...")

    # 1) Önce Client2 (alıcı) ile bağlantı
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_to_c2:
        server_to_c2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_to_c2.bind((HOST, PORT_CLIENT2))
        server_to_c2.listen(1)
        print(f"Client2 için dinleniyor: {HOST}:{PORT_CLIENT2}")

        conn_c2, addr_c2 = server_to_c2.accept()
        print(f"Client2 bağlandı: {addr_c2}")

        # 2) Şimdi Client1'den gelecek veriyi dinle
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_from_c1:
            server_from_c1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_from_c1.bind((HOST, PORT_CLIENT1))
            server_from_c1.listen(1)
            print(f"Client1 için dinleniyor: {HOST}:{PORT_CLIENT1}")

            conn_c1, addr_c1 = server_from_c1.accept()
            print(f"Client1 bağlandı: {addr_c1}")

            with conn_c1, conn_c2:
                # Client1'den paketi al
                packet = conn_c1.recv(4096).decode("utf-8")
                print(f"Client1'den gelen paket: {packet}")

                try:
                    data, method, control = packet.split("|")
                except ValueError:
                    print("Paket formatı hatalı!")
                    return

                print(f"Orijinal DATA : {data}")
                print(f"Method        : {method}")
                print(f"Control       : {control}")

                # Rastgele bir hata enjeksiyon yöntemi seç
                error_name, error_func = random.choice(ERROR_METHODS)
                corrupted_data = error_func(data)
                print(f"Kullanılan Hata Metodu : {error_name}")
                print(f"Bozulmuş DATA          : {corrupted_data}")

                # Yapı bozulmadan yeni paket
                new_packet = f"{corrupted_data}|{method}|{control}"
                print(f"Client2'ye gönderilecek paket: {new_packet}")

                conn_c2.sendall(new_packet.encode("utf-8"))
                print("Bozulmuş paket Client2'ye gönderildi.")


if __name__ == "__main__":
    main()
