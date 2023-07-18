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

    # Menyiapkan teks awal file
    teks_awal = """global
    log /dev/log    local0
    log /dev/log    local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Default SSL material locations
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private

    # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log    global
    mode    http
    option    httplog
    option    dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

"""

    # Menulis teks awal ke file
    with open(nama_file, 'w') as file:
        file.write(teks_awal)

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
