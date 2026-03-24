from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
# build-tag: v2
# build-tag: v6
# build-tag: v10
# build-tag: v14
# build-tag: v18
# build-tag: v22
