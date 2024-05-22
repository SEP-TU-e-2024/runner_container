class Validator():
    def __init__(self):
        print("created")

    def submit(self, val):
        print(f'Got this value: {val}')
        with open("/results/results.txt", "+a") as f:
            f.write(f"New value submitted: {val}")
    
    def get_state(self):
        return 5