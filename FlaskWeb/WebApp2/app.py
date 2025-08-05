from flask import Flask, render_template

app = Flask(__name__)

@app.route("/register")
def signup():
    return render_template("index.html",
        collector="http://collector:8080",
        app_id="flask-app-2"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
