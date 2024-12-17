from base64 import urlsafe_b64decode

import pytest
from cryptography.fernet import InvalidToken

from app.utils.crypto_utils import decrypt, encrypt, generate_key_from_passphrase


def test_generate_key_from_passphrase():
    """
    Тестирует функцию generate_key_from_passphrase, которая генерирует ключ из фразы-пароля и соли.

    Проверяется, что длина возвращаемого ключа составляет 44 символа (что соответствует стандарту Fernet).
    """
    passphrase = b"my_secret_passphrase"
    salt = b"my_secret_salt"

    key = generate_key_from_passphrase(passphrase, salt)

    assert len(key) == 44


def test_encrypt_decrypt():
    """
    Тестирует функции шифрования и дешифрования (encrypt и decrypt).

    Проверяется, что зашифрованный текст не совпадает с исходным секретом,
    и что расшифрованный текст совпадает с исходным секретом.
    """
    secret = "my_secret_data"
    passphrase = b"my_secret_passphrase"
    salt = b"my_secret_salt"
    key = generate_key_from_passphrase(passphrase, salt)

    encrypted_secret = encrypt(secret, key)

    assert encrypted_secret != secret

    decrypted_secret = decrypt(encrypted_secret, key)

    assert decrypted_secret == secret


def test_decrypt_with_wrong_key():
    """
    Тестирует попытку дешифровки с неправильным ключом.

    Проверяется, что при попытке дешифрования с неправильным ключом возникает исключение InvalidToken.
    """
    secret = "my_secret_data"
    passphrase = b"my_secret_passphrase"
    salt = b"my_secret_salt"
    wrong_passphrase = b"wrong_passphrase"

    key = generate_key_from_passphrase(passphrase, salt)
    wrong_key = generate_key_from_passphrase(wrong_passphrase, salt)

    encrypted_secret = encrypt(secret, key)

    with pytest.raises(InvalidToken):
        decrypt(encrypted_secret, wrong_key)


def test_encrypt_output_is_base64():
    """
    Тестирует, что результат функции encrypt является корректным base64.

    Проверяется, что зашифрованный секрет можно декодировать как base64.
    """
    secret = "my_secret_data"
    passphrase = b"my_secret_passphrase"
    salt = b"my_secret_salt"

    key = generate_key_from_passphrase(passphrase, salt)
    encrypted_secret = encrypt(secret, key)

    try:
        urlsafe_b64decode(encrypted_secret)
    except Exception as e:
        pytest.fail(f"Encrypted secret is not valid base64: {e}")
