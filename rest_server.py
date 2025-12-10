"""
Servidor REST API usando Flask
"""
from flask import Flask, jsonify
from flask_cors import CORS
from data import (
    get_user_by_id,
    get_posts_by_user_id,
    get_comments_by_post_id,
    get_all_users,
    USERS,
    POSTS
)

app = Flask(__name__)
CORS(app)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna um usuário completo por ID"""
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Retorna todos os posts de um usuário"""
    posts = get_posts_by_user_id(user_id)
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Retorna todos os comentários de um post"""
    comments = get_comments_by_post_id(post_id)
    return jsonify(comments)


@app.route('/api/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários"""
    return jsonify(get_all_users())


@app.route('/api/users/<int:user_id>/full', methods=['GET'])
def get_user_with_posts_and_comments(user_id):
    """
    Endpoint completo que retorna usuário com posts e comentários
    Simula o cenário de dados aninhados do REST
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Buscar posts do usuário
    posts = get_posts_by_user_id(user_id, limit=5)
    
    # Para cada post, buscar comentários
    for post in posts:
        post['comments'] = get_comments_by_post_id(post['id'], limit=3)
    
    # Incluir posts no usuário
    user_with_data = user.copy()
    user_with_data['posts'] = posts
    
    return jsonify(user_with_data)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "REST API"})


if __name__ == '__main__':
    print("Starting REST API server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
