from flask import Flask, render_template, request, url_for, redirect, flash


app = Flask(__name__)
app.secret_key = 'my_very_secret_library_key' 

categories = {
    1: {"name": "Фантастика"},
    2: {"name": "Детективы"},
    3: {"name": "Научная литература"},
    4: {"name": "Биографии"},
    5: {"name": "Детская литература"}
}

books = {
    1: {"title": "Дюна", "author": "Фрэнк Герберт", "category_id": 1},
    2: {"title": "Солярис", "author": "Станислав Лем", "category_id": 1},
    3: {"title": "Убийство в Восточном экспрессе", "author": "Агата Кристи", "category_id": 2},
    4: {"title": "Шерлок Холмс: Собрание рассказов", "author": "Артур Конан Дойл", "category_id": 2},
    5: {"title": "Краткая история времени", "author": "Стивен Хокинг", "category_id": 3},
    6: {"title": "Происхождение видов", "author": "Чарльз Дарвин", "category_id": 3},
    7: {"title": "Стив Джобс", "author": "Уолтер Айзексон", "category_id": 4},
    8: {"title": "Дневник Анны Франк", "author": "Анна Франк", "category_id": 4},
    9: {"title": "Малыш и Карлсон", "author": "Астрид Линдгрен", "category_id": 5},
    10: {"title": "Гарри Поттер и философский камень", "author": "Дж. К. Роулинг", "category_id": 5}
}



@app.route('/')
def index():
    selected_category = request.args.get("category", type=int)
    filtered_books = {
        k: v for k, v in books.items()
        if selected_category is None or v["category_id"] == selected_category
    }
    return render_template(
        "index.html",
        books=filtered_books,
        categories=categories,
        selected_category=selected_category
    )
        


if __name__ == "__main__":
    app.run(debug=True)

