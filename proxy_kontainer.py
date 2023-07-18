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
        for container in containers:
            id = container['id']
            nim = container['nim']
            port = container['port']

            acl_line = f"acl svr_{category}_{id} hdr(host) -i {nim}.jti.polinema.ac.id"
            use_backend_line = f"use_backend be_{category}_{id} if svr_{category}_{id}"
            backend_block = f"""
backend be_{category}_{id}
    mode http
    option forwardfor
    server 10.0.0.21 10.0.0.21:{port}
"""

            # Membuat file dengan nama kategori dan id sebagai nama file
            nama_file = f"{category}_{id}.txt"

            # Menulis ke file menggunakan open()
            with open(nama_file, 'w') as file:
                file.write(acl_line + "\n")
                file.write(use_backend_line + "\n")
                file.write(backend_block)

else:
    print(f"Permintaan gagal dengan kode status {response.status_code}")
