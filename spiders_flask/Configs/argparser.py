import argparse

parser = argparse.ArgumentParser(description='Example script for argparse')

parser.add_argument('-et', '--execute_time', type= int, default=20, help='time to execute')
parser.add_argument('-day', '--day_interval', type=int, default=1, help='number of days to wait before executing again')
parser.add_argument('-month', '--month_interval', type=int, default=0, help='number of months to wait before executing again')
parser.add_argument('-year', '--year_interval', type=int, default=0, help='number of years to wait before executing again')

args = parser.parse_args()

# Access the values of the arguments using the dot notation
print('Execute Time:', args.execute_time)
print('Day Interval:', args.day_interval)
print('Month Interval:', args.month_interval)
print('Year Interval:', args.year_interval)

