import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import inspect
import Verkiezingen_functies as verfuncs



def combineer_uitslagen_v15(df, n1=3, n2=3, optie_1='landelijk', optie_2='top n', weights1=dict(), weights2=dict()):
    """
    Lambda poging 5: hardcoded in dict. lambda dict functionality. Combineert de 'zetel' kolommen van 2 functie returns naar keuze. 
    """
    opties_dict = {# dictionary dient als switch. Hiermee kan worden meegegeven welke functies worden geplot
        'landelijk': lambda df, n: verfuncs.landelijke_uitslag(df), 
        'top n': lambda df, n: verfuncs.landelijke_uitslag_top_n(df, n),
        'kiesmannen': lambda df, n: verfuncs.landelijke_uitslag_kiesmannen(df),
        'per gemeente': lambda df, n: verfuncs.zetels_per_gewonnen_gemeente(df)
    }

    if optie_1 == 'per provincie':
        df_1 = verfuncs.provincie_als_landelijk(weights1)
    else: df_1 = opties_dict.get(optie_1)(df, n1)
    if optie_2 == 'per provincie':
        df_2 = verfuncs.provincie_als_landelijk(weights2)
    else: df_2 = opties_dict.get(optie_2)(df, n2)

    naam1 = optie_1.replace(" n", f" {n1}") 
    naam2 = optie_2.replace(" n", f" {n2}") 
    col_naam1 = f"zetels obv {naam1}"
    col_naam2 = f"zetels obv {naam2}"
    df_combi = pd.concat([df_1['zetels'], df_2['zetels']], axis=1).replace(np.nan, 0)
    df_combi.columns = [col_naam1, col_naam2]
    return df_combi[(df_combi.iloc[:,0] != 0) | (df_combi.iloc[:,1] != 0)], naam1, naam2


def plot_landelijk_vs_top_n_v2(combi_df, naam1, naam2, log=False):
    """
    Plot de huidige landelijke zetelverdeling tegen de verdeling op basis van de grootste n partijen per gemeente.
    """

    i = np.arange(0, len(list(combi_df.index))) #space the x axis labels
    width = 0.4

    fig, ax = plt.subplots(figsize=(10,5))
    fig.subplots_adjust(hspace = 1, wspace = .1)

    rects1 = ax.bar(i - width/2, height=combi_df.iloc[:,0], width = width, label=naam1, color='teal')
    rects2 = ax.bar(i + width/2, height=combi_df.iloc[:,1], width = width, label=naam2, color='black')

    ax.set_xticks(i, list(combi_df.index), rotation=90)
    if log: ax.set_yscale('log')
    plt.ylabel('zetels')
    plt.title('Zetelverdeling Tweede Kamer')
    ax.legend()

    ax.bar_label(rects1) # laat het aantal zien boven elke bar
    ax.bar_label(rects2)
    plt.tight_layout()
    plt.close() # voorkomt dubbel print van grafiek
    return fig


def plot_uitslag(df):
    fig, ax = plt.subplots(figsize=(10,7))              # maak het figuur (fig) en de subplot (ax)
    labels = df.index
    x_pos = range(len(labels))
    bars = ax.bar(x_pos, df['zetels'] )                 # data x & y as
    ax.set_xticks(x_pos, labels, rotation=90)           # x-as labels (90 graden draaien voor leesbaarheid)
    ax.bar_label(bars)                                  # labels aan de bars toevoegen; neemt automatisch de waardes van de data in de bars
    plt.title('Uitslag (totaal aantal zetels = ' + str(df['zetels'].sum()) + ')')
    ax.set_ylabel('Zetels')
    plt.tight_layout()                                  # zorgt ervoor dat de labels niet afgesneden worden in de uiteindelijke png
    plt.close()                                         # voorkomt dubbele print
    return fig
