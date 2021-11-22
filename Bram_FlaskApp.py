import pandas as pd
from flask import Flask
import Bram_Verkiezingen_functies as verfuncs


uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')

app = Flask(__name__)


@app.route("/" ,methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/landelijke_uitslag", methods=['GET'])
def getLandelijkeUitslag():
    return verfuncs.landelijkeUitslag(uitslagenDF)


@app.route("/uitslag/<gemeente>", methods=['GET'])
def getUitslagGemeente(gemeente):
    return verfuncs.uitslagGemeente(uitslagenDF, gemeente)


@app.route("/rangschikking/", methods=['GET'])
@app.route("/rangschikking/<partij>",methods=['GET'])
def getVolgordeGemeentes(partij=""):
    if partij == "": return "Geef in de url aan van welke partij je de rangschikking wil zien."
    else: return verfuncs.volgordeGemeentes(uitslagenDF, partij)
    

@app.route("/geldig/", methods=['GET'])
def getVolgordePercOngeldig():
    return verfuncs.volgordePercOngeldig(uitslagenDF)


@app.route("/geldig/<gemeente>", methods=['GET'])
def getPercOngeldigGemeente(gemeente):
    return verfuncs.percOngeldigGemeente(uitslagenDF, gemeente)


if __name__ == '__main__':
    app.run(port=8000,debug=True)