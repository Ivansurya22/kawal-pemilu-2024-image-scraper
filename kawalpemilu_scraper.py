import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


class KawalPemiluScraper:
    def __init__(self):
        # Setup Selenium Firefox
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.set_preference("dom.webdriver.enabled", False)
        self.driver = None
        
    def init_driver(self):
        """Initialize Selenium driver"""
        self.driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=self.options
        )
    
    def close_driver(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
    
    # ========================
    # STEP 1: Scrape Links
    # ========================
    def scrape_links(self, url):
        """Scrape all hierarchy links from a page"""
        print(f"\n[STEP 1] Scraping links dari: {url}")
        
        if not self.driver:
            self.init_driver()
        
        self.driver.get(url)
        time.sleep(3)
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        links = []
        for a in soup.find_all("a", class_="hierarchy"):
            href = a.get("href")
            if href:
                full_url = "https://kawalpemilu.org" + href
                links.append(full_url)
        
        print(f"Total link ditemukan: {len(links)}")
        return links
    
    # ========================
    # STEP 2: Scrape Data TPS
    # ========================
    def scrape_tps_data(self, urls, csv_filename="hasil_multi_tps.csv"):
        """Scrape TPS data from multiple URLs and save to CSV"""
        print(f"\n[STEP 2] Scraping data TPS dari {len(urls)} URL...")
        
        if not self.driver:
            self.init_driver()
        
        # Open CSV file
        csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "url",
            "nama_tps",
            "pas1",
            "pas2",
            "pas3",
            "dpt",
            "image_links",
            "pas1_gambar",
            "pas2_gambar",
            "pas3_gambar"
        ])
        
        for url in urls:
            self._scrape_page(url, csv_writer)
        
        csv_file.close()
        print(f"\n[STEP 2] Selesai! Data tersimpan di {csv_filename}")
        return csv_filename
    
    def _scrape_page(self, url, csv_writer):
        """Scrape single page"""
        self.driver.get(url)
        time.sleep(3)
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        tps_items = soup.find_all("div", class_="tps-item")
        print(f"Menemukan {len(tps_items)} TPS pada {url}")
        
        for item in tps_items:
            # Nama TPS
            tps_num = item.find("span", class_="tps-number")
            nama_tps = tps_num.get_text(strip=True) if tps_num else ""
            
            # Paslon result (angka atas)
            pas1 = pas2 = pas3 = ""
            r = item.find("span", class_="tps-result")
            if r:
                b = r.find_all("b")
                if len(b) == 3:
                    pas1 = b[0].get_text(strip=True)
                    pas2 = b[1].get_text(strip=True)
                    pas3 = b[2].get_text(strip=True)
            
            # DPT
            dpt = ""
            dpt_span = item.find("span", class_="tps-dpt")
            if dpt_span and dpt_span.find("b"):
                dpt = dpt_span.find("b").get_text(strip=True)
            
            # Angka bawah gambar
            pas1_g = pas2_g = pas3_g = ""
            pw = item.find("div", class_="paslon-wrapper")
            if pw:
                votes = pw.find_all("div", class_="vote")
                if votes:
                    vote_spans = votes[0].find_all("div")
                    for v in vote_spans:
                        text = v.get_text(strip=True)
                        if text.startswith("Pas1"):
                            pas1_g = text.split(":")[1].strip()
                        if text.startswith("Pas2"):
                            pas2_g = text.split(":")[1].strip()
                        if text.startswith("Pas3"):
                            pas3_g = text.split(":")[1].strip()
            
            # Gambar
            image_links = []
            image_tags = item.select("a")
            for im in image_tags:
                href = im.get("href")
                if href and "googleusercontent" in href:
                    image_links.append(href)
            
            img_out = "|".join(image_links) if image_links else ""
            
            # Simpan ke CSV
            csv_writer.writerow([
                url, nama_tps, pas1, pas2, pas3, dpt,
                img_out, pas1_g, pas2_g, pas3_g
            ])
            
            print(f"[OK] {nama_tps}: P1={pas1} P2={pas2} P3={pas3} DPT={dpt} Gambar={len(image_links)}")
    
    # ========================
    # STEP 3: Download Images
    # ========================
    def download_images(self, csv_filename="hasil_multi_tps.csv"):
        """Download all images from CSV file"""
        print(f"\n[STEP 3] Downloading gambar dari {csv_filename}...")
        
        with open(csv_filename, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                url = row["url"]
                imgs = row["image_links"]
                
                # Skip jika tidak ada gambar
                if not imgs.strip():
                    continue
                
                # Kode kelurahan dari URL
                kel_code = url.rstrip("/").split("/")[-1]
                
                # Buat folder
                folder = f"img_{kel_code}"
                os.makedirs(folder, exist_ok=True)
                
                # TPS numbering
                tps_name = row["nama_tps"]
                tps_num = ''.join([c for c in tps_name if c.isdigit()])
                if tps_num == "":
                    continue
                tps_3 = f"{int(tps_num):03d}"
                
                # Base filename
                base_filename = f"raw_{kel_code}_{tps_3}"
                
                # Download setiap gambar
                images = imgs.split("|")
                for i, img_url in enumerate(images, start=1):
                    ext = ".jpg"
                    filename = base_filename + (f"_{i}" if len(images) > 1 else "") + ext
                    save_path = os.path.join(folder, filename)
                    self._download_image(img_url, save_path)
        
        print("\n[STEP 3] Selesai download gambar!")
    
    def _download_image(self, url, save_path):
        """Download single image"""
        try:
            r = requests.get(url, timeout=10, stream=True)
            if r.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                print(f"[OK] Saved {save_path}")
            else:
                print(f"[SKIP] Status {r.status_code} for {url}")
        except Exception as e:
            print(f"[ERR] Gagal download {url} karena {e}")


# ========================
# MAIN EXECUTION
# ========================
if __name__ == "__main__":
    scraper = KawalPemiluScraper()
    
    try:
        # OPTION 1: Scrape links terlebih dahulu dari parent URL
        parent_url = "https://kawalpemilu.org/h/510806"
        links = scraper.scrape_links(parent_url)
        
        # OPTION 2: Atau gunakan list URL yang sudah ada
        # links = [
        #     "https://kawalpemilu.org/h/5108062016",
        #     "https://kawalpemilu.org/h/5108062002",
        #     # ... dst
        # ]
        
        # Scrape data TPS
        csv_file = scraper.scrape_tps_data(links)
        
        # Download gambar
        scraper.download_images(csv_file)
        
        print("\n" + "="*50)
        print("SEMUA PROSES SELESAI!")
        print("="*50)
        
    finally:
        scraper.close_driver()
