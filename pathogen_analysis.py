"""Correlations between disease related news themes and MFTs"""

from matplotlib import pyplot as plt
import pandas as pd

file = '/Users/Freddy/PycharmProjects/GDELT:MoNA/mft_pathogen_jan.csv'

df = pd.DataFrame.from_csv(file)

#Do some filtering for wordcounts
df = df[df.wordcount < 1800]
df = df[df.wordcount > 500]

#select specific source locations:
location = 'IN'
df = df[df.source_location == location]

#select specific sources:

#Order mfts inside df
cols = df.columns.tolist()
mft_cols = cols[6:17]
cols = cols[:6] + [cols[6]] + cols[9:17] + [cols[7]] + [cols[8]] + cols[17:]
df = df[cols]

#rename MFT variables
mft_vars = ['c25.{}'.format(i) for i in range(1,12)]
mft_names = ['HarmVirtue', 'HarmVice', 'FairnessVirtue', 'FairnessVice','IngroupVirtue', 'IngroupVice', 'AuthorityVirtue', 'AuthorityVice','PurityVirtue', 'PurityVice', 'MoralityGeneral']
newcols = dict(zip(mft_vars, mft_names)) #create dictionary that contains new columns names
df.rename(columns=newcols, inplace=True)


corrtable = df.corr()

# check correlation between any two variables with dict-style keys
"""corrtable['mft_sum']['tone']
corrtable['pct_mft_words']['tone']"""


# use some string tricks to quickly pick out the columns we want
theme_cols = [c for c in corrtable.columns if c.isupper() and c != 'ID']
mft_cols = [c for c in corrtable.columns if not c.isupper() and not c.islower()]

# plot stuff
# first correlations of MFT variables by theme
# passing colormap="Paired" makes bars for pairs of MFT foundations look similar (matplotlib builtin)
corrtable[mft_cols].select(lambda c: c in theme_cols).plot(kind="bar",grid=True,colormap="Paired")

#Define notes for figure
plt.title('mft_pathogen_jan_correlations_between_theme_mfts')
plt.ylabel("Correlations with MFTs")
plt.xlabel("GDELT_News_Themes")
plt.text(0, .15, 'TimePeriod:January2017\nSources: AllWhitelist\nSourceLocation:%s' %(location))
plt.show()


# correlations of tone with themes and MFT variables
corrtable['tone'].select(lambda c: c in theme_cols or c in mft_cols).plot(kind="bar",grid=True)
plt.title('mft_pathogen_jan_jan_correlations_between_tone_themes_mfts')
plt.ylabel("Correlations with Tone")
plt.text(0, .15, 'TimePeriod:January2017\nSources: AllWhitelist\nSourceLocation:%s' %(location))
plt.show()