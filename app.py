import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask import Response
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import Verkiezingen_functies as verfuncs
import Verkiezingen_grafieken as vergrafs


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



@app.route("/gemeente/list", methods=['GET'])
def get_alle_gemeentes():
    return uitslagenDF['RegioNaam'].to_json()

@app.route("/gemeente/uitslag/", methods=['GET'])
@app.route("/gemeente/uitslag/<gemeente>", methods=['GET'])
def get_uitslag_gemeente(gemeente=""):
    if gemeente == "": return "Geef in de url aan van welke gemeente je de uitslag wil zien."
    elif gemeente in list(uitslagenDF['RegioNaam']):
        return verfuncs.uitslag_gemeente(uitslagenDF, gemeente).to_json()
    else: return "De gemeentenaam wordt niet herkend!", 400


@app.route("/gemeente/geldig/", methods=['GET'])
def get_volgorde_perc_ongeldig():
    return verfuncs.volgorde_perc_ongeldig(uitslagenDF).to_html()


@app.route("/gemeente/geldig/<gemeente>", methods=['GET'])
def get_perc_ongeldig_gemeente(gemeente):
    if gemeente in list(uitslagenDF['RegioNaam']):
        return verfuncs.perc_ongeldig_gemeente(uitslagenDF, gemeente).to_html()
    else: return "De gemeentenaam wordt niet herkend!", 400


@app.route("/gemeente/rangschikking/", methods=['GET'])
@app.route("/gemeente/rangschikking/<partij>",methods=['GET'])
def get_volgorde_gemeentes(partij=""):
    if partij == "": return "Geef in de url aan van welke partij je de rangschikking wil zien."
    else: 
        partijnaam = ""
        naam_found = False
    
        for vol_naam in uitslagenDF.columns[10:]:
          if partij in vol_naam:
                partijnaam = vol_naam
                naam_found = True

        if not naam_found:
            return "De partijnaam wordt niet herkend!", 400
        else:
            return verfuncs.volgorde_gemeentes(uitslagenDF, partijnaam).to_html()


@app.route("/alternatief/gemeente/winnaar")
def get_populairste_per_gemeente():
    return verfuncs.populairste_per_gemeente(uitslagenDF).to_html()

@app.route("/alternatief/gemeente/zetels")
def get_zetels_per_gewonnen_gemeente():
    return verfuncs.zetels_per_gewonnen_gemeente(uitslagenDF).to_html() 


@app.route('/plotten/<optie>')
@app.route('/plotten/2/<n>')
def plot_enkel(optie=2, n=3):
    optie, n = int(optie), int(n)
    opties_dict = {
        1: lambda df, n: verfuncs.landelijke_uitslag(df),
        2: lambda df, n: verfuncs.landelijke_uitslag_top_n(df,n),
        3: lambda df, n: verfuncs.landelijke_uitslag_kiesmannen(df),
        4: lambda df, n: verfuncs.zetels_per_gewonnen_gemeente(df)
    }

    zetelsDF = opties_dict[optie](uitslagenDF, n)
    fig = vergrafs.plot_uitslag(zetelsDF)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plotten_v2/<n1>/<n2>/<optie1>/<optie2>')
def plot_v2(n1, n2, optie1, optie2):
    n1, n2, optie1, optie2 = int(n1), int(n2), int(optie1), int(optie2)
    fig = vergrafs.plot_landelijk_vs_top_n_v2(uitslagenDF, n1, n2, optie1, optie2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(port=8000,debug=True)
