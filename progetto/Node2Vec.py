import gensim
import loadXES
import networkx as nx
from node2vec import Node2Vec

def learn(folderName, vectorsize):
    #---------------------------------------------------------
    graph = nx.read_edgelist("input/"+folderName+".graph", nodetype=str, create_using=nx.DiGraph())
    for edge in graph.edges():
        graph[edge[0]][edge[1]]['weight'] = 1

    graph = graph.to_undirected()
    #---------------------------------------------------------

    # Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
    node2vec = Node2Vec(graph, dimensions=vectorsize, walk_length=30, num_walks=200, workers=8)  # Use temp_folder for big graphs

    # Embed nodes
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    
    # Save embeddings for later use
    model.save('output/'+folderName+'N2VVS'+str(vectorsize) +'.model')
    model.wv.save_word2vec_format('output/'+folderName+ 'N2VVS'+str(vectorsize) + '.node2vec')

def startCluster(folderName, vectorsize):
    model= gensim.models.Doc2Vec.load('output/'+folderName+'N2VVS'+str(vectorsize) +'.model')

    corpus=getTrace(folderName)
    vectors = []
    print("inferring vectors")
    for line in corpus:
        inferred_vector = model.wv[line]
        vectors.append(inferred_vector)
    print("done")
    return vectors, corpus

def endCluster(folderName, assigned_clusters, vectorsize, clusterType, corpus):
    trace_list = getTrace(folderName)
    clusterResult= {}
    for doc_id in range(len(corpus)):
        clusterResult[trace_list[doc_id]]=assigned_clusters[doc_id]

    resultFile= open('output/'+folderName+'N2VVS'+str(vectorsize)+clusterType+'.csv','w')
    for doc_id in range(len(corpus)):
        resultFile.write(trace_list[doc_id]+','+str(assigned_clusters[doc_id])+"\n")

    resultFile.close()
    print("done with " , clusterType , " on event log ", folderName)

def getY(folderName):
    text_file = open("input/"+folderName+".graph.real", "r")
    y=[]
    for line in text_file.readlines():
        y.append(int(line.split(",")[1]))
    return y

def getTrace(folderName):
    text_file = open("input/"+folderName+".graph.real", "r")
    y=[]
    for line in text_file.readlines():
        y.append(line.split(",")[0])
    return y