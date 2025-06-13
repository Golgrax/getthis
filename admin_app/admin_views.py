import dominate
from dominate.tags import *
from dominate.util import raw

def generate_admin_page():
    doc = dominate.document(title="Shop Admin - Inventory")
    with doc.head:
        meta(charset="UTF-8")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")

    with doc.body(cls="bg-gray-100 p-8"):
        h1("PUP Shop - Inventory Management", cls="text-3xl font-bold text-gray-800 mb-6")
        
        # Form
        with div(cls="bg-white p-6 rounded-lg shadow-md mb-8"):
            h2("Manage Item", cls="text-xl font-semibold mb-4")
            with form(id="item-form", cls="grid grid-cols-1 md:grid-cols-2 gap-4"):
                input_(type="hidden", id="item-id")
                input_(type="text", id="item-name", placeholder="Item Name", cls="p-2 border rounded")
                input_(type="number", id="item-quantity", placeholder="Quantity", cls="p-2 border rounded")
                input_(type="number", id="item-price", placeholder="Price (PHP)", step="0.01", cls="p-2 border rounded")
                textarea(id="item-description", placeholder="Description", rows="3", cls="p-2 border rounded md:col-span-2")
            with div(cls="flex space-x-2 mt-4"):
                button("Add Item", onclick="addItem()", cls="bg-blue-500 text-white px-4 py-2 rounded")
                button("Update Item", onclick="updateItem()", cls="bg-green-500 text-white px-4 py-2 rounded")
                button("Delete Item", onclick="deleteItem()", cls="bg-red-500 text-white px-4 py-2 rounded")
                button("Clear Form", type="button", onclick="clearForm()", cls="bg-gray-500 text-white px-4 py-2 rounded")
        
        with div(cls="bg-white p-6 rounded-lg shadow-md"):
            h2("Current Inventory", cls="text-xl font-semibold mb-4")
            with table(id="inventory-table", cls="w-full text-left"):
                with thead(cls="border-b-2"):
                    with tr():
                        th("ID", cls="p-2")
                        th("Name", cls="p-2")
                        th("Quantity", cls="p-2")
                        th("Price", cls="p-2")
                tbody(id="inventory-body")

        script(raw("""
            async function loadInventory() {
                const products = await window.pywebview.api.get_products();
                const tbody = document.getElementById('inventory-body');
                tbody.innerHTML = products.map(p => `
                    <tr class="border-b hover:bg-gray-50 cursor-pointer" onclick="selectItem(${p.id}, '${p.name}', ${p.quantity}, ${p.price}, '${p.description || ''}')">
                        <td class="p-2">${p.id}</td>
                        <td class="p-2">${p.name}</td>
                        <td class="p-2">${p.stock}</td>
                        <td class="p-2">₱${p.price.toFixed(2)}</td>
                    </tr>
                `).join('');
            }
            
            function selectItem(id, name, quantity, price, description) {
                document.getElementById('item-id').value = id;
                document.getElementById('item-name').value = name;
                document.getElementById('item-quantity').value = quantity;
                document.getElementById('item-price').value = price;
                document.getElementById('item-description').value = description;
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
                if (!name || !quantity || !price) { alert('Please fill all fields'); return; }
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

            window.addEventListener('pywebviewready', loadInventory);
        """))

    return doc