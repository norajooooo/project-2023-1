import numpy as np
import matplotlib.pyplot as plt
import csv

f=open('/home/d06/Downloads/RANSAC_data.csv')
rdr=csv.reader(f)
dt=[]
for line in rdr:
    x_dt=float(line[0])
    y_dt=float(line[1])
    dt.append([x_dt,y_dt])
f.close()
data=np.array(dt)

def ransac_line_fitting(data,n_iterations=100,threshold=1,min_inliers=10):
    best_fit=None
    best_error=np.inf
    best_inliers=None
    for i in range(n_iterations):
        sample=data[np.random.choice(data.shape[0],2,replace=False),:]
        x1,y1=sample[0]
        x2,y2=sample[1]
        a=(y2-y1)/(x2-x1)
        b=y1-a*x1
        dist=np.abs(a*data[:,0]-data[:,1]+b/np.sqrt(a**2+1))
        inliers=data[dist<threshold]
        if len(inliers)>=min_inliers:
            error=np.sum(dist**2)
            if error<best_error:
                best_fit=(a,b)
                best_error=error
                best_inliers=inliers
    return best_fit, best_inliers

model,inliers=ransac_line_fitting(data,n_iterations=100,threshold=1,min_inliers=10)