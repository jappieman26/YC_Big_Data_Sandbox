import pandas as pd


def provincie_gemeente():
    """
    Laad het xls bestand met gemeentes en provincies in, en return een dataframe met als indices de gemeentenamen,
    en in de kolom 'Provincienaam' de naam van de bijbehorende provincie.
    """
    df = pd.read_excel('Gemeenten alfabetisch 2019.xls')
    prov_gem_df = pd.DataFrame(data=list(df['Provincienaam']), columns=['Provincienaam'], index=list(df['Gemeentenaam']))
    prov_gem_df.index.name = 'Gemeentenaam'
    return prov_gem_df