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
x=data[:,0]
y=data[:,1]

def fit_quad_RANSAC(x,y,n_iterations=100,threshold=0.1):
    best_score=0
    best_coeff=None
    for i in range(n_iterations):
        sample_indices=np.random.choice(len(x),size=3,replace=False)
        sample_x=x[sample_indices]
        sample_y=y[sample_indices]
        x=np.column_stack([sample_x**2,sample_x,np.ones(3)])
        coeff=np.linalg.lstsq(y,sample_y,rcond=None)[0]
        dist=np.abs(x-np.polyval(coeff,sample_x))
        inliers=dist<threshold
        num_inliers=np.count_nonzero(inliers)
        if num_inliers>best_score:
            best_score=num_inliers
            best_coeff=coeff
            
    return tuple(best_coeff)

a,b,c=fit_quad_RANSAC(x,y)
fig,ax=plt.subplots()
ax.scatter(x,y,color='blue')
ax.plot(x,a*x**2+b*x+c,color='red')
plt.show()