from flask import Flask, jsonify
from . import admin_payload

app = Flask(__name__)

# The key is defined once at the top level.
XOR_KEY = "Admin-Panel-Key-2024"

@app.route('/')
def admin_bootloader():
    # --- Step 1: Define the JavaScript as a plain multiline string ---
    # We use a placeholder {key} which is safe for .format()
    # All other ${...} syntax is now correctly ignored by Python.
    js_template = """
        <script>
            const K="{key}";
            function D(b){{const s=atob(b);let r="";for(let i=0;i<s.length;i++)r+=String.fromCharCode(s.charCodeAt(i)^K.charCodeAt(i%K.length));return r;}}
            async function I(){{const r=await fetch('/data');const p=await r.json();document.getElementById('root').innerHTML=D(p.payload);loadInventory();}}
            
            async function loadInventory() {{
                const p = await window.pywebview.api.get_products();
                document.getElementById('inventory-body').innerHTML = p.map(i => `
                    <tr class="border-b hover:bg-gray-50 cursor-pointer" onclick='selectItem(${JSON.stringify(i)})'>
                        <td class="p-2">${i.id}</td>
                        <td class="p-2">${i.name}</td>
                        <td class="p-2">${i.stock}</td>
                        <td class="p-2">₱${i.price.toFixed(2)}</td>
                    </tr>
                `).join('');
            }}

            function selectItem(itemObject) {{
                document.getElementById('item-id').value = itemObject.id;
                document.getElementById('item-name').value = itemObject.name;
                document.getElementById('item-quantity').value = itemObject.stock;
                document.getElementById('item-price').value = itemObject.price;
                document.getElementById('item-description').value = itemObject.description || '';
            }}
            
            function clearForm(){{document.getElementById('item-form').reset();document.getElementById('item-id').value='';}}
            
            async function handleAddItem(){{const data={{name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value}};const r=await window.pywebview.api.add_product(data.name,data.price,data.quantity,data.description);if(r && r.status==='error')alert(r.message);clearForm();loadInventory();}}
            async function handleUpdateItem(){{const id=document.getElementById('item-id').value;if(!id){{alert('Select an item first.');return;}}const data={{name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value}};const r=await window.pywebview.api.update_product(id,data.name,data.price,data.quantity,data.description);if(r && r.status==='error')alert(r.message);clearForm();loadInventory();}}
            async function handleDeleteItem(){{const id=document.getElementById('item-id').value;if(!id){{alert('Select an item first.');return;}}if(confirm('Are you sure?')){{await window.pywebview.api.delete_product(id);clearForm();loadInventory();}}}}

            window.addEventListener('pywebviewready', I);
        </script>
    """

    # --- Step 2: Safely inject the key using .format() ---
    # This replaces {key} with the actual XOR key.
    js_bootloader = js_template.format(key=XOR_KEY)

    # --- Step 3: Return the final HTML page ---
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