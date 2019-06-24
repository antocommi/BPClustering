f1=open("../progetto/input/BPIC15GroundTruth_ridotto2.xes", "r")
f2=open("../progetto/input/BPIC15GroundTruth_ridotto2.graph.real", "w")
traceID=0
newTrace=False
for line in f1:
    if("<trace>" in line):
        newTrace=True
    if(newTrace & ("cluster:label" in line)):
        cluster=line[line.index("value"):]
        cluster=cluster[cluster.index("=")+2:]
        cluster=cluster[:cluster.index("/")-1]
        cluster=int(cluster)-1
        cluster=str(cluster)
        f2.write("trace_"+str(traceID)+","+cluster+"\n")
        newTrace=False
        traceID+=1
f2.close()

f1=open("../progetto/input/BPIC15GroundTruth_ridotto2.xes", "r")
f2=open("../progetto/input/BPIC15GroundTruth_ridotto2.real", "w")
newTrace=False
newEvent=False
for line in f1:
    if("<trace>" in line):
        newTrace=True
    if(("concept:name" in line) & newTrace):
        id=line[line.index("value"):]
        id=id[id.index("=")+2:]
        id=id[:id.index("/")-1]
        f2.write(id+",")
        newTrace=False
        newEvent=True
    if(newEvent & ("cluster:label" in line)):
        cluster=line[line.index("value"):]
        cluster=cluster[cluster.index("=")+2:]
        cluster=cluster[:cluster.index("/")-1]
        cluster=int(cluster)-1
        cluster=str(cluster)
        f2.write(cluster+"\n")
        newEvent=False
        traceID+=1
f2.close()