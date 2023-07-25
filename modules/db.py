import sqlite3
from modules.html_process import *
import os

def start_db():
    """starts and (potentially) populates a sqlite database for this app to work off of in a production setting we'd use a
    separate postgres instance but this dummy db works for a dev env
    """

    conn = sqlite3.connect("dummyDB.db")
    cur = conn.cursor()

    file_dir = './DummyData'
    files = ['/'.join([file_dir,file]) for file in os.listdir(file_dir)]

    res = cur.execute("SELECT name FROM sqlite_master WHERE name='emails'")
    if not res.fetchone():
        # create a db schema with the following fields
        cur.execute("CREATE TABLE emails(id, file, html, receipt_status, customer, company, total, sub_total)")
        
        data = []
        for idx, file in enumerate(files):
            handler = HtmlHandler(filepath=file)
            html = handler.raw_html
            data.append((idx, file.split('/')[-1],html,True,'','',0.0,0.0))

        cur.executemany("INSERT INTO emails VALUES(?, ?, ?, ?, ?, ?, ?, ?)",data)

        conn.commit()


    cur.close()
    conn.close()

    
