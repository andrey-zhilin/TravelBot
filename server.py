from flask import Flask
import json
from class_query import query
from pprint import pprint 

app = Flask(__name__)

@app.route('/generate/<origin>')
def generate(origin):
    q = query(origin)
    q.run()
    pprint((json.dumps(q.response_dict, ensure_ascii=False)))

    return((json.dumps(q.response_dict, ensure_ascii=False)))

if __name__ == '__main__':
    app.run(debug=True)


#фильтр входных переменных
# обработать исключения