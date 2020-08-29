from django.core.paginator import Paginator
from django.db import models as db_models
from django.http import Http404, HttpRequest
from django.shortcuts import render

from diplom.settings import OBJECTS_PER_PAGE, DATA_MULTIPLIER
from shop.models import Phone, SiteField, Comment, CartCompanion, Order, CartCompanionSupport, OrderSupport
from django.urls import path
from shop import views


def get_choice_result(model, choice):
    for i in model.choices:
        if choice == i[0]:
            return i[1]
    return choice


def tuples(array):
    arr = []
    cache = []
    true = False
    for i in array:
        cache.append(i)
        true = True
        if len(cache) % 3 == 0:
            arr.append(cache)
            cache = []
            true = False
    if true:
        arr.append(cache)
    return arr


def support(request, obj, phrase, b_action):
    first = obj.objects.filter(visible_status="v", id=int(request.GET.get("id", None))).first()
    obj: Phone = obj.objects.filter(visible_status="v", id=int(request.GET.get("id", None))).first()
    if obj:
        context = {
            "comments": [
                {
                    "ratio": get_choice_result(db_models.RatioChoives, item.ratio),
                    "author": item.author,
                    "content": item.content
                } for item in obj.comments.order_by("pub_date").filter(visible_status="v")
            ],
            "phone_name": obj.name,
            "description": obj.description,
            "staticpath": obj.staticpath,
            "phone_id": obj.id
        }
        context = context_generator(request, **context)
        return render(request, "phone.html", context=context)
    raise Http404("Phone does not exist")


def ul_generator(page_number, paginator):
    arr = []
    for num in paginator.page_range:
        if (page_number - 5) < num < (page_number + 5):
            arr.append({
                "status": "active" if num == page_number else "",
                "num": num
            })
    return arr


def fun(request, ty_pe, title):
    if not request.user.is_authenticated:
        phrase = "Войти"
        b_action = "/login/"
    else:
        phrase = "Выйти"
        b_action = "/logout/"
    objects = Phone.objects.filter(visible_status="v", type__phone_type=ty_pe)
    raw_content = []
    for obj in objects:
        raw_content.append({
            "name": obj.name,
            "link": f"/phone?id={obj.id}",
            "staticpath": obj.staticpath,
            "cartform_action": "/cart",
            "phone_id": obj.id
        })
    content = raw_content * DATA_MULTIPLIER
    data = tuples(content)
    paginator = Paginator(data, OBJECTS_PER_PAGE)
    page = paginator.get_page(int(request.GET.get("page", 1)))
    page_number = int(request.GET.get("page", 1))
    string = ""
    for char in request.get_full_path():
        if char == "?":
            break
        string += char
    nav = {
        "prev": {
            "status": "disabled" if not page.has_previous() else "",
            "link": page.previous_page_number() if page.has_previous() else "#"
        },
        "ul": ul_generator(page_number, paginator),
        "next": {
            "status": "disabled" if not page.has_next() else "",
            "link": page.next_page_number() if page.has_next() else "#"
        },
        "type": request.GET.get("type", None),
        "page": string,
        "host": request.get_host()
    }
    context = {
        "title": title,
        "iter": page.object_list,
        "nav": nav
    }
    context = context_generator(request, **context)
    return render(request, "smartphones.html", context)


def context_generator(request: HttpRequest, include_baseview: bool = True, **kwargs):
    raw_context = {}
    if include_baseview:
        cache = []
        objects = SiteField.objects.order_by("id").filter(visible_status="v", main=True)
        for obj in objects:
            cache.append({
                "name": obj.name,
                "dropdown": obj.is_dropdown,
                "dropdown_fields": [{
                    "name": item.name,
                    "dropdown": item.is_dropdown,
                    "dropdown_fields": [],
                    "handler": f"/smartphones/?type={item.phone_type}"
                } for item in obj.dropdown_fields.filter(visible_status="v", main=False)],
                "handler": f"{obj.handler}{'?type='+obj.phone_type if obj.phone_type else ''}"
            })
        raw_context["baseview"] = {
            "fields": cache,
            "phrase": "Выйти" if request.user.is_authenticated else "Войти",
            "b_action": "/logout/" if request.user.is_authenticated else "/login/",
        }
    context = {**raw_context, **kwargs}
    return context


def cart_to_order(cart: CartCompanion):
    order = Order.objects.create(user=cart.user)
    for phone in cart.cart.filter(visible_status="v"):
        m = CartCompanionSupport.objects.filter(phones=phone, cart=cart).first()
        m1 = OrderSupport.objects.create(
            cart=order,
            phones=phone,
            count=m.count
        )
        m1.save()
    cart.delete()
    return order
