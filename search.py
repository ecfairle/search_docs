import pickle
import os
prefix = 'David'

with open('doc_id_to_path.csv', 'r') as f:
    lines = f.read().splitlines()
    id_2_doc_path = {l.split(',')[0]: l.split(',')[1] for l in lines}

print (id_2_doc_path)
trie = pickle.load(open( "trie.p", "rb" ))

index_dir = 'w_docs'
indexes = set()
for key in trie.keys(prefix):
    with open(os.path.join(index_dir, key), 'r') as f:
        indexes |= set(f.read().splitlines())

print(indexes)
doc_paths = [id_2_doc_path[i] for i in indexes]
for p in doc_paths:
    with open(p, 'r') as f:
        print(f.read())
        break
