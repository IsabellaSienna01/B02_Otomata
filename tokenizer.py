from flask import Flask, request, render_template, send_file
import io

app = Flask(__name__)

DOUBLE_OPERATORS = {"==", "!=", "<=", ">=", "&&", "||"}
SINGLE_OPERATORS = {"+", "-", "*", "/", "=", "<", ">"}
PUNCTUATION = {";", ",", "(", ")", "{", "}"}
KEYWORDS = {"int", "float", "if", "else", "while", "return", "for", "print"}


def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        c = code[i]

        if c.isspace():
            i += 1
            continue

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
                token += " [UNTERMINATED STRING]"
            tokens.append(token)
            continue

        if i + 1 < len(code) and code[i:i+2] == "//":
            token = ""
            while i < len(code) and code[i] != '\n':
                token += code[i]
                i += 1
            tokens.append(token)
            continue

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
                token += " [UNTERMINATED COMMENT]"
            tokens.append(token)
            continue

        if i + 1 < len(code) and code[i:i+2] in DOUBLE_OPERATORS:
            tokens.append(code[i:i+2])
            i += 2
            continue

        if c in SINGLE_OPERATORS:
            tokens.append(c)
            i += 1
            continue

        if c in PUNCTUATION:
            tokens.append(c)
            i += 1
            continue

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

        if c.isalpha() or c == "_":
            token = ""
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                token += code[i]
                i += 1
            tokens.append(token)
            continue

        tokens.append(c)
        i += 1

    return tokens


def classify(token):
    if token in KEYWORDS:
        return "Reserve Word"
    if token.startswith("//") or token.startswith("/*"):
        return "Comment"
    if token in DOUBLE_OPERATORS or token in SINGLE_OPERATORS:
        return "Kalimat Matematika / Operator"
    if token in PUNCTUATION:
        return "Simbol dan Tanda Baca"
    if token.startswith('"') and token.endswith('"'):
        return "String"
    if token.replace('.', '', 1).isdigit():
        return "Number"
    if token and (token[0].isalpha() or token[0] == "_"):
        return "Variabel"
    return "Unknown"


def count_tokens(tokens):
    stats = {}
    for token in tokens:
        token_type = classify(token)
        stats[token_type] = stats.get(token_type, 0) + 1
    return stats


@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    tokens = []
    stats = {}

    if request.method == "POST":
        uploaded_file = request.files.get("code_file")
        code_from_textarea = request.form.get("code", "")

        if uploaded_file and uploaded_file.filename:
            raw_data = uploaded_file.read()
            try:
                code = raw_data.decode("utf-8")
            except UnicodeDecodeError:
                code = raw_data.decode("latin-1")
        else:
            code = code_from_textarea

        if code.strip():
            tokens = tokenize(code)
            stats = count_tokens(tokens)

    token_rows = [(token, classify(token)) for token in tokens]

    return render_template(
        "index.html",
        code=code,
        tokens=tokens,
        token_rows=token_rows,
        stats=stats,
        total_tokens=len(tokens),
        total_categories=len(stats)
    )


@app.route("/download")
def download():
    code = request.args.get("code", "")
    tokens = tokenize(code)
    output = io.StringIO()

    for token in tokens:
        output.write(f"{token:20} : {classify(token)}\n")

    buffer = io.BytesIO(output.getvalue().encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="hasil_token.txt",
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(debug=True)
