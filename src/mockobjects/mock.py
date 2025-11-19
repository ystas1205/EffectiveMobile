from typing import Dict, Any

products_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Laptop", "price": 1000.0, "category": "Electronics"},
    2: {"id": 2, "name": "Book", "price": 20.0, "category": "Education"},
    3: {"id": 3, "name": "Phone", "price": 500.0, "category": "Electronics"},
    4: {"id": 4, "name": "Chair", "price": 150.0, "category": "Furniture"},
    5: {"id": 5, "name": "Notebook", "price": 5.0, "category": "Education"}
}


posts_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "title": "First Post", "content": "This is a sample post.", "author": "user1"},
    2: {"id": 2, "title": "Second Post", "content": "Another example.", "author": "admin"},
    3: {"id": 3, "title": "Third Post", "content": "Discussing tech trends.", "author": "user2"},
    4: {"id": 4, "title": "Fourth Post", "content": "A guide to productivity.", "author": "admin"},
    5: {"id": 5, "title": "Fifth Post", "content": "Random thoughts on life.", "author": "user1"}
}