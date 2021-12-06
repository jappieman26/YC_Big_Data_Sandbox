import pandas as pd
import numpy as np



def landelijke_uitslag(uitslagenDF):
    """
    Bereken de landelijke uitslag van de Tweede Kamerverkiezingen in het aantal
    stemmen dat iedere partij heeft gekregen, en de zetels die dat oplevert.
    Return een string met een html-tabel met de uitslagen.
    """
    aantal_zetels = 150
    totaal_stemmen = uitslagenDF['GeldigeStemmen'].sum()
    kiesdeler = int(totaal_stemmen / aantal_zetels + 0.5)
    
    
    zetelsDF = pd.DataFrame(columns=['totaal aantal stemmen', 'aantal zetels'],
                            index=uitslagenDF.columns[10:])
    
    # Bereken het aantal stemmen en volledige zetels voor elke partij
    for partij in uitslagenDF.columns[10:]:
        partij_stemmen = int(uitslagenDF[partij].sum())
        zetelsDF.loc[partij, 'totaal aantal stemmen'] = partij_stemmen
        
        aantal_volle_zetels = int(partij_stemmen/kiesdeler)
        zetelsDF.loc[partij, 'aantal zetels'] = aantal_volle_zetels
     
    # Haal de partijen die niet minstens 1 volledige zetel hebben gehaald uit het primaire DF,
    # zodat ze niet meegaan in de berekening van de restzetels. Sla ze op in hun eigen DF.
    idx_partijen_zonder_zetels = zetelsDF[zetelsDF['aantal zetels']==0].index
    partijen_zonder_zetels = zetelsDF.loc[idx_partijen_zonder_zetels]
    zetelsDF = zetelsDF.drop(idx_partijen_zonder_zetels)
        
    zetelsDF.insert(2, 'stemmen per zetel', [0]*len(zetelsDF.index))
    
    # Toekenning restzetels
    restzetels = 150 - zetelsDF['aantal zetels'].sum()
    zetelsDF['stemmen per zetel'] = zetelsDF['totaal aantal stemmen'] / (zetelsDF['aantal zetels'] + 1)
    zetelsDF['stemmen per zetel'] = pd.to_numeric(zetelsDF['stemmen per zetel'])
    
    while restzetels > 0:
        i_max = zetelsDF['stemmen per zetel'].idxmax() # index (partijnaam) van hoogste aantal stemmen per zetel
        zetelsDF.loc[i_max, 'aantal zetels'] += 1
        zetelsDF.loc[i_max, 'stemmen per zetel'] = zetelsDF.loc[i_max, 'totaal aantal stemmen'] / (zetelsDF.loc[i_max, 'aantal zetels'] + 1)
        restzetels -= 1
    
    zetelsDF = zetelsDF.drop('stemmen per zetel', axis=1)
    zetelsDF = pd.concat([zetelsDF, partijen_zonder_zetels])
    
    zetel_tabel = zetelsDF.to_html()
    
    return "<h2>Landelijke uitslag Tweede Kamerverkiezingen 2021</h2>" + zetel_tabel



def volgorde_gemeentes(uitslagenDF, partij):
    """
    Bepaal de rangschikking van de gemeentes op basis van het aantal stemmen voor
    een specifieke partij. Return een string met een html-tabel met de resultaten.
    """
    partijnaam = ""
    naam_found = False
    
    for vol_naam in uitslagenDF.columns[10:]:
        if partij in vol_naam:
            partijnaam = vol_naam
            naam_found = True
            
    if not naam_found:
        return "De partijnaam wordt niet herkend!"
    
    else:        
        partijDF = pd.DataFrame(data=list(uitslagenDF[partijnaam]), columns=['aantal stemmen'],
                                index=list(uitslagenDF['RegioNaam']))
        
        # Sorteer op aantal stemmen, waar NaN wordt vervangen door 0.
        sorted_partijDF = partijDF.sort_values('aantal stemmen', ascending=False,
                                               key=replace_NaN(partijDF['aantal stemmen']))
        # Maak alle entries van type int (in het geval het nog floats zijn).
        sorted_partijDF = sorted_partijDF.astype(int)
        sorted_partij_tabel = sorted_partijDF.to_html()
        
        return "<h2>Rangschikking gemeentes naar aantal stemmen op " + partij + "</h2>" + sorted_partij_tabel
    
    
   
def volgorde_perc_ongeldig(uitslagenDF):
    """"
    Bepaal de rangschikking van de gemeentes op basis van het percentage ongeldige stemmen.
    Return een string met een html-tabel met de percentages ongeldige en blanco stemmen.
    """
    ongeldig_perc_list = list(uitslagenDF['OngeldigeStemmen']/uitslagenDF['Opkomst']*100)
    blanco_perc_list = list(uitslagenDF['BlancoStemmen']/uitslagenDF['Opkomst']*100)
    
    geldigDF = pd.DataFrame(data={'Ongeldige stemmen (%)' : ongeldig_perc_list,
                                  'Blanco stemmen (%)' : blanco_perc_list}, index=list(uitslagenDF['RegioNaam']))
    
    sorted_geldigDF = geldigDF.sort_values('Ongeldige stemmen (%)')
    sorted_geldigTabel = sorted_geldigDF.to_html()
    
    return "<h2>Rangschikking gemeentes naar ongeldige stemmen als percentage van de totale opkomst</h2>" + sorted_geldigTabel



def perc_ongeldig_gemeente(uitslagenDF, gemeente):
    """
    Bepaal het percentage ongeldige en blanco stemmen van de totale opkomst voor
    een bepaalde gemeente. Return deze in een html-string.
    """
    if gemeente in list(uitslagenDF['RegioNaam']):
        gemeente_idx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
        perc_ongeldig = uitslagenDF.loc[gemeente_idx, 'OngeldigeStemmen'] / uitslagenDF.loc[gemeente_idx, 'Opkomst'] * 100
        perc_blanco = uitslagenDF.loc[gemeente_idx, 'BlancoStemmen'] / uitslagenDF.loc[gemeente_idx, 'Opkomst'] * 100
        
        return ("<h2>Ongeldige en blanco stemmen als percentage van de totale opkomst in " + gemeente + "</h2>" +
                "Percentage ongeldig: " + str(perc_ongeldig) + "<br>" + "Percentage blanco: " + str(perc_blanco))
        
    else:
        return "De gemeentenaam wordt niet herkend!"
    
    
  
def uitslag_gemeente(uitslagenDF, gemeente):
    """
    Bepaal de rangschikking van de partijen naar het aantal stemmen in een bepaalde gemeente.
    Return een string met een html-tabel met de resultaten.
    """
    if gemeente in list(uitslagenDF['RegioNaam']):
        
        gemeente_idx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
        gemeenteDF = pd.DataFrame(data=list(uitslagenDF.loc[gemeente_idx, uitslagenDF.columns[10:]]),
                                  columns=['aantal stemmen'], index=list(uitslagenDF.columns[10:]))
        
        # Sorteer op aantal stemmen, waar NaN wordt vervangen door 0.
        sorted_gemeenteDF = gemeenteDF.sort_values('aantal stemmen', ascending=False,
                                                  key=replace_NaN(gemeenteDF['aantal stemmen']))
        # Maak alle entries van type int (in het geval het nog floats zijn).
        sorted_gemeenteDF = sorted_gemeenteDF.astype(int)
        sorted_gemeente_tabel = sorted_gemeenteDF.to_html()
        
        return "<h2>De gesorteerde uitslag in " + gemeente + "</h2>" + sorted_gemeente_tabel
        
    else:
        return "De gemeentenaam wordt niet herkend!"
    
def populairste_per_gemeente(df):
    """
    Bepaal welke politieke partij in elke gemeente heeft gewonnen
    """
    gemeente_uitslag_df = df.iloc[:,np.r_[0,10:47]]
    gemeente_uitslag_df = gemeente_uitslag_df.fillna(0)
    cols = gemeente_uitslag_df.columns.drop('RegioNaam')
    
    gemeente_uitslag_df[cols] = gemeente_uitslag_df[cols].astype(int)
    
    gemeente_uitslag_df['Winnaar'] = gemeente_uitslag_df[cols].idxmax(axis=1)
    gemeente_winnaar = gemeente_uitslag_df.iloc[:,np.r_[0,38]]

    return gemeente_winnaar

def zetels_per_gewonnen_gemeente(df):
    """
    Zetel berekening aan de hand van winnende de partij binnen gemeentes krijgen alle stemmen daat
    """
    gemeente_winnaars = populairste_per_gemeente(df)
    gemeente_count = len(gemeente_winnaars.index)
    winnaar_count = gemeente_winnaars.groupby(['Winnaar']).count()
    zetels = pd.DataFrame(columns=['Fractie','Zetels'])
    zetel_per_winst = 150/gemeente_count

    for index,row in winnaar_count.iterrows():
        if round(row[0] * zetel_per_winst) > 1:
            volle_zetels = round(row[0] * zetel_per_winst)
            zetels = zetels.append({'Fractie': index,'Zetels': volle_zetels, 'winst_per_zetel': (volle_zetels+1)/row[0], 'totaal_winst': row[0] },ignore_index=True)
    
    rest_zetels = 150 - zetels['Zetels'].sum()

    while rest_zetels > 0:
        i_max = zetels['winst_per_zetel'].idxmax() # index (partijnaam) van hoogste aantal stemmen per zetel
        zetels.loc[i_max, 'Zetels'] += 1
        zetels.loc[i_max, 'winst_per_zetel'] = zetels.loc[i_max, 'totaal_winst'] / (zetels.loc[i_max, 'Zetels'] + 1)
        rest_zetels -= 1

    zetels = zetels.drop(columns=['totaal_winst','winst_per_zetel'])

    return zetels


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
        replace_NaN(temp_ser)
        temp_ser = temp_ser.astype(int)
        winnaar = temp_ser.idxmax()
        gemeente = uitslagenDF.loc[i, 'RegioNaam']
        zetelsDF.loc[winnaar, 'Aantal zetels'] += kiesmannenDF.loc[gemeente, 'Kiesmannen']
        
    zetel_tabel = zetelsDF.to_html()
        
    return ("<h2>Landelijke uitslag Tweede Kamerverkiezingen 2021</h2> Op basis van een kiesdistrictstelsel met " +
            str(aantal_zetels) + " zetels." + zetel_tabel)


def replace_NaN(ser):
    for i in ser.index:
        if np.isnan(ser[i]):
            ser[i] = 0