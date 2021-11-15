from flask import Flask, render_template

app = Flask(__name__)

# default-page
@app.route("/")
def home():
    return render_template("home.html")

# about-page
@app.route("/about")
def about():
    return render_template("About.html")

if __name__ == "__main__":
    app.run(debug=True)