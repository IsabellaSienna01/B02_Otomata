# FSM Recognizer (fsm-recognizer.py)
---
## Deskripsi
Program ini merupakan implementasi Deterministic Finite Automaton (DFA) yang berfungsi sebagai language recognizer. Program digunakan untuk memvalidasi apakah suatu string biner termasuk dalam bahasa formal:

$L = \{ x \in (0+1)^+ \mid x \text{ berakhir dengan } 1 \text{ dan tidak mengandung } 00 \}$

Antarmuka pengguna dibangun menggunakan pustaka Tkinter, sehingga pengguna dapat melihat proses transisi state secara visual dan interaktif.

## Tujuan
* **Otomasi Identifikasi**
Memvalidasi string biner sesuai aturan bahasa formal secara cepat dan akurat.
* **Visualisasi Konsep FSM**
Membantu pemahaman konsep Finite State Machine melalui tampilan graf state dan transisi.
* **Analisis Step-by-Step**
Menyediakan trace log untuk menelusuri proses pembacaan string karakter demi karakter.

## Fitur
* **Diagram State Interaktif**
Menampilkan graf FSM dengan penyorotan (highlight) state aktif secara real-time.
* **Simulasi Animasi**
Proses transisi berjalan otomatis per karakter dengan jeda waktu tertentu.
* **Validasi Input**
Hanya menerima karakter 0 dan 1, dengan notifikasi jika input tidak valid.
* **Trace Log Detail**
Menampilkan tabel proses dengan format: (Step, From State, Input Symbol, To State) beserta status akhir (Accepted/Rejected).
* **Statistik Sederhana**
Menghitung jumlah string yang diterima dan ditolak selama program berjalan.

## Cara Menjalankan
1. Pastikan Python sudah terinstall.
2. Lakukan git clone
    ```bash
    git clone https://github.com/IsabellaSienna01/B02_Otomata.git
    ```
3. Masuk ke direktori `Praktikum 2`
    ```bash
    cd "Praktikum 2"
    ```
4. Jalankan program pada terminal:
    ```bash
    python fsm-recognizer.py
    ```
5. Cara penggunaan:
    1. Masukkan string biner (contoh: 101, 1101) pada kolom input.
    2. Tekan tombol RUN atau Enter.
    3. Program akan menampilkan:
        * Animasi Perpindahan state
        * Trace log proses
        * Status akhir string (Accepted/Rejected)  

## Definisi State
FSM terdiri dari 4 State utama:
| State | Peran           | Deskripsi                          |
|------|----------------|----------------------------------|
| S    | Initial State  | State awal sebelum input dibaca  |
| A    | Transient      | State terakhir membaca `0`       |
| B    | Accept (Final) | State terakhir membaca `1`       |
| C    | Dead / Trap    | Menemukan substring `00`         |

## Kriteria Accepted
String akan diterima jika:
 * Tidak mengandung substring `00`
 * Karakter terakhir adalah `1`.
 * State akhir berada di B (Accept State).

## Konsep yang Digunakan
* **Deterministic Finite Automaton (DFA)**
Setiap input memiliki satu transisi yang pasti (tidak ambigu).
* **State Transition Mapping**
Menggunakan struktur data seperti dictionary untuk mendefinisikan perpindahan state.
* **Event-Driven Programming**
GUI merespon input pengguna melalui event (klik tombol / keyboard).
