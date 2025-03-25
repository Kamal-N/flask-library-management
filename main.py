from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from forms import RegisterForm, LogInForm, SearchForm, EditBookForm
from flask import request
import json
import requests
from datetime import datetime

app = Flask('__name__')
app.secret_key = '23hriu23hf9u32903uf2j3ihr823ho1h21l'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

# Put your api key below in order for the app to work
GOOGLE_API_KEY = ""

login_manager = LoginManager()
login_manager.init_app(app)

from db_models import User, Book, Borrow, db
db.init_app(app)

with app.app_context():
    db.create_all()

def check_overdue():
    records = list(db.session.execute(db.select(Borrow).where(Borrow.user_id == current_user.id, Borrow.returned == False)).scalars())
    for record in records:
        due_date = datetime.strptime(record.due_date, '%d-%B-%Y').date()
        if datetime.now().date() > due_date:
            record.status = 'overdue'
            db.session.commit()

    for record in records:
        if record.status == 'overdue':
            return True

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            full_name=request.form["full_name"],
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login", id=user.id))
        # return "Success"
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.username == request.form["username"])).scalar()
        if user:
            if request.form["password"] == user.password:
                # if user.username == 'admin':
                login_user(user)
                if check_overdue():
                    flash(f'You have one or more overdue books.', 'error')
                return redirect(url_for("show_books"))
            else:
                flash("Uh Oh! Wrong password", 'error')
        else:
            flash("There is no user with this username", 'error')
            # return "There is no user with this username"
    return render_template("login.html", form=form)

@app.route('/users')
@login_required
def dashboard():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("dashboard.html", users=users)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched_text = request.form["query"]
        query = '+'.join(searched_text.split())
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_API_KEY}')
        data = response.json()
        print(data)
        book_list = []
        if data.get('items'):
            for item in data['items']:
                try:
                    book_dict = {
                        'title': item['volumeInfo']['title'],
                        'author_list': ', '.join(item['volumeInfo']['authors']),
                        'publisher': item['volumeInfo']['publisher'],
                        'published_date': item['volumeInfo']['publishedDate'],
                        'description': item['volumeInfo']['description'],
                        'page_count': item['volumeInfo']['pageCount'],
                        'img_url': item['volumeInfo']['imageLinks']['thumbnail'],
                        'language': item['volumeInfo']['language'],
                        'isbn': item['volumeInfo']['industryIdentifiers'][0]['identifier'],
                    }
                except KeyError:
                    continue
                book_list.append(book_dict)
        else:
            return "Couldn't find the book"
        return render_template("results.html", books=book_list, json=json)
    return render_template("search.html", form=form)

@app.route('/import/<kwargs>', methods=['GET', 'POST'])
@login_required
def import_book(kwargs):
    kwargs = json.loads(kwargs)
    book = Book(
        title=kwargs['title'],
        author_name=kwargs['authors'],
        description=kwargs['description'],
        cover_url=kwargs['cover_url'].replace("_$_", "/"),
        language=kwargs['language'],
        page_count=kwargs['page_count'],
        publisher=kwargs['publisher'],
        published_date=kwargs['published_date'],
        isbn=kwargs['isbn'],
    )
    db.session.add(book)
    db.session.commit()
    flash(f'Book added successfully', 'success')
    return redirect(url_for("show_books"))

@app.route('/books')
@login_required
def show_books():
    # return render_template("books.html")
    books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    return render_template("books.html", books=books)

@app.route('/book/<id>') # Route To Show Individual Book
@login_required
def book_preview(id):
    book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    return render_template('book_preview.html', book=book)

@app.route('/profile')
@login_required
def user_profile():
    return render_template('profile.html')

@app.route('/borrow_book/<book_id>')
@login_required
def borrow_book(book_id):
    try:
        user = db.get_or_404(User, current_user.id)
        book = db.get_or_404(Book, book_id)
        borrow = Borrow()
        borrow.book = book
        user.borrowed_book.append(borrow)
        db.session.add(borrow)
        book.copies_available = book.copies_available - 1
        book.total_borrowed = book.total_borrowed + 1
        db.session.commit()
        flash("You successfully borrowed this book.", "success")
        return redirect(url_for("book_preview", id=book_id))
    except IntegrityError:
        db.session.rollback()
        flash("You already borrowed this book and didn't returned it!", "error")
        return redirect(url_for("book_preview", id=book_id))


@app.route('/edit_book/<book_id>', methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    book = db.get_or_404(Book, book_id)
    form = EditBookForm()
    form.title.data = book.title
    form.author_name.data = book.author_name
    form.cover.data = book.cover_url
    form.page_count.data = book.page_count
    form.language.data = book.language
    form.isbn.data = book.isbn
    form.publisher.data = book.publisher
    form.published_date.data = book.published_date
    form.description.data = book.description

    if form.validate_on_submit():
        book.title = request.form["title"]
        book.cover_url = request.form["cover"]
        book.author_name = request.form["author_name"]
        book.page_count = request.form["page_count"]
        book.language = request.form["language"]
        book.isbn = request.form["isbn"]
        book.publisher = request.form["publisher"]
        book.published_date = request.form["published_date"]
        book.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("show_books"))
    return render_template('edit_book.html', form=form)

@app.route('/delete_book/<book_id>')
@login_required
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("show_books"))

@app.route('/delete_user/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route('/borrowed_books')
@login_required
def show_borrows():
    if current_user.role == "admin":
        all_detail = db.session.execute(db.select(Borrow, User, Book).join(User).join(Book)).all()
        return render_template("borrowed_books.html", data=all_detail)
    else:
        all_detail = db.session.execute(db.select(Borrow, User, Book).join(User).join(Book).where(Borrow.user_id == current_user.id)).all()
        return render_template("borrowed_books.html", data=all_detail)

@app.route('/edit_profile', methods=["POST", "GET"])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Retrieve the selected avatar and bio from the form
        selected_avatar = request.form['selected-avatar']
        bio = request.form['bio']
        current_user.profile_url = f"../static/img/{selected_avatar}"
        if bio:
            current_user.bio = bio
        db.session.commit()

        # Retrieve other user data from the session (if needed)
        # full_name = session.get('full_name')
        # username = session.get('username')

        return redirect(url_for('user_profile'))
    return render_template('edit_profile.html')

@app.route('/return/<book_id>')
@login_required
def return_book(book_id):
    book = db.session.execute(db.select(Borrow).where(Borrow.user_id == current_user.id, Borrow.book_id == book_id)).scalar()
    book.status = "pending return"
    db.session.commit()
    flash("Please wait for an admin to approve your book return.", "success")
    return redirect(url_for('show_borrows'))

@app.route('/submit_return/<user_id>/<book_id>', methods=['GET', 'POST'])
@login_required
def submit_return(user_id, book_id):
    borrow_record = db.session.execute(db.select(Borrow).where(Borrow.user_id == user_id, Borrow.book_id == book_id)).scalar()
    book = db.get_or_404(Book, book_id)
    if not borrow_record.returned:
        borrow_record.returned = True
        borrow_record.returned_date = datetime.now().strftime("%d-%B-%Y")
        book.copies_available = book.copies_available + 1
        db.session.delete(borrow_record)
        db.session.commit()
        flash("Borrow record removed!", "success")
        return redirect(url_for('show_borrows'))
    return "Book is already returned!"

@app.route('/logout')  # Route To Logout
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == int(user_id))).scalar()
    return user

if "__main__" == __name__:
    app.run(debug=True, port=3000)
