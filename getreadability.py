"""Obtain readability scores for all texts in corpus, produce .csv file."""
import pandas as pd
import readability
import syntok.segmenter as segmenter
from tqdm import tqdm

def tokenize(text):
	tokenized = '\n\n'.join(
			'\n'.join(' '.join(token.value for token in sentence)
				for sentence in paragraph)
			for paragraph in segmenter.analyze(text))
	return tokenized


def main():
	subset = pd.read_csv(
			'metadata-pg-genres-subset.tsv', sep='\t', index_col='id').index
	names = []
	results = []
	with open('gutenberg-clean.ol', encoding='utf8') as inp:
		lines = (line for line in inp if line[:line.index('\t')] in subset)
		for line in tqdm(lines, 'Getting readability scores', total=len(subset)):
			name, text = line.split('\t', 1)
			if not text.strip():
				continue
			text = tokenize(text)
			try:
				result = readability.getmeasures(text, lang='en', merge=True)
			except ValueError:
				continue
			names.append(name)
			results.append(result)
	df = pd.DataFrame(results, index=names)
	df.to_csv('readability.csv')


if __name__ == '__main__':
	main()
