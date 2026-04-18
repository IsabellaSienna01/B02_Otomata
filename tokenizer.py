DOUBLE_OPERATORS = {"==", "!=", "<=", ">=", "&&", "||"}
SINGLE_OPERATORS = {"+", "-", "*", "/", "=", "<", ">"}
PUNCTUATION = {";", ",", "(", ")", "{", "}"}
KEYWORDS = {"int", "float", "if", "else", "while", "return", "for", "print"}


#FILE INPUT
def main():
    print("==== TOKEN ANALYZER (FILE MODE) ====")
    filename = input("Masukkan nama file (contoh: test.c): ")

    try:
        #coba utf-8 dulu
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except UnicodeDecodeError:
        #fallback kalau gagal
        with open(filename, "r", encoding="latin-1") as f:
            code = f.read()
    except FileNotFoundError:
        print("Error: file tidak ditemukan!")
        return ""

    print("\nFile berhasil dibaca!\n")
    print("Isi file:\n", code)
    return code


# TOKENIZER
def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        c = code[i]

        # skip spasi
        if c.isspace():
            i += 1
            continue

        # string
        if c == '"':
            token = '"'
            i += 1
            while i < len(code) and code[i] != '"':
                token += code[i]
                i += 1
            if i < len(code):
                token += '"'
                i += 1
            else:
                print("Warning: string tidak ditutup!")
            tokens.append(token)
            continue

        # comment //
        if i + 1 < len(code) and code[i:i+2] == "//":
            token = ""
            while i < len(code) and code[i] != '\n':
                token += code[i]
                i += 1
            tokens.append(token)
            continue

        # comment /* */
        if i + 1 < len(code) and code[i:i+2] == "/*":
            token = "/*"
            i += 2
            while i + 1 < len(code) and code[i:i+2] != "*/":
                token += code[i]
                i += 1
            if i + 1 < len(code):
                token += "*/"
                i += 2
            else:
                print("Warning: komentar tidak ditutup!")
            tokens.append(token)
            continue

        # double operator
        if i + 1 < len(code) and code[i:i+2] in DOUBLE_OPERATORS:
            tokens.append(code[i:i+2])
            i += 2
            continue

        #single operator
        if c in SINGLE_OPERATORS:
            tokens.append(c)
            i += 1
            continue

        #punctuation
        if c in PUNCTUATION:
            tokens.append(c)
            i += 1
            continue

        #number
        if c.isdigit():
            token = ""
            has_dot = False
            while i < len(code) and (code[i].isdigit() or (code[i] == '.' and not has_dot)):
                if code[i] == '.':
                    has_dot = True
                token += code[i]
                i += 1
            tokens.append(token)
            continue

        #identifier
        if c.isalpha() or c == "_":
            token = ""
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                token += code[i]
                i += 1
            tokens.append(token)
            continue

        #fallback
        tokens.append(c)
        i += 1

    return tokens


#CLASSIFIER
def classify(token):
    if token in KEYWORDS:
        return "Reserved Word"
    elif token.startswith("//") or token.startswith("/*"):
        return "Comment"
    elif token in DOUBLE_OPERATORS or token in SINGLE_OPERATORS:
        return "Operator"
    elif token in PUNCTUATION:
        return "Punctuation"
    elif token.startswith('"') and token.endswith('"'):
        return "String"
    elif token.replace('.', '', 1).isdigit():
        return "Number"
    elif token[0].isalpha() or token[0] == "_":
        return "Variable"
    else:
        return "Unknown"


#STATISTICS
def count_tokens(tokens):
    stats = {}
    for t in tokens:
        t_type = classify(t)
        stats[t_type] = stats.get(t_type, 0) + 1
    return stats


#OUTPUT
def print_tokens(tokens):
    print("\nHasil:")
    for t in tokens:
        print(f"{t:15} : {classify(t)}")


def print_stats(stats):
    print("\nStatistik:")
    for k, v in stats.items():
        print(f"{k:15} : {v}")


def save_to_file(tokens):
    with open("hasil_token.txt", "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(f"{t:15} : {classify(t)}\n")
    print("\nHasil disimpan ke hasil_token.txt")


#MAIN
if __name__ == "__main__":
    code = main()

    if code == "":
        exit()

    tokens = tokenize(code)

    print_tokens(tokens)

    stats = count_tokens(tokens)
    print_stats(stats)

    save_to_file(tokens)