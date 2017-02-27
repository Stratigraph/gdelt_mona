"""TimeSeries of MFT & THEMES Across November 2016 - January 2017"""

from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime

file = '/Users/Freddy/PycharmProjects/GDELT:MoNA/all_whitelist_dec_nov_jan_unfiltered.csv'

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
location = 'GM'
df = df[df.source_location == location]

#Order mfts inside df
cols = df.columns.tolist()
mft_cols = cols[17:28]
cols = cols[:17] + [cols[17]] + cols[20:28] + [cols[18]] + [cols[19]] + cols[28:]
df = df[cols]

#rename MFT variables
mft_vars = ['c25.{}'.format(i) for i in range(1,12)]
mft_names = ['HarmVirtue', 'HarmVice', 'FairnessVirtue', 'FairnessVice','IngroupVirtue', 'IngroupVice', 'AuthorityVirtue', 'AuthorityVice','PurityVirtue', 'PurityVice', 'MoralityGeneral']
newcols = dict(zip(mft_vars, mft_names)) #create dictionary that contains new column names
df.rename(columns=newcols, inplace=True)

#Calculate the mean for each day
df = df.resample("1d").sum().fillna(0).rolling(window=1, min_periods=1).mean()

# use some string tricks to quickly pick out the columns we want
theme_cols = [c for c in df.columns if c.isupper()]
mft_cols = [c for c in df.columns if not c.isupper() and not c.islower()]

mft_themes = theme_cols + mft_cols

#Protest Themes
df.plot(x=df.index, y=[x for x in theme_cols if x == 'MOVEMENT_SOCIAL' or x == 'PROTEST' or x == 'REBELLION'], kind='line')
plt.title('TimeSeries of Protest Themes')
plt.ylabel("Average Mention of Theme Per Day")
plt.xlabel("Date")
plt.text(0, .15, 'TimePeriod:November2016-January2017\nSources: AllWhitelist\nSourceLocation:%s' %(location))
plt.plot([2], [0.5], 'o')
plt.annotate('20thJanuary\nInaugurationDay2017', xy=('2017-01-20', 100), xytext=('2017-01-20', 90), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('8thNovember\nElectionDay2017', xy=('2016-11-08', 57), xytext=('2016-11-08', 47), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('1stDecember\n#NoDAPL Global Day of Action', xy=('2016-12-01', 57), xytext=('2016-12-01', 47), arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()

"""#MFT_Themes
df.plot(x=df.index, y=[x for x in mft_cols], kind='line')
plt.title('TimeSeries of MoralFoundations')
plt.ylabel("Average Counts of MFTs Per Day")
plt.xlabel("Date")
plt.text(0, .15, 'TimePeriod:November2016-January2017\nSources: AllWhitelist\nSourceLocation:%s' %(location))
plt.plot([10], [0.5], 'o')
plt.annotate('20thJanuary\nInaugurationDay2017', xy=('2017-01-20', 100), xytext=('2017-01-20', 90), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('8thNovember\nElectionDay2017', xy=('2016-11-08', 1800), xytext=('2016-11-08', 1700), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('8thNovember\nElectionDay2017', xy=('2016-11-08', 1800), xytext=('2016-11-08', 1700), arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()"""

#MFT_Themes
df.plot(x=df.index, y=[x for x in mft_cols], kind='line')
plt.title('TimeSeries of MoralFoundations')
plt.ylabel("Average Counts of MFTs Per Day")
plt.xlabel("Date")
plt.text(0, .15, 'TimePeriod:November2016-January2017\nSources: AllWhitelist\nSourceLocation:%s' %(location))
plt.plot([10], [0.5], 'o')
plt.annotate('19thDecember\nTerrorAttackChristmasMarket', xy=('2016-12-19', 50), xytext=('2016-12-19', 40), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('8thNovember\nElectionDay2017', xy=('2016-11-08', 1800), xytext=('2016-11-08', 1700), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('8thNovember\nElectionDay2017', xy=('2016-11-08', 1800), xytext=('2016-11-08', 1700), arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()