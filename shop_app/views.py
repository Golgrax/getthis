import dominate
from dominate.tags import *

def generate_main_page(products):
    doc = dominate.document(title="PUP Mobile Store - StudywithStyle")

    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")
        link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css")
        link(rel="stylesheet", href="/static/css/style.css") # Link to our custom font styles

        style("""
            :root {
                --pup-burgundy: #722F37; --pup-gold: #FFD700; --pup-dark-burgundy: #5A252A;
            }
            body { font-family: 'RocaOne', sans-serif; } /* Ensure custom font is used */
            .pup-bg-burgundy { background-color: var(--pup-burgundy); }
            .pup-text-burgundy { color: var(--pup-burgundy); }
            .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; z-index: 50; }
            .content-container { padding-bottom: 80px; }
            .section { display: none; }
            .section.active { display: block; }
            .cart-badge {
                position: absolute; top: -8px; right: -8px; background: #EF4444; color: white;
                border-radius: 50%; width: 20px; height: 20px; font-size: 12px;
                display: flex; align-items: center; justify-content: center;
            }
        """)

    # THIS IS THE CRITICAL FIX:
    # Set attributes on the existing doc.body object directly.
    doc.body['class'] = 'bg-gray-50 font-sans'
    
    # The `with doc:` block adds content INSIDE the <body> tag.
    with doc:
        # Header (Using with header(...) is correct because we are creating a new tag)
        with header(class_="pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40"):
            with div(class_="flex items-center justify-between"):
                with div(class_="flex items-center space-x-3"):
                    img(src="/static/images/pup_logo.png", class_="w-10 h-10")
                    with div():
                        h1("StudywithStyle", class_="text-lg font-bold")
                        p("PUP Official Store", class_="text-xs opacity-90")
                with div(class_="flex space-x-3"):
                    with button(onclick="showSection('cart')", class_="relative p-2 bg-black bg-opacity-20 rounded-full"):
                        i(class_="fas fa-shopping-cart")
                        span(id="cart-badge", class_="cart-badge", style="display: none;")
                    with button(onclick="showSection('profile')", class_="p-2 bg-black bg-opacity-20 rounded-full"):
                        i(class_="fas fa-user")
        
        # Main Content
        with main(class_="content-container"):
            # Homepage Section
            with section(id="homepage", class_="section active p-4"):
                with div(class_="mb-6"):
                    h2("Featured Products", class_="text-2xl font-bold pup-text-burgundy mb-2")
                    p("Official PUP merchandise and study essentials", class_="text-gray-600")
                
                with div(id="product-list", class_="grid grid-cols-1 md:grid-cols-2 gap-4"):
                    pass

            # Shopping Cart Section
            with section(id="cart", class_="section p-4"):
                h2("Shopping Cart", class_="text-2xl font-bold pup-text-burgundy mb-4")
                div(id="cart-items", class_="space-y-4 mb-6")
                with div(id="cart-summary", style="display: none;", class_="bg-white rounded-lg shadow-lg p-4 mb-6"):
                    with div(class_="flex justify-between items-center text-lg font-bold pup-text-burgundy"):
                        span("Total:")
                        span(id="cart-total")
                    button(id="checkout-btn", onclick="checkout()", class_="w-full mt-4 pup-bg-burgundy text-white py-3 rounded-lg font-bold")

            # Profile/Login/Register Section
            with section(id="profile", class_="section p-4"):
                h2("Profile & Account", class_="text-2xl font-bold pup-text-burgundy mb-4")
                p("Login, registration, and profile details would go here.")

        # Bottom Navigation
        with nav(class_="bottom-nav pup-bg-burgundy text-white"):
            with div(class_="flex justify-around items-center py-3"):
                with button(onclick="showSection('homepage')", class_="nav-btn flex flex-col items-center space-y-1"):
                    i(class_="fas fa-home text-xl")
                    span("Home", class_="text-xs")
                with button(onclick="showSection('cart')", class_="nav-btn flex flex-col items-center space-y-1 relative"):
                    i(class_="fas fa-shopping-cart text-xl")
                    span("Cart", class_="text-xs")
                    span(id="nav-cart-badge", class_="cart-badge", style="display: none;")
                with button(onclick="showSection('profile')", class_="nav-btn flex flex-col items-center space-y-1"):
                    i(class_="fas fa-user text-xl")
                    span("Profile", class_="text-xs")
        
        # JavaScript logic
        script(raw("""
            // --- UI Navigation ---
            function showSection(sectionName) {
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.getElementById(sectionName).classList.add('active');
                if (sectionName === 'cart') {
                    loadCart(); 
                }
            }

            // --- Product Display ---
            function renderProducts(products) {
                const container = document.getElementById('product-list');
                container.innerHTML = products.map(p => `
                    <div class="bg-white rounded-lg shadow-md p-4 flex flex-col justify-between">
                        <div>
                           <div class="w-full h-32 pup-bg-burgundy rounded-lg flex items-center justify-center text-white mb-4">
                                <i class="fas fa-tshirt fa-2x"></i> <!-- Placeholder Icon -->
                           </div>
                           <h4 class="font-semibold pup-text-burgundy">${p.name}</h4>
                           <p class="text-sm text-gray-600">${p.description}</p>
                        </div>
                        <div class="flex justify-between items-center mt-4">
                            <span class="font-bold text-lg pup-text-burgundy">₱${p.price.toFixed(2)}</span>
                            <button onclick="addToCart(${p.id})" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full font-bold text-sm transition-colors">
                                ADD
                            </button>
                        </div>
                    </div>
                `).join('');
            }

            // --- Cart Logic (communicating with Python) ---
            async function addToCart(productId) {
                await window.pywebview.api.add_to_cart(productId);
                showNotification(`Added to cart!`);
                updateCartBadge();
            }
            
            async function loadCart() {
                const cartItems = await window.pywebview.api.get_cart();
                const container = document.getElementById('cart-items');
                const summary = document.getElementById('cart-summary');
                
                if (cartItems.length === 0) {
                    container.innerHTML = '<p class="text-center text-gray-500">Your cart is empty.</p>';
                    summary.style.display = 'none';
                } else {
                    container.innerHTML = cartItems.map(item => `
                        <div class="bg-white rounded-lg shadow-md p-4 flex items-center justify-between">
                            <div>
                                <h4 class="font-semibold pup-text-burgundy">${item.name}</h4>
                                <p class="text-gray-600">₱${item.price.toFixed(2)}</p>
                            </div>
                            <div class="flex items-center space-x-2">
                                <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})" class="w-8 h-8 bg-gray-200 rounded-full">-</button>
                                <span class="w-8 text-center font-semibold">${item.quantity}</span>
                                <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})" class="w-8 h-8 bg-gray-200 rounded-full">+</button>
                            </div>
                        </div>
                    `).join('');

                    const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                    document.getElementById('cart-total').textContent = `₱${total.toFixed(2)}`;
                    document.getElementById('checkout-btn').textContent = `CHECK OUT (₱${total.toFixed(2)})`;
                    summary.style.display = 'block';
                }
                updateCartBadge();
            }

            async function updateQuantity(productId, newQuantity) {
                await window.pywebview.api.update_cart_quantity(productId, newQuantity);
                loadCart(); // Reload cart to show changes
            }

            async function updateCartBadge() {
                const cartItems = await window.pywebview.api.get_cart();
                const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
                const badges = document.querySelectorAll('.cart-badge');
                badges.forEach(badge => {
                    if (totalItems > 0) {
                        badge.textContent = totalItems;
                        badge.style.display = 'flex';
                    } else {
                        badge.style.display = 'none';
                    }
                });
            }

            function checkout() {
                alert('Checkout process initiated! (Functionality to be implemented)');
            }

            // --- Utility ---
            function showNotification(message) {
                const el = document.createElement('div');
                el.className = 'fixed top-20 left-1/2 -translate-x-1/2 bg-green-500 text-white p-3 rounded-lg shadow-lg z-50';
                el.textContent = message;
                document.body.appendChild(el);
                setTimeout(() => el.remove(), 2000);
            }

            // --- Initial Load ---
            window.addEventListener('pywebviewready', async () => {
                const products = await window.pywebview.api.get_products();
                renderProducts(products);
                updateCartBadge();
            });
        """))
    return doc
