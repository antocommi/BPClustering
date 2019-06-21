import Trace2Vec

logName='BPIC15GroundTruth'
vectorsize=16
#Trace2Vec.learn(logName,vectorsize)

#Trace2Vec.cluster(logName,vectorsize,"KMeans")
#Trace2Vec.cluster(logName,vectorsize,"GMM")
#Trace2Vec.cluster(logName,vectorsize,"SVC")
#Trace2Vec.cluster(logName,vectorsize,"T2VH")
Trace2Vec.cluster(logName,vectorsize,"RandomForest")