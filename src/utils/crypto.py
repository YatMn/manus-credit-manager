"""
加密工具模块
用于对称加密存储 Manus AI 账户密码
"""
import base64
from cryptography.fernet import Fernet
import os

class PasswordCrypto:
    def __init__(self, key=None):
        if key is None:
            # 从环境变量获取密钥，如果没有则生成一个新的
            key = os.environ.get('ENCRYPTION_KEY')
            if key is None:
                key = Fernet.generate_key()
                print(f"Generated new encryption key: {key.decode()}")
                print("Please set ENCRYPTION_KEY environment variable for production use")
            else:
                key = key.encode()
        
        self.cipher_suite = Fernet(key)
    
    def encrypt_password(self, password):
        """加密密码"""
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return base64.b64encode(encrypted_password).decode()
    
    def decrypt_password(self, encrypted_password):
        """解密密码"""
        try:
            encrypted_data = base64.b64decode(encrypted_password.encode())
            decrypted_password = self.cipher_suite.decrypt(encrypted_data)
            return decrypted_password.decode()
        except Exception as e:
            print(f"Failed to decrypt password: {e}")
            return None

# 全局实例
crypto = PasswordCrypto()

