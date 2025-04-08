from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import SessionLocal, User, Post
app = FastAPI()
templates = Jinja2Templates(directory="templates")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/users", response_class=HTMLResponse)
def get_users_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
@app.get("/users/new", response_class=HTMLResponse)
def new_user_page(request: Request):
    return templates.TemplateResponse("new_user.html", {"request": request})
@app.post("/users/new")
def create_user(
    username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db) ):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)
@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})
@app.put("/users/edit/{user_id}")
def update_user(
    user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db) ):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    return RedirectResponse(url="/users", status_code=303)
@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)
@app.get("/posts", response_class=HTMLResponse)
def get_posts_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})
@app.get("/posts/new", response_class=HTMLResponse)
def new_post_page(request: Request):
    return templates.TemplateResponse("new_post.html", {"request": request})
@app.post("/posts/new")
def create_post(
    title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db) ):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    new_post = Post(title=title, content=content, user_id=user_id)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)
@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def get_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})
@app.put("/posts/edit/{post_id}")
def update_post(
    post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db) ):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)
@app.delete("/posts/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)