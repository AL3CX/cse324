from evaluate import eval
from parse import parse

def main():
    print("> Welcome to the fancy new Prompt LIS INTERPRETER, type in LISP commands! >")

    # REPL
    while True:
        try:
            user_input = input("> ")
            parsed_input = parse(user_input)
            result = eval(parsed_input)
            # Only print if result is not None
            if result is not None:
                print(lispexp(result))
        except Exception as e:
            print(f"Error: {e}")


def lispexp(value):
    if isinstance(value, list):
        return '(' + ' '.join(lispexp(item) for item in value) + ')'
    else:
        return str(value)


if __name__ == "__main__":
    main()
