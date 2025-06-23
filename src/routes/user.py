from flask import Blueprint, jsonify, request, session
from src.models.user import User, ManusAccount, CreditHistory, db
from datetime import datetime, date
import functools

user_bp = Blueprint('user', __name__)

def login_required(f):
    """登录验证装饰器"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """获取用户资料"""
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict())

@user_bp.route('/manus-accounts', methods=['GET'])
@login_required
def get_manus_accounts():
    """获取用户的 Manus AI 账户列表"""
    user = User.query.get(session['user_id'])
    accounts = [account.to_dict() for account in user.manus_accounts]
    return jsonify(accounts)

@user_bp.route('/manus-accounts', methods=['POST'])
@login_required
def add_manus_account():
    """添加 Manus AI 账户"""
    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # 检查该邮箱是否已被当前用户添加
    existing_account = ManusAccount.query.filter_by(
        user_id=session['user_id'], 
        email=data['email']
    ).first()
    
    if existing_account:
        return jsonify({'error': 'This Manus AI account already exists'}), 400
    
    account = ManusAccount(
        user_id=session['user_id'],
        email=data['email']
    )
    account.set_password(data['password'])
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({'message': 'Manus AI account added successfully', 'account': account.to_dict()}), 201

@user_bp.route('/manus-accounts/<int:account_id>', methods=['DELETE'])
@login_required
def delete_manus_account(account_id):
    """删除 Manus AI 账户"""
    account = ManusAccount.query.filter_by(
        id=account_id, 
        user_id=session['user_id']
    ).first_or_404()
    
    db.session.delete(account)
    db.session.commit()
    
    return jsonify({'message': 'Manus AI account deleted successfully'}), 200

@user_bp.route('/manus-accounts/<int:account_id>/history', methods=['GET'])
@login_required
def get_credit_history(account_id):
    """获取积分获取历史"""
    account = ManusAccount.query.filter_by(
        id=account_id, 
        user_id=session['user_id']
    ).first_or_404()
    
    history = [record.to_dict() for record in account.credit_history]
    return jsonify(history)

@user_bp.route('/trigger-daily-credits', methods=['POST'])
@login_required
def trigger_daily_credits():
    """手动触发每日积分获取"""
    user = User.query.get(session['user_id'])
    results = []
    
    for account in user.manus_accounts:
        # 检查今天是否已经获取过积分
        today = date.today()
        existing_record = CreditHistory.query.filter_by(
            account_id=account.id,
            date=today
        ).first()
        
        if existing_record:
            results.append({
                'account_id': account.id,
                'email': account.email,
                'status': 'skipped',
                'message': 'Credits already obtained today'
            })
            continue
        
        # 这里应该调用实际的 Manus AI 登录和积分获取逻辑
        # 暂时模拟成功
        try:
            # TODO: 实现实际的 Manus AI 登录逻辑
            credits_gained = 300  # 模拟获取的积分数
            
            # 记录积分获取历史
            history_record = CreditHistory(
                account_id=account.id,
                date=today,
                credits_gained=credits_gained,
                status='success'
            )
            
            # 更新账户状态
            account.last_login = datetime.utcnow()
            account.daily_credits_obtained = True
            
            db.session.add(history_record)
            db.session.commit()
            
            results.append({
                'account_id': account.id,
                'email': account.email,
                'status': 'success',
                'credits_gained': credits_gained
            })
            
        except Exception as e:
            # 记录失败
            history_record = CreditHistory(
                account_id=account.id,
                date=today,
                credits_gained=0,
                status='failed',
                error_message=str(e)
            )
            
            db.session.add(history_record)
            db.session.commit()
            
            results.append({
                'account_id': account.id,
                'email': account.email,
                'status': 'failed',
                'error': str(e)
            })
    
    return jsonify({'results': results})

