import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


generated_paths = pd.read_csv(r'Project_offline\movement_paterns\generated_path.csv')
labels = pd.read_csv(r'Project_offline\movement_paterns\labels.csv')

generated_path_per_bee = []
for bee in range(max(generated_paths.bee_id)):
    x = generated_paths[generated_paths.bee_id == bee+1].values.tolist()
    for i in x:
        del i[3]
    generated_path_per_bee.append(x)

def get_features():
    features = []
    for bee_id in range(len(generated_path_per_bee)):
        total_distance = 0
        total_accelaretion = 0
        total_rotation = 0
        total_rotation_accelaretion = 0
        average_distance_from_centre = 0

        total_distance_from_centre = 0
        for ii in generated_path_per_bee[bee_id]:
            x,y,r = ii
            total_distance_from_centre += ((x-200)**2 + (y-200)**2)**0.5
        average_distance_from_centre = total_distance_from_centre/len(generated_path_per_bee[bee_id])

        for ii in range(len(generated_path_per_bee[bee_id])-1):
            x1,y1,r1 = generated_path_per_bee[bee_id][ii]
            x2,y2,r2 = generated_path_per_bee[bee_id][ii+1]

            total_distance += ((x1-x2)**2 + (y1-y2)**2)**0.5
            total_rotation += abs(r2-r1)

        for ii in range(len(generated_path_per_bee[bee_id])-2):
            x1,y1,r1 = generated_path_per_bee[bee_id][ii]
            x2,y2,r2 = generated_path_per_bee[bee_id][ii+1]
            x3,y3,r3 = generated_path_per_bee[bee_id][ii+2]

            total_accelaretion += abs(((x1-x2)**2 + (y1-y2)**2)**0.5 - ((x2-x3)**2 + (y2-y3)**2)**0.5)
            total_rotation_accelaretion += abs(abs(r2-r1)-abs(r3-r2))
        


        features.append([int(total_distance),int(total_accelaretion),int(total_rotation), int(total_rotation_accelaretion), int(average_distance_from_centre)])
    
    return features
    
        

X = get_features()
y = labels['Class 2']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Create a KMeans instance with the desired number of clusters
kmeans = KMeans(n_clusters=2)

# Fit the model to the data
kmeans.fit(X_train)

# Get the cluster assignments for each data point
y_pred = kmeans.predict(X_test)

print(confusion_matrix(y_test,y_pred))
