"""
定时任务模块
用于每日自动获取 Manus AI 积分
"""
import schedule
import time
import threading
from datetime import datetime, date
from src.models.user import ManusAccount, CreditHistory, db
from src.utils.manus_bot import ManusAIBot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreditScheduler:
    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None
        
    def start(self):
        """启动定时任务"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
            
        self.running = True
        
        # 设置每日任务 - 每天早上 9 点执行
        schedule.every().day.at("09:00").do(self._daily_credit_job)
        
        # 启动调度器线程
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info("Credit scheduler started")
    
    def stop(self):
        """停止定时任务"""
        self.running = False
        schedule.clear()
        logger.info("Credit scheduler stopped")
    
    def _run_scheduler(self):
        """运行调度器"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def _daily_credit_job(self):
        """每日积分获取任务"""
        logger.info("Starting daily credit collection job")
        
        with self.app.app_context():
            try:
                # 获取所有需要处理的账户
                accounts = ManusAccount.query.all()
                
                for account in accounts:
                    self._process_account(account)
                    
                logger.info("Daily credit collection job completed")
                
            except Exception as e:
                logger.error(f"Error in daily credit job: {e}")
    
    def _process_account(self, account):
        """处理单个账户的积分获取"""
        try:
            # 检查今天是否已经获取过积分
            today = date.today()
            existing_record = CreditHistory.query.filter_by(
                account_id=account.id,
                date=today
            ).first()
            
            if existing_record:
                logger.info(f"Credits already obtained today for account {account.email}")
                return
            
            # 获取解密后的密码
            password = account.get_password()
            if not password:
                logger.error(f"Could not decrypt password for account {account.email}")
                self._record_failure(account, "Could not decrypt password")
                return
            
            # 使用机器人登录并获取积分
            bot = ManusAIBot(headless=True)
            success, message, credits_info = bot.login(account.email, password)
            
            if success:
                # 记录成功
                credits_gained = credits_info.get('daily_credits', 300)
                self._record_success(account, credits_gained)
                logger.info(f"Successfully obtained {credits_gained} credits for {account.email}")
            else:
                # 记录失败
                self._record_failure(account, message)
                logger.error(f"Failed to obtain credits for {account.email}: {message}")
                
        except Exception as e:
            logger.error(f"Error processing account {account.email}: {e}")
            self._record_failure(account, str(e))
    
    def _record_success(self, account, credits_gained):
        """记录成功的积分获取"""
        history_record = CreditHistory(
            account_id=account.id,
            date=date.today(),
            credits_gained=credits_gained,
            status='success'
        )
        
        # 更新账户状态
        account.last_login = datetime.utcnow()
        account.daily_credits_obtained = True
        
        db.session.add(history_record)
        db.session.commit()
    
    def _record_failure(self, account, error_message):
        """记录失败的积分获取"""
        history_record = CreditHistory(
            account_id=account.id,
            date=date.today(),
            credits_gained=0,
            status='failed',
            error_message=error_message
        )
        
        db.session.add(history_record)
        db.session.commit()

# 全局调度器实例
scheduler = None

def init_scheduler(app):
    """初始化调度器"""
    global scheduler
    scheduler = CreditScheduler(app)
    return scheduler

