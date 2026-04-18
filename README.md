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

Cara Menjalankan
1. Pastikan Python sudah terinstall.
2. Pastikan struktur project seperti berikut, bisa dilakukan dengan git clone

```
 project/
 ├── app.py
 ├── requirements.txt
 ├── templates/
 │   └── index.html
 └── static/
     └── style.css
```

```
 git clone https://github.com/IsabellaSienna01/B02_Otomata.git
```
3. Install dependency Flask:
```
 pip install -r requirements.txt
```
4. Jalankan program:
```
 python tokenizer.py
```
5. Buka browser, lalu akses:
```
 http://127.0.0.1:5000
```

7. Masukkan program yang ingin dicek dengan salah satu cara berikut:
- upload file kode seperti test.c
- tempel langsung kode program ke textarea
8. Tekan tombol Analyze untuk melihat hasil tokenisasi dan klasifikasinya.

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
