#%%
import csv
import os

import graphviz
import pandas
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

#%%
BASE_PATH = 'C:\\Users\\Pende\\Documents\\myapps\\my_machine_learning'

data = pandas.read_csv(os.path.join(BASE_PATH, 'data', 'japan_2018_fixed.csv'))
columns = ['age_in_2018', 'height', 'weight', 'spike', 'block']
df = pandas.DataFrame(data, columns=columns)

#%%
# X = [[187, 45], [184, 62], [178, 56], [178, 59]]
# y = [167, 175, 187, 188]

X = df[['height', 'weight', 'age_in_2018']]
y = df['spike']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.5, test_size=0.5, random_state=0)

#%%
classifier = KNeighborsClassifier(n_neighbors=5, weights='uniform')

#%%
model = classifier.fit(X_train, y_train)

#%%
# Make a prediction for the spike
# for a girl who is 193 tall and 82kg
observation = [[180, 64, 30]]
prediction = model.predict(observation)

#%%
pct = model.predict_proba(observation)

#%%
# Compare X against y
score = model.score(X, y)
# Tells how well the model interprets the data it was trained with
score = model.score(X_train, y_train)
# Equivalent to (X_test, y_pred) and gives the
# accuracy of the model: predictions vs. true data
score = model.score(X_test, y_test)

#%%
# No need to calculate y_pred because done
# internally but for the accuracy score,
# we need the predicted data
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_train, y_pred)

#%%
report = classification_report(y_test, y_pred)
print(report)

# #%%
message = f'Prediction: {prediction}, Probability: %%, Score: {score}, Accuracy: {accuracy}'
print(message)

#%%
# tree.plot_tree(model)
# dot_data = tree.export_graphviz(classifier, out_file='tree_graph_data', filled=True)
# graph = graphviz.Source(dot_data, format='pdf')
# graph.render(filename='tree_graph', view=True)
