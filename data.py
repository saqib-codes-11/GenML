import pandas
#import './genius_api.py'
import math  
import caret
import numpy as np

# Turn file into dataframe!
f = './data.csv'
df = pandas.read_csv(f)

# Shuffle dataframe!
df = df.sample(frac=1)


msk = np.random.rand(len(df)) < 0.7
train = df[msk]
test = df[~msk]

train.to_csv('./train.csv')
test.to_csv('./test.csv')


f = './test.csv'
df = pandas.read_csv(f)
median = df['Total_Votes'].median()

df['Class'] = df['Total_Votes']

for x in df['Total_Votes']:
	if x>=median:
		df['Class'] = "High"
	else:
		df['Class'] = 'Low' 