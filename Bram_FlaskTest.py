import Bram_Zetelberekening_Tweede_Kamer_2021 as zet
import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route("/",methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test",methods=['GET'])
def test():
    zetelTabel = zet.zetelsDF.to_html()
    return zetelTabel

if __name__ == '__main__':
    app.run(port=8000,debug=True)