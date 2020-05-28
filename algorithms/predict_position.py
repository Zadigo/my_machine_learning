#%%
import graphviz
import pandas
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from my_machine_learning.settings.conf import explorer

#%%
data = pandas.read_csv(explorer('combined.csv'))
columns = ['height', 'weight', 'spike', 'block', 'position_number', 'country', 'age']
df = pandas.DataFrame(data, columns=columns)

#%%
X = df[['height', 'weight']]
y = df['position_number']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.3)

#%%
classifier = tree.DecisionTreeClassifier(criterion='gini', random_state=1)

#%%
model = classifier.fit(X_train, y_train)

#%%
observations = [[187, 72]]
prediction = model.predict(observations)

#%%
pct = model.predict_proba(observations)

#%%
# score = model.score(X_test, y_test)
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_train, y_pred)

#%%
message = f'You would play at position: {prediction[0]}'
print(message)