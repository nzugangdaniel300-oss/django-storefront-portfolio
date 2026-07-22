from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Category
from .cart import Cart

def product_list(request):
    """Affiche la liste des produits avec recherche et filtre par catégorie (ID)."""
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = None

    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    })

def product_detail(request, pk):
    """Affiche le détail d'un produit."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@require_POST
def cart_add(request, product_id):
    """Ajoute un produit au panier."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Supprime un produit du panier."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    """Affiche le contenu du panier."""
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})