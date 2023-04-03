import pandas as pd
from sklearn import decomposition, manifold

dtm = pd.read_csv('lda/doctopics_pertext.tsv.gz', sep='\t', index_col=0)

# Creating topic_scaled.csv (2D coordinates for topics)
reducer = decomposition.PCA(n_components=99)
pcared = pd.DataFrame(
		reducer.fit_transform(dtm.T))
reducer2 = manifold.MDS(n_components=2, dissimilarity='euclidean', metric=False)
pcared = pd.DataFrame(
		reducer2.fit_transform(pcared.values))
pcared.to_csv('topic_scaled.csv', header=False, index=False)

# Creating per-chunk metadata file
df = pd.read_csv('metadata-pg-genres-subset.tsv', sep='\t')
genres = ['Western', 'Adventure', 'Love', 'War', 'Humour', 'Sea',
		'Pulp fiction', 'SciFi & Fantasy', 'General fiction',
		'Mystery & Detective stories', 'Juvenile', 'Translations']
df['subject'] = [
		', '.join(genre for genre in genres if df.at[pgid, genre])
		for pgid in df.index]
# df['author.x'] = df['author.x'].str.split(' \\(').str[0]
# The columns expected by https://github.com/agoldst/dfr-browser
cols = [
	'id',                   # DOI
	'title',                # title
	'author',               # author(s)
	'subject',              # journal title
	'downloads',            # volume
	'language',             # issue
	'year-ref',             # publication date (ISO 8601)
	'year-birth'            # page range
	]
df = df.loc[:, cols]
df.to_csv('meta.csv', float_format='%g', index=True, header=False)
