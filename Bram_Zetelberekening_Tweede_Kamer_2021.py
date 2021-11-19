import pandas as pd


uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')
uitslagenDF


aantalZetels = 150
totaalStemmen = uitslagenDF['GeldigeStemmen'].sum()
kiesdeler = int(totaalStemmen / aantalZetels + 0.5)


zetelsDF = pd.DataFrame(columns=['totaal aantal stemmen', 'aantal zetels'],
                        index=uitslagenDF.columns[10:])

for partij in uitslagenDF.columns[10:]:
    partijStemmen = int(uitslagenDF[partij].sum())
    zetelsDF.loc[partij, 'totaal aantal stemmen'] = partijStemmen
    
    aantalVolleZetels = int(partijStemmen/kiesdeler)
    if aantalVolleZetels > 0:
        zetelsDF.loc[partij, 'aantal zetels'] = aantalVolleZetels
    else:
        zetelsDF = zetelsDF.drop(partij)
    
zetelsDF.insert(2, 'stemmen per zetel', [0]*len(zetelsDF.index))
zetelsDF


restzetels = 150 - zetelsDF['aantal zetels'].sum()
zetelsDF['stemmen per zetel'] = zetelsDF['totaal aantal stemmen'] / (zetelsDF['aantal zetels'] + 1)
zetelsDF['stemmen per zetel'] = pd.to_numeric(zetelsDF['stemmen per zetel'])

while restzetels > 0:
    imax = zetelsDF['stemmen per zetel'].idxmax() # index (partijnaam) van hoogste aantal stemmen per zetel
    zetelsDF.loc[imax, 'aantal zetels'] += 1
    zetelsDF.loc[imax, 'stemmen per zetel'] = zetelsDF.loc[imax, 'totaal aantal stemmen'] / (zetelsDF.loc[imax, 'aantal zetels'] + 1)
    restzetels -= 1

zetelsDF = zetelsDF.drop('stemmen per zetel', axis=1)