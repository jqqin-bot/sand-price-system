# 砂石报价系统（演示原型）

## 目录结构
```
sand-price-system/
├── app.py              # Flask 服务：登录、会话、模拟行情、JSON 接口
├── requirements.txt
├── README.md
├── templates/
│   ├── login.html      # 手机号 + 验证码登录页
│   └── dashboard.html  # 股东报价看板（每 3 秒刷新）
└── static/style.css
```

## 启动
```bash
pip install -r requirements.txt
python app.py          # 或：nohup python app.py > app.log 2>&1 &
```
浏览器打开 http://localhost:5000

## 演示账号
- 手机号：13800000000
- 验证码：123456（演示模式，不发送真实短信）

## 说明
- 价格为服务端随机游走模拟数据，未接入真实行情；无支付功能。
- 接口：`GET /api/prices`（需登录）。
