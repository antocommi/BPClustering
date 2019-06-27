import itertools


def transform_file(filename, attributes):
    in_file = open(filename,'r')
    out_file = open("transformed.csv",'w')
    out_file.write( ','.join(attributes) +'\n')
    for line in in_file:
        l = ','.join(line.split(' '))
        out_file.write(l)
    
def addColumn(values, out_filename):
    out_file = open(out_filename,'r')
    new_file = open('transformed2.csv','w')
    for l,v in zip(out_file,values):
        l = l[:-2] + ',' + v
        if(l[-7:]=='cluster'):
                l=l + '\n'
        new_file.write(l)

vectorsize = 16
filename = 'output/BPIC15GroundTruth_ridotto2N2VVS16_trace.node2vec'
attributes = ['trace_name']
attributes += ['d']*vectorsize
for i in range(1,vectorsize+1):
    attributes[i] = attributes[i] + str(i) 

transform_file(filename, attributes)
values=["cluster"]
f = open('output/BPIC15GroundTruth_ridotto2N2VVS16KMeans.csv','r')
for l in f:
    values.append( l.split(',')[1] )

addColumn(values, "transformed.csv")