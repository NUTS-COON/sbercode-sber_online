import psycopg2


def save_comment(text, label, mood):
    con = psycopg2.connect(
        database="review_classification",
        user="postgres",
        password="admin",
        host="127.0.0.1",
        port="5432",
        gssencmode='disable'
    )
    cursor = con.cursor()
    cursor.execute("""
    INSERT INTO comment (Text, Label, Mood) 
    VALUES (%s,%s,%s)""", (text, label, mood))
    con.commit()
    con.close()
