import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.utils.scheduler import init_scheduler

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 启用 CORS 支持跨域请求
CORS(app, supports_credentials=True)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api')

# 数据库配置 - 使用相对路径，在部署环境中会自动创建
# 在本地开发时使用持久化路径，在部署时使用相对路径
if os.path.exists('/home/ubuntu/data'):
    # 本地开发环境
    persistent_db_path = '/home/ubuntu/data/app.db'
else:
    # 部署环境
    persistent_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    # 确保数据库目录存在
    os.makedirs(os.path.dirname(persistent_db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{persistent_db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# 初始化定时任务调度器
scheduler = init_scheduler(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return {'status': 'healthy', 'message': 'Manus Credit Manager is running'}

@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """启动定时任务"""
    try:
        scheduler.start()
        return {'status': 'success', 'message': 'Scheduler started'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """停止定时任务"""
    try:
        scheduler.stop()
        return {'status': 'success', 'message': 'Scheduler stopped'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    # 在开发模式下自动启动调度器
    if os.environ.get('FLASK_ENV') != 'production':
        try:
            scheduler.start()
            print("Scheduler started in development mode")
        except Exception as e:
            print(f"Failed to start scheduler: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

