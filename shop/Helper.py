from django.http import Http404
from django.shortcuts import render


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
    obj = obj.objects.filter(visible_status="v", id=int(request.GET.get("id", None))).first()
    if obj:
        context = {
            "phone_name": obj.name,
            "description": obj.description,
            "staticpath": obj.staticpath,
            "phone_id": obj.id,
            "phrase": phrase,
            "b_action": b_action
        }
        return render(request, "phone.html", context=context)
    raise Http404("Phone does not exist")


def ul_generator(request, paginator):
    arr = []
    for num in paginator.page_range:
        if (int(request.GET["page"]) - 5) < num < (int(request.GET["page"]) + 5):
            arr.append({
                "status": "active" if num == int(request.GET["page"]) else "",
                "num": num
            })
    return arr