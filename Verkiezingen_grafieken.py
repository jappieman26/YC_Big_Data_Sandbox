#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import Verkiezingen_functies as verfuncs

uitslagenDF = pd.read_csv('Uitslag_alle_gemeenten_TK20210317.csv', sep=';')


# In[2]:


df1 = verfuncs.landelijke_uitslag(uitslagenDF)
df2 = verfuncs.landelijke_uitslag_kiesmannen(uitslagenDF)
df3 = verfuncs.landelijke_uitslag_top_n(uitslagenDF)
df4 = verfuncs.zetels_per_gewonnen_gemeente(uitslagenDF)


# In[14]:


def plot_uitslag(df):
    plt.figure(figsize=(15,10))                  # totale figuur
    plt.bar(df.index, df['zetels'] )             # data x & y as
    plt.xticks(rotation=90)                      # leesbaarheid x as labels (90 graden draaien)
    plt.title('Uitslag (totaal aantal zetels = ' + str(df['zetels'].sum()) + ')')
    plt.ylabel('Zetels')
    plt.plot()


# In[ ]:


def insert_lege_partijen(uitslagenDF):
    


# In[16]:


plot_uitslag(df1)


# In[17]:


plot_uitslag(df2)


# In[18]:


plot_uitslag(df3)


# In[19]:


plot_uitslag(df4)


# In[ ]:




