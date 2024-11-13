from django.shortcuts import render, get_object_or_404
from shop.models import ProductProxy
from django.http import JsonResponse, HttpRequest
from .cart import Cart


def cart_view(request: HttpRequest):
    cart = Cart(request)
    context = {"cart": cart}
    return render(request, "cart/cart-view.html", context=context)


def cart_add(request: HttpRequest):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        product_qty = request.POST.get("product_qty")
        print(product_id, product_qty)
        if not product_id or not product_qty:
            raise Exception("Invalid form submission")
        product = get_object_or_404(ProductProxy, id=int(product_id))
        cart.add(product=product, quantity=int(product_qty))
        cart_qty = len(cart)
        response = JsonResponse({"qty": cart_qty, "product": product.title})
        return response


def cart_delete(request: HttpRequest):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        if not product_id:
            raise Exception("Invalid form submission")
        cart.delete(product_id)
        cart_qty = len(cart)
        cart_total = cart.get_total_price()
        response = JsonResponse({"qty": cart_qty, "total": cart_total})
        return response


def cart_update(request: HttpRequest):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        product_qty = request.POST.get("product_qty")
        if not product_id or not product_qty:
            raise Exception("Invalid form submission")
        cart.update(product_id, quantity=int(product_qty))
        cart_qty = len(cart)
        cart_total = cart.get_total_price()
        response = JsonResponse({"qty": cart_qty, "total": cart_total})
        return response
