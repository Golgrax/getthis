import base64


def _create_icon(icon_class):
    return f'<i class="fas {icon_class}"></i>'

def _generate_auth_view():
    html = f"""
    <div id="auth-view" class="page-view active">
        <section id="login-section" class="auth-section active p-4">
            <div class="text-center mb-6">
                <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4">{_create_icon('fa-star text-red-800 text-2xl')}</div>
                <h2 class="text-2xl font-bold pup-text-burgundy">Welcome Back</h2>
            </div>
            <form id="login-form" class="bg-white rounded-lg shadow-lg p-6 space-y-4">
                <div><label class="block font-semibold mb-1">Email:</label><input id="login-email" type="email" class="w-full p-3 border rounded-lg"></div>
                <div><label class="block font-semibold mb-1">Password:</label><input id="login-password" type="password" class="w-full p-3 border rounded-lg"></div>
                <div class="space-y-3 pt-2">
                    <button type="submit" class="w-full pup-bg-burgundy text-white py-3 rounded-lg font-semibold">LOGIN</button>
                    <button type="button" onclick="showAuthSection('register-section')" class="w-full bg-cyan-400 text-white py-3 rounded-lg font-semibold">Create Account</button>
                </div>
            </form>
        </section>
        <section id="register-section" class="auth-section p-4" style="display: none;">
             <!-- Register form HTML here -->
        </section>
    </div>
    """
    return base64.b64encode(html.encode('utf-8')).decode('utf-8')

def _generate_main_app_view(products):
    # Builds the HTML for the main application (header, content, nav)
    products_html = "".join([f'<div class="bg-white p-4 rounded-lg shadow-md flex items-center space-x-4"><div class="w-16 h-16 pup-bg-burgundy rounded-lg flex items-center justify-center text-white">{_create_icon("fa-tshirt")}</div><div class="flex-1"><h4 class="font-semibold">{p["name"]}</h4><p class="text-sm text-gray-500">₱{p["price"]:.2f}</p></div><button onclick="handleAddToCart({p["id"]})" class="bg-red-500 text-white px-4 py-2 rounded-full font-bold text-sm">ADD</button></div>' for p in products])
    
    html = f"""
    <div id="main-app-view" class="page-view">
        <header class="pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40">
             <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">{_create_icon('fa-star w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center text-red-800')}<div><h1 class="text-lg font-bold">StudywithStyle</h1></div></div>
                <div class="flex space-x-3"><button onclick="showAppSection('cart-app-view')" class="p-2 relative">{_create_icon('fa-shopping-cart')}<span id="header-cart-badge" class="cart-badge" style="display:none">0</span></button><button onclick="showAppSection('profile-app-view')" class="p-2">{_create_icon('fa-user')}</button></div>
             </div>
        </header>
        <main class="content-container">
            <section id="homepage-app-view" class="app-view active p-4"><div class="mb-4"><h2 class="text-2xl font-bold pup-text-burgundy">Products</h2></div><div class="space-y-4">{products_html}</div></section>
            <section id="cart-app-view" class="app-view p-4"><h2 class="text-2xl font-bold pup-text-burgundy mb-4">Shopping Cart</h2><div id="cart-items" class="space-y-4"></div><div id="cart-summary" class="mt-6 pt-4 border-t" style="display:none"><div class="flex justify-between font-bold text-lg"><p>Total:</p><p id="cart-total"></p></div><button onclick="showAppSection('checkout-app-view')" class="w-full mt-4 pup-bg-burgundy text-white py-3 rounded-lg font-bold">PROCEED TO CHECKOUT</button></div></section>
            <section id="checkout-app-view" class="app-view p-4"><h2 class="text-2xl font-bold pup-text-burgundy mb-4">Checkout</h2><div class="bg-white p-4 rounded-lg shadow"><h3 class="font-bold mb-2">Order Summary</h3><div id="checkout-summary-items" class="text-sm space-y-1"></div><div class="flex justify-between font-bold text-lg mt-4 border-t pt-2"><p>Total:</p><p id="checkout-total"></p></div></div><div class="bg-white p-4 rounded-lg shadow mt-4"><h3 class="font-bold mb-2">Payment</h3><p>Cash on Delivery</p></div><button onclick="handlePlaceOrder()" class="w-full mt-6 pup-bg-burgundy text-white py-3 rounded-lg font-bold">PLACE ORDER</button></section>
            <section id="profile-app-view" class="app-view p-4"><div class="text-center"><h2 id="user-name-display" class="text-2xl font-bold"></h2><button onclick="handleLogout()" class="mt-4 bg-gray-200 px-4 py-2 rounded">Logout</button></div></section>
        </main>
        <nav class="bottom-nav pup-bg-burgundy text-white"><div class="flex justify-around py-2"><button onclick="showAppSection('homepage-app-view')">{_create_icon('fa-home')}</button><button onclick="showAppSection('cart-app-view')" class="relative">{_create_icon('fa-shopping-cart')}<span id="nav-cart-badge" class="cart-badge" style="display:none">0</span></button><button onclick="showAppSection('profile-app-view')">{_create_icon('fa-user')}</button></div></nav>
    </div>
    """
    return base64.b64encode(html.encode('utf-8')).decode('utf-8')


def generate_full_page(products):
    # These variables now hold the OBFUSCATED HTML strings.
    auth_view_b64 = _generate_auth_view()
    main_app_view_b64 = _generate_main_app_view(products)

    # The main template is now very clean. It just holds the cryptic strings and the JS to decode them.
    return f"""
<!DOCTYPE html><html><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PUP E-Commerce Shop</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <style>:root{{--pup-burgundy:#722F37;}}.pup-bg-burgundy{{background-color:var(--pup-burgundy);}}.pup-text-burgundy{{color:var(--pup-burgundy);}}.page-view,.app-view{{display:none;}}.page-view.active,.app-view.active{{display:block;}}.bottom-nav{{position:fixed;bottom:0;left:0;right:0;z-index:50;}}.content-container{{padding-bottom:80px;}}.cart-badge{{position:absolute;top:-5px;right:-5px;background:#EF4444;color:white;border-radius:50%;width:18px;height:18px;font-size:11px;display:flex;align-items:center;justify-content:center;}}</style>
</head><body class="bg-gray-100">
    <div id="auth-placeholder"></div><div id="app-placeholder"></div>
    <script>
        // --- DECODER & INITIALIZER ---
        function decodeAndInject(b64, targetId) {{
            const decodedHtml = atob(b64); // atob() is the browser's built-in Base64 decoder
            document.getElementById(targetId).innerHTML = decodedHtml;
        }}
        window.addEventListener('pywebviewready', () => {{
            decodeAndInject('{auth_view_b64}', 'auth-placeholder');
            decodeAndInject('{main_app_view_b64}', 'app-placeholder');
            document.getElementById('login-form').addEventListener('submit', handleLogin);
        }});

        // --- Navigation & State ---
        function showAuthSection(id){{document.querySelectorAll('.auth-section').forEach(s=>s.style.display='none');document.getElementById(id).style.display='block';}}
        function showAppSection(id){{document.querySelectorAll('.app-view').forEach(s=>s.style.display='none');document.getElementById(id).style.display='block';if(id==='cart-app-view')loadCart();if(id==='checkout-app-view')loadCheckoutSummary();}}
        function showMainApp(user){{document.getElementById('auth-view').style.display='none';document.getElementById('main-app-view').style.display='block';document.getElementById('user-name-display').textContent=`Welcome, ${{user.name}}!`;updateCartBadge();}}
        function showAuthView(){{document.getElementById('main-app-view').style.display='none';document.getElementById('auth-view').style.display='block';showAuthSection('login-section');}}

        // --- API Handlers ---
        async function handleLogin(e){{e.preventDefault();const r=await window.pywebview.api.login(document.getElementById('login-email').value,document.getElementById('login-password').value);if(r.success)showMainApp(r.user);else alert(r.message);}}
        async function handleLogout(){{await window.pywebview.api.logout();showAuthView();}}
        async function handleAddToCart(id){{const r=await window.pywebview.api.add_to_cart(id);if(r.status==='success'){{showNotification('Added to cart!');updateCartBadge();}}else alert(r.message);}}
        async function handleUpdateQuantity(id,qty){{await window.pywebview.api.update_cart_quantity(id,qty);loadCart();}}
        async function handlePlaceOrder(){{const r=await window.pywebview.api.place_order();alert(r.message);if(r.success){{showAppSection('homepage-app-view');updateCartBadge();}}}}

        // --- UI Rendering ---
        async function loadCart(){{const items=await window.pywebview.api.get_cart();const cont=document.getElementById('cart-items');const summary=document.getElementById('cart-summary');if(!items||items.length===0){{cont.innerHTML='<p class="text-center text-gray-500 py-8">Your cart is empty.</p>';summary.style.display='none';return;}}cont.innerHTML=items.map(i=>`<div class="bg-white p-3 rounded shadow flex justify-between items-center"><div><p class="font-semibold">${{i.name}}</p><p class="text-xs text-gray-600">₱${{i.price.toFixed(2)}}</p></div><div class="flex items-center space-x-2"><button onclick="handleUpdateQuantity(${{i.id}},${{i.quantity-1}})" class="font-bold w-6 h-6 bg-gray-200 rounded-full">-</button><span>${{i.quantity}}</span><button onclick="handleUpdateQuantity(${{i.id}},${{i.quantity+1}})" class="font-bold w-6 h-6 bg-gray-200 rounded-full">+</button></div></div>`).join('');const total=items.reduce((s,i)=>s+(i.price*i.quantity),0);document.getElementById('cart-total').textContent=`₱${{total.toFixed(2)}}`;summary.style.display='block';}}
        async function loadCheckoutSummary(){{const items=await window.pywebview.api.get_cart();if(!items||items.length===0)return;const summaryCont=document.getElementById('checkout-summary-items');summaryCont.innerHTML=items.map(i=>`<div class="flex justify-between"><span>${{i.name}} x${{i.quantity}}</span><span>₱${{(i.price*i.quantity).toFixed(2)}}</span></div>`).join('');const total=items.reduce((s,i)=>s+(i.price*i.quantity),0);document.getElementById('checkout-total').textContent=`₱${{total.toFixed(2)}}`;}}
        async function updateCartBadge(){{const items=await window.pywebview.api.get_cart();const count=!items?0:items.reduce((s,i)=>s+i.quantity,0);document.querySelectorAll('.cart-badge').forEach(b=>{{b.style.display=count>0?'flex':'none';b.textContent=count;}});}}
        function showNotification(msg){{const el=document.createElement('div');el.className='fixed top-5 left-1/2 -translate-x-1/2 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg z-50';el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2000);}}
    </script>
</body></html>
    """