from flask import Flask, render_template, request,redirect
import mysql.connector as m
from datetime import datetime
app = Flask(__name__)
db = m.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='expense_tracker'
)
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/main", methods=['GET'])
def mainpage():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_added DESC")  
    posts = cursor.fetchall()

    
    return render_template('mainpage.html', posts=posts)


@app.route("/add_new", methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        category = request.form['category']
        content = request.form['content']
        amount = request.form['amount']
        date = request.form['date_added'] 

       
        errors = []
        if len(category) > 50:
            errors.append("Category is too long. Maximum length is 50 characters.")
        if len(content) > 50:
            errors.append("Content is too long. Maximum length is 50 characters.")
        if not amount.isdigit(): 
            errors.append("Amount must be a valid integer.")

        if errors:
           
            for error in errors:
                flash(error) 
            return render_template('add_new.html', category=category, content=content, amount=amount, date=date)

       
        cursor = db.cursor()
        category=category[0].upper()+category[1:].lower()
        cursor.execute("INSERT INTO posts (category, content, amount, date_added) VALUES (%s, %s, %s, %s)",
                       (category, content, amount, date))
        db.commit()
        return redirect("/main")

    return render_template('add_new.html')


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM posts 
        WHERE category LIKE %s 
        OR DATE_FORMAT(date_added, '%M %Y') LIKE %s 
        OR YEAR(date_added) = %s
        OR DATE_FORMAT(date_added, '%%M %%d') LIKE %s
    """, (f"%{query}%", f"%{query}%", query, f"%{query}%"))

    search_results = cursor.fetchall()

    return render_template('mainpage.html', posts=search_results)

@app.route("/analysis")
def analysis():
    my=db.cursor()
    my.execute("SELECT * FROM posts")
    posts=my.fetchall()


    return render_template('analysis.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/delete/<int:id>", methods=['POST'])
def delete_post(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    db.commit()
    return '', 204  


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
        category=category[0].upper()+category[1:].lower()
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
