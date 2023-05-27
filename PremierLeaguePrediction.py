import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from tkinter import Tk, Label, Button, OptionMenu, StringVar, messagebox


def predict_result():
    # Get the selected home team and away team
    home_team = home_team_var.get()
    away_team = away_team_var.get()

    # Create a new instance for prediction
    instance = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0]], columns=features)

    # Get the home team and away team statistics from the dataset
    home_team_stats = filtered_data[filtered_data['HomeTeam'] == home_team][features].tail(1)
    away_team_stats = filtered_data[filtered_data['AwayTeam'] == away_team][features].tail(1)

    # Update the instance with the statistics
    instance.update(home_team_stats)
    instance.update(away_team_stats)

    # Make the prediction
    result = model.predict(instance)
    if result[0] == 'H':
        winner = home_team
        loser = away_team
    else:
        winner = away_team
        loser = home_team

    messagebox.showinfo("Prediction Result", "{} wins ({} loses)".format(winner, loser))


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

# Get the list of unique teams
teams = sorted(set(filtered_data['HomeTeam']).union(set(filtered_data['AwayTeam'])))

# GUI setup
window = Tk()
window.title("Premier League Prediction")
window.geometry("400x200")

# Home team selection
home_team_label = Label(window, text="Home Team:")
home_team_label.pack()

home_team_var = StringVar(window)
home_team_var.set(teams[0])  # Set the default value
home_team_menu = OptionMenu(window, home_team_var, *teams)
home_team_menu.pack()

# Away team selection
away_team_label = Label(window, text="Away Team:")
away_team_label.pack()

away_team_var = StringVar(window)
away_team_var.set(teams[1])  # Set the default value
away_team_menu = OptionMenu(window, away_team_var, *teams)
away_team_menu.pack()

# Predict button
predict_button = Button(window, text="Predict", command=predict_result)
predict_button.pack()

window.mainloop()
