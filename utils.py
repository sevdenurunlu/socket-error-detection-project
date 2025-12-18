# utils.py

# Ortak: metni bit string'e çevir
def text_to_bits(text: str) -> str:
    return ''.join(f'{ord(c):08b}' for c in text)


def compute_even_parity(text: str) -> str:
    """
    Tek boyutlu even parity.
    Tüm bitlerdeki 1 sayısını sayar:
    - Çift ise 0
    - Tek ise 1 döner
    """
    bits = text_to_bits(text)
    ones_count = bits.count('1')
    return '0' if ones_count % 2 == 0 else '1'


def compute_2d_parity(text: str) -> str:
    """
    2D parity:
    - Her karakter 8 bitlik satır (row)
    - Her satır için bir parity biti
    - Her sütun (bit pozisyonu) için bir parity biti

    Kontrol bilgisi formatı: "R<rowparity>-C<colparity>"
    Örnek: R0101-C11001010
    """
    if not text:
        return "R-C"

    rows = [f'{ord(c):08b}' for c in text]

    # Satır (row) paritileri
    row_parity_bits = []
    for row in rows:
        ones = row.count('1')
        row_parity_bits.append('0' if ones % 2 == 0 else '1')
    row_parity = ''.join(row_parity_bits)

    # Sütun (column) paritileri (8 bitlik sütunlar)
    col_parity_bits = []
    for col in range(8):
        ones = sum(1 for row in rows if row[col] == '1')
        col_parity_bits.append('0' if ones % 2 == 0 else '1')
    col_parity = ''.join(col_parity_bits)

    return f"R{row_parity}-C{col_parity}"


def compute_crc16_ccitt(text: str, poly: int = 0x1021, init_crc: int = 0xFFFF) -> str:
    """
    Metin için CRC-16/CCITT-FALSE hesaplar.
    Sonucu 4 haneli HEX string olarak döner (örn: '87AF').
    """
    crc = init_crc
    data = text.encode("utf-8")

    for b in data:
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # 16-bit maske

    return f"{crc:04X}"


# ----- Hamming(7,4) tabanlı check bitleri ----- #

def _hamming74_parity_bits(nibble_bits: str) -> str:
    """
    nibble_bits: 'd1d2d3d4' şeklinde 4 bitlik string.
    Hamming(7,4) için p1, p2, p3 hesaplar:
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    """
    nibble_bits = nibble_bits.ljust(4, '0')  # eksikse 0 ile doldur
    d1, d2, d3, d4 = [int(b) for b in nibble_bits[:4]]

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    return f"{p1}{p2}{p3}"


def compute_hamming_checkbits(text: str) -> str:
    """
    Tüm metni bit dizisine çevirir,
    her 4 bitlik nibble için Hamming(7,4) parity bitlerini hesaplar.
    Çıktı: tüm nibble'ların parity bitlerinin ardışık string hâli.
    """
    bits = text_to_bits(text)
    if not bits:
        return ""

    check_bits_chunks = []
    for i in range(0, len(bits), 4):
        nibble = bits[i:i+4]
        check_bits_chunks.append(_hamming74_parity_bits(nibble))

    return ''.join(check_bits_chunks)
