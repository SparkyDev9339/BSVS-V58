numbers = [127074068]
hex_str = ''.join(format(num, 'x') for num in numbers)
print(hex_str)

def hex_decoder(hex_str):
    decoded_str = bytes.fromhex(hex_str).decode('utf-8')
    return decoded_str

byte_str = bytes.fromhex(hex_str)

byte_value = b'\x9e\xd9n\x05W\xf9\xde\xea\xccy\xb1\xe4;O]\xd9\x19!q\xb9w\xab\xcd\xf6\x0b\xb9\xb9\x16\x8c\x98k\x14'
# Convert byte to hexadecimal
hex_value = hex(int.from_bytes(byte_value, byteorder='big'))

print(hex_value)

hex_str1 = "48656c6c6f20576f726c64" # Hello World!

decoded_str = hex_decoder(hex_str1)
print(decoded_str)  # Выводит decoded_str

str_len = "2BFDF6E5DA6D5D68C45A756F42EAD024"

print(len(str_len))