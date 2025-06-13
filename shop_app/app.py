from flask import Flask, jsonify
from . import layout_payload
from . import content_payload
import base64

app = Flask(__name__, static_folder='../assets', static_url_path='/static')

CLEAN_JS_BOOTLOADER = """
    async function initializeUI() {
        try {
            const response = await fetch('/content');
            const payload = await response.json();
            decryptAndInject(payload.c, 'root');
            loadProductList();
            attachEventListeners();
        } catch (e) {
            console.error("Failed to initialize UI:", e);
            document.getElementById('root').innerHTML = '<p style="color:red;text-align:center;">Error: Could not load application content.</p>';
        }
    }

    function loadProductList() {
        window.pywebview.api.get_products().then(products => {
            if (!products) return;
            const productListHTML = products.map(p => `
                <div class='bg-white p-4 rounded-lg shadow-md flex items-center space-x-4'>
                    <img src='${p.image_url || '/static/images/placeholder.png'}' alt='${p.name}' class='w-20 h-20 object-cover rounded-lg'>
                    <div class='flex-1'>
                        <h4 class='font-semibold'>${p.name}</h4>
                        <p class='text-sm text-gray-500'>₱${p.price.toFixed(2)}</p>
                    </div>
                    <button onclick='handleAddToCart(${p.id})' class='bg-red-500 text-white px-4 py-2 rounded-full font-bold text-sm'>ADD</button>
                </div>
            `).join('');
            document.getElementById('product-list').innerHTML = productListHTML || '<p>No products found.</p>';
        });
    }

    function attachEventListeners() {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
        document.getElementById('register-form').addEventListener('submit', handleRegister);
    }

    function showAuthSection(id) { document.querySelectorAll('.auth-section').forEach(s => s.style.display = 'none'); document.getElementById(id).style.display = 'block'; }
    function showAppSection(id) { document.querySelectorAll('.app-view').forEach(s => s.style.display = 'none'); document.getElementById(id).style.display = 'block'; if (id === 'cart-app-view') loadCart(); if (id === 'checkout-app-view') loadCheckoutSummary(); }
    function showMainApp(user) { document.getElementById('auth-view').style.display = 'none'; document.getElementById('main-app-view').style.display = 'block'; document.getElementById('user-name-display').textContent = `Welcome, ${user.name}!`; updateCartBadge(); }
    function showAuthView() { document.getElementById('main-app-view').style.display = 'none'; document.getElementById('auth-view').style.display = 'block'; showAuthSection('login-section'); }

    async function handleLogin(e) { e.preventDefault(); const r = await window.pywebview.api.login(document.getElementById('login-email').value, document.getElementById('login-password').value); if (r.success) showMainApp(r.user); else alert(r.message); }
    async function handleRegister(e) { e.preventDefault(); const r = await window.pywebview.api.register(document.getElementById('register-name').value, document.getElementById('register-email').value, document.getElementById('register-password').value); if (r.success) { alert('Success!'); showAuthSection('login-section'); } else alert(r.message); }
    async function handleLogout() { await window.pywebview.api.logout(); showAuthView(); }
    async function handleAddToCart(id) { const r = await window.pywebview.api.add_to_cart(id); if (r.status === 'success') { showNotification('Added to cart!'); updateCartBadge(); } else alert(r.message); }
    async function handleUpdateQuantity(id, qty) { await window.pywebview.api.update_cart_quantity(id, qty); loadCart(); }
    async function handlePlaceOrder() { const r = await window.pywebview.api.place_order(); alert(r.message); if (r.success) { showAppSection('homepage-app-view'); updateCartBadge(); } }

    async function loadCart() { const items = await window.pywebview.api.get_cart(); const cont = document.getElementById('cart-items'); const summary = document.getElementById('cart-summary'); if (!items || items.length === 0) { cont.innerHTML = '<p class=text-center text-gray-500 py-8>Your cart is empty.</p>'; summary.style.display = 'none'; return; } cont.innerHTML = items.map(i => `<div class=bg-white p-3 rounded shadow flex justify-between items-center><div><p class=font-semibold>${i.name}</p><p class=text-xs text-gray-600>₱${i.price.toFixed(2)}</p></div><div class=flex items-center space-x-2><button onclick=handleUpdateQuantity(${i.id},${i.quantity - 1}) class='font-bold w-6 h-6 bg-gray-200 rounded-full'>-</button><span>${i.quantity}</span><button onclick=handleUpdateQuantity(${i.id},${i.quantity + 1}) class='font-bold w-6 h-6 bg-gray-200 rounded-full'>+</button></div></div>`).join(''); const total = items.reduce((s, i) => s + (i.price * i.quantity), 0); document.getElementById('cart-total').textContent = `₱${total.toFixed(2)}`; summary.style.display = 'block'; }
    async function loadCheckoutSummary() { const items = await window.pywebview.api.get_cart(); if (!items || items.length === 0) return; const summaryCont = document.getElementById('checkout-summary-items'); summaryCont.innerHTML = items.map(i => `<div class=flex justify-between><span>${i.name} x${i.quantity}</span><span>₱${(i.price * i.quantity).toFixed(2)}</span></div>`).join(''); const total = items.reduce((s, i) => s + (i.price * i.quantity), 0); document.getElementById('checkout-total').textContent = `₱${total.toFixed(2)}`; }
    async function updateCartBadge() { const items = await window.pywebview.api.get_cart(); const count = !items ? 0 : items.reduce((s, i) => s + i.quantity, 0); document.querySelectorAll('.cart-badge').forEach(b => { b.style.display = count > 0 ? 'flex' : 'none'; b.textContent = count; }); }
    
    function showNotification(msg) { const el = document.createElement('div'); el.className = 'fixed top-5 left-1/2 -translate-x-1/2 bg-green-600 text-white px-4 py-2 z-50'; el.textContent = msg; document.body.appendChild(el); setTimeout(() => el.remove(), 2000); }
    
    window.addEventListener('pywebviewready', initializeUI);
"""

JS_BOOTLOADER_KEY = "JavaScriptSecretKey"

def get_bootloader_script():
    encrypted_chars = [chr(ord(CLEAN_JS_BOOTLOADER[i]) ^ ord(JS_BOOTLOADER_KEY[i % len(JS_BOOTLOADER_KEY)])) for i in range(len(CLEAN_JS_BOOTLOADER))]
    encoded_payload = base64.b64encode("".join(encrypted_chars).encode('utf-8')).decode('utf-8')
    decoder_js = f"const K='{JS_BOOTLOADER_KEY}';function D(b,t){{const s=atob(b);let r='';for(let i=0;i<s.length;i++)r+=String.fromCharCode(s.charCodeAt(i)^K.charCodeAt(i%K.length));if(t)document.getElementById(t).innerHTML=r;else eval(r);}}D('{encoded_payload}');"
    return f"<script>{decoder_js}</script>"

@app.route('/')
def main_route():
    layout_html = layout_payload.layout_builder.b()
    bootloader_script = get_bootloader_script()
    final_html = layout_html.replace('{bootloader_script}', bootloader_script)
    return final_html

@app.route('/content')
def content_route():
    content = content_payload.content_builder.b()
    return jsonify({'c': content})
