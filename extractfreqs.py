"""Extract (absolute) word counts from files

Selects MFW from training and extracts counts for those words from full set.
Resulting document-term frequencies has columns ordered by overall term
frequency in the training set."""
import os
import re
from glob import glob
import numpy as np
import pandas as pd
from sklearn import feature_extraction

CORPUSDIR = '../../data/literaryanxiety/'
MFW = 5000  # number of most frequent words to extract


def stripfn(fnames):
    """Return basename without extension."""
    return [os.path.splitext(os.path.basename(a))[0] for a in fnames]


def preprocessor(text):
    """Lowercase and normalize unicode punctuation to ASCII."""
    # U+2018 left single quotation mark
    # U+2019 right single quotation mark
    return re.sub(r"[\u2018\u2019]", "'", text).lower()


# A word is a sequence of letters (no digits),
# optionally including an apostrophe inside.
WORD_PATTERN = re.compile(r"\b[^\W\d]+(?:'[^\W\d]+)?\b", flags=re.UNICODE)
vec = feature_extraction.text.TfidfVectorizer(
            input='filename', max_features=MFW, use_idf=False,
            token_pattern=WORD_PATTERN, preprocessor=preprocessor)
high = sorted(glob(CORPUSDIR + 'High Literary Corpus/*.txt'))
pop = sorted(glob(CORPUSDIR + 'Pop Fiction Corpus/*.txt'))
relfreqs = vec.fit_transform(high + pop).toarray()

# sort columns of document-term matrix by frequency (highest first)
newindex = np.argsort(relfreqs.sum(axis=0))[::-1]
feature_names = vec.get_feature_names()
features = [feature_names[i] for i in newindex]

# extract absolute counts for selected features in whole corpus
newvec = feature_extraction.text.CountVectorizer(
            input='filename', vocabulary=features,
            token_pattern=WORD_PATTERN, preprocessor=preprocessor)
# now include the King books, but don't fit on them
king = sorted(glob(CORPUSDIR + 'King novels and novellas corpus/*.txt'))
counts = newvec.transform(king + high + pop).toarray()  # don't need to fit
df = pd.DataFrame(counts, index=stripfn(king + high + pop), columns=features)
categories = ['king'] * len(king) + ['high'] * len(high) + ['pop'] * len(pop)
df.insert(0, 'category_', categories)
df.to_csv('bow%d.csv' % MFW)
