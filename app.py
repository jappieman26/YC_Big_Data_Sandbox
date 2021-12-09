import pandas as pd
from flask import Flask
from flask_cors import CORS
import Verkiezingen_functies as verfuncs


# Het DataFrame met de stemmen inladen
uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')


app = Flask(__name__)
CORS(app)


@app.route("/" , methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/landelijke_uitslag/werkelijk", methods=['GET'])
def get_landelijke_uitslag():
    return verfuncs.landelijke_uitslag(uitslagenDF).to_json()


@app.route("/landelijke_uitslag/kiesmannen", methods=['GET'])
def get_landelijke_uitslag_kiesmannen():
    return verfuncs.landelijke_uitslag_kiesmannen(uitslagenDF).to_html()

@app.route('/landelijke_uitslag/top_n_partijen/<aantal>')
def landelijk_top_n_partijen(aantal):
    """
    Print de landelijke uitslag op basis vd top n partijen per gemeente.
    """
    aantal = int(aantal)
    return verfuncs.landelijke_uitslag_top_n(uitslagenDF, aantal).to_html()


@app.route("/gemeente/uitslag/", methods=['GET'])
@app.route("/gemeente/uitslag/<gemeente>", methods=['GET'])
def get_uitslag_gemeente(gemeente=""):
    if gemeente == "": return "Geef in de url aan van welke gemeente je de uitslag wil zien."
    elif gemeente in list(uitslagenDF['RegioNaam']):
        return verfuncs.uitslag_gemeente(uitslagenDF, gemeente).to_html()
    else: return "De gemeentenaam wordt niet herkend!", 400


@app.route("/gemeente/geldig/", methods=['GET'])
def get_volgorde_perc_ongeldig():
    return verfuncs.volgorde_perc_ongeldig(uitslagenDF).to_html()


@app.route("/gemeente/geldig/<gemeente>", methods=['GET'])
def get_perc_ongeldig_gemeente(gemeente):
    if gemeente in list(uitslagenDF['RegioNaam']):
        return verfuncs.perc_ongeldig_gemeente(uitslagenDF, gemeente).to_html()
    else: return "De gemeentenaam wordt niet herkend!", 400


@app.route("/partij/rangschikking/", methods=['GET'])
@app.route("/partij/rangschikking/<partij>",methods=['GET'])
def get_volgorde_gemeentes(partij=""):
    if partij == "": return "Geef in de url aan van welke partij je de rangschikking wil zien."
    else: return verfuncs.volgorde_gemeentes(uitslagenDF, partij).to_html()


@app.route("/alternatief/gemeente/winnaar")
def populairste_per_gemeente():
    return verfuncs.populairste_per_gemeente(uitslagenDF).to_html()

@app.route("/alternatief/gemeente/zetels")
def zetels_per_gewonnen_gemeente():
    return verfuncs.zetels_per_gewonnen_gemeente(uitslagenDF).to_html() 


if __name__ == '__main__':
    app.run(port=8000,debug=True)
