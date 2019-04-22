from lexical_analysis import CLexicalAnalysis


def main():
    c_lexical_analysis = CLexicalAnalysis()
    source_code = input()
    while not source_code.endswith('$'):
        source_code += "\n{}".format(input())
    c_lexical_analysis.perform(list(source_code)[:-1])
    for identifier in c_lexical_analysis.identifiers:
        print(identifier)


if __name__ == '__main__':
    main()
