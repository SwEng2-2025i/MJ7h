from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "email" in request.form:
            email = request.form["email"]
            password = request.form["password"]
            requests.post("http://localhost:5001/users", json={"email": email, "password": password})
        if "title" in request.form:
            title = request.form["title"]
            requests.post("http://localhost:5002/tasks", json={"title": title})
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
