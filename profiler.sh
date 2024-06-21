#!/bin/bash

# remove the file if it exists and create it
touch $1

# print header to the CSV file
echo "CPU Usage percent, RAM Usage MB" > $1

while true
do
  # get CPU usage using mpstat
  cpu_usage=$(mpstat 1 1 | awk '/all/ {print 100 - $12}' | head -n 1)
  # this includes a second wait, while it calculates the average
  
  # get RAM usage using free
  ram_usage=$(free -m | awk 'NR==2{print $3}') # this is the absolute value
  
  # save to CSV file
  echo "$cpu_usage, $ram_usage" >> $1

done
