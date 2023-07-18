import requests

# Membuat permintaan GET ke API Laravel untuk mendapatkan data kontainer per kategori
url = 'http://10.0.0.19/api/containers'  # Ganti URL dengan URL API Laravel yang sesuai
response = requests.get(url)

# Memeriksa kode status permintaan
if response.status_code == 200:
    # Mendapatkan data JSON dari respons
    data = response.json()

    # Membuat file untuk menyimpan semua konfigurasi
    nama_file = "config.txt"

    # Menulis ke file menggunakan open()
    with open(nama_file, 'w') as file:
        # Memproses data JSON
        for category, containers in data.items():
            for container in containers:
                id = container['id']
                nim = container['nim']
                port = container['port']

                acl_line = f"    acl svr_{id} hdr(host) -i {nim}.jti.polinema.ac.id"
                use_backend_line = f"    use_{category} be_{id} if svr_{id}"
                backend_block = f"""
{category} be_{id}
    mode http
    option forwardfor
    server 10.0.0.21 10.0.0.21:{port}
"""

                # Menulis konfigurasi ke file
                file.write(acl_line + "\n")
                file.write(use_backend_line + "\n")
                file.write(backend_block)
                file.write("\n")  # Menambahkan baris kosong sebagai pemisah antara konfigurasi

else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
