from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Kunci untuk sesi, pastikan aman dan unik

# Dummy produk untuk simulasi
products = [
    {'id': 1, 'name': 'Produk A', 'price': 100000, 'description': 'Produk A adalah produk terbaik!', 'image': 'https://via.placeholder.com/150'},
    {'id': 2, 'name': 'Produk B', 'price': 150000, 'description': 'Produk B sangat berkualitas!', 'image': 'https://via.placeholder.com/150'},
    {'id': 3, 'name': 'Produk C', 'price': 200000, 'description': 'Produk C populer di kalangan anak muda!', 'image': 'https://via.placeholder.com/150'}
]

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Route untuk halaman detail produk
@app.route('/product/<int:product_id>')
def product(product_id):
    # Ambil produk dari ID
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Produk tidak ditemukan!", 404
    return render_template('product.html', product=product)

# Route untuk menambahkan produk ke cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Ambil produk dari ID
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Produk tidak ditemukan!", 404

    # Ambil kuantitas dari form
    quantity = int(request.form['quantity'])

    # Inisialisasi cart jika belum ada
    if 'cart' not in session:
        session['cart'] = []

    # Tambahkan produk ke cart dengan kuantitas
    session['cart'].append({'id': product['id'], 'name': product['name'], 
                            'price': product['price'], 'quantity': quantity})
    session.modified = True
    return redirect(url_for('cart'))


# Route untuk melihat cart
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total_price)

# Route untuk menghapus produk dari cart
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart_items = session.get('cart', [])
    # Hapus produk berdasarkan ID
    session['cart'] = [item for item in cart_items if item['id'] != product_id]
    session.modified = True
    return redirect(url_for('cart'))

# Route untuk halaman checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Ambil data dari form
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        voucher = int(request.form['voucher'])  # Diskon dalam persen
        shipping_cost = int(request.form['shipping'])  # Ongkos kirim
        
        # Ambil data dari cart
        cart_items = session.get('cart', [])
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Hitung diskon berdasarkan voucher
        if voucher == 5 and total_price >= 100000:
            discount = total_price * 0.05
        elif voucher == 10 and total_price >= 200000:
            discount = total_price * 0.10
        elif voucher == 15 and total_price >= 300000:
            discount = total_price * 0.15
        else:
            discount = 0
        
        # Total akhir
        final_price = total_price - discount + shipping_cost
        
        # Reset cart setelah checkout
        session.pop('cart', None)
        
        # Tampilkan halaman konfirmasi
        return render_template(
            'confirmation.html',
            name=name,
            address=address,
            phone=phone,
            cart_items=cart_items,
            total_price=total_price,
            discount=discount,
            shipping_cost=shipping_cost,
            final_price=final_price,
            success_message="Checkout Berhasil!"
        )
    
    # Jika GET, tampilkan halaman checkout
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('checkout.html', cart=cart_items, total=total_price)




if __name__ == '__main__':
    app.run(debug=True)
