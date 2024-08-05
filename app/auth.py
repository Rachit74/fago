from flask import Blueprint, render_template, redirect, url_for, request
import requests
from . import API_URL

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('useremail')
        password = request.form.get('userpassword')
        response = requests.post(f"{API_URL}/signup", json={
            "username": username,
            "email": email,
            "password": password,
        })
        if response.status_code == 201:
            print("USER CREATED")
            return redirect(url_for('views.index'))
        else:
            return "Error creating blog", response.status_code

    return render_template("signup.html")