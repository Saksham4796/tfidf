import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv


start=datetime.now()
with open('statementResult.csv','r') as in_file, open('uniqueResult.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)
t1= (datetime.now() - start)


cwd =os.getcwd()
version=cwd.split("/")[-1]
program_name=cwd.split("/")[-2].split("_")[0]
print(cwd)
str_cwd=cwd.replace("/"+version,"")
print(str_cwd)
f_l=0

start_time=datetime.now()

with open('faultyLine.txt') as f:
    f_l = f.readline()

print("**************")
print(f_l)
print("**************")

f_l=int(f_l)
df_train=pd.read_csv('uniqueResult.csv')

#training output dataset
y = np.array([df_train['Result']]).T
y=y.tolist()
#print y

#training input dataset
df_train.drop(['Result'],1 , inplace=True)
t_in = df_train.values.tolist()
x = np.array(t_in)
x=x.tolist()
#print len(y[0])
total_failed=np.count_nonzero(y)
total_passed=len(y)-total_failed

suspicious=[]
#print len(y)
#print len(x[0])
#print total_passed,total_failed


for i in range(0,len(x[0])):
	nsuccess=0
	nfailure=0
	for j in range(0,len(y)):
		#print x[j][i],y[j][0]
		if x[j][i]==1 and y[j][0]==0:
			nsuccess=nsuccess+1
		elif x[j][i]==1 and y[j][0]==1:
			nfailure=nfailure+1
	try:
		
		#print nfailure,nsuccess
		if total_failed!=0:
			fail_score=float(nfailure)/float(total_failed)
		if total_passed!=0:
			pass_score=float(nsuccess)/float(total_passed)
		sus_score=fail_score/(fail_score+pass_score)
		suspicious.append(sus_score)
		print(str(i)+"   "+str(sus_score))
	except ZeroDivisionError:
		suspicious.append(0)

d = {}
for i in range(0,len(suspicious)):
	key = float(suspicious[i])
	#print key
	if key !=0:
		if key not in d:
			d[key] = []
		d[key].append(i)

ct1=0
ct2=0
ct3=0
fct=0
print("Faulty line:"+str(f_l))
for x in sorted(d):
	print (x,len(d[x]))
	if f_l not in d[x] and fct==0:
		ct1=ct1+len(d[x])
	elif f_l not in d[x] and fct==1:
		ct3=ct3+len(d[x])
	else: 
		fct=1
		ct2=len(d[x])
print("We have to search "+str(ct3+1)+" to "+str(ct3+ct2))


end_time=datetime.now()
csvfile=open(str_cwd+"/tarantula_unique.csv", "a+")
spamwriter1 = csv.writer(csvfile, delimiter=',')
stmt_complex=[]
stmt_complex.append(program_name);
stmt_complex.append(str(version));
#stmt_complex.append(str(sys.argv[1]));
stmt_complex.append(f_l);
stmt_complex.append(str(ct3+1));
stmt_complex.append(ct2+ct3);
stmt_complex.append(start_time);
stmt_complex.append(end_time);
stmt_complex.append(end_time-start_time);
stmt_complex.append(end_time-start_time+t1);
stmt_complex.append(total_passed);
stmt_complex.append(total_failed);
spamwriter1.writerow(stmt_complex);


