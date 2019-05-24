import random
import string
import hashlib

def encrypt_string(string):
	return hashlib.sha256(string.encode('utf-8')).hexdigest()