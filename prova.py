import networkx as nx
from node2vec import Node2Vec

EMBEDDING_FILENAME="out"
EMBEDDING_MODEL_FILENAME="model"
EDGES_EMBEDDING_FILENAME="edge"
INPUT_FILENAME="graph utils/graph_BPI_2015_ridotto2.txt"

#---------------------------------------------------------
graph = nx.read_edgelist(INPUT_FILENAME, nodetype=str, create_using=nx.DiGraph())
for edge in graph.edges():
  graph[edge[0]][edge[1]]['weight'] = 1

graph = graph.to_undirected()
#---------------------------------------------------------
# Create a graph
#graph = nx.fast_gnp_random_graph(n=100, p=0.5)

# Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
node2vec = Node2Vec(graph, dimensions=16, walk_length=30, num_walks=200, workers=8)  # Use temp_folder for big graphs

# Embed nodes
model = node2vec.fit(window=10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)

# Look for most similar nodes
#model.wv.most_similar('2')  # Output node names are always strings

# Save embeddings for later use
model.wv.save_word2vec_format(EMBEDDING_FILENAME)

# Save model for later use
#model.save(EMBEDDING_MODEL_FILENAME)

print("inizio parte mia")

corpus=open("graph utils/graph_BPI_2015_ridotto2_trace.txt", "r")
vectors = []
NUM_CLUSTERS= 5
print("inferring vectors")
for line in corpus:
  print(model.wv.most_similar(line[:-1]))
  inferred_vector = model.wv[line[:-1]]
  vectors.append(inferred_vector)

print("done")
    
# Embed edges using Hadamard method
from node2vec.edges import HadamardEmbedder

edges_embs = HadamardEmbedder(keyed_vectors=model.wv)

# Get all edges in a separate KeyedVectors instance - use with caution could be huge for big networks
edges_kv = edges_embs.as_keyed_vectors()

# Look for most similar edges - this time tuples must be sorted and as str
edges_kv.most_similar(str(('1', '2')))
print(edges_kv.most_similar(str(('1', '2'))))
print(edges_kv.most_similar("trace_0"))

# Save embeddings for later use
edges_kv.save_word2vec_format(EDGES_EMBEDDING_FILENAME)