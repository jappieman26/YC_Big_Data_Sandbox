import pandas as pd
import numpy as np



def landelijke_uitslag(uitslagenDF):
    """
    Bereken de landelijke uitslag van de Tweede Kamerverkiezingen in het aantal
    stemmen dat iedere partij heeft gekregen, en de zetels die dat oplevert.
    Return dataframe met de uitslagen.
    """
    aantal_zetels = 150
    totaal_stemmen = uitslagenDF['GeldigeStemmen'].sum()
    kiesdeler = int(totaal_stemmen / aantal_zetels + 0.5)
    
    
    zetelsDF = pd.DataFrame(columns=['stemmen', 'zetels'],
                            index=uitslagenDF.columns[10:])
    
    # Bereken het aantal stemmen en volledige zetels voor elke partij
    for partij in uitslagenDF.columns[10:]:
        partij_stemmen = int(uitslagenDF[partij].sum())
        zetelsDF.loc[partij, 'stemmen'] = partij_stemmen
        
        aantal_volle_zetels = int(partij_stemmen/kiesdeler)
        zetelsDF.loc[partij, 'zetels'] = aantal_volle_zetels
     
    # Haal de partijen die niet minstens 1 volledige zetel hebben gehaald uit het primaire DF,
    # zodat ze niet meegaan in de berekening van de restzetels. Sla ze op in hun eigen DF.
    idx_partijen_zonder_zetels = zetelsDF[zetelsDF['zetels']==0].index
    partijen_zonder_zetels = zetelsDF.loc[idx_partijen_zonder_zetels]
    zetelsDF = zetelsDF.drop(idx_partijen_zonder_zetels)
        
    zetelsDF.insert(2, 'stemmen per zetel', [0]*len(zetelsDF.index))
    
    # Toekenning restzetels
    restzetels = 150 - zetelsDF['zetels'].sum()
    zetelsDF['stemmen per zetel'] = zetelsDF['stemmen'] / (zetelsDF['zetels'] + 1)
    zetelsDF['stemmen per zetel'] = pd.to_numeric(zetelsDF['stemmen per zetel'])
    
    while restzetels > 0:
        i_max = zetelsDF['stemmen per zetel'].idxmax() # index (partijnaam) van hoogste aantal stemmen per zetel
        zetelsDF.loc[i_max, 'zetels'] += 1
        zetelsDF.loc[i_max, 'stemmen per zetel'] = zetelsDF.loc[i_max, 'stemmen'] / (zetelsDF.loc[i_max, 'zetels'] + 1)
        restzetels -= 1
    
    zetelsDF = zetelsDF.drop('stemmen per zetel', axis=1)
    zetelsDF = pd.concat([zetelsDF, partijen_zonder_zetels])
    
    return zetelsDF



def volgorde_gemeentes(uitslagenDF, partij):
    """
    Bepaal de rangschikking van de gemeentes op basis van het aantal stemmen voor
    een specifieke partij. Return een dataframe met de resultaten.
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
        partijDF = pd.DataFrame(data=list(uitslagenDF[partijnaam]), columns=['stemmen'],
                                index=list(uitslagenDF['RegioNaam']))
        
        # Sorteer op aantal stemmen, waar NaN wordt vervangen door 0.
        sorted_partijDF = partijDF.sort_values('stemmen', ascending=False,
                                               key=replace_NaN(partijDF['stemmen']))
        # Maak alle entries van type int (in het geval het nog floats zijn).
        sorted_partijDF = sorted_partijDF.astype(int)
        
        return sorted_partijDF
    
    
   
def volgorde_perc_ongeldig(uitslagenDF):
    """"
    Bepaal de rangschikking van de gemeentes op basis van het percentage ongeldige stemmen.
    Return een dataframe met de percentages ongeldige en blanco stemmen.
    """
    ongeldig_perc_list = list(uitslagenDF['OngeldigeStemmen']/uitslagenDF['Opkomst']*100)
    blanco_perc_list = list(uitslagenDF['BlancoStemmen']/uitslagenDF['Opkomst']*100)
    
    geldigDF = pd.DataFrame(data={'Ongeldige stemmen (%)' : ongeldig_perc_list,
                                  'Blanco stemmen (%)' : blanco_perc_list}, index=list(uitslagenDF['RegioNaam']))
    
    sorted_geldigDF = geldigDF.sort_values('Ongeldige stemmen (%)')
    
    return sorted_geldigDF



def perc_ongeldig_gemeente(uitslagenDF, gemeente):
    """
    Bepaal het percentage ongeldige en blanco stemmen van de totale opkomst voor
    een bepaalde gemeente. Return deze in een tuple.
    """
    
    gemeente_idx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
    perc_ongeldig = uitslagenDF.loc[gemeente_idx, 'OngeldigeStemmen'] / uitslagenDF.loc[gemeente_idx, 'Opkomst'] * 100
    perc_blanco = uitslagenDF.loc[gemeente_idx, 'BlancoStemmen'] / uitslagenDF.loc[gemeente_idx, 'Opkomst'] * 100
        
    percDF = pd.DataFrame(data={'Ongeldige stemmen (%)' : perc_ongeldig,
                                'Blanco stemmen (%)' : perc_blanco}, index=[gemeente])
    
    return percDF
    
    
  
def uitslag_gemeente(uitslagenDF, gemeente):
    """
    Bepaal de rangschikking van de partijen naar het aantal stemmen in een bepaalde gemeente.
    Return een dataframe met de resultaten.
    """
        
    gemeente_idx = uitslagenDF[uitslagenDF['RegioNaam'] == gemeente].index[0]
    gemeenteDF = pd.DataFrame(data=list(uitslagenDF.loc[gemeente_idx, uitslagenDF.columns[10:]]),
                              columns=['stemmen'], index=list(uitslagenDF.columns[10:]))
        
    # Sorteer op aantal stemmen, waar NaN wordt vervangen door 0.
    sorted_gemeenteDF = gemeenteDF.sort_values('stemmen', ascending=False,
                                               key=replace_NaN(gemeenteDF['stemmen']))
    # Maak alle entries van type int (in het geval het nog floats zijn).
    sorted_gemeenteDF = sorted_gemeenteDF.astype(int)
        
    return sorted_gemeenteDF


    
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
    zetels = pd.DataFrame(data=0, columns=['zetels', 'winst_per_zetel', 'totaal_winst'], index=df.columns[10:])
    zetel_per_winst = 150/gemeente_count

    for index,row in winnaar_count.iterrows():
        if round(row[0] * zetel_per_winst) > 1:
            volle_zetels = round(row[0] * zetel_per_winst)
            zetels.loc[index] = [volle_zetels, row[0]/(volle_zetels+1), row[0]]
    
    rest_zetels = 150 - zetels['zetels'].sum()
    zetels['winst_per_zetel'] = pd.to_numeric(zetels['winst_per_zetel'])

    while rest_zetels > 0:
        i_max = zetels['winst_per_zetel'].idxmax() # index (partijnaam) van hoogste aantal gewonnen gemeenten per zetel
        zetels.loc[i_max, 'zetels'] += 1
        zetels.loc[i_max, 'winst_per_zetel'] = zetels.loc[i_max, 'totaal_winst'] / (zetels.loc[i_max, 'zetels'] + 1)
        rest_zetels -= 1

    zetels = zetels.drop(columns=['totaal_winst','winst_per_zetel'])

    return zetels


def landelijke_uitslag_kiesmannen(uitslagenDF):
    """
    Bereken de landelijke uitslag van de Tweede Kamerverkiezingen als het aantal zetels wordt uitgebreid naar 1050,
    en elke gemeente op basis van zijn populatie een aantal kiesmannen toegewezen krijgt. De partij die wint in een
    gemeente krijgt alle kiesmannen. Return een dataframe met de uitslag.
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
    zetelsDF = pd.DataFrame(data=0, columns=['zetels'], index=uitslagenDF.columns[10:])
    zetelsDF.index.name = 'Partijnaam'
    
    for i in uitslagenDF.index:
        temp_ser = uitslagenDF.loc[i, 'VVD':'De Groenen']
        replace_NaN(temp_ser)
        temp_ser = temp_ser.astype(int)
        winnaar = temp_ser.idxmax()
        gemeente = uitslagenDF.loc[i, 'RegioNaam']
        zetelsDF.loc[winnaar, 'zetels'] += kiesmannenDF.loc[gemeente, 'Kiesmannen']
        
    return zetelsDF



def stem_stad_n(df, stad='Amsterdam', n=3):
    """
    Deze functie returnt een dataframe waarin het aantal stemmen per partij vd grootste n partijen van hoog naar laag staan in een meegegeven gemeente. Amsterdam is default.
    """
    df_stemmen = df[list(df.columns[10:])] 
    gemeente = df[df['RegioNaam'] == stad].index[0] 
    stemmen_per_gemeente = df_stemmen.loc[gemeente] 
    data = {'GeldigeStemmen': stemmen_per_gemeente}
    df_top_n = pd.DataFrame(data).sort_values(['GeldigeStemmen'], ascending=False)[:n] 
    df_top_n.index.name = 'Regio'
    return df_top_n

def zetels_per_n_grootste_partijen(df, gemeente='Amsterdam', n=3):
    """
    Deze functie berekent het aantal zetels dat de n grootste partijen zouden hebben als alleen de stemmen van deze stad meetellen.
    """
    data = stem_stad_n(df, gemeente, n)
    totaal_stemmen = data['GeldigeStemmen'].sum()
    totaal_zetels = 150
    kiesdeler = totaal_stemmen / totaal_zetels

    grootste_partijen = []
    stemmen_per_partij = {}
    zetels_per_partij = {}
    rest_zetels = {}
    column_names = []

    for i in range(0, data["GeldigeStemmen"].size) :
        partij = data.index[i]
        grootste_partijen.append(partij)
        aantal_stemmen = data["GeldigeStemmen"].loc[partij]
        stemmen_per_partij[partij] = aantal_stemmen
        zetels_per_partij[partij] = aantal_stemmen // kiesdeler
        aantal_zetels = zetels_per_partij[partij]
        rest_zetels[partij] = aantal_stemmen / (aantal_zetels + 1)
        column_names.append(f'{i+1}e')

    while sum(zetels_per_partij.values()) < totaal_zetels:
        hoogste = max(rest_zetels, key=rest_zetels.get)
        zetels_per_partij[hoogste] += 1
        rest_zetels[hoogste] = stemmen_per_partij[hoogste] / (zetels_per_partij[hoogste] +1)

    df_n_grootste_partijen = pd.DataFrame(data=[grootste_partijen, zetels_per_partij.values()], columns=column_names)
    return df_n_grootste_partijen

def landelijke_uitslag_top_n(df, n=3):
    """
    Deze functie telt het aantal volledige zetels op per partij die in de topn van een gemeente zijn geeindigd
    """
    landelijk = {}
    for stad in df["RegioNaam"]:
        df_drie_grootste = zetels_per_n_grootste_partijen(df, stad, n)
        for column in df_drie_grootste.columns:
            partij = df_drie_grootste[column].loc[0]
            zetel = df_drie_grootste[column].loc[1] / 355
            if partij in landelijk.keys():
                landelijk[partij] = landelijk[partij] + zetel
            else:
                landelijk[partij] = zetel
                
    my_df = pd.DataFrame(data=landelijk.values(), columns=['zetels'], index=landelijk.keys()).sort_values(["zetels"], ascending=False)
    my_df = my_df.drop(my_df[my_df['zetels'] < 1].index)
    my_df = my_df.astype({'zetels': int})

    # restzetels
    my_df.insert(1, "stemmen per zetel", [0]*len(my_df.index))
    my_df.insert(2, "stemmen", [0]*len(my_df.index))

    for partij in my_df.index:
        aantal_stemmen = df[partij].sum()
        my_df.loc[partij, 'stemmen'] = aantal_stemmen
        my_df.loc[partij, 'stemmen per zetel'] = aantal_stemmen / (my_df["zetels"][partij] +1)              

    while my_df['zetels'].sum() < 150:
        i_max = my_df['stemmen per zetel'].idxmax()
        my_df.loc[i_max, 'zetels'] += 1
        my_df.loc[i_max, 'stemmen per zetel'] = my_df.loc[i_max, 'stemmen'] / (my_df.loc[i_max, 'zetels'] +1)
        
    my_df = my_df.drop('stemmen per zetel', axis=1)
        
    return my_df.sort_values(["zetels"], ascending=False)



def replace_NaN(ser):
    for i in ser.index:
        if np.isnan(ser[i]):
            ser[i] = 0