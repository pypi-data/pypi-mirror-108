import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
data=pd.read_csv("new_deaths.csv")
def main(country="Japan",days=440, degree=5):
 n=len(data[country])
 y=data[country][n-days:n]
 for i in y:
  print(i)
 x=np.arange(n-days,n)
 valid = ~(np.isnan(x) | np.isnan(y))
 model=np.poly1d(np.polyfit(x[valid],y[valid],degree))
 date=data['date'][n-1]
 x1=np.arange(n-days,n+7)
 y1=model(x1)
 ny1=[]
 for i in y1:
  if i<0:i=0
  ny1.append(i)
 plt.plot(x,y,'k')
 plt.plot(x1,ny1,'b')
 plt.legend(['daily deaths in '+str(country),str(days)+' days from '+str(date)+' '+str(degree)+'th'])
 plt.savefig(country+".png")
 plt.show()
country=""
days=440
degree=5
if len(sys.argv)==1:
 print('country name is needed!')
 sys.exit()
if len(sys.argv)==2:
 if sys.argv[1] in data.columns:
  country=str(sys.argv[1])
 else:
  print('correct country name!')
  sys.exit()
if len(sys.argv)==3:
 if sys.argv[1] in data.columns:
  country=str(sys.argv[1])
  if int(sys.argv[2])>len(data[country]):
   print('use smaller days')
   sys.exit()
  else:
   days=int(sys.argv[2])
 else:
  print('correct country name')
  sys.exit()
if len(sys.argv)==4:
 if sys.argv[1] in data.columns:
  country=str(sys.argv[1])
  if int(sys.argv[2])>len(data[country]):
   print('use smaller days')
   sys.exit()
  else:
   days=int(sys.argv[2])
   if int(sys.argv[3]) > 4:
    degree=int(sys.argv[3])
   else:
    print('use higher degree number')
    sys.exit()
 else:
  print('correct country name')
  sys.exit()
  
main(country,days,degree)
 
