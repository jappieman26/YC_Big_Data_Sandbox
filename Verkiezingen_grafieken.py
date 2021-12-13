import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Verkiezingen_functies as verfuncs



def combineer_uitslagen(df, n=3):
    """
    Combineert de dataframes van landelijke_uitslag() en landelijke_uitslag_top_n.
    """
    new_df = verfuncs.landelijke_uitslag(df)
    second_df = verfuncs.landelijke_uitslag_top_n(df, n)
    new_df.insert(2, f'zetels obv top {n} partijen', [0]*len(new_df.index))
    for partij in second_df.index:
        zetels = second_df.loc[partij ,'zetels']
        #if statement check if partij uit second_df is already in new_df or not and should be added. (Row insert)
        new_df.loc[partij, f'zetels obv top {n} partijen'] = zetels
    return new_df

def plot_landelijk_vs_top_n(df, n=3):
    """
    Plot de huidige landelijke zetelverdeling tegen de verdeling op basis van de grootste n partijen per gemeente.
    """
    new_df = combineer_uitslagen(df, n)
    i = np.arange(0, len(list(new_df.index)))
    width = 0.4

    fig, ax = plt.subplots(figsize=(10,5))
    rects1 = ax.bar(i - width/2, height=new_df['zetels'], width = width, label='landelijk', color='teal')
    rects2 = ax.bar(i + width/2, height=new_df[f'zetels obv top {n} partijen'], width = width, label=f'top {n}', color='black')

    ax.set_xticks(i, list(new_df.index))
    plt.xticks(rotation=90)
    plt.ylabel('zetels')
    plt.title('Zetelverdeling Tweede Kamer')
    ax.legend()

    ax.bar_label(rects1) # laat het aantal zien boven elke bar
    ax.bar_label(rects2)

    return fig



def plot_uitslag(df):
    plt.figure(figsize=(15,10))                  # totale figuur
    plt.bar(df.index, df['zetels'] )             # data x & y as
    plt.xticks(rotation=90)                      # leesbaarheid x as labels (90 graden draaien)
    plt.title('Uitslag (totaal aantal zetels = ' + str(df['zetels'].sum()) + ')')
    plt.ylabel('Zetels')
    plt.plot()
