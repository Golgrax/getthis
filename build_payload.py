import base64

# This key MUST match the key in the final JavaScript bootloader.
XOR_KEY = "PUP-Sinta-2024-IskolarNgBayan"

def xor_and_encode(html_string):
    """Encrypts a string with XOR and encodes it to Base64."""
    encrypted_chars = []
    for i in range(len(html_string)):
        key_char = XOR_KEY[i % len(XOR_KEY)]
        encrypted_char_code = ord(html_string[i]) ^ ord(key_char)
        encrypted_chars.append(chr(encrypted_char_code))
    
    encrypted_string = "".join(encrypted_chars)
    return base64.b64encode(encrypted_string.encode('utf-8')).decode('utf-8')

def create_payload_file():
    """Reads the clean UI, encrypts it, and writes it to shop_app/payload.py"""
    print("Starting UI compilation...")
    
    # Define the clean HTML for different parts of the app.
    # In a real project, you might read these from separate .html files.
    
    auth_view_html = """
    <div id="auth-view" class="page-view active">
        <section id="login-section" class="auth-section active p-4">
            <div class="text-center mb-6"><div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4"><i class="fas fa-star text-red-800 text-2xl"></i></div><h2 class="text-2xl font-bold pup-text-burgundy">Welcome Back</h2></div>
            <form id="login-form" class="bg-white rounded-lg shadow-lg p-6 space-y-4">
                <div><label class="block font-semibold mb-1">Email:</label><input id="login-email" type="email" class="w-full p-3 border rounded-lg"></div>
                <div><label class="block font-semibold mb-1">Password:</label><input id="login-password" type="password" class="w-full p-3 border rounded-lg"></div>
                <div class="space-y-3 pt-2"><button type="submit" class="w-full pup-bg-burgundy text-white py-3 rounded-lg font-semibold">LOGIN</button><button type="button" onclick="showAuthSection('register-section')" class="w-full bg-cyan-400 text-white py-3 rounded-lg font-semibold">Create Account</button></div>
            </form>
        </section>
        <section id="register-section" class="auth-section p-4" style="display: none;"><div class="text-center mb-6"><div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4"><i class="fas fa-star text-red-800 text-2xl"></i></div><h2 class="text-2xl font-bold pup-text-burgundy">Mula sayo para sa bayan</h2></div><form id="register-form" class="bg-white rounded-lg shadow-lg p-6 space-y-4"><div><label class="block font-semibold mb-1">Name:</label><input id="register-name" type="text" class="w-full p-3 border rounded-lg"></div><div><label class="block font-semibold mb-1">Email:</label><input id="register-email" type="email" class="w-full p-3 border rounded-lg"></div><div><label class="block font-semibold mb-1">Password:</label><input id="register-password" type="password" class="w-full p-3 border rounded-lg"></div><div class="space-y-3 pt-2"><button type="submit" class="w-full bg-cyan-500 text-white py-3 rounded-lg font-semibold">REGISTER</button><button type="button" onclick="showAuthSection('login-section')" class="w-full bg-gray-300 text-gray-800 py-3 rounded-lg font-semibold">Back to LOGIN</button></div></form></section>
    </div>
    """
    
    app_view_html = """
    <div id="main-app-view" class="page-view">
        <header class="pup-bg-burgundy text-white p-4 shadow-lg sticky top-0 z-40"><div class="flex items-center justify-between"><div class="flex items-center space-x-3"><i class="fas fa-star w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center text-red-800"></i><div><h1 class="text-lg font-bold">StudywithStyle</h1></div></div><div class="flex space-x-3"><button onclick="showAppSection('cart-app-view')" class="p-2 relative"><i class="fas fa-shopping-cart"></i><span id="header-cart-badge" class="cart-badge" style="display:none">0</span></button><button onclick="showAppSection('profile-app-view')" class="p-2"><i class="fas fa-user"></i></button></div></div></header>
        <main class="content-container"><section id="homepage-app-view" class="app-view active p-4"><div class="mb-4"><h2 class="text-2xl font-bold pup-text-burgundy">Products</h2></div><div id="product-list" class="space-y-4"></div></section><section id="cart-app-view" class="app-view p-4"><h2 class="text-2xl font-bold pup-text-burgundy mb-4">Shopping Cart</h2><div id="cart-items" class="space-y-4"></div><div id="cart-summary" class="mt-6 pt-4 border-t" style="display:none"><div class="flex justify-between font-bold text-lg"><p>Total:</p><p id="cart-total"></p></div><button onclick="showAppSection('checkout-app-view')" class="w-full mt-4 pup-bg-burgundy text-white py-3 rounded-lg font-bold">PROCEED TO CHECKOUT</button></div></section><section id="checkout-app-view" class="app-view p-4"><h2 class="text-2xl font-bold pup-text-burgundy mb-4">Checkout</h2><div class="bg-white p-4 rounded-lg shadow"><h3 class="font-bold mb-2">Order Summary</h3><div id="checkout-summary-items" class="text-sm space-y-1"></div><div class="flex justify-between font-bold text-lg mt-4 border-t pt-2"><p>Total:</p><p id="checkout-total"></p></div></div><div class="bg-white p-4 rounded-lg shadow mt-4"><h3 class="font-bold mb-2">Payment</h3><p>Cash on Delivery</p></div><button onclick="handlePlaceOrder()" class="w-full mt-6 pup-bg-burgundy text-white py-3 rounded-lg font-bold">PLACE ORDER</button></section><section id="profile-app-view" class="app-view p-4"><div class="text-center"><h2 id="user-name-display" class="text-2xl font-bold"></h2><button onclick="handleLogout()" class="mt-4 bg-gray-200 px-4 py-2 rounded">Logout</button></div></section></main>
        <nav class="bottom-nav pup-bg-burgundy text-white"><div class="flex justify-around py-2"><button onclick="showAppSection('homepage-app-view')"><i class="fas fa-home"></i></button><button onclick="showAppSection('cart-app-view')" class="relative"><i class="fas fa-shopping-cart"></i><span id="nav-cart-badge" class="cart-badge" style="display:none">0</span></button><button onclick="showAppSection('profile-app-view')"><i class="fas fa-user"></i></button></div></nav>
    </div>
    """

    # Encrypt both parts
    encrypted_auth = xor_and_encode(auth_view_html)
    encrypted_app = xor_and_encode(app_view_html)

    # Write the encrypted data to the payload.py file
    payload_content = f"""
# This file is auto-generated by build_payload.py. DO NOT EDIT.
# It contains the obfuscated UI data for the application.

AUTH_PAYLOAD = "{encrypted_auth}"

APP_PAYLOAD = "{encrypted_app}"
"""

    with open("shop_app/payload.py", "w") as f:
        f.write(payload_content)
        
    print("✅ Successfully compiled UI to shop_app/payload.py")

if __name__ == "__main__":
    create_payload_file()