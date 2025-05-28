from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)


def save_blog_post(dict_post):
    """Adds a new blog post to the list"""
    blog_posts = load_json()
    blog_posts.append(dict_post)
    save_json(blog_posts)


def save_json(blog_posts):
    """saves the blogs the a JSON file"""
    with open('./data/db.json', 'w', encoding='utf-8') as fileobj:
        json.dump(blog_posts, fileobj)


def load_json():
    """loads blog posts from JSON file"""
    with open('./data/db.json', 'r', encoding='utf-8') as fileobj:
        blog_posts = json.loads(fileobj.read())
    return blog_posts


def fetch_post_by_id(int_post_id):
    """returns a blog with a specific id."""
    list_blog_posts = load_json()
    return [blog_post for blog_post in list_blog_posts if blog_post['id'] == int_post_id][0]


def remove_post_by_id(int_post_id):
    """removes blog from list with specific id"""
    list_blog_posts = load_json()
    return [blog_post for blog_post in list_blog_posts if blog_post['id'] != int_post_id]


@app.route('/')
def index():
    """renders index.html"""
    blog_posts = load_json()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """manages adding new blog post"""
    if request.method == 'POST':
        str_title = request.form['title']
        str_author = request.form['author']
        str_content = request.form['content']
        if str_title != "" and str_author != "" and str_content != "":
            list_blogs = load_json()
            if len(list_blogs) > 0:
                int_id = max(post['id'] for post in list_blogs) + 1
            else:
                int_id = 1
            dict_blog = {'id': int_id,
                         'author': str_author,
                         'title': str_title,
                         'content': str_content}
            save_blog_post(dict_blog)
            return redirect(url_for('index'))
        return f"Invalid Input. go back here: <a href={url_for('index')}>Homepage<a>", 404
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """manages deleting a blog post."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    blog_posts_new = remove_post_by_id(post_id)
    save_json(blog_posts_new)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods = ['GET','POST'])
def update(post_id):
    """manages updating of a blog post"""
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        str_title = request.form['title']
        str_author = request.form['author']
        str_content = request.form['content']
        if str_title != "" and str_author != "" and str_content != "":
            list_posts_new = remove_post_by_id(post_id)
            dict_blog = {'id': post_id,
                         'author': str_author,
                         'title': str_title,
                         'content': str_content}
            print(dict_blog)
            list_posts_new.append(dict_blog)
            save_json(list_posts_new)
            return redirect(url_for('index'))
        return f"Invalid Input. Go back here: <a href={url_for('index')}>Homepage<a>", 404
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)