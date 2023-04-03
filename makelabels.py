import pandas as pd

df = pd.read_csv('metadata-fiction+worldcat+heuristics+fixes.csv', sep='\t')

# Format: label, followed by list of subjects, ending with empty line.
selection = """
Western
Western stories

Adventure
Adventure stories

Love
Love stories

War
War stories

Humour
Humorous stories

Sea
Sea stories

Pulp fiction
Dime novels

SciFi & Fantasy
Science fiction
Human-alien encounters -- Fiction
Fantasy fiction

General fiction
Fiction
Historical fiction
England -- Fiction
English fiction -- 19th century
Young women -- Fiction
Domestic fiction
Psychological fiction
Inheritance and succession -- Fiction
England -- Social life and customs -- 19th century -- Fiction
England -- Social life and customs -- Fiction
London (England) -- Fiction
Bildungsromans
New York (N.Y.) -- Fiction
Families -- Fiction
Political fiction
World War, 1914-1918 -- Fiction

Mystery & Detective stories
Mystery fiction
Mystery and detective stories
Detective and mystery stories

Juvenile
Children's stories
Conduct of life -- Juvenile fiction
Friendship -- Juvenile fiction
Children -- Conduct of life -- Juvenile fiction
Christian life -- Juvenile fiction
Animals -- Juvenile fiction
Adventure and adventurers -- Juvenile fiction
Voyages and travels -- Juvenile fiction
Brothers and sisters -- Juvenile fiction
Girls -- Juvenile fiction
Boys -- Juvenile fiction
Orphans -- Juvenile fiction
Youth -- Conduct of life -- Juvenile fiction
Schools -- Juvenile fiction
Families -- Juvenile fiction

Translations
German fiction -- Translations into English
French fiction -- Translations into English
"""

genres = {chunk.splitlines()[0]: set(chunk.splitlines()[1:])
		for chunk in selection.strip().split('\n\n')}
dfsubjects = [eval(subjects) for subjects in df['subjects']]
for genre, subjects in genres.items():
	df[genre] = [
			0 if len(subjects & x) == 0 else 1
			for x in dfsubjects]
subset = df.loc[
		(df.loc[:, ['Western',
       'Adventure', 'Love', 'War', 'Humour', 'Sea', 'Pulp fiction',
       'SciFi & Fantasy', 'General fiction', 'Mystery & Detective stories',
       'Juvenile', 'Translations']].sum(axis=1)>0)
		& (df['year-ref'] > 1870),
		:]
subset.to_csv('metadata-pg-genres-subset.tsv', sep='\t', index=False)
