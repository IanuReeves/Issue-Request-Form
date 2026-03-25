'''
Please Read!

I didn't want to notarize the html, so here's the jist:

- form section creates input sections attached to variables
- error correction is done mostly in app.py as explained later, but visual indicator is above submit

I wanted to add a dropdown, but I didn't have enough time


all code and form ideas were by me, however I will mark down where I was influenced by AI through a #*#
'''




# Import required prerequisites
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import re

# config and shortcuts for db and flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# creates a db class with the submitted form's items
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), index=True, unique=False)
    user_email = db.Column(db.String(120), index=True, unique=False)
    issue_description = db.Column(db.String(500), unique=False)

# creates the db in /instance/data.db
with app.app_context():
    db.create_all()

# sets the site directory to home, and allows sending get and post requests
@app.route('/', methods=['GET', 'POST'])
# defines the site by taking the submitted form's items and setting them to variables for later
def home():
    error = None #*# Google's AI overview told me the jist on how error correction could be made
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['user_email']
        bug_description = request.form['bug_description']
        print(user_name, user_email, bug_description)
        if not user_name or not user_email or not bug_description:
            error = 'Please fill out all forms before submitting'
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', user_email): #*# - I used google's ai overview to yoink the formula for this. Sorry if that's not allowed
            error = 'Email does not follow standard notation'
        else:
            new_issue = Issue(
                user_name=user_name,
                user_email=user_email,
                issue_description=bug_description
            )
            db.session.add(new_issue)
            db.session.commit() #*# 
            return redirect(url_for('confirmation')) # redirects user to confirmations page after submission
    # sends the user to the issues page
    return render_template('index.html', error=error)

# sets route for confirmation page after form submission
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# part of template. does it check if the namespace is local?
if __name__ == '__main__':
    app.run(debug=True)