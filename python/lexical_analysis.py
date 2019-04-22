from simplesm.simplesm import SimpleSM


class CLexicalAnalysis(SimpleSM):
    keywords = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum",
                "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed",
                "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    punctuations = "{}()[];,."
    signs = "+-/*=!<>&|"
    strings = "\""
    delimiters = "\t\n "
    all = digits + letters + punctuations + signs + strings + delimiters

    stream = ""
    identifiers = []

    start_state = "ST0"
    states = {
        "ST0": {
            "transitions": {
                "is_digit": {"state": "NUM1", "event": "update_stream"},
                "is_letter": {"state": "ID", "event": "update_stream"},
                "is_punctuation": {"state": "ST0", "event": "print_punctuation"},
                "is_delimiter": {"state": "ST0"},
                "\"": {"state": "STR", "event": "update_stream"},
                "+": {"state": "OPP", "event": "update_stream"},
                "-": {"state": "OPS", "event": "update_stream"},
                "*": {"state": "OPM", "event": "update_stream"},
                "=": {"state": "OPA", "event": "update_stream"},
                "!": {"state": "OPN", "event": "update_stream"},
                "<": {"state": "OPL", "event": "update_stream"},
                ">": {"state": "OPG", "event": "update_stream"},
                "&": {"state": "OPZ", "event": "update_stream"},
                "|": {"state": "OPX", "event": "update_stream"},
                "/": {"state": "OPD1", "event": "update_stream"},
                "other": {"state": "OTH", "event": "update_stream"}}},
        "NUM1": {
            "transitions": {
                "is_digit": {"state": "NUM1", "event": "update_stream"},
                ".": {"state": "NUM2", "event": "update_stream"},
                "e": {"state": "NUM4", "event": "update_stream"},
                "E": {"state": "NUM4", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_num1"}}},
        "NUM2": {
            "transitions": {
                "is_digit": {"state": "NUM3", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_error_ungetch"}}},
        "NUM3": {
            "transitions": {
                "is_digit": {"state": "NUM3", "event": "update_stream"},
                "e": {"state": "NUM4", "event": "update_stream"},
                "E": {"state": "NUM4", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_num3"}}},
        "NUM4": {
            "transitions": {
                "is_digit": {"state": "NUM6", "event": "update_stream"},
                "-": {"state": "NUM5", "event": "update_stream"},
                "+": {"state": "NUM5", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_error_ungetch"}}},
        "NUM5": {
            "transitions": {
                "is_digit": {"state": "NUM6", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_error_ungetch"}}},
        "NUM6": {
            "transitions": {
                "is_digit": {"state": "NUM6", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_num6"}}},
        "OPP": {
            "transitions": {
                "+": {"state": "ST0", "event": "do_opp_inc"},
                "=": {"state": "ST0", "event": "do_opp_add_assign"},
                "other": {"state": "ST0", "event": "do_opp_add"}}},
        "OPS": {
            "transitions": {
                "-": {"state": "ST0", "event": "do_ops_dec"},
                "=": {"state": "ST0", "event": "do_ops_sub_assign"},
                "other": {"state": "ST0", "event": "do_ops_sub"}}},
        "OPM": {
            "transitions": {
                "=": {"state": "ST0", "event": "do_opm_mul_assign"},
                "other": {"state": "ST0", "event": "do_opm_mul"}}},
        "OPA": {
            "transitions": {
                "=": {"state": "ST0", "event": "do_opa_eq"},
                "other": {"state": "ST0", "event": "do_opa_assign"}}},
        "OPN": {
            "transitions": {
                "=": {"state": "ST0", "event": "do_opn_ne"},
                "other": {"state": "ST0", "event": "do_opn_not"}}},
        "OPG": {
            "transitions": {
                "=": {"state": "ST0", "event": "do_opg_ge"},
                "other": {"state": "ST0", "event": "do_opg_gt"}}},
        "OPL": {
            "transitions": {
                "=": {"state": "ST0", "event": "do_opl_le"},
                "other": {"state": "ST0", "event": "do_opl_lt"}}},
        "OPZ": {
            "transitions": {
                "&": {"state": "ST0", "event": "do_opz_and"},
                "other": {"state": "ST0", "event": "do_error_ungetch"}}},
        "OPX": {
            "transitions": {
                "|": {"state": "ST0", "event": "do_opx_or"},
                "other": {"state": "ST0", "event": "do_error_ungetch"}}},
        "OPD1": {
            "transitions": {
                "*": {"state": "OPD2", "event": "update_stream"},
                "/": {"state": "OPD4", "event": "update_stream"},
                "=": {"state": "ST0", "event": "do_opd1_div_assign"},
                "other": {"state": "ST0", "event": "do_opd1_div"}}},
        "OPD2": {
            "transitions": {
                "*": {"state": "OPD3", "event": "update_stream"},
                "other": {"state": "OPD2", "event": "update_stream"}}},
        "OPD3": {
            "transitions": {
                "*": {"state": "OPD3", "event": "update_stream"},
                "/": {"state": "ST0", "event": "clear_stream"},
                "other": {"state": "OPD2", "event": "update_stream"}}},
        "OPD4": {
            "transitions": {
                "\n": {"state": "ST0", "event": "clear_stream"},
                "other": {"state": "OPD4", "event": "update_stream"}}},
        "STR": {
            "transitions": {
                "\"": {"state": "ST0", "event": "do_str"},
                "other": {"state": "STR", "event": "update_stream"}}},
        "ID": {
            "transitions": {
                "is_letter": {"state": "ID", "event": "update_stream"},
                "is_digit": {"state": "ID", "event": "update_stream"},
                "other": {"state": "ST0", "event": "do_id"}}},
        "OTH": {
            "transitions": {
                "is_in_all": {"state": "ST0", "event": "print_error"},
                "other": {"state": "OTH", "event": "update_stream"}}},
    }

    # type check
    def is_digit(self):
        if self.test_action in self.digits:
            return True
        return False

    def is_letter(self):
        if self.test_action in self.letters:
            return True
        return False

    def is_punctuation(self):
        if self.test_action in self.punctuations:
            return True
        return False

    def is_delimiter(self):
        if self.test_action in self.delimiters:
            return True
        return False

    def is_in_all(self):
        if self.test_action in self.all:
            return True
        return False

    def other(self):
        return True

    # prints
    def print_ungetch(self):
        if not self.test_action in self.delimiters:
            print("ungetch")

    def print_error(self):
        print("Error")
        self.stream = ""

    def print_num(self, _type):
        print("{}\t{}".format(self.stream, _type))
        self.stream = ""

    def print_str(self):
        print("{}\tSTR".format(self.stream))
        self.stream = ""

    def print_punctuation(self):
        print("{}\tPUNCTUATION".format(self.test_action))
        self.stream = ""

    def print_identifier(self):
        print("{}\tIDENTIFIER".format(self.stream))
        if self.stream in self.identifiers:
            print('false')
        else:
            print('true')
            self.identifiers.append(self.stream)
        self.stream = ""

    def print_operator(self, _type):
        print("{}\t{}".format(self.stream, _type))
        self.stream = ""

    def print_keyword(self):
        print("{}\tKEYWORD".format(self.stream))
        self.stream = ""

    # states definitions
    def update_stream(self):
        self.stream += self.test_action

    def clear_stream(self):
        self.stream = ""

    def do_error_ungetch(self):
        self.print_error()
        self.print_ungetch()
        self.perform(self.test_action)

    def do_num1(self):
        self.print_num('INT')
        self.print_ungetch()
        self.perform(self.test_action)

    def do_num3(self):
        self.print_num('REAL')
        self.print_ungetch()
        self.perform(self.test_action)

    def do_num6(self):
        self.print_num('SCI')
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opp_inc(self):
        self.update_stream()
        self.print_operator("INC")

    def do_opp_add_assign(self):
        self.update_stream()
        self.print_operator("ADD_ASSIGN")

    def do_opp_add(self):
        self.print_operator("ADD")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_ops_dec(self):
        self.update_stream()
        self.print_operator("DEC")

    def do_ops_sub_assign(self):
        self.update_stream()
        self.print_operator("SUB_ASSIGN")

    def do_ops_sub(self):
        self.print_operator("SUB")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opm_mul_assign(self):
        self.update_stream()
        self.print_operator("MUL_ASSIGN")

    def do_opm_mul(self):
        self.print_operator("MUL")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opa_eq(self):
        self.update_stream()
        self.print_operator("EQ")

    def do_opa_assign(self):
        self.print_operator("ASSIGN")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opn_ne(self):
        self.update_stream()
        self.print_operator("NE")

    def do_opn_not(self):
        self.print_operator("NOT")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opg_ge(self):
        self.update_stream()
        self.print_operator("GE")

    def do_opg_gt(self):
        self.print_operator("GT")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opl_le(self):
        self.update_stream()
        self.print_operator("LE")

    def do_opl_lt(self):
        self.print_operator("LT")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_opz_and(self):
        self.update_stream()
        self.print_operator("AND")

    def do_opx_or(self):
        self.update_stream()
        self.print_operator("OR")

    def do_opd1_div_assign(self):
        self.update_stream()
        self.print_operator("DIV_ASSIGN")

    def do_opd1_div(self):
        self.print_operator("DIV")
        self.print_ungetch()
        self.perform(self.test_action)

    def do_str(self):
        self.update_stream()
        self.print_str()

    def do_id(self):
        if self.stream in self.keywords:
            self.print_keyword()
        else:
            self.print_identifier()
        self.print_ungetch()
        self.perform(self.test_action)
