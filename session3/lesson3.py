from fastapi import FastAPI
app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Tran Van B",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available": True
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2023,
        "is_available": True
    }
]

@app.get("/books/statistics")
def get_statistics_book():
    total_book = len(books)
    available_book = len([book for book in books if book["is_available"] == True])
    borrowed_book = len([book for book in books if book["is_available"] == False])
    
    return {
        "total_book": total_book,
        "available_book": available_book,
        "borrowed_book": borrowed_book
    }
    
@app.get("/books/categories")
def get_categories():
    category = []
    for book in books:
        if book["category"] not in category:
            category.append(book["category"])
    return {
        "category": category
    }
    
@app.get("/books/latest")
def get_lastest_book():
    if not books:
        return {
            "message": "No books available"
        }
    
    lastest_book = books[0]
    for book in books:
        if book["year"] > lastest_book["year"]:
            lastest_book = book
                
    return {
        "lastest_book": lastest_book
    }