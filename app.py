from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Memori sementara untuk menyimpan pesanan
daftar_pesanan = []
nomor_antrean = 1

# ROUTE 1: Halaman Luas/Publik (Untuk orang di rumah)
@app.route('/')
def index():
    # Hanya menampilkan halaman index (tanpa form pemesanan dan antrean)
    return render_template('index.html')

# ROUTE 2: Halaman Khusus Outlet (Akses via Scan QR Code)
@app.route('/pesan-di-outlet', methods=['GET', 'POST'])
def pesan_di_outlet():
    global nomor_antrean
    if request.method == 'POST':
        nama = request.form.get('nama')
        menu = request.form.get('menu')
        topping = request.form.get('topping')
        pembayaran = request.form.get('pembayaran')

        harga_dasar = 15000
        tambahan = 2000 if topping else 0
        total_harga = harga_dasar + tambahan

        pesanan_baru = {
            'id': nomor_antrean,
            'nama': nama,
            'menu': menu,
            'topping': 'Extra Topping (+Rp 2.000)' if topping else 'Tanpa Topping',
            'pembayaran': pembayaran,
            'total': total_harga,
            'status': 'Menunggu ⏳'
        }
        daftar_pesanan.append(pesanan_baru)
        nomor_antrean += 1
        return redirect(url_for('pesan_di_outlet')) 

    # Tampilkan antrean hanya di halaman outlet
    antrean_aktif = [p for p in daftar_pesanan if p['status'] != 'Selesai ✅']
    return render_template('outlet.html', antrean=antrean_aktif)

# ROUTE 3: Halaman Kasir
@app.route('/kasir')
def kasir():
    total_pendapatan = sum(p['total'] for p in daftar_pesanan if p['status'] == 'Selesai ✅')
    return render_template('kasir.html', pesanan=daftar_pesanan, total_pendapatan=total_pendapatan)

# ROUTE 4: Update Status Kasir
@app.route('/update_status/<int:id>/<aksi>')
def update_status(id, aksi):
    for p in daftar_pesanan:
        if p['id'] == id:
            if aksi == 'dimasak':
                p['status'] = 'Sedang Dimasak 🍳'
            elif aksi == 'selesai':
                p['status'] = 'Selesai ✅'
    return redirect(url_for('kasir'))

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)