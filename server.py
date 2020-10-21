from flask import Flask
import json
from class_query import query
from pprint import pprint 

app = Flask(__name__)

@app.route('/generate/origin=<origin>')
def generate(origin):
    q = query()
    q.run(origin)
    #pprint((json.dumps(q.response_dict, ensure_ascii=False)))
    return((json.dumps(q.response_dict, ensure_ascii=False)))

@app.route('/resolve/city=<city>')
def resolve(city):
    q = query()
    resolve_dict = q.run_city_resolver(city)
    return((json.dumps(resolve_dict, ensure_ascii=False)))

if __name__ == '__main__':
    app.run(debug=True)


#фильтр входных переменных
# обработать исключения