import random, threading, time, os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "demo-secret-key")
DEMO_PHONE, DEMO_CODE = "13800000000", "123456"

ITEMS = [("河砂", 145), ("机制砂", 98), ("细砂", 120), ("碎石 5-10mm", 88),
         ("碎石 10-20mm", 82), ("碎石 20-31.5mm", 78), ("石粉", 45), ("毛石", 65)]
prices = {n: {"name": n, "base": b, "open": float(b), "price": float(b), "updated": ""} for n, b in ITEMS}
lock = threading.Lock()

def walk():
    while True:
        with lock:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for p in prices.values():
                p["price"] = round(max(p["base"] * 0.7, p["price"] * (1 + random.gauss(0, 0.004))), 2)
                p["updated"] = now
        time.sleep(3)

threading.Thread(target=walk, daemon=True).start()

@app.route("/")
def index():
    return redirect(url_for("dashboard" if session.get("user") else "login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("phone") == DEMO_PHONE and request.form.get("code") == DEMO_CODE:
            session["user"] = DEMO_PHONE
            return redirect(url_for("dashboard"))
        error = "手机号或验证码错误（演示账号：13800000000 / 123456）"
    return render_template("login.html", error=error)

@app.route("/send_code", methods=["POST"])
def send_code():
    return jsonify(ok=True, msg="演示模式：未发送真实短信，验证码为 123456")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/api/prices")
def api_prices():
    if not session.get("user"):
        return jsonify(error="未登录"), 401
    with lock:
        data = [{"name": p["name"], "price": p["price"],
                 "change": round(p["price"] - p["open"], 2),
                 "change_pct": round((p["price"] - p["open"]) / p["open"] * 100, 2),
                 "updated": p["updated"]} for p in prices.values()]
    return jsonify(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), items=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
