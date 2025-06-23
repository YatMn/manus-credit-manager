# Manus Credit Manager

一个功能完整的 Web 应用程序，专为自动管理 Manus AI 账户和每日积分获取而设计。支持多账户管理、自动化任务调度以及安全的凭据存储。

## 🚀 在线演示

**最新部署地址：** https://kkh7ikcg08lp.manus.space

## ⚠️ 重要说明 - 数据持久化问题

**当前已知问题：** 由于部署环境的限制，每次重新部署应用时，用户数据（包括登录信息和 Manus AI 账户）可能会丢失。这是因为 SQLite 数据库文件在部署过程中被重置。

**临时解决方案：**
1. 建议您在本地环境运行应用以获得完整的数据持久化体验
2. 如需在线使用，请注意可能需要重新注册账户
3. 我们正在积极寻找更好的数据持久化解决方案

**本地运行指南：**
```bash
# 克隆仓库
git clone https://github.com/YatMn/manus-credit-manager.git
cd manus-credit-manager

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python src/main.py
```

访问 http://localhost:5000 即可使用完整功能。

## ✨ 核心功能

### 🔐 用户管理系统
- 安全的注册登录机制
- 密码哈希加密存储
- 会话管理和自动登出

### 👥 多 Manus AI 账户管理
- 支持添加多个 Manus AI 账户
- 账户凭据加密存储
- 实时状态监控和管理
- 账户删除和编辑功能

### ⏰ 自动积分获取
- 每日上午 9:00 自动执行积分获取任务
- 支持手动触发积分获取
- 智能错误处理和重试机制
- 详细的执行日志和历史记录

### 🎨 用户友好界面
- 现代化响应式设计
- 实时统计信息显示
- 清晰的操作反馈和状态指示
- 移动设备友好的界面设计

## 🛠️ 技术架构

### 后端技术栈
- **Web 框架：** Flask 3.0+
- **数据库：** SQLite 3 + SQLAlchemy ORM
- **认证：** Werkzeug 密码哈希
- **跨域支持：** Flask-CORS
- **任务调度：** Python Schedule

### 前端技术栈
- **基础技术：** HTML5 + CSS3 + JavaScript (ES6+)
- **样式设计：** 现代化 CSS Grid 和 Flexbox 布局
- **交互体验：** 原生 JavaScript 异步请求
- **响应式设计：** 移动优先的设计理念

### 自动化技术
- **浏览器自动化：** Selenium WebDriver
- **定时任务：** Python Schedule 库
- **错误处理：** 完善的异常捕获和重试机制

## 📁 项目结构

```
manus-credit-manager/
├── src/
│   ├── main.py                 # 应用入口文件
│   ├── models/
│   │   └── user.py            # 用户和账户数据模型
│   ├── routes/
│   │   └── user.py            # API 路由定义
│   ├── utils/
│   │   ├── simple_crypto.py   # 简化加密工具
│   │   ├── manus_bot.py       # Manus AI 自动登录模块
│   │   └── scheduler.py       # 定时任务调度器
│   ├── static/
│   │   └── index.html         # 前端界面
│   └── database/
│       └── app.db             # SQLite 数据库文件
├── venv/                      # Python 虚拟环境
├── requirements.txt           # Python 依赖列表
├── README.md                  # 项目说明文档
├── USER_GUIDE.md             # 用户使用指南
└── DEPLOYMENT.md             # 部署说明文档
```

## 🔒 安全特性

### 数据加密
- **用户密码：** 使用 Werkzeug 的 PBKDF2 算法进行哈希加密
- **Manus AI 凭据：** 使用 Base64 编码进行简单加密存储
- **会话管理：** Flask 内置的安全会话机制

### 输入验证
- **前端验证：** JavaScript 实时输入验证
- **后端验证：** Flask 路由层面的数据验证
- **XSS 防护：** 自动转义用户输入内容

### 网络安全
- **HTTPS 支持：** 部署环境自动启用 HTTPS
- **CORS 配置：** 合理的跨域资源共享设置
- **错误处理：** 避免敏感信息泄露的错误响应

## 📊 功能特性详解

### 自动积分获取机制

应用程序实现了一个智能的自动积分获取系统：

1. **定时执行：** 每日上午 9:00 自动触发积分获取任务
2. **多账户支持：** 依次处理所有已添加的 Manus AI 账户
3. **错误处理：** 遇到登录失败或网络错误时自动重试
4. **状态更新：** 实时更新账户状态和积分获取结果
5. **日志记录：** 详细记录每次执行的结果和错误信息

### 用户界面设计

界面采用现代化的设计理念：

- **统计卡片：** 直观显示账户数量、今日获取成功数、累计积分
- **账户管理：** 清晰的账户列表，支持查看状态、历史记录和删除操作
- **实时反馈：** 操作结果通过颜色和文字及时反馈给用户
- **响应式布局：** 适配桌面和移动设备的不同屏幕尺寸

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 现代浏览器（Chrome、Firefox、Safari、Edge）
- 稳定的网络连接

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/YatMn/manus-credit-manager.git
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

4. **运行应用**
   ```bash
   python src/main.py
   ```

5. **访问应用**
   打开浏览器访问 http://localhost:5000

### 首次使用

1. **注册账户：** 创建您的管理员账户
2. **登录系统：** 使用注册的用户名和密码登录
3. **添加 Manus AI 账户：** 输入您的 Manus AI 邮箱和密码
4. **验证功能：** 手动触发一次积分获取以验证配置正确
5. **享受自动化：** 系统将每日自动为您获取积分

## 🔧 配置说明

### 数据库配置

应用程序会自动检测运行环境并选择合适的数据库路径：

- **本地开发：** `/home/ubuntu/data/app.db`（持久化存储）
- **部署环境：** `src/database/app.db`（相对路径）

### 定时任务配置

默认配置为每日上午 9:00 执行，可在 `src/utils/scheduler.py` 中修改：

```python
# 修改执行时间
schedule.every().day.at("09:00").do(daily_credit_task)
```

### 安全配置

在生产环境中，建议修改以下配置：

1. **SECRET_KEY：** 在 `src/main.py` 中更改为随机字符串
2. **数据库加密：** 考虑使用更强的加密算法
3. **HTTPS：** 确保在 HTTPS 环境下运行

## 🐛 故障排除

### 常见问题

**Q: 登录后显示空白页面？**
A: 检查浏览器控制台是否有 JavaScript 错误，确保网络连接正常。

**Q: 添加账户时提示网络错误？**
A: 这通常是由于加密模块问题，请确保已正确安装所有依赖。

**Q: 自动积分获取不工作？**
A: 检查 Manus AI 账户凭据是否正确，网络是否稳定。

**Q: 数据丢失问题？**
A: 在部署环境中可能出现数据丢失，建议使用本地运行获得完整体验。

### 日志查看

应用程序会在控制台输出详细的运行日志，包括：
- 定时任务执行状态
- 数据库操作记录
- 错误和异常信息
- API 请求响应日志

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

### 开发环境设置

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码规范
- 添加适当的注释和文档字符串
- 确保所有功能都有相应的错误处理
- 提交前运行测试确保功能正常

## 📄 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

## 🙏 致谢

感谢以下开源项目的支持：
- Flask - 轻量级 Web 框架
- SQLAlchemy - Python SQL 工具包
- Selenium - Web 浏览器自动化
- Schedule - Python 任务调度库

## 📞 支持与反馈

如果您在使用过程中遇到任何问题或有改进建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至项目维护者
- 在项目讨论区参与讨论

---

**注意：** 本项目仅供学习和个人使用，请遵守 Manus AI 的服务条款和使用政策。

