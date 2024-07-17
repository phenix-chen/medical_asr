from flask import Flask, request

app = Flask(__name__)


@app.route('/print', methods=['POST'])
def print_text():
    text = request.form.get('text')
    if text:
        print(f"Received text: {text}")
        return 'Text printed to console', 200
    else:
        return 'No text received', 400


if __name__ == '__main__':
    app.run(debug=True)
