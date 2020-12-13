from flask import Flask, request, render_template
import json, time, os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_url(article_id):
    with sql.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cursor = cur.execute("SELECT url FROM urls WHERE id = ?", (article_id,))
        url_val = cursor.fetchone()[0]
        return url_val
   
def insert_url(url):
    unix_time=int(time.time())
    with sql.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO urls (id,url) VALUES (?,?)", (unix_time,url))
        con.commit()

"""
def latest_article():
    unix_time=int(time.time())
    with sql.connect(DATABASE_URL) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO urls (id,url) VALUES (?,?)", (unix_time,url))
        con.commit()
"""      
      
@app.route("/post_url", methods=['POST'])
def post_new_url():
    if request.method == 'POST':
        url = request.form['url']       
        insert_url(url)
        return "Done"

@app.route("/api/article/<int:id>", methods=['GET'])
def get_article_by_id(id):
    if request.method == 'GET':        
        return str(get_url(id))

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