from flask import Flask, render_template, request,redirect,flash
import mysql.connector as m
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = "h3ll0_w0rld223991020209292"
db = m.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='expense_tracker'
)
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/main")
def mainpage():
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date_added DESC")  
    posts=cursor.fetchall()
    return render_template('mainpage.html',posts=posts)


@app.route("/add_new",methods=['GET','POST'])
def add_new():
    if request.method=='POST':
        category=request.form['category']
        content=request.form['content']
        amount=request.form['amount']
        date=request.form['date_added'] 
        errors=[]
        if len(category)>50:
            errors.append("Maximum Length Of The Category Must Be 50 Characters!")
        if len(content)>50:
            errors.append("Maximum Length Of The Content Must Be 50 Characters!")
        if not amount.isdigit(): 
            errors.append("Amount Must Be A Numeric Value!")
        if errors:
            for error in errors:
                flash(error) 
            return render_template('add_new.html',category=category,content=content,amount=amount,date=date)

        cursor = db.cursor()
        category=category[0].upper()+category[1:].lower()
        cursor.execute("INSERT INTO posts (category, content, amount, date_added) VALUES (%s,%s,%s,%s)",
                       (category, content, amount, date))
        db.commit()
        return redirect("/main")

    return render_template('add_new.html')

@app.route('/search',methods=['GET'])
def search():
    query=request.args.get('query', '').strip().lower()
    cursor=db.cursor(dictionary=True)
    input_query=f"%{query}%" 
    sql_query="""
        SELECT * FROM posts
        WHERE category LIKE %s
    """
    input=[input_query]

    months=["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    if query in months:
        sql_query+="OR MONTHNAME(date_added) LIKE %s"
        input.append(f"%{query}%")
    elif len(query.split())==2 and query.split()[1].isdigit():
        month, day=query.split()
        sql_query+="OR MONTHNAME(date_added) LIKE %s AND DAY(date_added)=%s"
        input.append(f"%{month}%")
        input.append(day)
    elif len(query.split())==2 and query.split()[1].isdigit() and len(query.split()[1])==4:
        month, year=query.split()
        sql_query+="OR MONTHNAME(date_added) LIKE %s AND YEAR(date_added)=%s"
        input.append(f"%{month}%")
        input.append(year)

    elif len(query.split())==3 and query.split()[1].isdigit() and query.split()[2].isdigit() and len(query.split()[2])==4:
        month,day,year=query.split()
        sql_query+="OR MONTHNAME(date_added) LIKE %s AND DAY(date_added)=%s AND YEAR(date_added)=%s"
        input.append(f"%{month}%")
        input.append(day)
        input.append(year)
    elif query.isdigit() and len(query)==4:
        sql_query+="OR YEAR(date_added)=%s"
        input.append(query)
    cursor.execute(sql_query,tuple(input))
    search_results=cursor.fetchall()
    return render_template('mainpage.html',posts=search_results)

@app.route("/analysis")
def analysis():
    my=db.cursor()
    my.execute("SELECT * FROM posts")
    posts=my.fetchall()
    return render_template('analysis.html',posts=posts)


@app.route("/delete/<int:id>", methods=['POST'])
def delete_post(id):
    cursor=db.cursor()
    cursor.execute("DELETE FROM posts WHERE id=%s", (id,))
    db.commit()
    return '', 204

@app.route("/update/<int:id>", methods=['GET','POST'])
def update_post(id):
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
    post=cursor.fetchone()

    if request.method=='POST':
        category=request.form['category']
        content=request.form['content']
        amount=request.form['amount']
        date=request.form['date_added']

        cursor=db.cursor()
        category=category[0].upper()+category[1:].lower()
        cursor.execute("""
            UPDATE posts 
            SET category=%s, content=%s, amount=%s, date_added=%s 
            WHERE id=%s """, (category, content, amount, date, id))
        db.commit()
        return redirect("/main")
    return render_template('update.html', post=post)
