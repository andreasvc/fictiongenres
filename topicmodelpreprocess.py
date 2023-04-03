import os
from glob import glob
from tqdm import tqdm
import pandas as pd
from syntok.tokenizer import Tokenizer


def chunks(tokens, chunksize):
	"""Split a list into chunks of ``chunksize`` tokens each."""
	for n in range(0, len(tokens), chunksize):
		yield tokens[n:n + chunksize]


def main(chunksize=1000):
	md = pd.read_csv('metadata-pg-genres-subset.tsv', sep='\t')
	ids = set(md['id'])
	with open('sw_jockers.txt') as inp:
		stopwords = set(inp.read().splitlines())
	stopwords.update('.,?!:;-_&%$*#+=()[]/"\'')
	stopwords.update({'--', '---', '...',
			"'s", "'t", "'m", "n't", "'ve", "'ll", "n't", "'re", "'d"})
	tok = Tokenizer(replace_not_contraction=False)
	with open('chunkedcorpus.txt', 'w', encoding='utf8') as out:
		with open('gutenberg-clean.ol', encoding='utf8') as inp:
			for line in tqdm(inp):
				name, text = line.split('\t', 1)
				if name not in ids:
					continue
				text = text.lower().replace('--', ' -- ')
				tokens = [token.value for token in tok.tokenize(text)
						if token.value not in stopwords
						and not token.value.isnumeric()]
				for n, chunk in enumerate(chunks(tokens, chunksize)):
					out.write('%s_%d\t%s_%d\t%s\n' % (
							name, n, name, n, ' '.join(chunk)))


if __name__ == '__main__':
	main()
