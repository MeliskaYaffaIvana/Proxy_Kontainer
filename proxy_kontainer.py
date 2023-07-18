import requests

# Membuat permintaan GET ke API Laravel untuk mendapatkan data kontainer per kategori
url = 'http://10.0.0.19/api/containers'  # Ganti URL dengan URL API Laravel yang sesuai
response = requests.get(url)

# Memeriksa kode status permintaan
if response.status_code == 200:
    # Mendapatkan data JSON dari respons
    data = response.json()

    # Membuat file untuk menyimpan semua konfigurasi
    nama_file = "proxy.txt"

    # Menyiapkan variabel untuk menyimpan data acl_line, use_backend_line, dan backend_block
    acl_lines = []
    use_backend_lines = []
    backend_blocks = []

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
    server 10.0.0.21:{port}
"""

            # Menyimpan data ke variabel
            acl_lines.append(acl_line)
            use_backend_lines.append(use_backend_line)
            backend_blocks.append(backend_block)

    # Menulis ke file menggunakan open()
    with open(nama_file, 'w') as file:
        # Menulis semua acl_line ke file
        for acl_line in acl_lines:
            file.write(acl_line + "\n")

        # Menulis semua use_backend_line ke file
        for use_backend_line in use_backend_lines:
            file.write(use_backend_line + "\n")

        # Menulis semua backend_block ke file
        for backend_block in backend_blocks:
            file.write(backend_block + "\n")

else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
