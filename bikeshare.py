import os
import time
import pandas as pd
import numpy as np


current_dir = os.path.dirname(os.path.abspath(__file__))
city_data = { 'chicago': os.path.join(current_dir, 'chicago.csv'),
             'new york city': os.path.join(current_dir, 'new_york_city.csv'), 
             'washington': os.path.join(current_dir, 'washington.csv') }              

day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
month_list = ['january', 'february', 'march', 'april', 'may','june','july',
              'august','september', 'october', 'november', 'december', 'all'] 

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('Select a city:\n chicago\n new york city\n washington\n').strip().lower()
    while city not in city_data:
        city = input('invalid city. please Choose from the three cities as shown.\n').strip().lower()
    month = input('Select a month: january, february, ... , june, all\n').strip().lower()
    while month not in month_list:
        month = input('invalid month. please select again.\n').strip().lower()
    day = input('Select a day: monday, tuesday, ... sunday, all\n').strip().lower()
    while day not in day_list:
        day = input('invalid day. please select again.\n').strip().lower()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable."""
    
    df = pd.read_csv(city_data[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    if month != 'all': df = df[df['month'] == month]
    if day != 'all': df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    if 'month' in df.columns:
        common_month = df['month'].mode()[0]
        print(f'most common month: {common_month}')
        
    # display the most common day of week
    if 'day_of_week' in df.columns:
        common_day = df['day_of_week'].mode()[0]
        print(f'most common day of week: {common_day}')
        
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f'most common start hour: {common_hour}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
        """Displays statistics on the most popular stations and trip."""
        
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        
        # display most commonly used start station
        common_start_station = df['Start Station'].mode()[0]
        print(f'The most Starting Station: {common_start_station}')
        
        # display most commonly used end station
        common_end_station = df['End Station'].mode()[0]
        print(f'The most End Station: {common_end_station}')
        
        # display most frequent combination of start station and end station trip
        common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print(f'Most popular trip from Start to End: {common_trip}')
        print('\nThis took %s seconds.' % (time.time() - start_time))
        print('_'*40)
        
        
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/3600
    print(f'Total Travel Time: {total_travel_time:.2f} hours')
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print(f'Mean Travel Time: {mean_travel_time:.2f} minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User Types: {user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
     gender_counts = df['Gender'].value_counts()
     print(f'\nGender Counts: {gender_counts}')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
     earliest_year = int(df['Birth Year'].min())
     most_recent_year = int(df['Birth Year'].max())
     common_year = int(df['Birth Year'].mode()[0])
     print(f'Earliest Year: {earliest_year}')
     print(f'Most Recent Year: {most_recent_year}')
     print(f'Common Year: {common_year}')
     print("\nThis took %s seconds." % (time.time() - start_time))
     print('-'*40)
     
def display_raw_data(df):
    """Displays 5 rows of raw data at a time upon user request."""
    
    row_start = 0  
    row_end = 5  
    show_data = input('Do you want to see the first 5 rows of the dataset? Enter yes or no.\n').strip().lower()

    while show_data == 'yes' and row_start < len(df):
        print(df.iloc[row_start:row_end])  
        row_start += 5  
        row_end += 5
        if row_start < len(df):  
            show_data = input('Do you want to see the next 5 rows of the dataset? Enter yes or no.\n').strip().lower()
        else:
            print("No more data to display.")
            break
     
     
     
def main():
    while True: 
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter 'yes' to restart or 'no' to exit.\n").lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
