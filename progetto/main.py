import Trace2Vec
import sklearn.metrics
import texttable
from texttable import Texttable

clustering=["KMeans", "GMM", "SVC", "T2VH", "RandomForest", "DecisionTree", "LogisticRegression"]
measure=["Precision", "Recall", "NMI", "F1", "RI"]
logName='BPIC15GroundTruth'
vectorsize=16

def main():
    # Trace2Vec.learn(logName,vectorsize)

    # for alg in clustering:
    #     Trace2Vec.cluster(logName, vectorsize, alg)

    scores=get_scores("Trace2Vec")
    print_scores(scores)

def compute_scores(y_true, y_pred):
    scores = {} 
    scores["Precision"] = sklearn.metrics.precision_score(y_true,y_pred,average='micro')
    scores["Recall"] = sklearn.metrics.recall_score(y_true,y_pred,average='micro')
    scores["NMI"] = sklearn.metrics.normalized_mutual_info_score(y_true,y_pred,average_method='min')
    scores["F1"] = sklearn.metrics.f1_score(y_true,y_pred,average='micro')
    scores["RI"] = sklearn.metrics.adjusted_rand_score(y_true,y_pred)
    return scores

def getDict(file):
    text_file = open(file, "r")
    vec={}
    for line in text_file.readlines():
        read=line.split(",")
        vec[read[0].strip()]=int(read[1])
    return vec

def get_scores(embedding):
    yD=getDict("input/"+logName+".real")
    table=[[embedding]+measure]

    for alg in clustering:
        y_predD=getDict("output/"+logName+"T2VVS16"+alg+".csv")
        y=[]
        y_pred=[]
        for trace in yD:
            y.append(yD[trace])
            y_pred.append(y_predD[trace])
        score=compute_scores(y, y_pred)
        line=[alg]
        for meas in measure:
            line.append(score[meas])
        table.append(line)
    print(table)
    return table

def print_scores(scores):
    t = Texttable()
    t.add_rows(scores)
    print(t.draw())

main()