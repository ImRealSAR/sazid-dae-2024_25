import random
import math
def validateMonth(month):
    while month < 1 or month > 12:
        month = int(input("Invalid month. Please enter value from 1-12: "))
    return month

# Check if a given year is a leap year
# Return 1 if it is a leap year, 0 otherwise
def leap_year(year):
    if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
        return 1
    return 0

# Check for and adjust day input 
def validateDay(month, day, year):
    days_in_month = [31, 28 + leap_year(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while day < 1 or day > days_in_month[month - 1]:
        day = int(input(f"Invalid day. Please enter value from 1-{days_in_month[month - 1]}: "))
    return day
# Event
# Date: Month Day, Year
def printEvents():
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    print("\n******************** List of Events ********************")
    for i in range(len(eventName)):
        print(f"Event: {eventName[i]}")
        print(f"Date: {month_names[eventMonth[i] - 1]} {eventDay[i]}, {eventYear[i]}\n")

# Follow the addEvent function
def addEvent():
    name = input("What is the event: ")
    year = int(input("What is the year: "))
    month = validateMonth(int(input("What is the month (number): ")))
    day = validateDay(month, int(input("What is the date: ")), year)
    eventName.append(name)
    eventMonth.append(month)
    eventDay.append(day)
    eventYear.append(year)

# Main code
eventName = []
eventMonth = []
eventDay = []
eventYear = []

addEvent()
while input("Do you want to enter another date? NO to stop: ").lower() == "yes":
    addEvent()

printEvents()
