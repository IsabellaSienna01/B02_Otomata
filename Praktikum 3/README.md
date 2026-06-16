# Automation PDA Simulator
Simulator Pushdown Automata (PDA) berbasis web yang interaktif untuk membantu visualisasi dan pemahaman konsep teori otomata. Aplikasi ini memungkinkan pengguna untuk merancang mesin PDA mereka sendiri atau menggunakan preset yang tersedia untuk menguji string tertentu.

---
Link Website: https://auto-pda.vercel.app/

## Fitur Utama

- **Konfigurasi Mesin Secara Kustom**: User dapat secara bebas menentukan state, alfabet input, alfabet stack, state awal, simbol stack awal, dan state penerima secara fleksibel.
- **Metode Penerimaan**: Mendukung dua metode penerimaan string:
  - **Final State**: String diterima jika mesin berakhir di salah satu state penerima.
  - **Empty Stack**: String diterima jika stack dalam keadaan kosong di akhir pemrosesan.
- **Visualisasi Interaktif**:
  - **Input Tape**: Melacak posisi pembacaan karakter pada string input.
  - **Stack Display**: Visualisasi tumpukan (stack) secara real-time.
  - **Transition Log**: Catatan riwayat transisi yang dilakukan mesin step-by-step.
- **Kontrol Simulasi**: Jalankan simulasi secara otomatis (Auto Play) atau manual (Next/Prev step).
- **Preset**: Tersedia preset siap pakai untuk kasus populer:
  - $a^n b^n$
  - Tanda Kurung Seimbang (Balanced Parentheses)
  - Odd Palindrome ($wcw^R$)
  - Even Palindrome ($ww^R$)

## Teknologi yang Digunakan

| Teknologi | Kegunaan |
| --- | --- |
| HTML5 | Struktur konten aplikasi |
| CSS3 (Vanilla) | Desain antarmuka yang modern dan responsif menggunakan CSS Grid dan Flexbox |
| JavaScript (Vanilla) | Logika simulator PDA dan manipulasi DOM |
| Google Fonts | Inter dan IBM Plex Mono untuk tipografi |

## Cara Penggunaan

1. **Konfigurasi Mesin**:
   - Masukkan definisi formal PDA (Q, Σ, Γ, q0, Z, F).
   - Tulis fungsi transisi dengan format: `State,Input,PopStack -> StateTujuan,PushStack`.
   - Gunakan `e` untuk melambangkan **Epsilon** (transisi kosong).
   - Klik **Terapkan Konfigurasi**.
2. **Uji String**:
   - Masukkan string yang ingin diuji pada panel "Uji String".
   - Klik **Cek Validasi**.
3. **Analisis Visual**:
   - Gunakan tombol **Auto Play** untuk melihat proses secara otomatis.
   - Gunakan **Next** atau **Prev** untuk meninjau transisi satu per satu.
   - Pantau perubahan pada **Input Tape** dan **Stack** di setiap langkahnya.

## Contoh Format Transisi

Jika Anda ingin menambahkan transisi di mana pada state `q0`, membaca input `a`, dan melakukan pop `Z`, lalu pindah ke `q0` dengan melakukan push `AZ`:
```
q0,a,Z -> q0,AZ
```

Untuk transisi epsilon (tanpa membaca input atau pop/push):
```
q1,e,Z -> q2,Z
```

---

© 2026 Kelompok B02 Otomata
