# kawal-pemilu-2024-image-scraper
A web scraper to collect and download images from Kawal Pemilu 2024 website for data analysis

---

````md
## Cara Menggunakan

1. **Pastikan Python dan Firefox terpasang**  
   Gunakan Python 3 dan browser Firefox (dibutuhkan oleh Selenium).

2. **Install dependensi**
   ```bash
   pip install selenium beautifulsoup4 requests webdriver-manager
````

3. **Atur URL awal (opsional)**
   Pada bagian `__main__`, ubah `parent_url` sesuai wilayah yang ingin di-scrape:

   ```python
   parent_url = "https://kawalpemilu.org/h/510806"
   ```

4. **Jalankan program**

   ```bash
   python scraper.py
   ```

5. **Proses otomatis berjalan**

   * Mengambil link wilayah turunan
   * Mengambil data TPS dan link gambar
   * Menyimpan data ke file CSV
   * Mengunduh gambar ke folder masing-masing wilayah

6. **Hasil output**

   * Data TPS tersimpan di: `hasil_multi_tps.csv`
   * Gambar tersimpan di folder: `img_<kode_wilayah>/`

Selesai. Tidak perlu konfigurasi tambahan.

```

---

Jika ingin, saya bisa:
- Memadatkan jadi **3 langkah saja**
- Menyesuaikan untuk **user non-teknis**
- Menambahkan **catatan error umum**

Tinggal bilang.
```
