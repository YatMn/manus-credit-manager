from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.utils.simple_crypto import crypto

db = SQLAlchemy()

class User(db.Model):
    """Web 应用用户表"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联的 Manus AI 账户
    manus_accounts = db.relationship('ManusAccount', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'manus_accounts_count': len(self.manus_accounts)
        }


class ManusAccount(db.Model):
    """Manus AI 账户表"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    encrypted_password = db.Column(db.Text, nullable=False)  # 使用对称加密存储
    last_login = db.Column(db.DateTime, nullable=True)
    daily_credits_obtained = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 积分获取历史
    credit_history = db.relationship('CreditHistory', backref='account', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """设置 Manus AI 密码（对称加密存储）"""
        self.encrypted_password = crypto.encrypt_password(password)

    def get_password(self):
        """获取 Manus AI 密码（解密）"""
        return crypto.decrypt_password(self.encrypted_password)

    def __repr__(self):
        return f'<ManusAccount {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'daily_credits_obtained': self.daily_credits_obtained,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CreditHistory(db.Model):
    """积分获取历史表"""
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('manus_account.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    credits_gained = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'success' or 'failed'
    error_message = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CreditHistory {self.account_id} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'date': self.date.isoformat() if self.date else None,
            'credits_gained': self.credits_gained,
            'status': self.status,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

