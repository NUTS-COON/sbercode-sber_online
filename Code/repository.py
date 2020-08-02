import pyodbc


def save_comment(text, label, mood):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=.;DATABASE=ReviewClassification;Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("""
    INSERT INTO dbo.Comments (Text, Label, Mood) 
    VALUES (?,?,?)""", text, label, mood)
    cnxn.commit()
