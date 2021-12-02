import pandas as pd
from flask import Flask
df = pd.read_csv(r'C:/Users/Braba/Downloads/Uitslag_alle_gemeenten_TK20210317.csv', sep=';')

def stem_stad(stad='Amsterdam'):
    """
    Deze functie returnt een dataframe waarin het aantal stemmen per partij van hoog naar laag staan in een meegegeven gemeente. Amsterdam is default.
    """
    df_stemmen = df[list(df.columns[10:])] #slice van df met alleen partij kolommen
    gemeente = df[df['RegioNaam'] == stad].index[0] #index van opgegeven stad
    stemmen_per_gemeente = df_stemmen.loc[gemeente] # de rij
    data = {'GeldigeStemmen': stemmen_per_gemeente}
    df_top3 = pd.DataFrame(data).sort_values(['GeldigeStemmen'], ascending=False)[:3] # hoogste3 partijen isoleren uit stadrij
    df_top3.index.name = 'Regio'
    return df_top3


def zetels_per_3_grootste_partijen(stad='Amsterdam'):
    """
    Deze functie berekent het aantal zetels dat de 3 grootste partijen zouden hebben als alleen de stemmen van deze stad meetellen.
    """
    data = stem_stad(stad)
    totaal_stemmen = data['GeldigeStemmen'].sum()
    totaal_zetels = 150
    kiesdeler = totaal_stemmen / totaal_zetels

    grootste_partijen = []
    stemmen_per_partij = {}
    zetels_per_partij = {}
    rest_zetels = {}

    for i in range(0, data["GeldigeStemmen"].size) :
        partij = data.index[i]
        grootste_partijen.append(partij)
        aantal_stemmen = data["GeldigeStemmen"].loc[partij]
        stemmen_per_partij[partij] = aantal_stemmen
        zetels_per_partij[partij] = aantal_stemmen // kiesdeler
        aantal_zetels = zetels_per_partij[partij]
        rest_zetels[partij] = aantal_stemmen / (aantal_zetels + 1)

    while sum(zetels_per_partij.values()) < totaal_zetels:
        hoogste = max(rest_zetels, key=rest_zetels.get)
        zetels_per_partij[hoogste] += 1
        rest_zetels[hoogste] = stemmen_per_partij[hoogste] / (zetels_per_partij[hoogste] +1)

    df_drie_grootste_partijen = pd.DataFrame(data=[grootste_partijen, zetels_per_partij.values()], columns=['grootste', 'tweede', 'derde'])
    return df_drie_grootste_partijen


def landelijke_uitslag_top3():
    """
    Deze functie telt het aantal volledige zetels op per partij die in de top3 van een gemeente zijn geeindigd
    """
    landelijk = {}
    for stad in df["RegioNaam"]:
        df_drie_grootste = zetels_per_3_grootste_partijen(stad)
        for column in df_drie_grootste.columns:
            partij = df_drie_grootste[column].loc[0]
            zetel = df_drie_grootste[column].loc[1] / 355
            if partij in landelijk.keys():
                landelijk[partij] = landelijk[partij] + zetel
            else:
                landelijk[partij] = zetel
                
    data = {"partij": landelijk.keys(), "zetels": landelijk.values()}
    my_df = pd.DataFrame(data).sort_values(["zetels"], ascending=False)
    my_df = my_df.drop(my_df[my_df['zetels'] < 1].index)
    my_df = my_df.astype({'zetels': int})

    # restzetels
    my_df.insert(2, "stemmen per zetel", [0]*len(my_df.index))
    my_df.insert(3, "aantal stemmen", [0]*len(my_df.index))

    for i in range(0, len(my_df.index)):
        index = my_df.index[i]
        partij = my_df["partij"].loc[index]
        aantal_stemmen = df[partij].sum()
        my_df.loc[index, 'aantal stemmen'] = aantal_stemmen
        my_df.loc[index, 'stemmen per zetel'] = aantal_stemmen / (my_df["zetels"][index] +1)              

    while my_df['zetels'].sum() < 150:
        i_max = my_df['stemmen per zetel'].idxmax()
        my_df.loc[i_max, 'zetels'] += 1
        my_df.loc[i_max, 'stemmen per zetel'] = my_df.loc[i_max, 'aantal stemmen'] / (my_df.loc[i_max, 'zetels'] +1)
    return my_df.sort_values(["zetels"], ascending=False)

app = Flask(__name__)

@app.route('/landelijk/top3partijen')
def landelijk_top3_partijen():
    """
    Print de landelijke uitslag op basis vd top 3 partijen.
    """
    return landelijke_uitslag_top3().to_html()

if __name__ == '__main__':
    app.run(port = 8000, debug=True, use_reloader=False)