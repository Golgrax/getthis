def create_icon(icon_class):
    return f'<i class="fas {icon_class}"></i>'

def create_button(text, onclick, style_class):
    return f'<button onclick="{onclick}" type="button" class="{style_class}">{text}</button>'

def create_submit_button(text, style_class):
    return f'<button type="submit" class="{style_class}">{text}</button>'

# --- Page Section Generators ---

def generate_auth_view():
    login_form = f"""
    <section id="login-section" class="auth-section active p-4">
        <div class="text-center mb-6">
            <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4">{create_icon('fa-star text-red-800 text-2xl')}</div>
            <h2 class="text-2xl font-bold pup-text-burgundy">Welcome Back</h2>
        </div>
        <form id="login-form" class="bg-white rounded-lg shadow-lg p-6">
            <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Email:</label><input id="login-email" type="email" class="w-full p-3 border rounded-lg"></div>
            <div class="mb-6"><label class="block text-gray-700 font-semibold mb-2">Password:</label><input id="login-password" type="password" class="w-full p-3 border rounded-lg"></div>
            <div class="space-y-3">
                {create_submit_button('LOGIN', 'w-full pup-bg-burgundy text-white py-3 rounded-lg font-semibold')}
                {create_button('Create Account', "showAuthSection('register-section')", 'w-full bg-cyan-400 text-white py-3 rounded-lg font-semibold')}
            </div>
        </form>
    </section>
    """

    register_form = f"""
    <section id="register-section" class="auth-section p-4" style="display: none;">
        <div class="text-center mb-6"><div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4">{create_icon('fa-star text-red-800 text-2xl')}</div><h2 class="text-2xl font-bold pup-text-burgundy">Mula sayo para sa bayan</h2></div>
        <form id="register-form" class="bg-white rounded-lg shadow-lg p-6">
            <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Name:</label><input id="register-name" type="text" class="w-full p-3 border rounded-lg"></div>
            <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Email:</label><input id="register-email" type="email" class="w-full p-3 border rounded-lg"></div>
            <div class="mb-6"><label class="block text-gray-700 font-semibold mb-2">Password:</label><input id="register-password" type="password" class="w-full p-3 border rounded-lg"></div>
            <div class="space-y-3">
                {create_submit_button('REGISTER', 'w-full bg-cyan-500 text-white py-3 rounded-lg font-semibold')}
                {create_button('Back to LOGIN', "showAuthSection('login-section')", 'w-full bg-gray-300 text-gray-800 py-3 rounded-lg font-semibold')}
            </div>
        </form>
    </section>
    """
    return f'<div id="auth-view" class="page-view active">{login_form}{register_form}</div>'

def generate_main_app_view(products):
    products_html = ""
    for p in products:
        products_html += f"""
        <div class="bg-white rounded-lg shadow-md p-4 product-card">
            <div class="flex items-center space-x-4">
                <div class="w-16 h-16 pup-bg-burgundy rounded-lg flex items-center justify-center text-white">{create_icon('fa-tshirt')}</div>
                <div class="flex-1">
                    <h4 class="font-semibold pup-text-burgundy">{p['name']}</h4>
                    <p class="text-sm text-gray-600">{p['description']}</p>
                    <div class="flex justify-between items-center mt-2">
                        <span class="font-bold pup-text-burgundy">₱{p['price']:.2f}</span>
                        {create_button('ADD TO CART', f"handleAddToCart({p['id']})", 'bg-red-500 text-white px-4 py-1 rounded-full text-sm')}
                    </div>
                </div>
            </div>
        </div>
        """

    header_html = f"""
    <header class="pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3"><div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center">{create_icon('fa-star text-red-800')}</div><div><h1 class="text-lg font-bold">StudywithStyle</h1><p class="text-xs opacity-90">PUP Official Store</p></div></div>
            <div class="flex space-x-3"><div class="relative"><button onclick="showAppSection('cart-app-view')" class="p-2 bg-black bg-opacity-20 rounded-full">{create_icon('fa-shopping-cart')}</button><span id="header-cart-badge" class="cart-badge" style="display: none;">0</span></div><button onclick="showAppSection('profile-app-view')" class="p-2 bg-black bg-opacity-20 rounded-full">{create_icon('fa-user')}</button></div>
        </div>
    </header>
    """

    homepage_html = f"""
    <section id="homepage-app-view" class="app-view active p-4">
        <div class="mb-6"><h2 class="text-2xl font-bold pup-text-burgundy mb-2">Featured Products</h2><p class="text-gray-600">Official PUP merchandise</p></div>
        <div id="product-list" class="grid grid-cols-1 gap-4">{products_html}</div>
    </section>
    """

    cart_html = f"""
    <section id="cart-app-view" class="app-view p-4">
        <h2 class="text-2xl font-bold pup-text-burgundy mb-4">Shopping Cart</h2>
        <div id="cart-items" class="space-y-4 mb-6"></div>
        <div id="cart-summary" style="display: none;" class="bg-white rounded-lg shadow-lg p-4 mb-6"><div class="flex justify-between items-center text-lg font-bold pup-text-burgundy"><span>Total:</span><span id="cart-total">₱0</span></div></div>
        {create_button('CHECK OUT', 'handleCheckout()', 'w-full pup-bg-burgundy text-white py-4 rounded-lg font-bold text-lg')}
    </section>
    """

    profile_html = f"""
    <section id="profile-app-view" class="app-view p-4">
        <div class="text-center mb-6"><div class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4">{create_icon('fa-user text-3xl text-gray-600')}</div><h2 class="text-2xl font-bold pup-text-burgundy">Profile</h2><p id="user-name-display" class="text-gray-600"></p></div>
        {create_button('Logout', 'handleLogout()', 'w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold')}
    </section>
    """
    
    navbar_html = f"""
    <nav class="bottom-nav pup-bg-burgundy text-white">
        <div class="flex justify-around items-center py-3">
            <button onclick="showAppSection('homepage-app-view')" class="flex flex-col items-center">{create_icon('fa-home text-xl')}<span class="text-xs">Home</span></button>
            <button onclick="showAppSection('cart-app-view')" class="flex flex-col items-center relative">{create_icon('fa-shopping-cart text-xl')}<span class="text-xs">Cart</span><span id="nav-cart-badge" class="cart-badge" style="display: none;">0</span></button>
            <button onclick="showAppSection('profile-app-view')" class="flex flex-col items-center">{create_icon('fa-user text-xl')}<span class="text-xs">Profile</span></button>
        </div>
    </nav>
    """

    return f'<div id="main-app-view" class="page-view">{header_html}<main class="content-container">{homepage_html}{cart_html}{profile_html}</main>{navbar_html}</div>'


def generate_full_page(products):
    auth_view = generate_auth_view()
    main_app_view = generate_main_app_view(products)
    
    # This is the main template that holds everything together.
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PUP E-Commerce Shop</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <style>
        :root {{ --pup-burgundy: #722F37; }}
        body {{ font-family: sans-serif; }} /* Tailwind will override this */
        .pup-bg-burgundy {{ background-color: var(--pup-burgundy); }}
        .pup-text-burgundy {{ color: var(--pup-burgundy); }}
        .page-view, .app-view {{ display: none; }}
        .page-view.active, .app-view.active {{ display: block; }}
        .bottom-nav {{ position: fixed; bottom: 0; left: 0; right: 0; z-index: 50; }}
        .content-container {{ padding-bottom: 80px; }}
        .cart-badge {{ position: absolute; top: -8px; right: -8px; background: #EF4444; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; align-items: center; justify-content: center; }}
    </style>
</head>
<body class="bg-gray-50">
    {auth_view}
    {main_app_view}
    <script>
        // --- Navigation & State ---
        function showAuthSection(id) {{ document.querySelectorAll('.auth-section').forEach(s => s.style.display = 'none'); document.getElementById(id).style.display = 'block'; }}
        function showAppSection(id) {{ document.querySelectorAll('.app-view').forEach(s => s.style.display = 'none'); document.getElementById(id).style.display = 'block'; if (id === 'cart-app-view') loadCart(); }}
        function showMainApp(user) {{ document.getElementById('auth-view').style.display = 'none'; document.getElementById('main-app-view').style.display = 'block'; document.getElementById('user-name-display').textContent = `Welcome, ${{user.name}}!`; updateCartBadge(); }}
        function showAuthView() {{ document.getElementById('main-app-view').style.display = 'none'; document.getElementById('auth-view').style.display = 'block'; showAuthSection('login-section'); }}

        // --- API Handlers ---
        async function handleLogin(e) {{ e.preventDefault(); const email = document.getElementById('login-email').value; const password = document.getElementById('login-password').value; const r = await window.pywebview.api.login(email, password); if (r.success) showMainApp(r.user); else alert(r.message); }}
        async function handleRegister(e) {{ e.preventDefault(); const name = document.getElementById('register-name').value; const email = document.getElementById('register-email').value; const password = document.getElementById('register-password').value; const r = await window.pywebview.api.register(name, email, password); if (r.success) {{ alert('Registration successful! Please log in.'); showAuthSection('login-section'); }} else alert(r.message); }}
        async function handleLogout() {{ await window.pywebview.api.logout(); showAuthView(); }}
        async function handleAddToCart(id) {{ const r = await window.pywebview.api.add_to_cart(id); if (r.status === 'success') {{ showNotification('Added to cart!'); updateCartBadge(); }} else alert(r.message); }}
        async function handleUpdateQuantity(id, qty) {{ await window.pywebview.api.update_cart_quantity(id, qty); loadCart(); }}
        function handleCheckout() {{ alert('Checkout is not yet implemented. This would proceed to a payment page.'); }}

        // --- UI Rendering ---
        async function loadCart() {{
            const items = await window.pywebview.api.get_cart();
            const container = document.getElementById('cart-items');
            if (!items || items.length === 0) {{ container.innerHTML = '<div class="text-center text-gray-500 py-8">{create_icon("fa-shopping-cart text-4xl mb-4")}<p>Your cart is empty</p></div>'; document.getElementById('cart-summary').style.display = 'none'; return; }}
            container.innerHTML = items.map(item => `
                <div class="bg-white rounded-lg shadow-md p-4 flex items-center justify-between">
                    <div class="flex items-center space-x-3">{create_icon('fa-gift w-12 h-12 pup-bg-burgundy rounded flex items-center justify-center text-white')}<div><h4 class="font-semibold">${{item.name}}</h4><p class="text-xs">₱${{item.price.toFixed(2)}}</p></div></div>
                    <div class="flex items-center space-x-2"><button onclick="handleUpdateQuantity(${{item.id}}, ${{item.quantity - 1}})" class="w-8 h-8 bg-gray-200 rounded-full">-</button><span class="w-8 text-center">${{item.quantity}}</span><button onclick="handleUpdateQuantity(${{item.id}}, ${{item.quantity + 1}})" class="w-8 h-8 bg-gray-200 rounded-full">+</button></div>
                </div>
            `).join('');
            const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            document.getElementById('cart-total').textContent = `₱${{total.toFixed(2)}}`; document.getElementById('cart-summary').style.display = 'block';
        }}
        async function updateCartBadge() {{ const items = await window.pywebview.api.get_cart(); const count = !items ? 0 : items.reduce((sum, item) => sum + item.quantity, 0); document.querySelectorAll('.cart-badge').forEach(b => {{ b.style.display = count > 0 ? 'flex' : 'none'; b.textContent = count; }}); }}

        // --- Utility ---
        function showNotification(msg) {{ const el = document.createElement('div'); el.className = 'fixed top-20 left-1/2 -translate-x-1/2 bg-green-500 text-white p-3 rounded-lg z-50'; el.textContent = msg; document.body.appendChild(el); setTimeout(() => el.remove(), 2000); }}
        
        // --- Initializer ---
        window.addEventListener('pywebviewready', () => {{ document.getElementById('login-form').addEventListener('submit', handleLogin); document.getElementById('register-form').addEventListener('submit', handleRegister); }});
    </script>
</body>
</html>