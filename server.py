from flask import Flask
from class_query import query

app = Flask(__name__)

@app.route('/')
def generate():
    q = query('LED')
    q.run()
    return(q.response_dict)