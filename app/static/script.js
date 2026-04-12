// Fetch and display products
function loadProducts() {
    fetch('/products')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('product-list');
            list.innerHTML = data.map(p => `
                <div class="product-item">
                    <span>${p.name}</span>
                    <span>$${p.price}</span>
                </div>
            `).join('');
        });
}

// Post a new product
function addProduct() {
    const name = document.getElementById('name').value;
    const price = document.getElementById('price').value;

    fetch('/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price })
    }).then(() => {
        document.getElementById('name').value = '';
        document.getElementById('price').value = '';
        loadProducts();
    });
}

// Check API Health
fetch('/health')
    .then(res => res.json())
    .then(data => {
        document.getElementById('health-status').innerText = `System Status: ${data.status} | Tier: ${data.tier}`;
    });

loadProducts();
