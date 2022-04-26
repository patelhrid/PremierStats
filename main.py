"""File description"""

import csv
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from ttkthemes import ThemedStyle


def read_data(file_name: str) -> tuple[dict, dict, dict]:
    """Read the dataset in <file_name>"""
    with open(file_name) as file:
        reader = csv.reader(file)
        next(reader)

        teams = {}
        ft_goals = {}
        scored_conceded = {}

        for row in reader:
            home_team = row[2]
            away_team = row[3]
            home_ft_goals = int(row[4])
            away_ft_goals = int(row[5])
            result = row[6]
            stats_adder(home_team, home_ft_goals, away_ft_goals,
                        result, teams, ft_goals, scored_conceded)
            stats_adder(away_team, away_ft_goals, home_ft_goals,
                        result, teams, ft_goals, scored_conceded)

    return teams, ft_goals, scored_conceded


def stats_adder(team_name: str, ft_goals_scored: int,
                ft_goals_conceded: int, result: str, teams: dict, ft_goals: dict, scored_conceded: dict) -> None:
    """Add the given stats for each team"""
    if team_name not in teams:
        if result == 'H':
            teams[team_name] = [[1, 0, 0], 1]
        elif ft_goals_scored == ft_goals_conceded:
            teams[team_name] = [[0, 1, 0], 1]
        else:
            teams[team_name] = [[0, 0, 1], 1]
        ft_goals[team_name] = ft_goals_scored
        scored_conceded[team_name] = [ft_goals_scored, ft_goals_conceded]
    else:
        if result == 'H':
            teams[team_name][0][0] += 1
            teams[team_name][1] += 1
        elif ft_goals_scored == ft_goals_conceded:
            teams[team_name][0][1] += 1
            teams[team_name][1] += 1
        else:
            teams[team_name][0][2] += 1
            teams[team_name][1] += 1
        ft_goals[team_name] += ft_goals_scored
        scored_conceded[team_name][0] += ft_goals_scored
        scored_conceded[team_name][1] += ft_goals_conceded


TEAMS, FT_GOALS, SCORED_CONCEDED = read_data('final_dataset.csv')
WIN = Tk()


def full_time_analyzer(teams: dict, scored_conceded: dict) -> dict:
    """Analyze the full time stats of every team"""
    stats = {}
    for team in scored_conceded:
        scored = scored_conceded[team][0]
        conceded = scored_conceded[team][1]
        games = teams[team][1]
        stats[team] = [(scored / games), (conceded / games)]
    return stats


def plot_fta_goals() -> None:
    """Plot the top 10 goals scored per game on a bar chart"""
    new_colours = ['green', 'blue', 'purple', 'brown', 'teal']
    teams, goals_scored_per_game = goals_per_game('scored')
    plt.bar(teams, goals_scored_per_game, color=new_colours)
    plt.title('Goals Scored per Game since 2000')
    plt.xlabel('Team')
    plt.ylabel('Goals Scored per Game')
    plt.show()


def plot_fta_conceded() -> None:
    """Plot the top 10 goals conceded per game on a bar chart"""
    new_colours = ['green', 'blue', 'purple', 'brown', 'teal']
    teams, goals_scored_per_game = goals_per_game('conceded')
    plt.bar(teams, goals_scored_per_game, color=new_colours)
    plt.title('Goals Conceded per Game since 2000')
    plt.xlabel('Team')
    plt.ylabel('Goals Conceded per Game')
    plt.show()


def goals_per_game(parameter: str) -> tuple[list, list]:
    """Calculate the top 10 teams with the highest goals scored per game
    or lowest goals conceded per game based on <parameter>"""
    results = full_time_analyzer(TEAMS, SCORED_CONCEDED)
    gpg = []
    teams = []
    while len(teams) < 10:
        if parameter == 'scored':
            min_max_key = None
            min_max_value = 0
        else:
            min_max_key = None
            min_max_value = 100
        for team in results:
            if parameter == 'scored':
                if results[team][0] > min_max_value:
                    min_max_value = results[team][0]
                    min_max_key = team
            else:
                if results[team][1] < min_max_value:
                    min_max_value = results[team][1]
                    min_max_key = team
        teams.append(min_max_key)
        gpg.append(min_max_value)
        results.pop(min_max_key)
    return teams, gpg


def highest_win_rate(answer: str) -> tuple[list, list]:
    """Return the top 10 teams with the highest win percentage"""
    all_rates = {}
    for team in TEAMS:
        if TEAMS[team][1] > int(answer):
            all_rates[team] = TEAMS[team][0][0] / TEAMS[team][1] * 100
    teams = []
    rates = []
    while len(teams) < 10:
        max_so_far = 0
        max_key = None
        for team in all_rates:
            if all_rates[team] > max_so_far:
                max_so_far = all_rates[team]
                max_key = team
        teams.append(max_key)
        rates.append(max_so_far)
        all_rates.pop(max_key)
    return teams, rates


def lowest_win_rate(answer: str) -> tuple[list, list]:
    """Return the top 10 teams with the highest win percentage"""
    all_rates = {}
    for team in TEAMS:
        if TEAMS[team][1] > int(answer):
            all_rates[team] = TEAMS[team][0][0] / TEAMS[team][1] * 100
    teams = []
    rates = []
    while len(teams) < 10:
        min_so_far = 100
        min_key = None
        for team in all_rates:
            if all_rates[team] < min_so_far:
                min_so_far = all_rates[team]
                min_key = team
        teams.append(min_key)
        rates.append(min_so_far)
        all_rates.pop(min_key)
    return teams, rates


min_input = StringVar()


def plot_win_rate_highest() -> None:
    """Plot the top 10 win rate stats on a bar chart"""
    textbox = Entry(WIN, textvariable=min_input)
    textbox.place(x=250, y=300)
    label = Label(WIN, text="Must be a number from 0 to 550", fg='red', font=("Arial Bold", 16))
    label.place(x=260, y=270)
    submit_button = Button(WIN, text='Submit', font=("Arial", 16), command=submit_highest)
    submit_button.place(x=450, y=300)


def submit_highest() -> None:
    new_colours = ['green', 'blue', 'purple', 'brown', 'teal']
    answer = min_input.get()

    teams, rates = highest_win_rate(answer)
    plt.bar(teams, rates, color=new_colours)
    plt.title('Highest Win % since 2000 (' + answer + '+ Games)')
    plt.xlabel('Team')
    plt.ylabel('Win Percentage')
    plt.show()


def plot_win_rate_lowest() -> None:
    """Plot the bottom 10 win rate stats on a bar chart"""
    textbox = Entry(WIN, textvariable=min_input)
    textbox.place(x=250, y=300)
    label = Label(WIN, text="Must be a number from 0 to 550", fg='red', font=("Arial Bold", 16))
    label.place(x=260, y=270)
    submit_button = Button(WIN, text='Submit', font=("Arial", 16), command=submit_lowest)
    submit_button.place(x=450, y=300)


def submit_lowest() -> None:
    new_colours = ['green', 'blue', 'purple', 'brown', 'teal']
    answer = min_input.get()

    teams, rates = lowest_win_rate(answer)
    plt.bar(teams, rates, color=new_colours)
    plt.title('Lowest Win % since 2000 (' + answer + '+ Games)')
    plt.xlabel('Team')
    plt.ylabel('Win Percentage')
    plt.show()


def ft_gui() -> None:
    """GUI Window for full time stats"""
    clear()
    add_home_button()
    scored = Button(WIN, text='Most Goals Scored Per Game', font=("Arial", 16), command=plot_fta_goals)
    conceded = Button(WIN, text='Least Goals Conceded Per Game', font=("Arial", 16), command=plot_fta_conceded)
    scored.place(x=280, y=50)
    conceded.place(x=265, y=100)


def win_rate_gui() -> None:
    """GUI Window for win rates"""
    clear()
    add_home_button()
    highest = Button(WIN, text='Highest Win %', font=("Arial", 16), command=plot_win_rate_highest)
    lowest = Button(WIN, text='Lowest Win %', font=("Arial", 16), command=plot_win_rate_lowest)
    highest.place(x=330, y=50)
    lowest.place(x=333, y=100)


def add_home_button() -> None:
    """Add a home button in the top left"""
    home = Button(WIN, text='Home', font=("Arial", 16), command=go_home)
    home.place(x=10, y=10)


def clear() -> None:
    for widgets in WIN.winfo_children():
        widgets.destroy()
    label = Label(WIN, text="Please close graph window after each plot", fg='red', font=("Arial Bold", 12))
    label.place(x=270, y=700)
    img = ImageTk.PhotoImage(Image.open("Untitled-1.png").resize((570, 200)))
    panel = Label(WIN, image=img)
    panel.pack()


def go_home() -> None:
    """Return to the home GUI"""
    for widgets in WIN.winfo_children():
        widgets.destroy()
    main_gui_window()


def main_gui_window() -> None:
    """Main GUI Window"""
    WIN.title('PremierStats')
    b1 = Button(WIN, text='Full time stats', font=("Arial", 16), command=ft_gui)
    b2 = Button(WIN, text='Win Rate', font=("Arial", 16), command=win_rate_gui)
    b3 = Button(WIN, text='More soon...', font=("Arial", 16))
    b1.place(x=330, y=210)
    b2.place(x=345, y=260)
    b3.place(x=333, y=310)
    WIN.geometry("800x800+320+10")
    label = Label(WIN, text="Please close graph window after each plot", fg='red', font=("Arial Bold", 12))
    label.place(x=270, y=700)
    img = ImageTk.PhotoImage(Image.open("Untitled-1.png").resize((570, 200)))
    panel = Label(WIN, image=img)
    panel.pack()
    b4 = Button(WIN, text='Night Mode', font=("Arial", 16), command=night_mode)
    b5 = Button(WIN, text='Day Mode', font=("Arial", 16), command=anti_night_mode)
    b4.place(x=340, y=610)
    b5.place(x=345, y=560)
    WIN.mainloop()


def night_mode() -> None:
    """Change the background to night mode"""
    WIN['background'] = '#323232'


def anti_night_mode() -> None:
    """Change the background to day mode"""
    WIN['background'] ='#EBEBEB'


if __name__ == '__main__':
    main_gui_window()
