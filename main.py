from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify('Desafio Cashback')

if __name__ == "__main__":
    app.run()
