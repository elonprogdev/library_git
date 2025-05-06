# library_git

Реализовать веб-сайт для управления библиотекой книг, где можно:

1. Добавлять новые книги с названием, автором и категорией.
2. Просматривать список всех книг, с фильтром по категориям.
3. Редактировать и удалять книги.
4. Искать книги по названию или автору.
5. Добавлять новые категории для книг.


- Функционал -

Добавление книги:
   - Форма с полями: название, автор, категория (выпадающий список).
   - После добавления: редирект на главную.

*Доп. задание:
   - После добавления: уведомление "Книга '[Название]' добавлена!"



Список книг:
   - Выводится таблица: Название, Автор, Категория, Действия (Редактировать, Удалить).
   - Фильтр по категориям через выпадающий список.
   - Кнопка "Добавить книгу" ведёт на форму добавления.



Редактирование и удаление:
   - Кнопка "Редактировать" открывает форму с текущими данными книги.
   - После изменения: редирект на страницу со списком книг.
   - Кнопка "Удалить" удаляет книгу. (логично)

*Доп. задание:
   - После удаления: уведомление "Книга '[Название]' удалена!". 



Поиск книг:
   - Поле для ввода запроса на главной странице и отдельной странице поиска.
   - Поиск по названию или автору (регистронезависимый) .
   - Результаты показываются в таблице: Название, Автор, Категория.

*Доп. задание:
   - Если ничего не найдено: уведомление "Ничего не найдено!".



Добавление категории:
   - Форма с полем для названия категории.
   - Если поле пустое: уведомление "Введите название категории!".
   - После добавления: редирект на страницу списка книг.

*Доп. задание:
   - После добавления: уведомление "Категория '[Название]' добавлена!". Как неожиданно, правда?


- Проверки:
  - Нельзя добавить книгу с пустыми полями или несуществующей категорией.
  - Нельзя редактировать/удалить несуществующую книгу.
  - Нельзя добавить категорию с пустым названием.



Структура данных:     *Можно в ООП*

  - books: {id: {"title": str, "author": str, "category_id": int}}
  - categories: {id: {"name": str}}



- Git:
  - Создать репозиторий с веткой main.
  - Для каждой фичи — отдельная ветка.
  - Коммиты с описанием: "Добавлена [фича]".
  - Не сливать ветки.

Либо по своему усмотрению, это не строго, главное грамотное ведение и документирование.

*Пояснение*


Реализуй базовую структуру веб-приложения, а это - таблица со списком книг. Книги можно хранить банально в списке, а в качестве "category" у книги можно для начала хранить лишь строку, название этой категории, а не "category_id". Только лишь после реализации, начать создавать ответвления, ветки по каждой части функциональности. Суть задания в том, чтобы сначала всё реализовать, после чего на уроке слить воедино в основную ветку main. В каждой ветке функциональности/фичи реализовывать лишь её функционал! То есть в ветке "добавления", не должно быть возможности "удаления" книги.

@app.route('/search')
def search():
    query = request.args.get("q", "").strip().lower()
    results = {}
    if query:
        for id, book in books.items():
            if query in book["title"].lower() or query in book["author"].lower():
                results[id] = book
    return render_template("search.html", query=query, results=results, categories=categories)

    @app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = books.get(book_id)
    if not book:
        flash("Книга не найдена.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        category_id = int(request.form['category_id'])

        book['title'] = title
        book['author'] = author
        book['category_id'] = category_id

        flash(f"Книга '{title}' обновлена!")
        return redirect(url_for('index'))

    return render_template("edit_book.html", book=book, book_id=book_id, categories=categories)

    @app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = books.pop(book_id, None)
    if book:
        flash(f"Книга '{book['title']}' удалена!")
    else:
        flash("Книга не найдена.")
    return redirect(url_for('index'))


    @app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        if not name:
            flash("Введите название категории!")
            return redirect(url_for('add_category'))

        # Проверим, нет ли уже такой категории
        if any(cat["name"].lower() == name.lower() for cat in categories.values()):
            flash(f"Категория '{name}' уже существует!")
            return redirect(url_for('add_category'))

        new_id = max(categories.keys(), default=0) + 1
        categories[new_id] = {"name": name}
        flash(f"Категория '{name}' добавлена!")
        return redirect(url_for('index'))

    return render_template("add_category.html")


    <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Добавить категорию</title>
</head>
<body>
    <h2>Добавить категорию</h2>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: green;">
          {% for msg in messages %}
            <li>{{ msg }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <form method="post">
        <label>Название категории:</label><br>
        <input type="text" name="name" required><br><br>

        <button type="submit">Сохранить</button>
        <a href="{{ url_for('index') }}"><button type="button">Отмена</button></a>
    </form>
</body>
</html>