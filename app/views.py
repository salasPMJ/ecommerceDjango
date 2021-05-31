from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Product, Category


# Create your views here.


# def home(request):
#     return render(request, "home.html")


def home_redirect(request):
    return HttpResponseRedirect("/products")


# ************** SIGN IN / SIGN UP ***************

def do_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "accounts/login.html")

    login(request, user)
    return redirect('product_list')


def do_logout(request):
    logout(request)
    # NAME DEL PATH [ path('accounts/login', views.do_login, name="login")]
    return redirect('login')


def do_register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    User.objects.create_user(username, email, password)
    # NAME DEL PATH [ path('accounts/login', views.do_login, name="login")]
    return redirect('login')


# *************** CRUD ORDENADORES ***************


@login_required
def product_list(request):
    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all()
        #"notification": "Listado de libros",
        #"admin": False
    }
    return render(request, "products/product_list.html", context=data)


@login_required
def product_new(request):
    data = {
        "categories": Category.objects.all(),
    #    "genres": Genre.objects.all()
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_load(request, id):
    data = {
        "product": Product.objects.get(id=id), # recuperamos el producto
        "categories": Category.objects.exclude(product__isnull=False)
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_save(request):
    creation = not request.POST.get("id")
    # genres = request.POST.getlist('genres')

    category_id_str = request.POST.get("category_id")
    category_id = int(category_id_str) if category_id_str else None

    if creation:
        product = Product.objects.create(
            manufacturer=request.POST.get("manufacturer"),
            model=request.POST.get("model"),
            ram=request.POST.get("ram"),
            description=request.POST.get("description"),
            price=float(request.POST.get("price")),
            image=request.POST.get("image"),
            category_id=category_id
        )
        # book.genres.set(genres)
    else:
        # Editar un libro existente
        id_product = int(request.POST.get("id"))
        product = Product.objects.get(id=id_product)

        product.manufacturer = request.POST.get("manufacturer")
        product.model = request.POST.get("model")
        product.ram = request.POST.get("ram")
        product.description = request.POST.get("description")
        product.price = float(request.POST.get("price"))
        product.image = request.POST.get("image")
        product.category_id = category_id

        product.save()
    return HttpResponseRedirect("/products/{}/view".format(product.id))


@login_required
def product_filter(request):
    category_id_str = request.GET.get("category_id")
    #genres = request.GET.getlist("genres")
    category_id = int(category_id_str) if category_id_str else None

    products = None
    if category_id:
        products = Product.objects.filter(category_id=category_id).distinct()
    else:
        products = Product.objects.all()

    # FIX - no filtra bien:
    # filter_args = {}
    # if author_id:
    #     filter_args['author_id'] = author_id
    # if len(genres) > 1:
    #     filter_args['genres__id__in'] = genres
    #
    # books = Book.objects.filter(**filter_args).distinct()

    data = {
        "products": products,
        "categories": Category.objects.all(),
        #"genres": Genre.objects.all(),
        # Seleccionados en el filtro
        "category_id": category_id,
        #"genres_filtered": Genre.objects.filter(id__in=genres)
    }

    return render(request, "products/product_list.html", context=data)


@login_required
def product_view(request, id):
    product = Product.objects.get(id=id)
    data = {
        "product": product,
        # "genres": book.genres.all()
    }
    return render(request, "products/product_view.html", context=data)


@login_required
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return HttpResponseRedirect("/products")
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product no encontrado")

