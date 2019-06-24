f=open("graph_BPI_2015_ridotto2.txt", "r")
f1=open("graph_BPI_2015_ridotto2_trace.txt", "w")
for line in f:
  if("trace" in line):
    f1.write(line.split(" ")[0]+"\n")
f1.close()
print("fine")