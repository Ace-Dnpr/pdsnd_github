import time
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
import bikeshare as bs


while True:

    city, month, day = bs.get_filters()
    df = bs.load_data(city, month, day)
    bs.time_stats(df,month,day)
    bs.station_stats(df)
    bs.trip_duration_stats(df)
    bs.user_stats(df)

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
        break
