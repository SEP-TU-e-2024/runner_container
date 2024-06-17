# Dummy code for testing functionality of the IOModule

from time import sleep

from validator.validator import Validator

io = Validator()

a = io.obtain_data("Enter a number: ")
b = io.obtain_data("Enter another number: ")
sum = int(a) + int(b)

io.push_data(str(sum))

sleep(5)