import requests
import subprocess

# Membuat permintaan GET ke API Laravel untuk mendapatkan data kontainer per kategori
url = 'http://10.0.0.19/api/containers'  # Ganti URL dengan URL API Laravel yang sesuai
response = requests.get(url)

# Memeriksa kode status permintaan
if response.status_code == 200:
    # Mendapatkan data JSON dari respons
    data = response.json()
    print(data)

    # Memproses data JSON
    for category, containers in data.items():
        print(f"Kategori: {category}")
        # for container in containers:
        #     if 'nama_kontainer' in container:
        #         print(f"Nama Kontainer: {container['nama_kontainer']}")
        #     else:
        #         print("Kunci 'nama_kontainer' tidak ditemukan dalam objek kontainer")
        #     # Lakukan operasi lain sesuai kebutuhan

        #     if 'nim' in container:
        #         print(f"NIM: {container['nim']}")
        #     else:
        #         print("Kunci 'nim' tidak ditemukan dalam objek kontainer")
        

        # Membuat file dengan nama kategori sebagai nama file
            nama_file = f"{category}.txt"
            isi_teks = f"Nama Kontainer: {container['nama_kontainer']}\nNIM: {container['nim']}"

            # Menjalankan perintah echo melalui shell untuk menulis ke file
            subprocess.run(['echo', isi_teks, '>', nama_file], shell=True)


else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
