#!/bin/bash

output_file="results/metrics.csv"

# remove the file if it exists and create it
rm $output_file
touch $output_file

# print header to the CSV file
echo "CPU Usage percent, RAM Usage MB" > $output_file

while true
do
  # get CPU usage using mpstat
  cpu_usage=$(mpstat 1 1 | awk '/all/ {print 100 - $12}' | head -n 1)
  # this includes a second wait, while it calculates the average
  
  # get RAM usage using free
  # ram_usage=$(free -m | awk 'NR==2{printf "%.2f", $3*100/$2}') # this is the percentage
  ram_usage=$(free -m | awk 'NR==2{print $3 " MB"}') # this is the absolute value
  
  # save to CSV file
  echo "$cpu_usage, $ram_usage" >> $output_file

done
