# User Setting
from bot_dash import db 
from bot_dash.models import User
import sqlite3 as sql
def db_setting():
    # User DB Setting
    #master=User(id=1,username="master",password="123123",email="dashboard@good.com")
    #db.session.add(master)
    #db.session.commit()
    try:
        con = sql.connect('pybo.db')
        c =  con.cursor() 
        c.execute("insert into User values (?,?,?,?)",(1, "master","123123","dashboard@email.com"))
        con.commit()
        c.close() 
    


    except sql.Error as error:
        print("DB Insert Fail!!",error)
    else:
        print("DB Insert Success!!")