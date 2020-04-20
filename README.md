# Document retrieval System From Scratch
Implementation of an Information retrieval system with multiple functions(query expansion, different languages, and showing overview of the retrieved documents) from scratch 


## index.py
Script index.py creates an index from a collection of plain text documents. The script takes two input parameters: -d input-file -i output-index-directory. The input file is in CSV format.

### Usage:
Usage of the interactive command line interface:

```
python index.py -d Full-Economic-News-DFE-839861.csv -i index

arguments:
  -d input-file 
  -i output-index-directory.
```

## retrieve.py
Script retrieve.py uses an index created by the indexing script for the input query. The index directory is a directory created by the indexing script, which should contain all the files which script requires. On the output, there should be a list of the ids of the documents, which contain at least one query term, sorted according to their cosine distance on the TF-IDF scores from the query and the calculated scores.

```
python retrieve.py -x -l -e -s -i Index/ -q "Compra de inversionistas extranjeros"

arguments:
  -i index-directory 
  -q “query words”
  -l linguistic-based/dictionary query expansion methods. 
  -e embeddings-based query expansion methods. 
  -x if you query is spanish (don't include if query is English)
  -s Only show the results for top 10 documents with snippet
```
## utils.py
Implementation of Porter stemmer from scratch

## Word_Embedding.py
Implementation of query expansion method based on word embeddings

## Full-Economic-News-DFE-839861.csv, all_text.txt, past_tense_and_plural.txt.
The input file I used is [Full-Economic-News-DFE-839861.csv](https://data.world/crowdflower/economic-news-article-tone), which  is in CSV format.
all_text.txt is concatenation of the "text" column in the input file, which is used to train word embeddings.

past_tense_and_plural.txt is a hash table for the irregular plurality and past tense verb.



