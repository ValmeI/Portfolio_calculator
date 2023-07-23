import matplotlib.pyplot as plt
import matplotlib
from Functions import what_path_for_file
from Excel_functions import get_excel_column_values, get_last_row
from dateutil.parser import parse

path = what_path_for_file()
# x axis dates list, A column
x = get_excel_column_values("Portfell", 'A')
# y axis values list, E column
y = get_excel_column_values("Portfell", 'E')
# str to list of dates for axis X, converting to date also removes the problem of too many str date values
new_list1 = []
for i in x:
    date_i = parse(i)
    new_list1.append(date_i)


def show_diagram():
    ax = plt.gca()
    x1 = new_list1
    plt.plot(x1, y)
    ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    # month is in words, if removed then in numbers
    #ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%b'))
    # Display only year
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
    # move year down, so they would not overlay each other
    ax.tick_params(pad=20)
    plt.xlabel("Kuupäevad")
    plt.ylabel("Portfelli väärtus Eur")
    plt.title("Portfelli diagramm")
    # TkAgg backend, full size screen
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()


def show_percentages_diagram():
    real_estate = get_last_row("Portfell", 2)
    personal_stocks = get_last_row("Portfell", 3)
    company_stocks = get_last_row("Portfell", 4)
    labels = "Kinnisvara puhas väärtus", "Juriidilise isiku aktsiad"#, "Füüsilise isiku aktsiad",
    sizes = [real_estate, company_stocks] #personal_stocks,#miinuses hetkel
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    # Plot
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()


show_diagram()
show_percentages_diagram()
