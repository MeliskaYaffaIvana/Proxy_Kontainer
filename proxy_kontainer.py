import requests

# Membuat permintaan GET ke API Laravel untuk mendapatkan data kontainer per kategori
url = 'http://10.0.0.19/api/containers'  # Ganti URL dengan URL API Laravel yang sesuai
response = requests.get(url)

# Memeriksa kode status permintaan
if response.status_code == 200:
    # Mendapatkan data JSON dari respons
    data = response.json()
    
    # Memproses data JSON
    for category, containers in data.items():
        print(f"Kategori: {category}")
        for container in containers:
            print(f"Nama Kontainer: {container['nama_kontainer']}")
            # Lakukan operasi lain sesuai kebutuhan
            
else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
