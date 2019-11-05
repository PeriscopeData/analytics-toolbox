def add_center_label(df):
    percent = str(round(1.0*df.iloc[0, 0]/df.iloc[0, 1]*100)) + '%'
    return plt.text(0,
           0.2,
           percent,
           horizontalalignment='center',
           verticalalignment='center',
           fontsize = 40,
           family = 'sans-serif')

def add_sub_center_label(df):
    amount = 'Goal: ' + get_currency_label(df.iloc[0,1])
    return plt.text(0,
            -0.1,
            amount,
            horizontalalignment='center',
            verticalalignment='top',
            fontsize = 22,family = 'sans-serif')