import time
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
city_reference_list = ['Chicago','New York City','Washington']
month_reference_list = {0:'All',1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
day_reference_list = {'all':'All','m':'Monday','t':'Tuesday','w':'Wednesday','th':'Thursday','f':'Friday','sa':'Saturday','su':'Sunday'}

def readable_filters(user_entry,reference_list):
    """
        the whole purpose of this function is to make it easier to work with month entries.

        arguments:
            (list) user entry: user has the freedon to choose the month(s) by typing the names
            (dictionary) reference_list: takes the month_reference_list

        Returns:
            (list) readable_filter: a list of numbers each of which is a dict key that represents the associated month in the dictionary
    """
    readable_filter = []
    for entry in user_entry:
        readable_filter.append(reference_list[entry])
    return readable_filter

def invalid_entry_warning():
    print(Fore.RED+"Seems like a wrong entry. Please try again.")
    print(Style.RESET_ALL)

def entry_validation(user_entry,reference_list):
    """
    Checks whether the user input for questions concerning filters(month and day) is a valid entry

    Arguments:
        (list) user_entry: name of month(s)/week day(s)
        (list) reference_list: list of the names of months(s)/week day(s)

    Returns:
        (int) valid_entry:  either 0(invalid entry) or 1(valid entry)

    """
    for entry in user_entry:
        if entry not in reference_list:
            invalid_entry_warning()
            valid_entry = 0
            break
        else:
            valid_entry = 1
            continue
    return valid_entry

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(Fore.RED+'Hello! Let\'s explore some US bikeshare data!')
    print(Style.RESET_ALL)
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print("Please specify in which of the following cities you're interested. It's case insensitive.\nChicago, New York City, Washington")
        print(Fore.GREEN+"City of...")
        city = input(Fore.BLUE).strip().title()
        print(Style.RESET_ALL)
        if city in city_reference_list:
            break
        else:
            invalid_entry_warning()

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_entry = 0
    while not valid_entry:
            print("\nPlease specify the month(s) your interested in.\nType all for no filter\nOr\nJanuary, February, March, ... , December")
            print(Fore.GREEN+"It's case insensitive and you can filter by more than one month. Separate entries with a ','")
            month = input(Fore.BLUE).strip().replace(" ","").title().split(',')
            print(Style.RESET_ALL)
            month_number = []
            for m in month:
                for key,value in month_reference_list.items():
                    if  m == value:
                        month_number.append(key)
                        break
            month = month_number
            valid_entry = entry_validation(month,month_reference_list)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_entry = 0
    while not valid_entry:
            print("\nPlease specify the day(s) your interested in.\nType all for no filter\nOr\nM:Monday, T:Tuesday, W:Wednesday, Th:Thursday, F:Friday, Sa:Saturday, Su:Sunday")
            print(Fore.GREEN+"It's case insensitive and you can filter by more than one day.Separate entries with a ','")
            day = input(Fore.BLUE).strip().replace(" ","").lower().split(',')
            print(Style.RESET_ALL)
            valid_entry = entry_validation(day,day_reference_list)

    print(Fore.RED+"Stats to follow are generated base on the givern filters:",Fore.GREEN,"\nCity: {}, Month(s): {}, Day(s): {}".format(city.title(),','.join(map(str, readable_filters(month,month_reference_list))).title(),','.join(map(str, readable_filters(day,day_reference_list))).title()))
    print(Style.RESET_ALL)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.title()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    df_main = df
    # filter by month if applicable
    if 0 not in month:
    # filter by month to create the new dataframe
        for i,m in enumerate(month):
            if df_main[df_main['month'] == m].size != 0:
                if df.equals(df_main):
                    df = df[df['month'] == m]
                else:
                    df = df.append(df_main[df_main['month'] == m])
            #this part checks ,on top of filtering, if there's data available for the entry and gives the appropriate warnings
            else:
                print(Fore.RED,"\nNo data available for ", month_reference_list[m],Style.RESET_ALL)
                if len(month) == 1:
                    while True:
                        print(Fore.GREEN)
                        print("Filter will be considered 'All'. Do you want to continue or restar?c:Continue, r:Restart\n",Fore.BLUE)
                        cont_or_res = input()
                        print(Style.RESET_ALL)
                        if cont_or_res == 'c':
                            month = month_reference_list[0]
                            break
                        elif cont_or_res == 'r':
                            main()
                            break
                        else:
                            invalid_entry_warning()
        #this part helps generate the proper warning when there's more than one entry and there's data available for some entries but not the others
        if len(month)!=1 and len(month)>df['month'].unique().size:
            print(Fore.GREEN,"\nOther month(s) you entered were considered when filtering",Style.RESET_ALL)

    df_main = df
    # filter by day of week if applicable
    if 'all' not in day:
    # filter by day of week to create the new dataframe
        for i,d in enumerate(day):
            if df_main[df_main['day_of_week'] == day_reference_list[d]].size != 0:
                if df.equals(df_main):
                    df = df[df['day_of_week'] == day_reference_list[d]]
                else:
                    df = df.append(df_main[df_main['day_of_week'] == day_reference_list[d]])

            else:
                #this part checks ,on top of filtering, if there's data available for the entry and gives the appropriate warnings
                print(Fore.RED,"No data available for ", day_reference_list[d],Style.RESET_ALL)
                if i == len(day)-1:
                    while True:
                        print(Fore.GREEN)
                        print("Filter will be considered 'All'. Do you want to continue or restar?c:Continue, r:Restart\n",Fore.BLUE)
                        cont_or_res = input()
                        print(Style.RESET_ALL)
                        if cont_or_res == 'c':
                            day = day_reference_list['all']
                            break
                        elif cont_or_res == 'r':
                            main()
                            break
                        else:
                            invalid_entry_warning()
        #this part helps generate the proper warning when there's more than one entry and there's data available for some entries but not the others
        if len(day)!=1 and len(day)>df['day_of_week'].unique().size:
                print(Fore.GREEN,"Other day(s) you entered were considered when filtering",Style.RESET_ALL)


    return df


def time_stats(df,month,day):
    #"""Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #TO DO: display the most common month

    if df['month'].unique().size == 1:
        print("Most common month of travel is the one month given as filter:",Fore.GREEN,month_reference_list[df['month'].iloc[0]],Style.RESET_ALL)
    else:
        month_num = df['month'].mode().iloc[0]
        most_common_month = month_reference_list[month_num]
        print("Most common month of travel is:", Fore.GREEN,most_common_month.title(),Style.RESET_ALL)

    # TO DO: display the most common day of week
    if df['day_of_week'].unique().size == 1:
        print("Most common day of travel is the one day given as filter:",Fore.GREEN,df['day_of_week'].iloc[0].title(),Style.RESET_ALL)
    else:
        most_common_day = df['day_of_week'].mode()[0]
        print("Most common day of travel is:",Fore.GREEN,most_common_day.title(),Style.RESET_ALL)


    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print("Most frequent start hour of travel is:",Fore.GREEN,"{}:00".format(popular_hour) if popular_hour>9 else "0{}:00".format(popular_hour),Style.RESET_ALL)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    #"""Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most common start station is:",Fore.GREEN,most_common_start_station,Style.RESET_ALL)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most common end station is:",Fore.GREEN,most_common_end_station,Style.RESET_ALL)

    # TO DO: display most frequent combination of start station and end station trip
    df['tour'] = ['From '] + df['Start Station'] +[' to '] + df['End Station']
    most_common_tour = df['tour'].mode()[0]
    print('Most common rout is:',Fore.GREEN,most_common_tour,Style.RESET_ALL)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print("Total travel time amounts to:",Fore.GREEN,"{} hr {} min {} s ".format(total_travel_time//3600,total_travel_time%3600//60,total_travel_time%3600%60),Style.RESET_ALL)
    # TO DO: display mean travel time
    average_travel_time = int(df['Trip Duration'].mean())
    print("Average travel time amounts to:",Fore.GREEN,"{} hr {} min {} s ".format(average_travel_time//3600,average_travel_time%3600//60,average_travel_time%3600%60),Style.RESET_ALL)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Distribution of user acount types:\n")
    for i in range(user_types.size):
        print(user_types.index[i],":",Fore.GREEN,user_types[i],Style.RESET_ALL)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("\nGender distribution of travelers:\n")
        gender_count = df['Gender'].value_counts()
        for i in range(gender_count.size):
            print(gender_count.index[i],":",Fore.GREEN,gender_count[i],Style.RESET_ALL)
    else:
        print(Fore.RED,"\nNo info on gender distribution available for this city",Style.RESET_ALL)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest year of birth:",Fore.GREEN,df['Birth Year'].min(),Style.RESET_ALL)
        print("Most recent year of birth:",Fore.GREEN,df['Birth Year'].max(),Style.RESET_ALL)
        print("Most common year of birth:",Fore.GREEN,df['Birth Year'].mode()[0],Style.RESET_ALL)
    else:
        print(Fore.RED,"\nNo info on birth year available for this city",Style.RESET_ALL)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print(Style.RESET_ALL)
    city, month, day = get_filters()
    df = load_data(city, month, day)
    time_stats(df,month,day)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

if __name__ == "__main__":
	main()
