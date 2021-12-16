import pandas as pd
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')


def landelijkeUitslag(uitslagenDF):
    






















if __name__ == '__main__':
    app.run(port=8000,debug=True)