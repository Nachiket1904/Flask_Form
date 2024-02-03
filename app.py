from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import random

app = Flask(__name__)
app.debug = True  # Consider setting to False in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for form submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Submission {self.name}>"

# Home page route
@app.route('/')
def home():
    # Select a random quote
    quotes = [
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Your time is limited, don’t waste it living someone else’s life. - Steve Jobs",
    ]
    random_quote = random.choice(quotes)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = "Sunny, 24°C"  # Example weather information
    return render_template('index.html', current_time=current_time, random_quote=random_quote, weather_info=weather_info)

# Route to handle form submission
@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    new_submission = Submission(
        name=request.form['name'],
        email=request.form['email'],
        contact=request.form['contact'],
        age=request.form['age'],
        message=request.form['message']
    )
    db.session.add(new_submission)
    db.session.commit()
    return redirect(url_for('submissions'))

# Route to display all submissions
@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.order_by(Submission.date_submitted.desc()).all()
    return render_template('submissions.html', submissions=all_submissions)

# Route to delete a submission
@app.route('/delete/<int:id>')
def erase(id):
    submission_to_delete = Submission.query.get_or_404(id)
    db.session.delete(submission_to_delete)
    db.session.commit()
    return redirect(url_for('submissions'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
