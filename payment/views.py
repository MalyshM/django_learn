from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress


@login_required(login_url="account:login")
def shipping(request: HttpRequest):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None
    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect("account:dashboard")
    return render(
        request,
        "payment/shipping.html",
        {"form": ShippingAddressForm(instance=shipping_address)},
    )


def checkout(request: HttpRequest):
    if request.user.is_authenticated:
        shipping_adress = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_adress:
            return render(
                request,
                "payment/checkout.html",
                {"shipping_address": shipping_adress},
            )
    return render(request, "payment/checkout.html")


def complete_order(request: HttpRequest):
    if request.POST.get("action") == "payment":
        name = request.POST.get("name")
        email = request.POST.get("email")
        street_address = request.POST.get("street_address")
        apartment_address = request.POST.get("apartment_address")
        country = request.POST.get("country")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": name,
                "email": email,
                "street_adress": street_address,
                "apartment_adress": apartment_address,
                "country": country,
                "city": city,
                "zip_code": zip_code,
            },
        )
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            amount=total_price,
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["qty"],
                user=request.user,
            )
        return JsonResponse({"success": True})


def payment_success(request: HttpRequest):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "payment/payment-success.html")


def payment_failed(request: HttpRequest):
    return render(request, "payment/payment-failed.html")
