fileName="BPIC15GroundTruth"
#per testare altri algoritmi basta aggiungerne il nome al vettore out sottostante
out=["KMeans", "GMM", "SVC", "T2VH", "RandomForest"]

real=[[], []]
text_file = open("input/"+fileName+".real", "r")
for line in text_file.readlines():
    for col in range(len(real)):
        real[col].append(int(line.split(",")[col]))

counter=[0]*len(out)
max=[0]*len(out)
for i in range(len(out)):
    text_file = open("output/"+fileName+"T2VVS16"+out[i]+".csv", "r")
    for line in text_file.readlines():
        val=line.split(",")
        for id in range(len(real[0])):
            if(real[0][id]==int(val[0])):
                if(real[1][id]==int(val[1])):
                    counter[i]+=1
                if(int(val[1])>max[i]):
                    max[i]=int(val[1])
                break

print("# trace:", len(real[0]))
print("\t", end="")
print(out)
print("equals\t", end="")
print(counter)
print("max\t", end="")
print(max)