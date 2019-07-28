import pickle
import os
import argparse
import time

from index import word_doc_id_file, TRIE_FILE, ID_2_DOC_PATH_FILE

parser = argparse.ArgumentParser()
parser.add_argument("prefix")
args = parser.parse_args()
prefix = args.prefix

# load id2docpath and trie
with open(ID_2_DOC_PATH_FILE, 'r') as f:
    lines = f.read().splitlines()
    id_2_doc_path = {l.split(',')[0]: l.split(',')[1] for l in lines}

print (id_2_doc_path)
trie = pickle.load(open(TRIE_FILE, "rb"))

t = time.time()
# get doc indexes that prefix shows up in
indexes = set()
for key in trie.keys(prefix):
    with open(word_doc_id_file(key), 'r') as f:
        indexes |= set(f.read().splitlines())

print(indexes)
doc_paths = [id_2_doc_path[i] for i in indexes]
for p in doc_paths:
    with open(p, 'r') as f:
        print(f.read())
        break

print("Actual processing:", time.time() - t)
