import base64

XOR_KEY = "Admin-Panel-Key-2024"

def xor_and_encode(html_string):
    encrypted_chars = []
    for i in range(len(html_string)):
        key_char = XOR_KEY[i % len(XOR_KEY)]
        encrypted_char_code = ord(html_string[i]) ^ ord(key_char)
        encrypted_chars.append(chr(encrypted_char_code))
    encrypted_string = "".join(encrypted_chars)
    return base64.b64encode(encrypted_string.encode('utf-8')).decode('utf-8')

def create_admin_payload():
    print("Compiling Admin UI...")
    admin_html = """
    <div class="bg-gray-100 p-8 font-sans">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">PUP Shop - Inventory Management</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1 bg-white p-6 rounded-lg shadow-md">
                <h2 class="text-xl font-semibold mb-4">Manage Item</h2>
                <form id="item-form" class="space-y-4">
                    <input type="hidden" id="item-id">
                    <div><label class="block text-sm font-medium text-gray-700">Item Name</label><input type="text" id="item-name" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md"></div>
                    <div><label class="block text-sm font-medium text-gray-700">Quantity</label><input type="number" id="item-quantity" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md"></div>
                    <div><label class="block text-sm font-medium text-gray-700">Price (PHP)</label><input type="number" id="item-price" step="0.01" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md"></div>
                    <div><label class="block text-sm font-medium text-gray-700">Description</label><textarea id="item-description" rows="3" class="mt-1 block w-full p-2 border border-gray-300 rounded-md"></textarea></div>
                    <div class="flex space-x-2 pt-2">
                        <button type="button" onclick="handleAddItem()" class="flex-1 bg-blue-500 text-white px-4 py-2 rounded-md">Add</button>
                        <button type="button" onclick="handleUpdateItem()" class="flex-1 bg-green-500 text-white px-4 py-2 rounded-md">Update</button>
                    </div>
                    <div class="flex space-x-2">
                         <button type="button" onclick="handleDeleteItem()" class="flex-1 bg-red-500 text-white px-4 py-2 rounded-md">Delete</button>
                         <button type="button" onclick="clearForm()" class="flex-1 bg-gray-500 text-white px-4 py-2 rounded-md">Clear</button>
                    </div>
                </form>
            </div>
            <div class="md:col-span-2 bg-white p-6 rounded-lg shadow-md">
                <h2 class="text-xl font-semibold mb-4">Current Inventory</h2>
                <div class="overflow-x-auto"><table class="w-full text-left"><thead class="border-b-2"><tr><th class="p-2">ID</th><th class="p-2">Name</th><th class="p-2">Stock</th><th class="p-2">Price</th></tr></thead><tbody id="inventory-body"></tbody></table></div>
            </div>
        </div>
    </div>
    """
    encrypted_payload = xor_and_encode(admin_html)
    with open("admin_app/admin_payload.py", "w") as f:
        f.write("# This file is auto-generated. DO NOT EDIT.\n")
        f.write(f'ADMIN_PAYLOAD = "{encrypted_payload}"')
    print("✅ Admin UI compiled successfully.")

if __name__ == "__main__":
    create_admin_payload()
