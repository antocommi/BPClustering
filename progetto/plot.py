from pandas.plotting import parallel_coordinates 
import pandas as pd
import matplotlib.pyplot as plt
from yellowbrick.features import RadViz
from sklearn.manifold import MDS
import seaborn as sns 
from pandas.plotting import scatter_matrix

def plot():
    plotted_trace=10
    colors = ('#ff1e00','#fffb17','#2dff0d','#0dffff','#fb00ff')
    color_column = 'cluster'
    data = pd.read_csv('transformed2.csv')
    data.drop(columns='trace_name', inplace=True)
    features = [ i for i in data.keys()[:-1]]
    classes = [0,1,2,3,4]
    
    
    ## PLOT TIPO 1 
    # plt.figure()
    # parallel_coordinates(data.head(n=plotted_trace), color_column, data.columns[3:6],color=colors)
    # plt.show()

    # # PLOT TIPO 2 
    # X = data[features[0:]]
    # X = X.transform(lambda x:x*20000)
    # y = data['cluster']
    # # Instantiate the visualizer
    # visualizer = RadViz(classes=classes, features=features, alpha=0.5)
    # visualizer.fit(X, y)      # Fit the data to the visualizer
    # visualizer.transform(X)   # Transform the data
    # visualizer.poof()         # Draw/show/poof the data

    ## PLOT TIPO 3
    # scatter_matrix(data, alpha = 0.2, figsize = (6, 6), diagonal = 'kde' )
    # plt.show()

plot()