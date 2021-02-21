import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv


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
df_train=pd.read_csv('statementResult.csv')

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

stmt_complex=[]
csvfile=open("failed.csv", "w")
spamwriter1 = csv.writer(csvfile, delimiter=',')
print(len(x[0]))
for k in range(1, len(x[0])+1):
	stmt_complex.append(k);
spamwriter1.writerow(stmt_complex);
#stmt_complex=[]
#stmt_complex.append(program_name);
count=0
for i in y:
	stmt_complex=[]
	count=count+1
	if(i[0]==1):
		#print (x[count])
		for j in x[count]:
			stmt_complex.append(j);
		spamwriter1.writerow(stmt_complex);
