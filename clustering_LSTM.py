# in dit script worden de gegenereerde paden geclusterd in verschillende groepen. 
# op het einde wordt bepaald hoe goed dit is gedaan.

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

#het inlezen van de gegenereerde data
generated_paths = pd.read_csv(r'Project_offline\movement_paterns\generated_path.csv')
labels = pd.read_csv(r'Project_offline\movement_paterns\labels.csv')

# hieronder wordt de dataset opgedeeld per bij id. format of list: [ [[pos1bij1],[pos2bij1],[...]] , [[pos1bij2][...]] , [[...]] ]
# paden zijn aan te roepen door "ganerated_path_per_bee["bee_index"]["timestamp"][0 voor xpos, 1 voor ypos, 2 voor rotatie]"
generated_path_per_bee = []
for bee in range(max(generated_paths.bee_id)):
    x = generated_paths[generated_paths.bee_id == bee+1].values.tolist()
    for i in x:
        del i[3]
    generated_path_per_bee.append(x)


timesteps = len(generated_path_per_bee[0])
input_dim = len(generated_path_per_bee[0][0])

X = np.array(generated_path_per_bee)
y = labels.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build the LSTM model
model = keras.Sequential()
model.add(keras.layers.LSTM(64, input_shape=(timesteps, input_dim)))
model.add(keras.layers.Dense(2, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=50)

# Make prediction on test data
predictions = model.predict(X_test)

for i in range(len(predictions)):
    if predictions[i][0] > predictions[i][1]:
        predictions[i] = [1,0]
    elif predictions[i][0] < predictions[i][1]:
        predictions[i] = [0,1]


tp,fp,fn,tn = 0,0,0,0

for i in range(len(predictions)):
    
    if predictions[i][0] and y_test[i][0]:
        tp += 1
    
    elif predictions[i][0] and y_test[i][1]:
        fp += 1
    
    elif predictions[i][1] and y_test[i][0]:
        fn += 1
    
    elif predictions[i][1] and y_test[i][1]:
        tn += 1

print(' true positive:', tp, '\n','false positive:', fp, '\n','false negative:', fn, '\n','true negative:', tn, '\n')




