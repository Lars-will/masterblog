from flask import Flask, render_template
import json

app = Flask(__name__)


def load_json():
    with open('./data/db.json', 'r') as fileobj:
        blog_posts = json.loads(fileobj.read())
    return blog_posts


@app.route('/')
def index():
    blog_posts = load_json()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)