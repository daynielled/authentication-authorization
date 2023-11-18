from flask import Flask, render_template, redirect, session, flash, url_for
from models import connect_db, db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm
from werkzeug.exceptions import Unauthorized, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///critique"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "dee123"

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
     return redirect('/register')


@app.route('/register', methods=['GET','POST'])
def register():
     """Registration Form- show form and handle its submission"""

     if "username" in session:
        return redirect(f"/users/{session['username']}")
     

     form = RegistrationForm()

     if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email= form.email.data
        first = form.first_name.data
        last = form.last_name.data

        user = User.register(username, pwd, email, first, last)
       
        db.session.commit()
        session["username"] = user.username

        flash('Registration successful! Welcome!')

        return redirect(f"/users/{user.username}")
     
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
          session["username"] = user.username  # keep logged in
          return redirect(f"/users/{user.username}")
        
        else:
            form.username.errors = ["Incorrect username and/or password"]
            return render_template("login.html", form=form)
        
    return render_template("login.html", form=form)
  
@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    if "user_id" in session:
        session.pop("user_id")

    return redirect(url_for("login"))

@app.route('/users/<username>')
def user_profile(username):
    """Displays information about the current user"""

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        abort(401)
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        return render_template("user_profile.html", user=user)
    else:
        flash('User not found', 'danger')
        return redirect('/register')
     
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user from app"""
    if "username" not in session or username != session['username']:
        flash("Unauthorized Access", "danger")
        return redirect("/login")
    
    user = User.query.get(username)

    if not user:
        flash('User not found', 'danger')
        return redirect("/register")
    
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Display a form to add feedback and handle its submission"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()
    feedback = None

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            user_username=session['username'],
        )    

        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback added successfully', 'success')

        return redirect(f"/users/{feedback.user.username}")
    else:
        return render_template('add_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Edit and Update Feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.user.username != session['username']:
       raise Unauthorized()
    

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback updated successfully', 'success')
        return redirect(f"/users/{feedback.user.username}")
    
    return render_template('edit_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.user.username != session['username']:
        flash("Unauthorized Access", "danger")
        return redirect("/login")
    
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully', 'success')

    return redirect(f"/users/{feedback.user.username}")




if __name__ == '__main__':
    # This block ensures that the database tables are created when you run the script
     db.create_all()
     app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5100)