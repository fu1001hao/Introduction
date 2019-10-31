import numpy as np
import open3d as o3d

N , s , thre = 10, 3, 5e-2

pcd = o3d.io.read_point_cloud("record_00348.pcd")
#o3d.visualization.draw_geometries([pcd])
data =np.asarray(pcd.points)

def Find_Plane(p1, p2, p3):
    
    x1 , y1, z1= p2[0]- p1[0], p2[1]- p1[1], p2[2]- p1[2]
    
    x2 , y2, z2= p2[0]- p3[0], p2[1]- p3[1], p2[2]- p3[2]
    
    b = (x1*y2 - x2*y1)/(z1*y2- z2*y1)
    
    a = (x1 - b*z1)/y1
    
    c = p1[0]-a*p1[1]-b*p1[2]
    
    return a, b, c

def Check(data, a, b, c, thre):
    
    count = 0
    
    for point in data:
        
        if np.abs(point[0]-a*point[1]-b*point[2]-c)< thre:
            
            count=count+1
            
    return count

def Draw(data, a, b, c, thre):
    
    Ps = []
    Outlier = []
    for point in data:
        
        if np.abs(point[0]-a*point[1]-b*point[2]-c)< thre:
            
            Ps.append(point)
        
        else:
            Outlier.append(point)
            
    return np.array(Ps), np.array(Outlier)


num = -1
for i in range(N):
    
    np.random.shuffle(data)
    a, b, c = Find_Plane(data[0], data[1], data[2])
    
    num_cur = Check(data, a, b, c, thre)
    
    if num_cur > num:
        
        num = num_cur
        
        Points = [a, b, c]
        
Ps , Outlier= Draw(data, Points[0], Points[1], Points[2], thre)
np_colors = np.array([[0,255,0]]*len(Ps))
pcd1 = o3d.geometry.PointCloud()
pcd1.points = o3d.utility.Vector3dVector(Ps)
pcd1.colors = o3d.utility.Vector3dVector(np_colors)

np_colors = np.array([[0,0,255]]*len(Outlier))
pcd2 = o3d.geometry.PointCloud()
pcd2.points = o3d.utility.Vector3dVector(Outlier)
pcd2.colors = o3d.utility.Vector3dVector(np_colors)

o3d.visualization.draw_geometries([pcd1+pcd2])
