import sys
import time
from datetime import datetime
start_time=datetime.now()
import pandas as pd
import numpy as np
import math
import os
import csv
import sklearn
from sklearn.metrics import matthews_corrcoef as mcc
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

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

M=len(y)
l=len(x[0])
N=[0 for z in range(0,len(y))]
for i in range(0,len(y)):
	for j in range(0,len(x[0])):
		if x[i][j]==1 :
			N[i]=N[i]+1

Df=[0 for z in range(0,M)]
for i in range(0,len(x[0])):
	for j in range(0,len(y)):
		if x[j][i]==1 :
			Df[i]=Df[i]+1

TFIDF=[[0 for i in range(l)] for j in range(M)]
for i in range(0,len(y)):
	for j in range(0,len(x[0])):
		TFIDF[i][j]= x[i][j]*(1.0/math.log10(N[i]))*math.log10(float(M)/(float(1+Df[j])))

I=np.identity(len(x[0]))

tfidf=np.array(TFIDF)
x_train=tfidf
y_train=np.array(y)

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical


# Initializing the ANN
classifier = Sequential()

# Adding the first hidden layer 
layer_info = Dense(units=l+10 ,activation='relu',input_dim=l)
classifier.add(layer_info)

# Adding second hidden layer
layer_info = Dense(units=l+10,activation='relu')
classifier.add(layer_info)

# Adding third hidden layer
layer_info = Dense(units=l+10,activation='relu')
classifier.add(layer_info)

# Adding output layer
layer_info = Dense(units=1,activation='sigmoid')
classifier.add(layer_info)


# Compiling the ANN
classifier.compile( loss='mean_squared_error',optimizer='adam', metrics=['accuracy'])

# Fitting the ANN to the training set
classifier.fit(x_train, y_train, epochs=200 , batch_size=100)
epochs=200
batch_size=100

x_test=I


# Predicting the Test set results
y_pred = classifier.predict(x_test)
print (y_pred)

for i in range(l):
	suspicious.append(y_pred[i])
 

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
csvfile=open(str_cwd+"/tfidf_v40.csv", "a+")
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
stmt_complex.append(total_passed);
stmt_complex.append(total_failed);
stmt_complex.append(epochs);
stmt_complex.append(batch_size)
spamwriter1.writerow(stmt_complex);



