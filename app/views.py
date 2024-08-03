from flask import Flask, render_template, redirect, url_for, Blueprint, request
from . import API_URL
import requests

views = Blueprint('views', __name__)

@views.route("/")
def index():
    # sends a get request to golang api at /blogs
    response = requests.get(f"{API_URL}/blogs")

    if response.status_code == 200:
        blogs = response.json()
        print(blogs)
    else:
        blogs = []
    
    return render_template("index.html", blogs=blogs)

@views.route("/write", methods=["GET", "POST"])
def write_blog():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        response = requests.post(f"{API_URL}/blogs", json={
            "title": title,
            "content": content,
        })
        if response.status_code == 201:
            return redirect(url_for('views.index'))
        else:
            return "Error creating blog", response.status_code
    return render_template("write.html")

@views.route("/blog/<int:id>")
def blog(id):
    response = requests.get(f"{API_URL}/blogs/{id}")
    if response.status_code == 200:
        blog = response.json()
    else:
        return "Blog not found", 404
    return render_template("blog.html", blog=blog)
