import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Step 1: Load the CSV data
data = pd.read_csv('final_dataset.csv')

# Step 2: Preprocess the data
# Convert the outcome column to numerical labels
le = LabelEncoder()
data['FTR'] = le.fit_transform(data['FTR'])

# Select relevant features for the model
features = data[['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HTFormPts', 'ATFormPts', 'HTWinStreak3', 'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5', 'ATWinStreak3', 'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5', 'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts']]

# Select the target variable
target = data['FTR']

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Step 4: Train the Decision Tree model
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)

# Step 5: Evaluate the Decision Tree model
y_pred = decision_tree.predict(X_test)
print(classification_report(y_test, y_pred))

# Step 6: Make predictions (optional)
# ...
