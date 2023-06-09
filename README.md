# Code and data for the chapter "Computational Methods for the Analysis of Fiction Genres"

The Project Gutenberg metadata is from: https://github.com/dh-trier/pg-fiction/

The genre labels were selected using `makelabels.py`.

The cleaned corpus with Project Gutenberg texts is available here:
http://corpus.leeds.ac.uk/serge/webgenres/gutenberg-clean.ol.xz

The topic model was created using Mallet: https://mimno.github.io/Mallet/
See `lda.sh`.

The list of stop words and names `sw_jockers.txt` (included here for reproducibility)
comes from https://www.matthewjockers.net/2013/04/12/secret-recipe-for-topic-modeling-themes/

An interactive browser of the topic model is available here: https://urd2.let.rug.nl/~andreas/lorentztopics/

The data for the topic model browser is generated by `convmeta.py`; the topic model browser is https://github.com/agoldst/dfr-browser

The Biber features were extracted using https://github.com/ssharoff/biberpy

Readability features were extracted using https://github.com/andreasvc/readability/

