from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///critique"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "dee123"

connect_db(app)
db.create_all()

@app.route('/')
def root():
     return redirect('/register')

@app.route('/register')
def show_registration_form():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST'])
def process_registration_form():
     form = RegistrationForm()

     if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email= form.email.data
        first = form.first_name.data
        last = form.last_name.data

        user = User.register(username, pwd, email, first, last)
        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
     
     else:
        return render_template('register.html', form=form)


@app.route('/secret')
def secret():
    return "You made it!"
     






if __name__ == '__main__':
    # This block ensures that the database tables are created when you run the script
     db.create_all()
     app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5100)