import validator

def main():
    v = validator.Validator()
    v.submit(1)
    state = v.get_state()
    print(state)