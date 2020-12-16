from flask import Flask, request, render_template
import json, time, os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_url(article_id):
    with psycopg2.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cursor = cur.execute("SELECT url FROM urls WHERE id = %s;", [article_id,])
        url_val = cur.fetchone()[0]
        return url_val
   
def insert_url(url):
    unix_time=int(time.time())
    with psycopg2.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO urls (id,url) VALUES (%s,%s);", (unix_time,url))
        con.commit()
        
def get_all_data():
    with psycopg2.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cursor = cur.execute("SELECT * FROM urls;")
        url_val = cur.fetchall()
        print(f"url_val: {url_val}")
        return url_val

"""
def latest_article():
    unix_time=int(time.time())
    with psycopg2.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO urls (id,url) VALUES (?,?)", (unix_time,url))
        con.commit()
"""      
      
@app.route("/post_url", methods=['POST'])
def post_new_url():
    if request.method == 'POST':
        url = request.form['url']       
        insert_url(url)
        return f"Done with post request from: {url}"

@app.route("/api/article/<int:id>", methods=['GET'])
def get_article_by_id(id):
    if request.method == 'GET':        
        return str(get_url(id))

@app.route("/api/article/all", methods=['GET'])
def get_all_articles():
    if request.method == 'GET':        
        return str(get_all_data())
       
"""
@app.route("/api/article/latest-article", methods=['GET'])
def get_article_by_id():
    if request.method == 'GET':        
        return f'<div>{latest_article()}</div>'        
"""

@app.route("/")
def home():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
    