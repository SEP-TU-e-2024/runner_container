# Dummy code for testing functionality of the IOModule

from validator.validator import Validator

io = Validator()

a = io.obtain_data()
b = io.obtain_data()
sum = int(a) + int(b)

io.push_data(str(sum))
