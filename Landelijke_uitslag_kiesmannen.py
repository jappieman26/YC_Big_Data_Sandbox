import pandas as pd
import Verkiezingen_functies as verfuncs


def landelijke_uitslag_kiesmannen(uitslagenDF):
    """
    Bereken de landelijke uitslag van de Tweede Kamerverkiezingen als het aantal zetels wordt uitgebreid naar 1050,
    en elke gemeente op basis van zijn populatie een aantal kiesmannen toegewezen krijgt. De partij die wint in een
    gemeente krijgt alle kiesmannen. Return een string met de uitslag in een html-tabel.
    """
    # Moet gelijk of hoger zijn aan het aantal gemeenten (355)
    aantal_zetels = 1050
    
    # Toewijzing kiesmannen
    # Elke gemeente krijgt in eerste instantie 1 kiesman
    kiesmannenDF = pd.DataFrame(data={'Kiesmannen': 1,
                                      'Quotiënt': list(uitslagenDF['Kiesgerechtigden']/2**(1/2)),
                                      'Kiesgerechtigden': list(uitslagenDF['Kiesgerechtigden'])},
                                index=list(uitslagenDF['RegioNaam']))
    kiesmannenDF.index.name = 'Gemeentenaam'
    rest_kiesmannen = aantal_zetels - len(uitslagenDF)
    
    while rest_kiesmannen > 0:
        i_max = kiesmannenDF['Quotiënt'].idxmax()
        kiesmannenDF.loc[i_max, 'Kiesmannen'] += 1
        kiesmannen_temp = kiesmannenDF.loc[i_max, 'Kiesmannen']
        kiesmannenDF.loc[i_max, 'Quotiënt'] = kiesmannenDF.loc[i_max, 'Kiesgerechtigden'] / (kiesmannen_temp*(kiesmannen_temp+1))**(1/2)
        rest_kiesmannen -= 1
    
    
    # Bepalen van de winnaar in elke gemeente en het toekennnen van de kiesmannen
    zetelsDF = pd.DataFrame(data=0, columns=['Aantal zetels'], index=uitslagenDF.columns[10:])
    zetelsDF.index.name = 'Partijnaam'
    
    for i in uitslagenDF.index:
        temp_ser = uitslagenDF.loc[i, 'VVD':'De Groenen']
        verfuncs.replace_NaN(temp_ser)
        temp_ser = temp_ser.astype(int)
        winnaar = temp_ser.idxmax()
        gemeente = uitslagenDF.loc[i, 'RegioNaam']
        zetelsDF.loc[winnaar, 'Aantal zetels'] += kiesmannenDF.loc[gemeente, 'Kiesmannen']
        
    zetel_tabel = zetelsDF.to_html()
        
    return ("<h2>Landelijke uitslag Tweede Kamerverkiezingen 2021</h2> Op basis van een kiesdistrictstelsel met " +
            str(aantal_zetels) + " zetels." + zetel_tabel)