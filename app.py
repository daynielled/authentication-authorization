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

        session["user_id"] = user.id

        flash('Registration successful! Welcome!')

        return redirect('/secret')
     
     else:
        return render_template('register.html', form=form)
     

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username, pwd)

        if user:
          session["user_id"] = user.id  # keep logged in
          return redirect("/secret")
        
        else:
            form.username.errors = ["Incorrect username and/or password"]

    return render_template("login.html", form=form)
  


@app.route('/users/<username>')
def user_profile(username):
    """Displays information about the current user"""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        return render_template("user_profile.html", user=user)
    else:
        flash('User not found', 'danger')
        return redirect('/')
     

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")





if __name__ == '__main__':
    # This block ensures that the database tables are created when you run the script
     db.create_all()
     app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5100)