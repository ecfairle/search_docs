from nltk import word_tokenize
from collections import defaultdict
from pathlib import Path
import time
import os
import pickle

import pygtrie

documents = ["hi my name is eugene", "index this document"]

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
    for path in pathlist:
        path = str(path)
        if 'DS_Store' in path:
            continue

        doc_id_to_path[c] = path
        with open(path, 'r', encoding="utf8", errors='ignore') as f:
            doc = f.read()
            w_freq = document_to_freq(doc)
            for w in w_freq:
                w_docs[w].append(c)

        c+=1
        if c%1000 == 0:
            print (c, len(w_docs))

        if c > 100:
            break

    return w_docs, doc_id_to_path


t = time.time()
trie = pygtrie.CharTrie()
w_docs, doc_id_to_path = index_documents()
print(time.time() - t)

index_dir = 'w_docs'
os.mkdir(index_dir)

t = time.time()
for w in w_docs:
    with open(os.path.join(index_dir, w), 'w') as f:
        for item in w_docs[w]:
            f.write("%s\n" % item)

with open('doc_id_to_path.csv', 'w') as f:
    for id, path in doc_id_to_path.items():
        f.write("{},{}\n".format(id, path))

t = time.time()
pickle.dump(trie, open( "trie.p", "wb" ))
print(time.time() - t)
