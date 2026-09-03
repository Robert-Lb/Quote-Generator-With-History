import mysql.connector
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'random quotes'
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "db_task4"
)

cursor = db.cursor()

@app.route("/")
def index():
    # 1. Fetch from external API (ZenQuotes API)
    api_url = "https://zenquotes.io/api/random"
    quote_text = "Could not fetch quote."
    author_text = "Unknown"

    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            quote_text = data[0]["q"]
            author_text = data[0]["a"]

            # 2. Log successful fetch to MySQL
            sql_query="INSERT INTO tbl_quotes (quote, author) VALUES (%s, %s)"
            cursor.execute(sql_query, (quote_text, author_text,))
            db.commit()            
        
    except Exception as e:
        print(f"Error occurred: {e}")

    return render_template(
        "index.html", quote=quote_text, author=author_text
    )

@app.route("/history")
def history():
    # Fetch historical logs from database    
    try:        
        cursor.execute("SELECT * FROM tbl_quotes ORDER BY fetched_at DESC LIMIT 20")
        quotes = cursor.fetchall()
        db.commit()        
                                           
    except Exception as e:
        print(f"Database error: {e}")

    return render_template(
        "history.html", quotes=quotes
    )

if __name__ == '__main__':
    app.run(debug=True)