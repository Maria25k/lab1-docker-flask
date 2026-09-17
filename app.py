import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Сборка строки подключения из переменных окружения ---
DB_USER = os.environ.get("DB_USER", "app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "changeme")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "visits_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Модель Visit ---
class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Visit {self.id} {self.ip_address} {self.visited_at}>"


# --- Создание таблиц при старте ---
with app.app_context():
    db.create_all()


# --- Маршрут /hello ---
@app.route("/hello", methods=["GET"])
def hello():
    # 1. Текущее время
    now = datetime.utcnow()

    # 2. IP-адрес клиента
    # Если приложение за прокси — использовать X-Forwarded-For
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    # 3. Сохранить запись в таблицу Visit
    visit = Visit(visited_at=now, ip_address=ip)
    db.session.add(visit)
    db.session.commit()

    # 4. Вернуть 200 OK с телом «Hello»
    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)