from nltk import word_tokenize
from collections import defaultdict
from pathlib import Path
import time
import os
import pickle

import pygtrie

TRIE_FILE = 'trie.p'
ID_2_DOC_PATH_FILE = 'doc_id_to_path.csv'
WORD_DOC_MAP_FILE = 'w_docs'

def word_doc_id_file(word):
    return os.path.join(WORD_DOC_MAP_FILE, word)

def tokenize(text, case_sensitive=True):
    tokens = word_tokenize(text)
    words = [word for word in tokens if word.isalpha()]
    if not case_sensitive:
        words = [word.lower() for word in words]

    return words

def document_to_freq(text, case_sensitive=True):
    words = tokenize(text)
    w_freq = defaultdict(int)
    for word in words:
        w_freq[word] = 1
        trie[word] = True

    return w_freq

def index_documents():
    c = 0
    pathlist = Path('maildir').glob('**/*.*')

    doc_id_to_path = {}
    w_docs = defaultdict(list)
    for i, path in enumerate(pathlist):
        path = str(path)
        if 'DS_Store' in path:
            continue

        doc_id_to_path[i] = path
        with open(path, 'r', encoding="utf8", errors='ignore') as f:
            doc = f.read()
            w_freq = document_to_freq(doc)
            for w in w_freq:
                w_docs[w].append(i)

        if i%1000 == 0:
            print (c, len(w_docs))

        if i > 100000:
            break

    return w_docs, doc_id_to_path


if __name__ == "__main__":
    # index documents and build trie
    t = time.time()
    trie = pygtrie.CharTrie()
    w_docs, doc_id_to_path = index_documents()
    print(time.time() - t)

    os.mkdir(WORD_DOC_MAP_FILE)

    # write word -> documents to files
    t = time.time()
    for w in w_docs:
        with open(word_doc_id_file(w), 'w') as f:
            for item in w_docs[w]:
                f.write("%s\n" % item)

    # write id -> doc path map to file
    with open(ID_2_DOC_PATH_FILE, 'w') as f:
        for id, path in doc_id_to_path.items():
            f.write("{},{}\n".format(id, path))
    print(time.time() - t)

    t = time.time()
    pickle.dump(trie, open(TRIE_FILE, "wb"))
    print(time.time() - t)
