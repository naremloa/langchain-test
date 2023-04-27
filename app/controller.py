from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/query", methods=["GET"])
def query_index():
    query_text = request.args.get("text", None)
    if query_text is None:
        return "No text found, please include a ?text=blah parameter in the URL", 400
    response = "query_index"
    return str(response), 200


@app.route("/file", methods=["GET"])
def file_index():
    query_text = request.args.get("text", None)
    if query_text is None:
        return "No text found, please include a ?text=blah parameter in the URL", 400
    response = "file_index"
    return str(response), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5601,
        debug=True,
    )
