""" Fmotor Application Utils Module """

import base64


def encrypt_motor_id(motor_id: int):
	""" Encrypt Motor ID """
	return base64.b16encode(str(motor_id).encode("utf-8"))


def decrypt_motor_id(encrypt: str):
	""" Decrypt Motor ID """
	return base64.b16decode(encrypt).decode()
