from flask import Flask, render_template, redirect, url_for, Blueprint, blueprints

views = Blueprint('views', __name__)

blogs = [
    {
        "id": 1,
        "title": "why you must use rust",
        "content": "rust is a great language and hence you must use it for many purposes like web dev or system dev,rust is a great language and hence you must use it for many purposes like web dev or system dev,rust is a great language and hence you must use it for many purposes like web dev or system dev"
    },
        {
        "id": 2,
        "title": "why you must use FastAPI",
        "content": "rust is a API GO BRRRRRR  must use it for many purposes like web dev or system dev,rust is a great language and hence you must use it for many purposes like web dev or system dev,rust is a great language and hence you must use it for many purposes like web dev or system dev"
    }
]

@views.route("/")
def index():
    return render_template("index.html", blogs = blogs)