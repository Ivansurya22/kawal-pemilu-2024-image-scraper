# kawal-pemilu-2024-image-scraper
A web scraper to collect and download images from Kawal Pemilu 2024 website for data analysis

---
## Cara Menggunakan

### 1. Persiapan
````
Pastikan **Python 3** dan **Firefox** sudah terpasang di sistem.
```
pip install selenium beautifulsoup4 requests webdriver-manager
````

### 2. Atur URL Target (Opsional)

Ubah `parent_url` pada bagian `__main__` sesuai wilayah yang ingin diambil datanya:

```
parent_url = "https://kawalpemilu.org/h/510806"
```

### 3. Jalankan Program

```
python scraper.py
```

### 4. Proses Otomatis

Program akan secara otomatis:

* Mengambil link wilayah turunan
* Mengambil data TPS dan link gambar
* Menyimpan data ke file CSV
* Mengunduh gambar ke folder masing-masing wilayah

### 5. Hasil Output

* **Data TPS**: `hasil_multi_tps.csv`
* **Gambar**: `img_<kode_wilayah>/`
