import csv
import os
import subprocess
from datetime import datetime


def get_user_input():
    date = input("Enter the date (YYYY-MM-DD): ")
    weight = float(input("Enter your weight (in pounds): "))
    return date, weight

def store_data(date, weight):
    file_path = "data/data.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as file:
        fieldnames = ['Date', 'Weight (lb)']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({'Date': date, 'Weight (lb)' : weight})

def generate_weight_graph(data):
    # script = """
    # set terminal dumb
    # set title "Weight Loss Journey"
    # set xlabel "Date"
    # set ylabel "Weight (lb)"
    # plot '-' using 1:2 with lines title 'Weight'
    # """

    script = """
set terminal dumb size 180, 70
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set title "Weight Loss Journey"
set xlabel "Date"
set ylabel "Weight (lb)"
set xrange ['2023-01-01' : '2023-01-27']
set yrange ['150' : '190']

set ytics 1
plot '-' using 1:2 with lines title 'Weight (lb)' 
"""

    data_str = "\n".join(f"{date} {weight}" for date, weight in data)


    try:
        process = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE)
        process.communicate((script + data_str + "\nEOF\n").encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        process.terminate()                

if __name__ == "__main__":
    # date, weight = get_user_input()
    # store_data(date, weight)

    # print("Data stored successfully!")

    with open("data/data.csv", 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [(row['Date'], float(row['Weight (lb)'])) for row in csv_reader]
    generate_weight_graph(data)        


