# This is a dummy validator
# We will remove this and add the IOModule based implementation
class Validator():
    def __init__(self):
        print("created")

    #process submissions
    def submit(self, val):
        print(f'Got this value: {val}')
        with open("/results/results.txt", "+a") as f:
            f.write(f"New value submitted: {val}")
    
    def get_state(self):
        return 5