from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'


class Add_Books(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    rating = DecimalField(label='Rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    submit = SubmitField(label='Submit')
    
class Edit_Rating(FlaskForm):
    new_rating = DecimalField(label='Rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    submit = SubmitField(label='Submit')



# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Books model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incremented ID
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', data=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = Add_Books()
    if add_form.validate_on_submit():
        new_book = Book(title=add_form.book_name.data, author=add_form.book_author.data, rating=add_form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=add_form)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    edit_form = Edit_Rating()
    book_to_update = Book.query.get(id)
    if edit_form.validate_on_submit():
        book_to_update.rating = edit_form.new_rating.data
        db.session.commit()  
        return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form, book=book_to_update)

@app.route("/delete/<int:id>")
def delete(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

