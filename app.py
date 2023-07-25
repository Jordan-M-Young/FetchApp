from flask import Flask, jsonify, request
from modules.html_process import *
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from modules.ner import *
from modules.figures import *
from modules.db import start_db
import sqlite3

# initialize flask app
app = Flask(__name__)

# load huggingface models
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)
start_db()




@app.route("/process",methods=['POST'])
def process():
    """API endpoint used to parse html, extract relevant information,
    and save collected data to database. To use:

    curl -X POST http://localhost:5000/process -H "Content-Type: application/json" -d '{"filename":"dummy_order.html"}'

    to use endpoint. 

    
    """


    # open connection to sqlite db
    conn = sqlite3.connect("dummyDB.db")
    cur = conn.cursor()


    # get filepath from request data
    filepath = request.get_json()['filename']

    #check database for record of 
    res = cur.execute("SELECT * FROM emails WHERE file=?",(filepath,))

    # end early if no data exists for your requested file
    record = res.fetchone()
    if not record:
        return jsonify({})
    

    # cast record to list
    data = list(record)

    # parse html contained in record
    handler = HtmlHandler(raw_html=data[2])

    # html text as string and list of strings
    text = handler.html_text
    lines = handler.text_lines

    # get receipt total and subtotal
    figures = get_figures(lines)


    # exxtract entities (company and purchasing customer)
    ner_results = nlp(text)
    combined_results = combine_results(ner_results)
    entities = get_relevant_entities(combined_results)



    # update database with new data
    update_data = (
        entities['customer'],
        entities['company'],
        figures['total'],
        figures['subtotal'],
        data[1],
    )


    cur.execute("UPDATE emails SET customer=?, company=?, total=?, sub_total=? WHERE file=?",update_data)
    conn.commit()

    # close database connection
    cur.close()
    conn.close()

    return jsonify(update_data)


@app.route("/check",methods=['POST'])
def check():
    """Basic method used to check if database has been updated via the process endpoint run

    curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"filename":"dummy_order.html"}'

    to use endpoint. 

    """

    conn = sqlite3.connect("dummyDB.db")
    cur = conn.cursor()


    filepath = request.get_json()['filename']


    res = cur.execute("SELECT * FROM emails WHERE file=?",(filepath,))

    data = list(res.fetchone())



    return jsonify(data)