import validator


def main():
    print("ey bruv why you walkin")
    v = validator.Validator()
    v.submit(3)
    print(v.get_state())

if __name__ == "__main__":
    main()