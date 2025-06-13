# --- START OF THE DEFINITIVE, SIMPLIFIED views.py ---

def generate_product_html(products):
    """
    Takes a list of product dictionaries and generates just the HTML for the product cards.
    """
    if not products:
        return '<p class="text-center text-gray-500">No products available at the moment.</p>'

    product_cards = []
    for p in products:
        card_html = f"""
        <div class="bg-white rounded-lg shadow-md p-4 product-card">
            <div class="flex items-center space-x-4">
                <div class="w-16 h-16 pup-bg-burgundy rounded-lg flex items-center justify-center text-white">
                    <i class="fas fa-tshirt"></i>
                </div>
                <div class="flex-1">
                    <h4 class="font-semibold pup-text-burgundy">{p['name']}</h4>
                    <p class="text-sm text-gray-600">{p['description']}</p>
                    <div class="flex justify-between items-center mt-2">
                        <span class="font-bold pup-text-burgundy">₱{p['price']:.2f}</span>
                        <button onclick="handleAddToCart({p['id']})" class="bg-red-500 text-white px-4 py-1 rounded-full text-sm">ADD TO CART</button>
                    </div>
                </div>
            </div>
        </div>
        """
        product_cards.append(card_html)
    return "".join(product_cards)


def generate_full_page(products):
    """
    Generates the entire SPA page using a simple f-string template.
    This ensures the HTML structure is exactly as intended.
    """
    # Generate the HTML for all the product cards first.
    products_html_string = generate_product_html(products)

    # Now, place that product HTML into the main page template.
    # This is your "perfect" HTML sample, now acting as a template.
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PUP Mobile Store - StudywithStyle</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    <style>
        :root {{
            --pup-burgundy: #722F37;
        }}
        .pup-bg-burgundy {{ background-color: var(--pup-burgundy); }}
        .pup-text-burgundy {{ color: var(--pup-burgundy); }}
        
        .page-view, .app-view {{ display: none; }}
        .page-view.active, .app-view.active {{ display: block; }}

        .bottom-nav {{ position: fixed; bottom: 0; left: 0; right: 0; z-index: 50; }}
        .content-container {{ padding-bottom: 80px; }}
        .product-card {{ transition: transform 0.2s; }}
        .product-card:hover {{ transform: translateY(-2px); }}
        .cart-badge {{ position: absolute; top: -8px; right: -8px; background: #EF4444; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; align-items: center; justify-content: center; }}
    </style>
</head>
<body class="bg-gray-50 font-sans">

    <!-- Authentication View (Login/Register) -->
    <div id="auth-view" class="page-view active">
        <!-- Login Section -->
        <section id="login-section" class="auth-section active p-4">
            <div class="text-center mb-6">
                <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4"><i class="fas fa-star text-red-800 text-2xl"></i></div>
                <h2 class="text-2xl font-bold pup-text-burgundy">Welcome Back</h2>
            </div>
            <form id="login-form" class="bg-white rounded-lg shadow-lg p-6">
                <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Email Address:</label><input id="login-email" type="email" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500"></div>
                <div class="mb-6"><label class="block text-gray-700 font-semibold mb-2">Password:</label><input id="login-password" type="password" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500"></div>
                <div class="space-y-3"><button type="submit" class="w-full pup-bg-burgundy text-white py-3 rounded-lg font-semibold hover:bg-red-900 transition-colors">LOGIN</button><button onclick="showAuthSection('register-section')" type="button" class="w-full bg-cyan-400 text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors">Create Account</button></div>
            </form>
        </section>

        <!-- Registration Section -->
        <section id="register-section" class="auth-section p-4" style="display: none;">
            <div class="text-center mb-6"><div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4"><i class="fas fa-star text-red-800 text-2xl"></i></div><h2 class="text-2xl font-bold pup-text-burgundy">Mula sayo para sa bayan</h2></div>
            <form id="register-form" class="bg-white rounded-lg shadow-lg p-6">
                <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Name:</label><input id="register-name" type="text" class="w-full p-3 border border-gray-300 rounded-lg"></div>
                <div class="mb-4"><label class="block text-gray-700 font-semibold mb-2">Email Address:</label><input id="register-email" type="email" class="w-full p-3 border border-gray-300 rounded-lg"></div>
                <div class="mb-6"><label class="block text-gray-700 font-semibold mb-2">Password:</label><input id="register-password" type="password" class="w-full p-3 border border-gray-300 rounded-lg"></div>
                <div class="space-y-3"><button type="submit" class="w-full bg-cyan-500 text-white py-3 rounded-lg font-semibold hover:bg-cyan-600">REGISTER</button><button onclick="showAuthSection('login-section')" type="button" class="w-full bg-gray-300 text-gray-800 py-3 rounded-lg font-semibold">Back to LOGIN</button></div>
            </form>
        </section>
    </div>

    <!-- Main Application View (Homepage, Cart, etc.) -->
    <div id="main-app-view" class="page-view">
        <header class="pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3"><div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center"><i class="fas fa-star text-red-800"></i></div><div><h1 class="text-lg font-bold">StudywithStyle</h1><p class="text-xs opacity-90">PUP Official Store</p></div></div>
                <div class="flex space-x-3"><div class="relative"><button onclick="showAppSection('cart-app-view')" class="p-2 bg-black bg-opacity-20 rounded-full"><i class="fas fa-shopping-cart"></i></button><span id="header-cart-badge" class="cart-badge" style="display: none;">0</span></div><button onclick="showAppSection('profile-app-view')" class="p-2 bg-black bg-opacity-20 rounded-full"><i class="fas fa-user"></i></button></div>
            </div>
        </header>

        <main class="content-container">
            <!-- Homepage/Product Listing Section -->
            <section id="homepage-app-view" class="app-view active p-4">
                <div class="mb-6"><h2 class="text-2xl font-bold pup-text-burgundy mb-2">Featured Products</h2><p class="text-gray-600">Official PUP merchandise and study essentials</p></div>
                <div id="product-list" class="grid grid-cols-1 gap-4">
                    {products_html_string}
                </div>
            </section>
            
            <!-- Shopping Cart Section -->
            <section id="cart-app-view" class="app-view p-4">
                <h2 class="text-2xl font-bold pup-text-burgundy mb-4">Shopping Cart</h2>
                <div id="cart-items" class="space-y-4 mb-6"><div class="text-center text-gray-500 py-8"><i class="fas fa-shopping-cart text-4xl mb-4"></i><p>Your cart is empty</p></div></div>
                <div id="cart-summary" style="display: none;" class="bg-white rounded-lg shadow-lg p-4 mb-6"><div class="flex justify-between items-center text-lg font-bold pup-text-burgundy"><span>Total:</span><span id="cart-total">₱0</span></div></div>
                <button id="checkout-btn" onclick="handleCheckout()" style="display: none;" class="w-full pup-bg-burgundy text-white py-4 rounded-lg font-bold text-lg">CHECK OUT</button>
            </section>

            <!-- Profile Section -->
            <section id="profile-app-view" class="app-view p-4">
                <div class="text-center mb-6"><div class="w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4"><i class="fas fa-user text-3xl text-gray-600"></i></div><h2 class="text-2xl font-bold pup-text-burgundy">Profile</h2><p id="user-name-display" class="text-gray-600"></p></div>
                <button onclick="handleLogout()" class="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold">Logout</button>
            </section>
        </main>

        <nav class="bottom-nav pup-bg-burgundy text-white">
            <div class="flex justify-around items-center py-3">
                <button onclick="showAppSection('homepage-app-view')" class="nav-btn flex flex-col items-center space-y-1"><i class="fas fa-home text-xl"></i><span class="text-xs">Home</span></button>
                <button onclick="showAppSection('cart-app-view')" class="nav-btn flex flex-col items-center space-y-1 relative"><i class="fas fa-shopping-cart text-xl"></i><span class="text-xs">Cart</span><span id="nav-cart-badge" class="cart-badge" style="display: none;">0</span></button>
                <button onclick="showAppSection('profile-app-view')" class="nav-btn flex flex-col items-center space-y-1"><i class="fas fa-user text-xl"></i><span class="text-xs">Profile</span></button>
            </div>
        </nav>
    </div>

    <script>
        // --- State Management & Navigation ---
        function showAuthSection(sectionId) {{
            document.querySelectorAll('.auth-section').forEach(s => s.style.display = 'none');
            document.getElementById(sectionId).style.display = 'block';
        }}
        function showAppSection(sectionId) {{
            document.querySelectorAll('.app-view').forEach(s => s.style.display = 'none');
            document.getElementById(sectionId).style.display = 'block';
            if (sectionId === 'cart-app-view') {{
                loadCart();
            }}
        }}
        function showMainApp(user) {{
            document.getElementById('auth-view').style.display = 'none';
            document.getElementById('main-app-view').style.display = 'block';
            document.getElementById('user-name-display').textContent = `Welcome, ${{user.name}}!`;
            updateCartBadge();
        }}
        function showAuthView() {{
            document.getElementById('main-app-view').style.display = 'none';
            document.getElementById('auth-view').style.display = 'block';
            showAuthSection('login-section');
        }}

        // --- API-driven Handlers ---
        async function handleLogin(event) {{
            event.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            const result = await window.pywebview.api.login(email, password);
            if (result.success) {{
                showMainApp(result.user);
            }} else {{
                alert(result.message);
            }}
        }}
        async function handleRegister(event) {{
            event.preventDefault();
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const result = await window.pywebview.api.register(name, email, password);
            if (result.success) {{
                alert('Registration successful! Please log in.');
                showAuthSection('login-section');
            }} else {{
                alert(result.message);
            }}
        }}
        function handleLogout() {{ showAuthView(); }}
        async function handleAddToCart(productId) {{
            const result = await window.pywebview.api.add_to_cart(productId);
            if (result.status === 'success') {{
                showNotification('Added to cart!');
                updateCartBadge();
            }} else {{
                alert(result.message || 'Please log in to add items to your cart.');
            }}
        }}

        // --- Data Loading and Rendering ---
        async function loadCart() {{
            const items = await window.pywebview.api.get_cart();
            const container = document.getElementById('cart-items');
            const summary = document.getElementById('cart-summary');
            if (!items || items.length === 0) {{
                container.innerHTML = '<div class="text-center text-gray-500 py-8"><i class="fas fa-shopping-cart text-4xl mb-4"></i><p>Your cart is empty</p></div>';
                summary.style.display = 'none';
            }} else {{
                container.innerHTML = items.map(item => `
                    <div class="bg-white rounded-lg shadow-md p-4"><div class="flex items-center justify-between"><div class="flex items-center space-x-3"><div class="w-12 h-12 pup-bg-burgundy rounded flex items-center justify-center text-white"><i class="fas fa-gift"></i></div><div><h4 class="font-semibold pup-text-burgundy text-sm">${{item.name}}</h4><p class="text-gray-600 text-xs">₱${{item.price}}</p></div></div><div class="flex items-center space-x-2"><span class="w-8 text-center font-semibold">${{item.quantity}}</span></div></div></div>
                `).join('');
                const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                document.getElementById('cart-total').textContent = `₱${{total.toFixed(2)}}`;
                document.getElementById('checkout-btn').style.display = 'block';
                summary.style.display = 'block';
            }}
        }}
        async function updateCartBadge() {{
            const items = await window.pywebview.api.get_cart();
            const count = !items ? 0 : items.reduce((sum, item) => sum + item.quantity, 0);
            document.querySelectorAll('.cart-badge').forEach(b => {{
                b.style.display = count > 0 ? 'flex' : 'none';
                b.textContent = count;
            }});
        }}

        function showNotification(message) {{
            const el = document.createElement('div');
            el.className = 'fixed top-20 left-1/2 -translate-x-1/2 bg-green-500 text-white p-3 rounded-lg shadow-lg z-50';
            el.textContent = message;
            document.body.appendChild(el);
            setTimeout(() => el.remove(), 2000);
        }}
        
        function handleCheckout() {{ alert('Checkout not implemented.'); }}
        
        window.addEventListener('pywebviewready', () => {{
            document.getElementById('login-form').addEventListener('submit', handleLogin);
            document.getElementById('register-form').addEventListener('submit', handleRegister);
        }});
    </script>
</body>
</html>
    """
    return html_template

# --- END OF THE DEFINITIVE, SIMPLIFIED views.py ---