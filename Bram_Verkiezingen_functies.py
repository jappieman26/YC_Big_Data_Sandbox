import pandas as pd
import numpy as np


def landelijkeUitslag(uitslagenDF):

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
    
    # toekenning restzetels
    restzetels = 150 - zetelsDF['aantal zetels'].sum()
    zetelsDF['stemmen per zetel'] = zetelsDF['totaal aantal stemmen'] / (zetelsDF['aantal zetels'] + 1)
    zetelsDF['stemmen per zetel'] = pd.to_numeric(zetelsDF['stemmen per zetel'])
    
    while restzetels > 0:
        imax = zetelsDF['stemmen per zetel'].idxmax() # index (partijnaam) van hoogste aantal stemmen per zetel
        zetelsDF.loc[imax, 'aantal zetels'] += 1
        zetelsDF.loc[imax, 'stemmen per zetel'] = zetelsDF.loc[imax, 'totaal aantal stemmen'] / (zetelsDF.loc[imax, 'aantal zetels'] + 1)
        restzetels -= 1
    
    zetelsDF = zetelsDF.drop('stemmen per zetel', axis=1)
    
    zetelTabel = zetelsDF.to_html()
    
    return "<h2>Landelijke uitslag Tweede Kamerverkiezingen 2021</h2>" + zetelTabel


# Rangschikking van gemeentes op basis van aan stemmen voor partij
def volgordeGemeentes(uitslagenDF, partij):
    
    partijnaam = ""
    naamFound = False
    
    for volnaam in uitslagenDF.columns[10:]:
        if partij in volnaam:
            partijnaam = volnaam
            naamFound = True
            
    if not naamFound:
        return "De partijnaam wordt niet herkend!"
    
    else:
        partijDF = pd.DataFrame(data=list(uitslagenDF[partijnaam]), columns=['aantal stemmen'],
                                index=list(uitslagenDF['RegioNaam']))
        sortedPartijDF = partijDF.sort_values(by='aantal stemmen', ascending=False)
        #sortedPartijDF = sortedPartijDF.astype(int)
        
        sortedPartijTabel = sortedPartijDF.to_html()
        
        return "<h2>Rangschikking gemeentes naar aantal stemmen op " + partij + "</h2>" + sortedPartijTabel
    
    
# Rangschikking gemeentes op basis van percentage ongeldige stemmen    
def volgordePercOngeldig(uitslagenDF):
    
    ongeldigPercList = list(uitslagenDF['OngeldigeStemmen']/uitslagenDF['Opkomst']*100)
    blancoPercList = list(uitslagenDF['BlancoStemmen']/uitslagenDF['Opkomst']*100)
    
    geldigDF = pd.DataFrame(data={'Ongeldige stemmen (%)' : ongeldigPercList,
                                  'Blanco stemmen (%)' : blancoPercList}, index=list(uitslagenDF['RegioNaam']))
    
    sortedGeldigDF = geldigDF.sort_values(by='Ongeldige stemmen (%)')
    sortedGeldigTabel = sortedGeldigDF.to_html()
    
    return "<h2>Rangschikking gemeentes naar ongeldige stemmen als percentage van de totale opkomst</h2>" + sortedGeldigTabel


# Percentage ongeldige en blanco stemmen voor een bepaalde gemeente
def percOngeldigGemeente(uitslagenDF, gemeente):
    
    if gemeente in list(uitslagenDF['RegioNaam']):
        gemeenteIdx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
        percOngeldig = uitslagenDF.loc[gemeenteIdx, 'OngeldigeStemmen'] / uitslagenDF.loc[gemeenteIdx, 'Opkomst'] * 100
        percBlanco = uitslagenDF.loc[gemeenteIdx, 'BlancoStemmen'] / uitslagenDF.loc[gemeenteIdx, 'Opkomst'] * 100
        
        return ("<h2>Ongeldige en blanco stemmen als percentage van de totale opkomst in " + gemeente + "</h2>" +
                "Percentage ongeldig: " + str(percOngeldig) + "<br>" + "Percentage blanco: " + str(percBlanco))
        
    else:
        return "De gemeentenaam wordt niet herkend!"
    
    
# Rangschikking van uitslag in een bepaalde gemeente    
def uitslagGemeente(uitslagenDF, gemeente):
    
    if gemeente in list(uitslagenDF['RegioNaam']):
        
        gemeenteIdx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
        gemeenteDF = pd.DataFrame(data=list(uitslagenDF.loc[gemeenteIdx, uitslagenDF.columns[10:]]),
                                  columns=['aantal stemmen'], index=list(uitslagenDF.columns[10:]))
        sortedGemeenteDF = gemeenteDF.sort_values(by='aantal stemmen', ascending=False,
                                                  key = replaceNaN(gemeenteDF['aantal stemmen']))
        sortedGemeenteDF = sortedGemeenteDF.astype(int)
        sortedGemeenteTabel = sortedGemeenteDF.to_html()
        return "<h2>De gesorteerde uitslag in " + gemeente + "</h2>" + sortedGemeenteTabel
        
    else:
        return "De gemeentenaam wordt niet herkend!"
    

def replaceNaN(ser):
    for i in ser.index:
        if np.isnan(ser[i]):
            ser[i] = 0