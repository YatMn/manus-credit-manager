"""
简化版加密工具模块
使用base64编码代替复杂的加密（仅用于演示）
"""
import base64
import os

class SimpleCrypto:
    def __init__(self):
        # 使用简单的base64编码，实际生产环境应使用更安全的加密方法
        self.key = os.environ.get('SIMPLE_KEY', 'demo_key_12345')
    
    def encrypt(self, data):
        """简单加密（base64编码）"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        encoded = base64.b64encode(data).decode('utf-8')
        return encoded
    
    def decrypt(self, encrypted_data):
        """简单解密（base64解码）"""
        try:
            decoded = base64.b64decode(encrypted_data.encode('utf-8'))
            return decoded.decode('utf-8')
        except Exception:
            return None

# 全局实例
crypto = SimpleCrypto()

