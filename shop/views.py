from django.http import Http404
from django.shortcuts import render, redirect
from shop.models import Phone

PHRASE = "Войти"

def baseview(request):
    return render(request, "base.html")


def cart(request):
    cart_list = [
        {
            "name": "Nexus 5x",
            "description": "Неплохой телефон"
        },
        {
            "name": "iPhone 7",
            "description": "Телефон с яблоком"
        },
        {
            "name": "Pixel 2",
            "description": "Классная камера"
        },
        {
            "name": "Samsung Galaxy S8",
            "description": "Жалко, но этот телефон остался без описания"
        }
    ]
    context = {
        "cart": cart_list,
        "phrase": "Войти"
    }
    return render(request, "cart.html", context)


def mainview(request):
    context = {
        "staticpath": "nexus5x.webp",
        "phrase": "Войти"
    }
    return render(request, "index.html", context)


def smartphones(request):
    return render(request, "smartphones.html", {"phrase": "Войти"})


def login(request):
    return render(request, "login.html", {"phrase": "Войти"})


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
    random_phone = Phone.objects.filter(visible_status="v").first()
    if random_phone:
        context = {
            "phone_name": random_phone.name,
            "description": random_phone.description,
            "staticpath": random_phone.staticpath,
            "phrase": PHRASE
        }
        return render(request, "phone.html", context=context)
    raise Http404("Phone does not exist")