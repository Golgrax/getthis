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
