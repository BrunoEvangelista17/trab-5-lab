"""
Módulo de dados simulados para o experimento GraphQL vs REST
"""

# Base de dados simulada
USERS = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "city": "New York",
        "country": "USA"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "age": 35,
        "city": "London",
        "country": "UK"
    },
    {
        "id": 3,
        "name": "Carol White",
        "email": "carol@example.com",
        "age": 42,
        "city": "Toronto",
        "country": "Canada"
    },
    {
        "id": 4,
        "name": "David Brown",
        "email": "david@example.com",
        "age": 31,
        "city": "Sydney",
        "country": "Australia"
    },
    {
        "id": 5,
        "name": "Eve Davis",
        "email": "eve@example.com",
        "age": 26,
        "city": "Berlin",
        "country": "Germany"
    }
]

POSTS = [
    {"id": 1, "user_id": 1, "title": "Getting Started with GraphQL", "content": "GraphQL is amazing...", "likes": 42},
    {"id": 2, "user_id": 1, "title": "REST vs GraphQL", "content": "Let's compare...", "likes": 35},
    {"id": 3, "user_id": 1, "title": "API Design Best Practices", "content": "Here are some tips...", "likes": 58},
    {"id": 4, "user_id": 1, "title": "Microservices Architecture", "content": "Breaking down monoliths...", "likes": 67},
    {"id": 5, "user_id": 1, "title": "Database Optimization", "content": "Speed up your queries...", "likes": 44},
    {"id": 6, "user_id": 2, "title": "Python for Beginners", "content": "Start your journey...", "likes": 91},
    {"id": 7, "user_id": 2, "title": "Advanced Python Techniques", "content": "Level up your skills...", "likes": 73},
    {"id": 8, "user_id": 2, "title": "Testing in Python", "content": "Write better tests...", "likes": 52},
    {"id": 9, "user_id": 2, "title": "Async Programming", "content": "Master async/await...", "likes": 65},
    {"id": 10, "user_id": 2, "title": "Data Science with Python", "content": "Analyze your data...", "likes": 88},
    {"id": 11, "user_id": 3, "title": "Web Security Fundamentals", "content": "Protect your apps...", "likes": 102},
    {"id": 12, "user_id": 3, "title": "OAuth 2.0 Explained", "content": "Authentication done right...", "likes": 76},
    {"id": 13, "user_id": 3, "title": "DevOps Best Practices", "content": "CI/CD pipelines...", "likes": 84},
    {"id": 14, "user_id": 3, "title": "Docker for Developers", "content": "Containerize everything...", "likes": 95},
    {"id": 15, "user_id": 3, "title": "Kubernetes Basics", "content": "Orchestrate your containers...", "likes": 71},
    {"id": 16, "user_id": 4, "title": "React Hooks Deep Dive", "content": "Modern React patterns...", "likes": 108},
    {"id": 17, "user_id": 4, "title": "State Management in React", "content": "Redux vs Context...", "likes": 93},
    {"id": 18, "user_id": 4, "title": "TypeScript for React", "content": "Type safety matters...", "likes": 87},
    {"id": 19, "user_id": 4, "title": "Next.js Guide", "content": "Server-side rendering...", "likes": 79},
    {"id": 20, "user_id": 4, "title": "Frontend Performance", "content": "Optimize your apps...", "likes": 61},
    {"id": 21, "user_id": 5, "title": "Machine Learning Intro", "content": "AI for everyone...", "likes": 134},
    {"id": 22, "user_id": 5, "title": "Neural Networks", "content": "Deep learning basics...", "likes": 112},
    {"id": 23, "user_id": 5, "title": "Natural Language Processing", "content": "Text analysis...", "likes": 98},
    {"id": 24, "user_id": 5, "title": "Computer Vision", "content": "Image recognition...", "likes": 105},
    {"id": 25, "user_id": 5, "title": "AI Ethics", "content": "Responsible AI...", "likes": 89},
]

COMMENTS = [
    {"id": i, "post_id": (i % 25) + 1, "author": f"User{i % 10}", "text": f"Great post! Comment {i}"}
    for i in range(1, 101)
]


def get_user_by_id(user_id):
    """Retorna um usuário por ID"""
    return next((user for user in USERS if user["id"] == user_id), None)


def get_posts_by_user_id(user_id, limit=None):
    """Retorna posts de um usuário"""
    posts = [post for post in POSTS if post["user_id"] == user_id]
    if limit:
        posts = posts[:limit]
    return posts


def get_comments_by_post_id(post_id, limit=None):
    """Retorna comentários de um post"""
    comments = [comment for comment in COMMENTS if comment["post_id"] == post_id]
    if limit:
        comments = comments[:limit]
    return comments


def get_all_users():
    """Retorna todos os usuários"""
    return USERS
