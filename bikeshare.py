import time
import pandas as pd
import numpy as np
import statistics as st

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = '' 
    day = ''
    cities = {'chicago', 'new york city', 'washington'}
    months = {'all', 'january', 'february', 'march', 'april', 'may', 'june'}
    days = {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    
    while(city not in cities):
        city = input('Which city would you like to get data from : chicago, new york city or washington (choose one of them)? \n').lower()
        wrong = (city not in cities)
        if(wrong):
            print('PLEASE CHOOSE A CITY FROM THE GIVEN LIST!')
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while(month not in months):
        month = input('Which month would you like to filter the data from? (all, january, february, ..., june)\n').lower()
        wrong = (month not in months)
        if(wrong):
            print('PLEASE CHOOSE A MONTH FROM THE GIVEN LIST!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while(day not in days):
        day = input('Which day of the week would you like to filter the data from? (all, monday, tuesday, ... sunday)\n').lower()
        wrong = (day not in days)
        if(wrong):
            print('PLEASE CHOOSE A DAY FROM THE GIVEN LIST!')

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name 

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 # since months are from 1-6
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most popular month is: ', st.mode(df['month']))

    # TO DO: display the most common day of week
    print('The most popular day of the week is: ', st.mode( df['day_of_week']))

    # TO DO: display the most common start hour
    print('The most popular hour is: ', st.mode(df['Start Time'].dt.hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('the commonly used start station is: ', st.mode(df['Start Station']))

    # TO DO: display most commonly used end station
    print('the commonly used end station is: ', st.mode(df['End Station']))

    # TO DO: display most frequent combination of start station and end station trip
    combi_start_end_trip = df[['Start Station', 'End Station']].mode().iloc[0]
   
    print('The most combination of start station and end station trip: {} - {}'.format(combi_start_end_trip[0], combi_start_end_trip[1]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is: ', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('The mean travel time is: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('counts of user Types: \n', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        print('Counts of gender: \n', df['Gender'].value_counts())
    except KeyError:     # since there are no gender column in the washington dataset.. 
        print('No Gender given from the Washington DataSet..')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
	    print('The earliest year of birth is: ', df['Birth Year'].min())
	    print('The most recent year of birth is: ', df['Birth Year'].max())
	    print('The most common year of birth is: ', st.mode(df['Birth Year']))
    except KeyError:     # Since there are no gender column in the washington dataset.. 
        print('No Birth Year given in Washington..')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
	""" Let's define a raw_data function to display the 5 rows at a time """
		# we get the shape of our dataframe
	df_shape = df.shape
		# we get the number of rows from the shape
	num_rows = df_shape[0]
	
	for i in range(0, num_rows, 5):
		answer = input('Would you like to see the raw data? \'yes\' or \'no\':\n').lower()
		if(answer != 'yes'):
			break
		# we get the 5 row datas at a time here, with all of the columns...
		print(df.iloc[i:i+5,:])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
