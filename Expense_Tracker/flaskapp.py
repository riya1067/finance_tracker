from flask import Flask, render_template, request, redirect
import mysql.connector as m
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL database
db = m.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='expense_tracker'
)

# Homepage route
@app.route("/")
def homepage():
    return render_template('homepage.html')

# Main page route to display expenses
@app.route("/main", methods=['GET'])
def mainpage():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_added DESC")  # Order by date_added descending
    posts = cursor.fetchall()

    # Render the main page with all posts
    return render_template('mainpage.html', posts=posts)

# Add new expense route (GET and POST)
@app.route("/add_new", methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        category = request.form['category']
        content = request.form['content']
        amount = request.form['amount']
        date = request.form['date_added']  # Changed to 'date' to match the form

        # Validation
        errors = []
        if len(category) > 50:
            errors.append("Category is too long. Maximum length is 50 characters.")
        if len(content) > 50:
            errors.append("Content is too long. Maximum length is 50 characters.")
        if not amount.isdigit():  # Check if amount is an integer
            errors.append("Amount must be a valid integer.")

        if errors:
            # Display errors and repopulate the form
            for error in errors:
                flash(error)  # Use Flask's flash messaging system
            return render_template('add_new.html', category=category, content=content, amount=amount, date=date)

        # If no errors, insert the data into the database
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (category, content, amount, date_added) VALUES (%s, %s, %s, %s)",
                       (category, content, amount, date))
        db.commit()
        return redirect("/main")

    return render_template('add_new.html')

# Search route (for category or date)
@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    cursor = db.cursor(dictionary=True)

    # Adjust the query to perform a case-insensitive search and include year match
    cursor.execute("""
        SELECT * FROM posts 
        WHERE category LIKE %s 
        OR DATE_FORMAT(date_added, '%M %Y') LIKE %s 
        OR YEAR(date_added) = %s
    """, (f"%{query}%", f"%{query}%", query))

    search_results = cursor.fetchall()

    # Render the main page with search results
    return render_template('mainpage.html', posts=search_results)

# Analysis and About page routes
@app.route("/analysis")
def analysis():
    print("This is the analysis page")

@app.route("/about")
def about():
    return render_template('about.html')
# Route to delete a post
@app.route("/delete/<int:id>", methods=['POST'])
def delete_post(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    db.commit()
    return '', 204  # Return no content response to indicate success

# Route to update a post (GET and POST)
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update_post(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    if request.method == 'POST':
        category = request.form['category']
        content = request.form['content']
        amount = request.form['amount']
        date = request.form['date_added']

        cursor = db.cursor()
        cursor.execute("""
            UPDATE posts 
            SET category = %s, content = %s, amount = %s, date_added = %s 
            WHERE id = %s
        """, (category, content, amount, date, id))
        db.commit()

        return redirect("/main")

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
