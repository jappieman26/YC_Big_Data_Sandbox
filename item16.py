df1 = landelijke_uitslag()
df2 = landelijke_uitslag_top_n()

def plot_landelijke_uitslag(data1=df1, data2=df2):
    plt.figure(figsize=(15,10))                  # totale figuur
    plt.subplot(221)                             # subplot links boven
    plt.bar(df1['Partijen'], df1['Zetels'] )     # data x & y as
    plt.xticks(rotation=90)                      # leesbaarheid x as labels
    plt.title('Landelijke Uitslag')
    plt.ylabel('Zetels')

    plt.subplot(222)                             # subplot rechts boven
    plt.bar(x=df2['partij'], height = df2['zetels'])
    plt.xticks(rotation=90)
    plt.title('Uitslag op top 3 partijen')
    plt.ylabel('zetels')
    plt.plot()
plot_landelijke_uitslag()