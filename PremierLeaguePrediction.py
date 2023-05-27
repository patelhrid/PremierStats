import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Read the CSV file
data = pd.read_csv('final_dataset.csv')

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

# Extract the year from the 'Date' column and store it in a new column 'Year'
data['Year'] = data['Date'].dt.year

# Specify the range of years for inclusion in the decision tree
start_year = int(input("Enter the start year: "))
end_year = int(input("Enter the end year: "))

# Filter the data based on the specified year range
filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

# Select the relevant features and target variable for the decision tree
features = ['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'DiffPts', 'DiffFormPts']
target = 'FTR'

# Split the data into training and testing sets
X = filtered_data[features]
y = filtered_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the decision tree model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Generate the classification report
report = classification_report(y_test, y_pred)
print(report)
