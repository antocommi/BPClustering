f=open("karate.emb", "r")
f1=open("karate.trace.emb", "w")
dic={}
for line in f:
    if("trace_" in line):
        id=line[6:]
        id=id[:id.index(" ")]
        dic[id]=line
c=0
while(len(dic)>0):
    if(str(c) in dic):
        f1.write(dic[str(c)])
    del dic[str(c)]
    c+=1
f1.close()
f.close()