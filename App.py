from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    users = [
        {"name": "Alice", "role": "Admin"},
        {"name": "Bob", "role": "User"},
        {"name": "Charlie", "role": "Guest"}
    ]
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
