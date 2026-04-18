# Token Analyzer (tokenizer.py)

## Deskripsi

Program ini merupakan implementasi sederhana dari **lexical analyzer (lexer)** yang digunakan dalam konsep dasar compiler.
Program membaca sebuah file kode sumber, kemudian memecahnya menjadi **token-token** dan mengelompokkannya berdasarkan jenisnya.

Token yang dihasilkan kemudian diklasifikasikan ke dalam beberapa kategori seperti:

* Reserved Word
* Operator
* Punctuation
* Variable
* Number
* String
* Comment

---

## Tujuan

* Memahami konsep dasar **tokenization**
* Mempelajari cara kerja **lexical analysis dalam compiler**
* Mengelompokkan elemen kode program menjadi token yang bermakna

---

## Fitur

* Membaca input dari file (C / Python / dll)
* Tokenisasi berbasis karakter (char-by-char parsing)
* Support:

  * String literal (`"..."`)
  * Komentar (`//` dan `/* */`)
  * Operator 1 dan 2 karakter (`+`, `==`, `>=`, dll)
  * Number (integer & float)
  * Identifier (variable)
* Klasifikasi token
* Statistik jumlah token
* Export hasil ke file (`hasil_token.txt`)

---

## Cara Menjalankan

1. Pastikan Python sudah terinstall
2. Siapkan file kode (contoh: `test.c`)
3. Jalankan program:

```bash
python tokenizer.py
```

4. Masukkan nama file:

```text
test.c
```

---

## Contoh Input (C)

```c
int x = 10;
float y = 3.14;

// komentar
if (x >= 10) {
    print("Hello");
}
```

---

## Contoh Output

```text
int             : Reserved Word
x               : Variable
=               : Operator
10              : Number
;               : Punctuation
```

---

## Klasifikasi Token

| Jenis Token   | Contoh         |
| ------------- | -------------- |
| Reserved Word | int, float, if |
| Variable      | x, y           |
| Operator      | +, -, ==, >=   |
| Number        | 10, 3.14       |
| String        | "Hello"        |
| Comment       | //..., /*...*/ |
| Punctuation   | ; ( ) { } ,    |

---

## Keterbatasan

* Belum mendukung escape character pada string (`\"`)
* Belum mendukung komentar Python (`#`)
* Multi-line string Python dianggap sebagai string biasa
* Tidak melakukan parsing sintaks (hanya lexical)

---

## 🧠 Konsep yang Digunakan

Program ini menggunakan pendekatan:

* **Finite State-like parsing**
* **Character-by-character scanning**
* **Greedy matching (operator 2 karakter didahulukan)**

---
