import base64

class SimpleCrypto:
    def encrypt_password(self, password):
        # 使用 base64 编码作为简化的加密方式
        return base64.b64encode(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        # 使用 base64 解码作为简化的解密方式
        return base64.b64decode(encrypted_password.encode()).decode()

crypto = SimpleCrypto()

