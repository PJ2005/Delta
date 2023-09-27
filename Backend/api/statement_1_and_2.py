from flask import Flask
app = Flask(__name__)

count = 0

@app.route("/index")
def hello():
    global count
    count += 1
    out = f"You have requested this endpoint {count} times"
    return ("Hello World! " + out)
app.run()


