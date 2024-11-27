from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "1": "Alice",
    "2": "Bob",
    "3": "Charlie"
}


posts = [
    {"id": 1, "content": "Hello world!", "author_id": "1"},
    {"id": 2, "content": "Flask is awesome!", "author_id": "2"},
    {"id": 3, "content": "Sorting is tricky!", "author_id": "3"}
]


@app.route('/users', methods=['GET'])
def get_users():
    return users

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    return {"name": users[user_id]}

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    users[len(users) + 1] = data['name']
    return {"message": "User created successfully!"}

@app.route('/posts', methods=['GET'])
def get_posts():
    return posts

@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    post_id = int(post_id)
    for post in posts:
        if post['id'] == post_id:
            return post
    return {"message": "Post not found!"}

@app.route('/posts/sort', methods=['GET'])
def sort_posts():
    """
    Sorts posts by content alphabetically.
    """
    sorted_posts = sorted(posts, key=lambda x: x["content"])
    sorted_posts = sorted(sorted_posts, key=lambda x: -x["id"])
    return jsonify({"sorted_posts": sorted_posts})

@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    posts.append({"id": len(posts) + 1, "content": data["content"]})
    return {"message": "Post created!"}

@app.route('/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_id = int(post_id)
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            return {"message": "Post deleted"}
    return {"message": "Post not found!"}

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    users[user_id] = data['name']
    return {"message": "User updated!"}

@app.route('/users', methods=['DELETE'])
def delete_users():
    users.clear()
    return {"message": "All users deleted"}


if __name__ == '__main__':
    app.run(debug=True)