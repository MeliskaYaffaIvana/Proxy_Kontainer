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
        # Menulis konfigurasi frontend
        frontend_block = """
frontend haproxynode
    bind *:8080
    mode http
    option httplog
"""
        file.write(frontend_block + "\n")

        # Membuat list kosong untuk menyimpan konfigurasi
        config_lines = []

        # Memproses data JSON dan menyimpan konfigurasi ke list
        for category, containers in data.items():
            for container in containers:
                id = container['id']
                nim = container['nim']
                port = container['port']

                acl_line = f"    acl svr_{id} hdr(host) -i {nim}.jti.polinema.ac.id"
                use_backend_line = f"    use_backend be_{id} if svr_{id}"
                backend_block = f"""
backend be_{id}
    mode http
    option forwardfor
    server 10.0.0.21 10.0.0.21:{port}
"""

                # Menambahkan konfigurasi ke list
                config_lines.append(acl_line)
                config_lines.append(use_backend_line)
                config_lines.append(backend_block)

        # Menggabungkan semua konfigurasi dalam satu string
        config_text = "\n".join(config_lines)

        # Menulis konfigurasi ke file
        file.write(config_text)

else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
