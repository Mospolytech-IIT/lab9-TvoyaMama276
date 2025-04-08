"""Скрипт для извлечения данных из базы данных"""
from models import SessionLocal, User, Post
def fetch_all_users():
    """Выводит всех пользователей"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            print(f"User: {user.username}, Email: {user.email}")
    finally:
        db.close()
def fetch_posts_with_users():
    """Выводит все посты вместе с пользователями"""
    db = SessionLocal()
    try:
        posts = db.query(Post).all()
        for post in posts:
            print(f"Post: {post.title}, Author: {post.user.username}")
    finally:
        db.close()
if __name__ == "__main__":
    fetch_all_users()
    fetch_posts_with_users()