"""Quick timeseries between July and August"""

from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime

file = '/Users/Freddy/PycharmProjects/GDELT:MoNA/zika_analysis.csv'

df = pd.DataFrame.from_csv(file)

#Do some filtering for wordcounts & reformat ID to date
df = df[df.wordcount < 1800]
df = df[df.wordcount > 500]
df = df.rename(columns = {'ID': 'DATE'})

#strip of the last five characters and format dates to pandas timestamps
df['DATE'] = df['DATE'].map(lambda x: x[:14])
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d%H%M%S')

#set index to datetimes
df = df.set_index(df['DATE'], drop=False)

#select specific source locations:
location = 'US'
df = df[df.source_location == location]

#Order mfts inside df
cols = df.columns.tolist()
mft_cols = cols[6:17]
cols = cols[:6] + [cols[6]] + cols[9:17] + [cols[7]] + [cols[8]] + cols[17:]
df = df[cols]

#rename MFT variables
mft_vars = ['c25.{}'.format(i) for i in range(1,12)]
mft_names = ['HarmVirtue', 'HarmVice', 'FairnessVirtue', 'FairnessVice','IngroupVirtue', 'IngroupVice', 'AuthorityVirtue', 'AuthorityVice','PurityVirtue', 'PurityVice', 'MoralityGeneral']
newcols = dict(zip(mft_vars, mft_names)) #create dictionary that contains new column names
df.rename(columns=newcols, inplace=True)

#Calculate the mean for each day
df = df.resample("1d").sum().fillna(0).rolling(window=3, min_periods=1).mean()

df.plot(x=df.index, y='HarmVice', kind='line')
plt.show()

