from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from diplom.settings import DATA_MULTIPLIER, OBJECTS_PER_PAGE
from shop import Helper
from shop.models import Phone, CartCompanion, Article


def baseview(request):
    return render(request, "base.html")


def cart(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            phrase = "Войти"
            b_action = "/login/"
        else:
            phrase = "Выйти"
            b_action = "/logout/"
        if request.user.is_authenticated:
            # cart_list = [
            #     {
            #         "name": "Nexus 5x",
            #         "description": "Неплохой телефон"
            #     },
            #     {
            #         "name": "iPhone 7",
            #         "description": "Телефон с яблоком"
            #     },
            #     {
            #         "name": "Pixel 2",
            #         "description": "Классная камера"
            #     },
            #     {
            #         "name": "Samsung Galaxy S8",
            #         "description": "Жалко, но этот телефон остался без описания"
            #     }
            # ]
            if not (cart_obj := CartCompanion.objects.filter(user=request.user).first()):
                cart_obj = CartCompanion.objects.create(user=request.user)
            objects = cart_obj.cart.filter(visible_status="v")
            cart_list = []
            for obj in objects:
                cart_list.append({
                    "name": obj.name,
                    "description": obj.description
                })
            context = {
                "cart": cart_list,
                "phrase": phrase,
                "b_action": b_action
            }
            return render(request, "cart.html", context)
        else:
            return redirect("/login/")
    else:
        if request.user.is_authenticated:
            if not (cart_obj := CartCompanion.objects.filter(user=request.user).first()):
                cart_obj = CartCompanion.objects.create(user=request.user)
            if Phone.objects.filter(visible_status="v", id=request.POST["phone_id"]).first():
                cart_obj.cart.add(Phone.objects.filter(visible_status="v", id=request.POST["phone_id"]).first())
            return redirect(request.get_full_path())
        else:
            return redirect("/login/")


def mainview(request):
    if not request.user.is_authenticated:
        phrase = "Войти"
        b_action = "/login/"
    else:
        phrase = "Выйти"
        b_action = "/logout/"

    objects = Article.objects.order_by("pub_date").filter(visible_status="v")
    articles = []
    for obj in objects:
        articles.append({
            "title": obj.title,
            "content": obj.content,
            "phones": [{"name": item.name, "staticpath": item.staticpath, "phone_id": item.id} for item in
                       obj.phones.all()]
        })
    context = {
        "articles": articles,
        "phrase": phrase,
        "b_action": b_action
    }
    return render(request, "index.html", context)


def smartphones(request):
    if not request.user.is_authenticated:
        phrase = "Войти"
        b_action = "/login/"
    else:
        phrase = "Выйти"
        b_action = "/logout/"
    objects = Phone.objects.filter(visible_status="v")
    raw_content = []
    for obj in objects:
        raw_content.append({
            "name": obj.name,
            "link": f"/phone?id={obj.id}",
            "staticpath": obj.staticpath,
            "cartform_action": "/cart",
            "phone_id": obj.id
        })
    content = raw_content*DATA_MULTIPLIER
    data = Helper.tuples(content)
    paginator = Paginator(data, OBJECTS_PER_PAGE)
    if not request.GET.get("page", None):
        page = paginator.page(1)
    else:
        page = paginator.page(int(request.GET["page"]))
        print(paginator.page_range)
    nav = {
        "prev": {
            "status": "disabled" if not page.has_previous() else "",
            "link": page.previous_page_number() if page.has_previous() else "#"
        },
        "ul": Helper.ul_generator(request, paginator),
        "next": {
            "status": "disabled" if not page.has_next() else "",
            "link": page.next_page_number() if page.has_next() else "#"
        }
    }
    context = {
        "iter": page.object_list,
        "phrase": phrase,
        "b_action": b_action,
        "nav": nav
    }
    return render(request, "smartphones.html", context)


def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        auth_login(request, user)
        return redirect("/")
    return render(request, "login.html")


def phone(request):
    ###########################################################################
    # sets = [                                                                #
    #     {                                                                   #
    #         "phone_name": "Nexus 5X",                                       #
    #         "description": "Неплохой телефон",                              #
    #         "staticpath": "nexus5x.webp"                                    #
    #     },                                                                  #
    #     {                                                                   #
    #         "phone_name": "iPhone 7",                                       #
    #         "description": "Телефон с яблоком",                             #
    #         "staticpath": "iphone7.webp"                                    #
    #     },                                                                  #
    #     {                                                                   #
    #         "phone_name": "Pixel 2",                                        #
    #         "description": "Классная камера",                               #
    #         "staticpath": "pixel2.webp"                                     #
    #     },                                                                  #
    #     {                                                                   #
    #         "phone_name": "Samsung Galaxy S8",                              #
    #         "description": "Какое-то классное описание",                    #
    #         "staticpath": "samsungs8.webp"                                  #
    #     }                                                                   #
    # ]                                                                       #
    # context = {**__import__("random").choice(sets), **{"phrase": "Войти"}}  #
    ###########################################################################
    if not request.user.is_authenticated:
        phrase = "Войти"
        b_action = "/login/"
    else:
        phrase = "Выйти"
        b_action = "/logout/"
    if request.method != "GET":
        raise Http404("Incorrect Method")
    if not request.GET.get("id", None):
        raise Http404("Phone does not exist")
    if not request.GET.get("wchy", None):
        return Helper.support(request, Phone, phrase, b_action)
    else:
        return Helper.support(request, Phone, phrase, b_action)


def logout(request):
    auth_logout(request)
    return redirect("/")
