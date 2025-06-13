from flask import Flask, jsonify
from . import admin_payload

app = Flask(__name__)

XOR_KEY = "Admin-Panel-Key-2024"

@app.route('/')
def admin_bootloader():
    # We build the most complex line of JavaScript using simple concatenation
    # to avoid any f-string conflicts. This is 100% safe.
    onclick_handler = "'selectItem(\\'' + JSON.stringify(i) + '\\')'"
    
    table_row_template = (
        '<tr class="border-b hover:bg-gray-50 cursor-pointer" onclick=' + onclick_handler + '>'
        '<td class="p-2">{i.id}</td>'
        '<td class="p-2">{i.name}</td>'
        '<td class="p-2">{i.stock}</td>'
        '<td class="p-2">₱{i.price.toFixed(2)}</td>'
        '</tr>'
    )
    
    js_bootloader = f"""
        <script>
            const K="{XOR_KEY}";
            function D(b){{const s=atob(b);let r="";for(let i=0;i<s.length;i++)r+=String.fromCharCode(s.charCodeAt(i)^K.charCodeAt(i%K.length));return r;}}
            async function I(){{const r=await fetch('/data');const p=await r.json();document.getElementById('root').innerHTML=D(p.payload);loadInventory();}}
            
            async function loadInventory() {{
                const p = await window.pywebview.api.get_products();
                document.getElementById('inventory-body').innerHTML = p.map(i => `{table_row_template}`).join('');
            }}

            function selectItem(itemString) {{
                // Note: The string now comes with extra quotes, so we parse it twice.
                const item = JSON.parse(JSON.parse(itemString));
                document.getElementById('item-id').value = item.id;
                document.getElementById('item-name').value = item.name;
                document.getElementById('item-quantity').value = item.stock;
                document.getElementById('item-price').value = item.price;
                document.getElementById('item-description').value = item.description || '';
            }}
            
            function clearForm(){{document.getElementById('item-form').reset();document.getElementById('item-id').value='';}}
            
            async function handleAddItem(){{const data={{name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value}};const r=await window.pywebview.api.add_product(data.name,data.price,data.quantity,data.description);if(r && r.status==='error')alert(r.message);clearForm();loadInventory();}}
            async function handleUpdateItem(){{const id=document.getElementById('item-id').value;if(!id){{alert('Select an item first.');return;}}const data={{name:document.getElementById('item-name').value,quantity:document.getElementById('item-quantity').value,price:document.getElementById('item-price').value,description:document.getElementById('item-description').value}};const r=await window.pywebview.api.update_product(id,data.name,data.price,data.quantity,data.description);if(r && r.status==='error')alert(r.message);clearForm();loadInventory();}}
            async function handleDeleteItem(){{const id=document.getElementById('item-id').value;if(!id){{alert('Select an item first.');return;}}if(confirm('Are you sure?')){{await window.pywebview.api.delete_product(id);clearForm();loadInventory();}}}}

            window.addEventListener('pywebviewready', I);
        </script>
    """

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