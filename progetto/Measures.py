import sklearn.metrics
import numpy as np
import matplotlib.pyplot as plt
import plotly 
import pandas as pd

class ClusteringMeasures:
    
    def __init__(self):
        self.clusters_types = {}

    # Questo metodo calcola i vari score di una tecnica di clustering
    # y_true : cluster reale 
    # y_pred : cluster calcolato
    # name_cluster_type : nome identificativo della tecnica di clusterizzazione (Es: KMeans, ecc...)  
    def compute_scores(self, y_true, y_pred, name_cluster_type):
        scores = {}
        # MISURE DA CONTROLLARE 
        scores["precision"] = sklearn.metrics.precision_score(y_true,y_pred,average='micro')
        scores["recall"] = sklearn.metrics.recall_score(y_true,y_pred,average='micro')
        scores["NMI"] = sklearn.metrics.normalized_mutual_info_score(y_true,y_pred,average_method='min')
        scores["F1"] = sklearn.metrics.f1_score(y_true,y_pred,average='micro')
        scores["adjRI"] = sklearn.metrics.adjusted_rand_score(y_true,y_pred)
        self.clusters_types[name_cluster_type] = scores
        return scores
    
    def plot_all(self):
        print("plot non implementato")
        # plt.figure()
        # df2 = pd.DataFrame(np.random.rand(1, 4), columns=['a', 'b', 'c', 'd'])
        # df2.plot.bar()
        # plt.axhline(0, color='k')


# m = ClusteringMeasures()
# a = np.array([2,3,4])
# b = np.array([2,4,5])
# scores = m.compute_scores(a,b,"prova")
# # a = np.array([2,3,4])
# # b = np.array([2,4,5])
# # scores = m.compute_scores(a,b,"prova2")
# # a = np.array([2,3,4])
# # b = np.array([2,4,5])
# # scores = m.compute_scores(a,b,"prova3")
# # a = np.array([2,3,4])
# # b = np.array([2,4,5])
# # scores = m.compute_scores(a,b,"prova4")
# m.plot_all()