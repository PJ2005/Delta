from flask import Flask, jsonify
app = Flask(__name__)

count = 0

@app.route("/index")
def hello():
    global count
    count += 1
    return jsonify({"response":"Hello World!"}, {"times-requested": count})
app.run()