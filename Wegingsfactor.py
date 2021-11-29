import pandas as pd

uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')

def bevolking_wegingsfactor():
    """
    Bepaal voor elke gemeente een wegingsfactor door het aantal stemgerechtigden in die gemeente 
    te delen door het totaal aantal stemgerechtigden. 
    """
    stemgerechtigden_totaal = uitslagenDF['Kiesgerechtigden'].sum()
    wegingDF = pd.DataFrame(data = list(uitslagenDF['Kiesgerechtigden'] / stemgerechtigden_totaal),
                            columns=['Wegingsfactor'], index=list(uitslagenDF['RegioNaam']))
    wegingDF.index.name = 'Gemeentenaam'
    
    return wegingDF