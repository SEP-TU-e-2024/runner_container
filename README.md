# Runner Container
This contains the library based implementation.
The submitted code is run in the docker container and calls the library, which will also run in the container.
Then the library will write its results to a file.

## Unit Tests

In order to run the unit tests, navigate to the JudgeQueuer folder and run the following command:
`pytest -k test tests`

Adding new unit tests: 
- add a new file in the /tests folder. Make sure to prefix the filename with test_
- create a class in that file, prefix the name with Test. e.g.`TestCounter`
- Then, for each individual test you can write a method in that class. Each method signature must be prefixed with `test` again. e.g. `test_counter_generate(self):` 
- If you wish to add a method that needs to be ran before other tests, i.e. a 'set up' method, you can do the following
    - import pytest
    - above the set up method add the following decorator: `@pytest.fixture(autouse=True)`

This methodology allows us to neatly separate separate unit tests into different files. They will be automatically discovered when running the testing command. 

You can also check the `test_couter.py` for an example of this.