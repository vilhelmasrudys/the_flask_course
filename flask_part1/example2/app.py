from unicodedata import name
from flask import Flask, render_template
from articles.dictionary import data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)