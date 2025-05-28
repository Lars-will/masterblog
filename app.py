from flask import Flask, render_template, redirect, url_for, request
import json



app = Flask(__name__)

def save_blog_post(dict_post):
    blog_posts = load_json()
    print(blog_posts)
    blog_posts.append(dict_post)
    #print(blog_posts)
    with open('./data/db.json', 'w') as fileobj:
        json.dump(blog_posts, fileobj)


def load_json():
    with open('./data/db.json', 'r') as fileobj:
        blog_posts = json.loads(fileobj.read())
    return blog_posts


@app.route('/')
def index():
    blog_posts = load_json()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        str_title = request.form['title']
        str_author = request.form['author']
        str_content = request.form['content']
        int_id = max(post['id'] for post in load_json()) + 1
        dict_blog = {'id': int_id, 'author': str_author, 'title': str_title, 'content': str_content}
        print(dict_blog)
        save_blog_post(dict_blog)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)