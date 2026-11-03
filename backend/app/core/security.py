from pwdlib import PasswordHash

# Argon2id con i parametri raccomandati dalla libreria
_hasher = PasswordHash.recommended()


# codificA la password in chiaro usando Argon2id e restituisce l'hash
def hash_password(password: str) -> str:
    return _hasher.hash(password)


# decodifica la password in chiaro confrontandola con l'hash memorizzato e restituisce True se corrispondono, altrimenti False
def verify_password(password: str, hashed: str) -> bool:
    return _hasher.verify(password, hashed)
