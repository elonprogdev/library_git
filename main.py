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

        
@app.route('/delete/<book_id>')
def delete(book_id):
    book = books.pop(int(book_id), None)
    print(books)
    if book:
        flash(f"Книга '{book['title']}' удалена!")
    else:
        flash("Книга не найдена.")
    return redirect(url_for('index'))



@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        category_id = int(request.form.get('category_id'))

        if title and author and category_id:
            new_id = max(books.keys(), default=0) + 1
            books[new_id] = {
                "title": title,
                "author": author,
                "category_id": category_id
            }
            flash(f"Книга '{title}' добавлена!")
            return redirect(url_for('index'))
        else:
            flash("Пожалуйста, заполните все поля.")

    return render_template("add_book.html", categories=categories)

@app.route('/edit/<int:book_id>', methods=["GET", "POST"])
def edit_book(book_id):
    book = books.get(book_id)
    if not book:
        flash("Книга не найдена.")
        return redirect(url_for('index'))

    if request.method == "POST":
        new_title = request.form["title"].strip()
        new_author = request.form["author"].strip()
        new_category_id = int(request.form["category"])

        book["title"] = new_title
        book["author"] = new_author
        book["category_id"] = new_category_id

        flash(f"Книга '{new_title}' обновлена.")
        return redirect(url_for('index'))

    return render_template("edit.html", book_id=book_id, book=book, categories=categories)


    

if __name__ == "__main__":
    app.run(debug=True)

