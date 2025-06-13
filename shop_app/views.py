import dominate
from dominate.tags import *
from dominate.util import raw

# Helper function for a single form field
def form_field(label_text, input_id, input_type='text', placeholder=''):
    with div(class_='mb-4'):
        label(label_text, _for=input_id, class_='block text-gray-700 font-semibold mb-2')
        input_(id=input_id, type=input_type, placeholder=placeholder, class_='w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500')

# --- SECTION CREATORS (Functions that build parts of the page) ---

def _create_login_section():
    with section(id='login', class_='section p-4 active'): # Active by default
        with div(class_='text-center mb-6'):
            with div(class_='w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4'):
                i(class_='fas fa-star text-red-800 text-2xl')
            h2('Welcome Back', class_='text-2xl font-bold pup-text-burgundy')
        with form(id='login-form', class_='bg-white rounded-lg shadow-lg p-6'):
            form_field('Email Address:', 'login-email', 'email', 'iskolar@pup.edu.ph')
            form_field('Password:', 'login-password', 'password')
            with div(class_='space-y-3 mt-4'):
                button('LOGIN', type='submit', class_='w-full pup-bg-burgundy text-white py-3 rounded-lg font-semibold hover:bg-red-900 transition-colors')
                button('Create Account', type='button', onclick="showAuthSection('register')", class_='w-full bg-cyan-400 text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-colors')

def _create_register_section():
    with section(id='register', class_='section p-4'): # Hidden by default
        with div(class_='text-center mb-6'):
            with div(class_='w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4'):
                i(class_='fas fa-star text-red-800 text-2xl')
            h2('Mula sayo para sa bayan', class_='text-2xl font-bold pup-text-burgundy')
        with form(id='register-form', class_='bg-white rounded-lg shadow-lg p-6'):
            form_field('Name:', 'register-name', 'text', 'Juan Dela Cruz')
            form_field('Email Address:', 'register-email', 'email', 'juan.delacruz@iskolar.pup.edu.ph')
            form_field('Password:', 'register-password', 'password')
            with div(class_='space-y-3 mt-4'):
                 button('REGISTER', type='submit', class_='w-full bg-cyan-500 text-white py-3 rounded-lg font-semibold hover:bg-cyan-600 transition-colors')
                 button('Back to LOGIN', type='button', onclick="showAuthSection('login')", class_='w-full bg-gray-300 text-gray-800 py-3 rounded-lg font-semibold hover:bg-gray-400 transition-colors')

def _create_main_app_shell():
    with header(id='main-header', class_='pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40'):
        with div(class_='flex items-center justify-between'):
            with div(class_='flex items-center space-x-3'):
                with div(class_='w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center'):
                    i(class_='fas fa-star text-red-800')
                with div():
                    h1('StudywithStyle', class_='text-lg font-bold')
                    p('PUP Official Store', class_='text-xs opacity-90')
            with div(class_='flex space-x-3'):
                with button(onclick="showAppSection('cart')", class_='relative p-2 bg-black bg-opacity-20 rounded-full'):
                    i(class_='fas fa-shopping-cart')
                    span(id="cart-badge", class_='cart-badge', style='display: none;')
                button(onclick="showAppSection('profile')", class_='p-2 bg-black bg-opacity-20 rounded-full')

    with main(class_='content-container'):
        _create_homepage_section()
        _create_cart_section()
        _create_profile_section()

    with nav(id='bottom-nav', class_='bottom-nav pup-bg-burgundy text-white'):
        with div(class_='flex justify-around items-center py-3'):
            with button(onclick="showAppSection('homepage')", class_='nav-btn flex flex-col items-center space-y-1'):
                i(class_='fas fa-home text-xl')
                span('Home', class_='text-xs')
            with button(onclick="showAppSection('cart')", class_='nav-btn flex flex-col items-center space-y-1 relative'):
                i(class_='fas fa-shopping-cart text-xl')
                span('Cart', class_='text-xs')
                span(id='nav-cart-badge', class_='cart-badge', style='display: none;')
            with button(onclick="showAppSection('profile')", class_='nav-btn flex flex-col items-center space-y-1'):
                i(class_='fas fa-user text-xl')
                span('Profile', class_='text-xs')

def _create_homepage_section():
    with section(id='homepage', class_='app-section active p-4'):
        with div(class_="mb-6"):
            h2("Featured Products", class_="text-2xl font-bold pup-text-burgundy mb-2")
            p("Official PUP merchandise and study essentials", class_="text-gray-600")
        with div(id="product-list", class_="grid grid-cols-1 md:grid-cols-2 gap-4"):
            p("Loading products...")

def _create_cart_section():
    with section(id='cart', class_='app-section p-4'):
        h2("Shopping Cart", class_="text-2xl font-bold pup-text-burgundy mb-4")
        div(id="cart-items", class_="space-y-4 mb-6")
        with div(id="cart-summary", style="display: none;", class_="bg-white rounded-lg shadow-lg p-4 mb-6"):
            with div(class_="flex justify-between items-center text-lg font-bold pup-text-burgundy"):
                span("Total:")
                span(id="cart-total")
            button('CHECK OUT', id="checkout-btn", onclick="checkout()", class_="w-full mt-4 pup-bg-burgundy text-white py-3 rounded-lg font-bold")

def _create_profile_section():
    with section(id='profile', class_='app-section p-4'):
        with div(class_='text-center mb-6'):
            div(class_='w-20 h-20 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4', _children=[i(class_='fas fa-user text-3xl text-gray-600')])
            h2('Profile', class_='text-2xl font-bold pup-text-burgundy')
            p(id="user-name-display", class_="text-gray-600")
        button('Logout', onclick='handleLogout()', class_='w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold')


def generate_full_page():
    doc = dominate.document(title="PUP E-Commerce Shop")
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")

        # --- THIS IS THE CRITICAL CHANGE ---
        # 1. Use the Tailwind Play CDN script instead of the static CSS link.
        # 2. Configure our custom font and colors directly inside it.
        script(src="https://cdn.tailwindcss.com")
        script(raw("""
            tailwind.config = {
              theme: {
                extend: {
                  colors: {
                    'pup-burgundy': '#722F37',
                    'pup-gold': '#FFD700',
                  },
                  fontFamily: {
                    sans: ['RocaOne', 'sans-serif'],
                  }
                }
              }
            }
        """))
        # ------------------------------------

        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css")
        link(rel="stylesheet", href="/static/css/style.css") # Still needed for the @font-face rule

        style(raw("""
            /* This is now much simpler */
            .main-app-container { display: none; }
            .section, .app-section { display: none; }
            .section.active, .app-section.active { display: block; }
            .pup-text-burgundy { color: #722F37; }
            .pup-bg-burgundy { background-color: #722F37; }
            .cart-badge { position: absolute; top: -8px; right: -8px; background: #EF4444; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; align-items: center; justify-content: center; }
            .content-container { padding-bottom: 80px; }
            .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; z-index: 50; }
        """))

    doc.body['class'] = 'bg-gray-50 font-sans' # The custom font is now applied via tailwind.config
    with doc:
        with div(id='auth-container'):
            _create_login_section()
            _create_register_section()
        with div(id='main-app-container'):
            _create_main_app_shell()

        script(raw("""
            // --- STATE & NAVIGATION ---
            function showAuthSection(sectionName) { /* ... same as before ... */ }
            function showAppSection(sectionName) { /* ... same as before ... */ }
            // ... all other javascript functions are the same ...
            
            // --- STATE MANAGEMENT & NAVIGATION ---
            function showAuthSection(sectionName) {
                document.querySelectorAll('#auth-container .section').forEach(s => s.classList.remove('active'));
                document.getElementById(sectionName).classList.add('active');
            }
            
            function showAppSection(sectionName) {
                document.querySelectorAll('#main-app-container .app-section').forEach(s => s.classList.remove('active'));
                document.getElementById(sectionName).classList.add('active');
                if (sectionName === 'cart') loadCart();
            }

            function showMainApp(user) {
                document.getElementById('auth-container').style.display = 'none';
                document.getElementById('main-app-container').style.display = 'block';
                document.getElementById('user-name-display').textContent = `Welcome, ${user.name}!`;
                loadProducts();
                updateCartBadge();
            }

            function showAuthView() {
                document.getElementById('main-app-container').style.display = 'none';
                document.getElementById('auth-container').style.display = 'block';
                showAuthSection('login');
            }

            // --- API-driven Handlers ---
            async function handleLogin(event) {
                event.preventDefault();
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;
                const result = await window.pywebview.api.login(email, password);
                if (result.success) {
                    showMainApp(result.user);
                } else {
                    alert(result.message);
                }
            }

            async function handleRegister(event) {
                event.preventDefault();
                const name = document.getElementById('register-name').value;
                const email = document.getElementById('register-email').value;
                const password = document.getElementById('register-password').value;
                const result = await window.pywebview.api.register(name, email, password);
                if (result.success) {
                    alert('Registration successful! Please log in.');
                    showAuthSection('login');
                } else {
                    alert(result.message);
                }
            }
            
            function handleLogout() {
                // In a real app, you'd call an API to clear the server session
                // For now, we just switch the view
                showAuthView();
            }

            // --- Data Loading and Rendering ---
            async function loadProducts() {
                const products = await window.pywebview.api.get_products();
                const container = document.getElementById('product-list');
                container.innerHTML = products.map(p => `
                    <div class="bg-white rounded-lg shadow-md p-4 flex flex-col justify-between">
                        <div>
                           <div class="w-full h-32 bg-gray-200 rounded-lg flex items-center justify-center text-gray-500 mb-4">
                                <i class="fas fa-tshirt fa-3x"></i>
                           </div>
                           <h4 class="font-semibold pup-text-burgundy">${p.name}</h4>
                        </div>
                        <div class="flex justify-between items-center mt-4">
                            <span class="font-bold text-lg pup-text-burgundy">₱${p.price.toFixed(2)}</span>
                            <button onclick="addToCart(${p.id})" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full font-bold text-sm">ADD</button>
                        </div>
                    </div>
                `).join('') || '<p>No products found.</p>';
            }
            
            async function addToCart(productId) {
                const result = await window.pywebview.api.add_to_cart(productId);
                if (result.status === 'success') {
                    showNotification('Added to cart!');
                    updateCartBadge();
                } else {
                    alert(result.message);
                }
            }
            
            async function loadCart() {
                const items = await window.pywebview.api.get_cart();
                const container = document.getElementById('cart-items');
                const summary = document.getElementById('cart-summary');
                if (items.length === 0) {
                    container.innerHTML = '<div class="text-center text-gray-500 py-8"><i class="fas fa-shopping-cart text-4xl mb-4"></i><p>Your cart is empty</p></div>';
                    summary.style.display = 'none';
                } else {
                    container.innerHTML = items.map(item => `
                        <div class="bg-white rounded-lg p-3 flex justify-between items-center">
                            <div>
                                <h4 class="font-semibold pup-text-burgundy">${item.name}</h4>
                                <p class="text-sm text-gray-500">x ${item.quantity}</p>
                            </div>
                            <p class="font-bold">₱${(item.price * item.quantity).toFixed(2)}</p>
                        </div>`).join('');
                    const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                    document.getElementById('cart-total').textContent = `₱${total.toFixed(2)}`;
                    document.getElementById('checkout-btn').textContent = `CHECK OUT (₱${total.toFixed(2)})`;
                    summary.style.display = 'block';
                }
            }
            
            async function updateCartBadge() {
                const items = await window.pywebview.api.get_cart();
                const count = items.reduce((sum, item) => sum + item.quantity, 0);
                document.querySelectorAll('.cart-badge').forEach(b => {
                    b.style.display = count > 0 ? 'flex' : 'none';
                    b.textContent = count;
                });
            }

            // --- Init & Util ---
            function showNotification(message) {
                const notification = document.createElement('div');
                notification.className = 'fixed top-20 left-1/2 -translate-x-1/2 bg-green-500 text-white p-3 rounded-lg shadow-lg z-50';
                notification.textContent = message;
                document.body.appendChild(notification);
                setTimeout(() => notification.remove(), 2000);
            }
            
            function checkout() { alert('Checkout not implemented.'); }

            window.addEventListener('pywebviewready', () => {
                document.getElementById('login-form').addEventListener('submit', handleLogin);
                document.getElementById('register-form').addEventListener('submit', handleRegister);
            });
        """))
    return doc
