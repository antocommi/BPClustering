import numpy as np
import matplotlib.pyplot as plt

logName="BPIC15GroundTruth"
clustering=["KMeans", "GMM", "SVM", "T2VH", "RandomForest", "DecisionTree", "LogisticRegression"]
embed=["Trace2Vec", "Node2Vec", "NGrams"]
colors=['tab:blue', 'tab:red', 'tab:green', 'tab:brown', 'tab:grey']

def plotAll():
    for emb in embed:
        plot(emb)

def plot(emb):
    x, y = getXY(emb)
    fig, ax = plt.subplots(2, 4, figsize=(16, 12), dpi=80)
    fig.suptitle(emb, fontsize=16)
    plt.gcf().canvas.set_window_title(emb)

    for alg in range(len(clustering)):
        cluster=getCluster(clustering[alg], emb)
        xs, ys=separe(x, y, cluster)
        for i in range(5):
            ax[alg//4, alg%4].scatter(xs[i], ys[i], c=colors[i], label=colors[i], alpha=0.3, edgecolors='none')

        ax[alg//4, alg%4].legend()
        ax[alg//4, alg%4].grid(True)
        ax[alg//4, alg%4].set_title(clustering[alg])

    real=getReal()
    xs, ys=separe(x, y, real)
    for i in range(5):
        ax[1, 3].scatter(xs[i], ys[i], c=colors[i], label=colors[i], alpha=0.3, edgecolors='none')
    ax[1, 3].legend()
    ax[1, 3].grid(True)
    ax[1, 3].set_title("Real")

    plt.show()

def separe(x, y, cluster):
    if not(len(x)==len(y)==len(cluster)):
        print("bad dimensions")
        return
    xs=[[], [], [], [], []]
    ys=[[], [], [], [], []]
    for i in range(len(x)):
        ind=cluster[i]
        xs[ind].append(x[i])
        ys[ind].append(y[i])
    return xs, ys

def getXY(emb):
    f1=open("toBePlotted/"+logName+"_"+emb+".vectors", "r")
    x=[]
    y=[]
    for line in f1:
        l=line.split(" ")
        if len(l)>1:
            x.append(float(l[0]))
            y.append(float(l[1]))
    return np.array(x), np.array(y)

def getCluster(alg, emb):
    f1=open("toBePlotted/"+logName+"_"+emb+"_"+alg+".clusters", "r")
    x=[]
    for line in f1:
        x.append(int(line))
    return np.array(x)

def getReal():
    f1=open("input/"+logName+".real", "r")
    x=[]
    for line in f1:
        x.append(int(line.split(",")[1]))
    return np.array(x)