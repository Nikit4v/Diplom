from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from diplom.settings import DATA_MULTIPLIER, OBJECTS_PER_PAGE
from shop import Helper
from shop.models import Phone, CartCompanion, Article, Comment, CartCompanionSupport


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
                    "description": obj.description,
                    "count": CartCompanionSupport.objects.filter(phones=obj, cart=cart_obj).first().count
                })
            context = {
                "cart": cart_list,
                "phrase": phrase,
                "b_action": b_action
            }
            context = Helper.context_generator(request, **context)
            return render(request, "cart.html", context)
        else:
            return redirect("/login/")
    else:
        if request.user.is_authenticated:
            if not request.POST.get("order", None):
                if not (cart_obj := CartCompanion.objects.filter(user=request.user).first()):
                    cart_obj = CartCompanion.objects.create(user=request.user)
                if Phone.objects.filter(visible_status="v", id=request.POST["phone_id"]).first():
                    if Phone.objects.filter(visible_status="v",
                                            id=request.POST["phone_id"]).first() in cart_obj.cart.all():
                        print(obj := Phone.objects.filter(visible_status="v", id=request.POST["phone_id"]).first())
                        m1 = CartCompanionSupport.objects.filter(phones=obj, cart=cart_obj).first()
                        m1.count += 1
                        m1.save()
                    else:
                        m1 = CartCompanionSupport.objects.create(
                            cart=cart_obj,
                            phones=Phone.objects.filter(visible_status="v", id=request.POST["phone_id"]).first()
                        )
                        m1.save()
                return redirect(request.get_full_path())
            else:
                Helper.cart_to_order(request.user.cart)
                return redirect('/')
        else:
            return redirect("/login/")


def main_view(request):
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
                       obj.phones.all()] * DATA_MULTIPLIER
        })
    context = Helper.context_generator(request, articles=articles)
    return render(request, "index.html", context)


def smartphones(request):
    return Helper.fun(request, "p", "Смартфоны")


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
        comment = Comment.objects.create(ratio=request.POST["mark"], author=request.POST["name"],
                                         content=request.POST["description"], phone_id=request.GET["id"])
        comment.save()
        return redirect(request.get_full_path())
    if not request.GET.get("id", None):
        raise Http404("Phone does not exist")
    if not request.GET.get("wchy", None):
        return Helper.support(request, Phone, phrase, b_action)
    else:
        return Helper.support(request, Phone, phrase, b_action)


def logout(request):
    auth_logout(request)
    return redirect("/")


def accessories(request):
    return Helper.fun(request, "a", "Аксессуары")


def consoles(request):
    return Helper.fun(request, "c", "Игровые консоли")


def monitors(request):
    return Helper.fun(request, "m", "Мониторы")
