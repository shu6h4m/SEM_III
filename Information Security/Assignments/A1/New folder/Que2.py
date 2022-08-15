import random
import sys
import cryptomath_module as cryptomath

Characters = (
    r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"""
    r"""abcdefghijklmnopqrstuvwxyz{|}~"""
)


def check_keys(keyA: int, keyB: int, mode: str) -> None:
    if mode == "encrypt":
        if keyA == 1:
            sys.exit(
                "The affine cipher becomes weak when key "
                "A is set to 1. Choose different key"
            )
        if keyB == 0:
            sys.exit(
                "The affine cipher becomes weak when key "
                "B is set to 0. Choose different key"
            )
    if keyA < 0 or keyB < 0 or keyB > len(Characters) - 1:
        sys.exit(
            "Key A must be greater than 0 and key B must "
            f"be between 0 and {len(Characters) - 1}."
        )
    if cryptomath.gcd(keyA, len(Characters)) != 1:
        sys.exit(
            f"Key A {keyA} and the symbol set size {len(Characters)} "
            "are not relatively prime. Choose a different key."
        )


def encrypt_message(key: int, message: str) -> str:
    """
    >>> encrypt_message(4545, 'The affine cipher is a type of monoalphabetic '
    ...                       'substitution cipher.')
    'VL}p MM{I}p~{HL}Gp{vp pFsH}pxMpyxIx JHL O}F{~pvuOvF{FuF{xIp~{HL}Gi'
    """
    keyA, keyB = divmod(key, len(Characters))
    check_keys(keyA, keyB, "encrypt")
    cipherText = ""
    for symbol in message:
        if symbol in Characters:
            symIndex = Characters.find(symbol)
            cipherText += Characters[(symIndex * keyA + keyB) % len(Characters)]
        else:
            cipherText += symbol
    return cipherText


def decrypt_message(key: int, message: str) -> str:
    """
    >>> decrypt_message(4545, 'VL}p MM{I}p~{HL}Gp{vp pFsH}pxMpyxIx JHL O}F{~pvuOvF{FuF'
    ...                       '{xIp~{HL}Gi')
    'The affine cipher is a type of monoalphabetic substitution cipher.'
    """
    keyA, keyB = divmod(key, len(Characters))
    check_keys(keyA, keyB, "decrypt")
    plainText = ""
    modInverseOfkeyA = cryptomath.find_mod_inverse(keyA, len(Characters))
    for symbol in message:
        if symbol in Characters:
            symIndex = Characters.find(symbol)
            plainText += Characters[(symIndex - keyB) * modInverseOfkeyA % len(Characters)]
        else:
            plainText += symbol
    return plainText


def get_random_key() -> int:
    while True:
        keyA = random.randint(2, len(Characters))
        keyB = random.randint(2, len(Characters))
        if cryptomath.gcd(keyA, len(Characters)) == 1 and keyB % len(Characters) != 0:
            return keyA * len(Characters) + keyB


def main() -> None:
    """
    >>> key = get_random_key()
    >>> msg = "This is a test!"
    >>> decrypt_message(key, encrypt_message(key, msg)) == msg
    True
    """
    message = input("Enter Your Message: ").strip()
    key = int(input("Enter Key [2000 - 9000]: ").strip())
    mode = input("Pree E for Encryption & D for Decryption : ").strip().lower()

    if mode.startswith("e"):
        mode = "encrypt"
        translated = encrypt_message(key, message)
        print(f"\nEncrypted Text is: {translated}\n")
    elif mode.startswith("d"):
        mode = "decrypt"
        translated = decrypt_message(key, message)
        print(f"\nDecrypted Text is: {translated}\n")


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    main()