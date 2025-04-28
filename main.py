from evaluate import eval
from parse import parse

def main():
    print("> Welcome to the fancy new Prompt LISP INTERPRETER, type in LISP commands! >")

    # Open output file
    with open("results.file", "w") as output_file:
        # REPL
        while True:
            try:
                user_input = input("> ")
                # check if user exits
                if user_input == '(quit)':
                    # exit and write to output_file
                    print("bye")
                    output_file.write("EOF")
                    print("EXECUTION STOPPED\nOutput written in results.file")
                    break

                # else parse the input
                parsed_input = parse(user_input)
                result = eval(parsed_input)

                # Only print/write if result is not None
                if result is not None:
                    # Convert result to LISP format
                    # Convert boolean values to 'T' or 'NIL'
                    if isinstance(result, bool):
                        output = 'T' if result else 'NIL'
                    else:
                        # Convert result to LISP format
                        output = (lispexp(result))

                    # print output
                    print(output)
                    output_file.write(output)
                    output_file.write("\n")

            except Exception as e:
                print(f"Error: {e}")


def lispexp(value):
    if isinstance(value, list):
        return '(' + ' '.join(lispexp(item) for item in value) + ')'
    else:
        return str(value)


if __name__ == "__main__":
    main()
