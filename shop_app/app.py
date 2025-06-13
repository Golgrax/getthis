from flask import Flask, jsonify
from . import payload

app = Flask(__name__, static_folder='../assets', static_url_path='/static')

XOR_KEY = "PUP-Sinta-2024-IskolarNgBayan"

@app.route('/')
def bootloader():
    """secure application."""
    bootloader_html = f"""
<!DOCTYPE html><html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>PUP E-Commerce Shop</title>
    <script src="https://cdn.tailwindcss.com"></script><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <style>:root{{--pup-burgundy:#722F37;}}.pup-bg-burgundy{{background-color:var(--pup-burgundy);}}.pup-text-burgundy{{color:var(--pup-burgundy);}}.page-view,.app-view{{display:none;}}.page-view.active,.app-view.active{{display:block;}}.bottom-nav{{position:fixed;bottom:0;left:0;right:0;z-index:50;}}.content-container{{padding-bottom:80px;}}.cart-badge{{position:absolute;top:-5px;right:-5px;background:#EF4444;color:white;border-radius:50%;width:18px;height:18px;font-size:11px;display:flex;align-items:center;justify-content:center;}}</style>
</head>
<body class="bg-gray-100">
    <div id="root"><p style="text-align:center;padding:4rem;font-family:sans-serif;">Loading Secure Application...</p></div>
    <script>
        const K="{XOR_KEY}";
        function D(b){{const s=atob(b);let r="";for(let i=0;i<s.length;i++)r+=String.fromCharCode(s.charCodeAt(i)^K.charCodeAt(i%K.length));return r;}}
        async function I(){{try{{const r=await fetch('/data');const p=await r.json();const root=document.getElementById('root');root.innerHTML=D(p.auth)+D(p.app);document.getElementById('login-form').addEventListener('submit',handleLogin);document.getElementById('register-form').addEventListener('submit',handleRegister);L();}}catch(e){{root.innerHTML='<p style="color:red;text-align:center;">Failed to load application.</p>';console.error("Bootloader Error:",e);}}}}
        
        function L(){{
            window.pywebview.api.get_products().then(p => {{
                if (!p) return;
                document.getElementById('product-list').innerHTML = p.map(i => `
                    <div class="bg-white p-4 rounded-lg shadow-md flex items-center space-x-4">
                        <img src="${{i.image_url || '/static/images/placeholder.png'}}" alt="${{i.name}}" class="w-20 h-20 object-cover rounded-lg bg-gray-200">
                        <div class="flex-1">
                            <h4 class="font-semibold">${{i.name}}</h4>
                            <p class="text-sm text-gray-500">₱${{i.price.toFixed(2)}}</p>
                        </div>
                        <button onclick="handleAddToCart(${{i.id}})" class="bg-red-500 text-white px-4 py-2 rounded-full font-bold text-sm">ADD</button>
                    </div>
                `).join('') || '<p>No products available.</p>';
            }});
        }}

        function showAuthSection(id){{document.querySelectorAll('.auth-section').forEach(s=>s.style.display='none');document.getElementById(id).style.display='block';}}
        function showAppSection(id){{document.querySelectorAll('.app-view').forEach(s=>s.style.display='none');document.getElementById(id).style.display='block';if(id==='cart-app-view')loadCart();if(id==='checkout-app-view')loadCheckoutSummary();}}
        function showMainApp(user){{document.getElementById('auth-view').style.display='none';document.getElementById('main-app-view').style.display='block';document.getElementById('user-name-display').textContent=`Welcome, ${{user.name}}!`;updateCartBadge();}}
        function showAuthView(){{document.getElementById('main-app-view').style.display='none';document.getElementById('auth-view').style.display='block';showAuthSection('login-section');}}
        async function handleLogin(e){{e.preventDefault();const r=await window.pywebview.api.login(document.getElementById('login-email').value,document.getElementById('login-password').value);if(r.success)showMainApp(r.user);else alert(r.message);}}
        async function handleRegister(e){{e.preventDefault();const r=await window.pywebview.api.register(document.getElementById('register-name').value,document.getElementById('register-email').value,document.getElementById('register-password').value);if(r.success){{alert('Registration successful!');showAuthSection('login-section');}}else alert(r.message);}}
        async function handleLogout(){{await window.pywebview.api.logout();showAuthView();}}
        async function handleAddToCart(id){{const r=await window.pywebview.api.add_to_cart(id);if(r.status==='success'){{showNotification('Added to cart!');updateCartBadge();}}else alert(r.message);}}
        async function handleUpdateQuantity(id,qty){{await window.pywebview.api.update_cart_quantity(id,qty);loadCart();}}
        async function handlePlaceOrder(){{const r=await window.pywebview.api.place_order();alert(r.message);if(r.success){{showAppSection('homepage-app-view');updateCartBadge();}}}}
        async function loadCart(){{const items=await window.pywebview.api.get_cart();const cont=document.getElementById('cart-items');const summary=document.getElementById('cart-summary');if(!items||items.length===0){{cont.innerHTML='<p class="text-center text-gray-500 py-8">Your cart is empty.</p>';summary.style.display='none';return;}}cont.innerHTML=items.map(i=>`<div class="bg-white p-3 rounded shadow flex justify-between items-center"><div><p class="font-semibold">${{i.name}}</p><p class="text-xs text-gray-600">₱${{i.price.toFixed(2)}}</p></div><div class="flex items-center space-x-2"><button onclick="handleUpdateQuantity(${{i.id}},${{i.quantity-1}})" class="font-bold w-6 h-6 bg-gray-200 rounded-full">-</button><span>${{i.quantity}}</span><button onclick="handleUpdateQuantity(${{i.id}},${{i.quantity+1}})" class="font-bold w-6 h-6 bg-gray-200 rounded-full">+</button></div></div>`).join('');const total=items.reduce((s,i)=>s+(i.price*i.quantity),0);document.getElementById('cart-total').textContent=`₱${{total.toFixed(2)}}`;summary.style.display='block';}}
        async function loadCheckoutSummary(){{const items=await window.pywebview.api.get_cart();if(!items||items.length===0)return;const summaryCont=document.getElementById('checkout-summary-items');summaryCont.innerHTML=items.map(i=>`<div class="flex justify-between"><span>${{i.name}} x${{i.quantity}}</span><span>₱${{(i.price*i.quantity).toFixed(2)}}</span></div>`).join('');const total=items.reduce((s,i)=>s+(i.price*i.quantity),0);document.getElementById('checkout-total').textContent=`₱${{total.toFixed(2)}}`;}}
        async function updateCartBadge(){{const items=await window.pywebview.api.get_cart();const count=!items?0:items.reduce((s,i)=>s+i.quantity,0);document.querySelectorAll('.cart-badge').forEach(b=>{{b.style.display=count>0?'flex':'none';b.textContent=count;}});}}
        function showNotification(msg){{const el=document.createElement('div');el.className='fixed top-5 left-1/2 -translate-x-1/2 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50';el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2000);}}
        
        window.addEventListener('pywebviewready', I);
    </script>
</body></html>
    """
    return bootloader_html

@app.route('/data')
def get_payload_data():
    """Serves the obfuscated UI data as JSON."""
    return jsonify({'auth': payload.AUTH_PAYLOAD, 'app': payload.APP_PAYLOAD})