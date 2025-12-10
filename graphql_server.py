"""
Servidor GraphQL usando Graphene e Flask
"""
from flask import Flask
from flask_cors import CORS
import graphene
from graphene import ObjectType, String, Int, List, Field, Schema
from data import (
    get_user_by_id,
    get_posts_by_user_id,
    get_comments_by_post_id,
    get_all_users
)


# Definição dos tipos GraphQL
class Comment(ObjectType):
    id = Int()
    post_id = Int()
    author = String()
    text = String()


class Post(ObjectType):
    id = Int()
    user_id = Int()
    title = String()
    content = String()
    likes = Int()
    comments = List(Comment, limit=Int())

    def resolve_comments(self, info, limit=None):
        return get_comments_by_post_id(self.id, limit)


class User(ObjectType):
    id = Int()
    name = String()
    email = String()
    age = Int()
    city = String()
    country = String()
    posts = List(Post, limit=Int())

    def resolve_posts(self, info, limit=None):
        return [Post(**post) for post in get_posts_by_user_id(self.id, limit)]


# Queries disponíveis
class Query(ObjectType):
    user = Field(User, id=Int(required=True))
    users = List(User)
    
    # Query complexa: usuário com posts e comentários
    user_with_posts = Field(
        User,
        id=Int(required=True),
        posts_limit=Int(default_value=5),
        comments_limit=Int(default_value=3)
    )

    def resolve_user(self, info, id):
        user_data = get_user_by_id(id)
        if user_data:
            return User(**user_data)
        return None

    def resolve_users(self, info):
        return [User(**user) for user in get_all_users()]
    
    def resolve_user_with_posts(self, info, id, posts_limit=5, comments_limit=3):
        user_data = get_user_by_id(id)
        if not user_data:
            return None
        return User(**user_data)


# Schema GraphQL
schema = Schema(query=Query)

# Aplicação Flask
app = Flask(__name__)
CORS(app)


@app.route('/graphql', methods=['POST'])
def graphql_server():
    from flask import request, jsonify
    data = request.get_json()
    
    query = data.get('query')
    variables = data.get('variables')
    
    result = schema.execute(query, variables=variables)
    
    response = {}
    if result.data:
        response['data'] = result.data
    if result.errors:
        response['errors'] = [str(error) for error in result.errors]
    
    return jsonify(response)


@app.route('/health', methods=['GET'])
def health():
    from flask import jsonify
    return jsonify({"status": "ok", "service": "GraphQL API"})


if __name__ == '__main__':
    print("Starting GraphQL API server on http://localhost:5001")
    print("GraphQL endpoint: http://localhost:5001/graphql")
    app.run(host='0.0.0.0', port=5001, debug=False)
