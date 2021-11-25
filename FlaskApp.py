import pandas as pd
from flask import Flask
import Bram_Verkiezingen_functies as verfuncs


# Het DataFrame met de stemmen inladen, en de tweede instantie van de dubbele
# regionaam (Bergen) vervangen door Bergen NH
uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')
bergen2 = uitslagenDF[uitslagenDF['RegioCode']=='G0373'].copy()
bergen2_idx = uitslagenDF[uitslagenDF['RegioCode']=='G0373'].index[0]
bergen2.loc[bergen2_idx, 'RegioNaam'] = 'Bergen NH'
uitslagenDF = uitslagenDF.where(~uitslagenDF.duplicated(subset=['RegioNaam']), other=bergen2)


app = Flask(__name__)


@app.route("/" , methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/landelijke_uitslag/", methods=['GET'])
def get_landelijke_uitslag():
    return verfuncs.landelijke_uitslag(uitslagenDF)


@app.route("/gemeente/uitslag/", methods=['GET'])
@app.route("/gemeente/uitslag/<gemeente>", methods=['GET'])
def get_uitslag_gemeente(gemeente=""):
    if gemeente == "": return "Geef in de url aan van welke gemeente je de uitslag wil zien."
    else: return verfuncs.uitslag_gemeente(uitslagenDF, gemeente)


@app.route("/gemeente/geldig/", methods=['GET'])
def get_volgorde_perc_ongeldig():
    return verfuncs.volgorde_perc_ongeldig(uitslagenDF)


@app.route("/gemeente/geldig/<gemeente>", methods=['GET'])
def get_perc_ongeldig_gemeente(gemeente):
    return verfuncs.perc_ongeldig_gemeente(uitslagenDF, gemeente)


@app.route("/partij/rangschikking/", methods=['GET'])
@app.route("/partij/rangschikking/<partij>",methods=['GET'])
def get_volgorde_gemeentes(partij=""):
    if partij == "": return "Geef in de url aan van welke partij je de rangschikking wil zien."
    else: return verfuncs.volgorde_gemeentes(uitslagenDF, partij)


if __name__ == '__main__':
    app.run(port=8000,debug=True)