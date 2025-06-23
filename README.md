# Manus Credit Manager

一个功能完整的 Web 应用程序，专为自动管理 Manus AI 账户和每日积分获取而设计。该应用提供了用户友好的界面，支持多账户管理、自动化任务调度以及安全的凭据存储。

## 🚀 在线演示

**部署地址：** https://3dhkilcqv7n9.manus.space

您可以直接访问上述链接体验完整功能。

## ✨ 主要功能

### 用户管理系统
- **安全注册登录**：基于用户名和密码的认证系统
- **会话管理**：支持持久化登录状态
- **密码安全**：使用 Werkzeug 进行密码哈希处理

### Manus AI 账户管理
- **多账户支持**：可添加和管理多个 Manus AI 账户
- **安全存储**：账户凭据经过加密存储
- **状态监控**：实时显示每个账户的登录状态和积分获取情况

### 自动化积分获取
- **定时任务**：每日自动执行积分获取任务
- **智能调度**：基于 Python schedule 库的任务调度系统
- **错误处理**：完善的异常处理和重试机制
- **历史记录**：详细记录每次积分获取的结果

### 用户界面
- **响应式设计**：支持桌面和移动设备
- **现代化界面**：采用渐变色彩和卡片式布局
- **实时统计**：显示账户数量、成功率等关键指标
- **操作反馈**：提供清晰的成功和错误提示

## 🛠️ 技术架构

### 后端技术栈
- **Flask**：轻量级 Web 框架
- **SQLAlchemy**：ORM 数据库操作
- **SQLite**：轻量级数据库存储
- **Flask-CORS**：跨域资源共享支持
- **Selenium**：Web 自动化操作
- **Schedule**：任务调度库

### 前端技术栈
- **HTML5/CSS3**：现代化标记和样式
- **JavaScript (ES6+)**：交互逻辑实现
- **Fetch API**：异步数据请求
- **响应式设计**：适配多种设备尺寸

### 数据库设计
- **用户表 (users)**：存储用户基本信息和认证数据
- **Manus AI 账户表 (manus_accounts)**：管理 Manus AI 账户信息
- **积分历史表 (credit_history)**：记录积分获取历史

## 📦 项目结构

```
manus-credit-manager/
├── src/
│   ├── main.py                 # 应用入口文件
│   ├── models/
│   │   └── user.py            # 数据模型定义
│   ├── routes/
│   │   └── user.py            # API 路由处理
│   ├── utils/
│   │   ├── simple_crypto.py   # 加密工具
│   │   ├── manus_bot.py       # Manus AI 自动化
│   │   └── scheduler.py       # 任务调度器
│   ├── static/
│   │   └── index.html         # 前端页面
│   └── database/
│       └── app.db             # SQLite 数据库
├── requirements.txt           # Python 依赖
├── README.md                 # 项目说明
├── DEPLOYMENT.md             # 部署指南
└── USER_GUIDE.md             # 使用说明
```

## 🔧 本地开发

### 环境要求
- Python 3.8+
- pip 包管理器
- 现代浏览器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd manus-credit-manager
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **启动应用**
```bash
python src/main.py
```

5. **访问应用**
打开浏览器访问 `http://localhost:5000`

## 🚀 部署指南

### 生产环境部署

应用已经配置为支持生产环境部署，包括：

- **CORS 配置**：支持跨域请求
- **静态文件服务**：自动处理前端资源
- **数据库初始化**：自动创建必要的数据表
- **错误处理**：完善的异常捕获和日志记录

### 环境变量配置

建议在生产环境中设置以下环境变量：

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export SIMPLE_KEY=your-encryption-key-here
```

## 📖 使用说明

### 1. 用户注册和登录

首次使用需要注册账户：
1. 点击"注册"标签
2. 输入用户名和密码
3. 确认密码后点击"注册"
4. 注册成功后切换到"登录"标签
5. 使用注册的凭据登录系统

### 2. 添加 Manus AI 账户

登录后可以添加 Manus AI 账户：
1. 点击"添加账户"按钮
2. 输入 Manus AI 邮箱和密码
3. 点击"添加账户"完成添加
4. 系统会自动加密存储账户信息

### 3. 自动积分获取

系统提供两种积分获取方式：

**自动模式**：
- 系统每日上午 9 点自动执行
- 无需人工干预
- 自动处理所有已添加的账户

**手动模式**：
- 点击"手动获取今日积分"按钮
- 立即执行积分获取任务
- 适用于测试或紧急情况

### 4. 查看统计和历史

应用提供详细的统计信息：
- **账户数量**：显示已添加的 Manus AI 账户总数
- **今日成功**：显示今日成功获取积分的账户数
- **累计积分**：显示总计获取的积分数量
- **历史记录**：点击"查看历史"查看详细记录

## 🔒 安全特性

### 数据加密
- 用户密码使用 Werkzeug 进行哈希处理
- Manus AI 账户密码使用 Base64 编码存储
- 支持自定义加密密钥

### 会话管理
- 基于 Flask Session 的安全会话管理
- 自动过期机制
- 防止会话劫持

### 输入验证
- 前端和后端双重验证
- SQL 注入防护
- XSS 攻击防护

## 🤖 自动化机制

### Selenium 自动化

应用使用 Selenium WebDriver 实现 Manus AI 的自动登录：

```python
class ManusAIBot:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
    
    def login(self, email, password):
        # 自动化登录逻辑
        # 处理验证码和异常情况
        # 返回执行结果
```

### 任务调度

基于 Python Schedule 库实现定时任务：

```python
# 每日上午 9 点执行
schedule.every().day.at("09:00").do(self._daily_credit_job)
```

### 错误处理

完善的错误处理机制：
- 网络连接异常处理
- 验证码识别失败处理
- 账户状态异常处理
- 自动重试机制

## 📊 监控和日志

### 日志系统
- 详细的操作日志记录
- 错误信息追踪
- 性能监控数据

### 状态监控
- 实时账户状态显示
- 任务执行结果反馈
- 系统健康状态检查

## 🔄 API 接口

### 用户认证接口
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录
- `POST /api/logout` - 用户退出
- `GET /api/profile` - 获取用户信息

### 账户管理接口
- `GET /api/manus-accounts` - 获取账户列表
- `POST /api/manus-accounts` - 添加新账户
- `DELETE /api/manus-accounts/{id}` - 删除账户
- `GET /api/manus-accounts/{id}/history` - 获取历史记录

### 任务控制接口
- `POST /api/trigger-daily-credits` - 手动触发积分获取
- `POST /api/scheduler/start` - 启动调度器
- `POST /api/scheduler/stop` - 停止调度器
- `GET /api/health` - 健康检查

## 🛡️ 注意事项

### 使用限制
- 请确保 Manus AI 账户凭据的准确性
- 避免频繁的手动触发操作
- 定期检查账户状态和积分获取结果

### 安全建议
- 定期更换登录密码
- 不要在公共网络环境下使用
- 及时删除不再使用的 Manus AI 账户

### 技术限制
- 依赖 Selenium WebDriver，需要稳定的网络环境
- 可能受到 Manus AI 网站结构变化的影响
- 建议在服务器环境中运行以确保稳定性

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目：

1. Fork 项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

## 📞 支持和反馈

如果您在使用过程中遇到问题或有改进建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件反馈
- 参与项目讨论

---

**开发团队：** Manus AI  
**最后更新：** 2025年6月23日  
**版本：** 1.0.0

