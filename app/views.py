from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Product, Category, Profile, Manufacturer


# Create your views here.


def home_redirect(request):
    return HttpResponseRedirect("/products")


# ************** CARGA PAGINA DE INICIO ***************
def index_load(request):
    print(request.session.session_key)
    request.session["cart"] = []
    data = {
        "products": Product.objects.all(),
        "categories": Category.objects.all()
    }
    return render(request, "indice/index.html", context=data)
    #return HttpResponseRedirect("/indice")


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
    #return redirect('product_list')
    return redirect('index_load')


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


# *************** CRUD PROFILE ***************

def profile_create(request):
    email_form = request.POST.get("email")
    type_form = request.POST.get("type")

    user = User.objects.get(email=email_form).first()

    Profile.objects.create(user.id, type_form)
    # return HttpResponseRedirect("/products")
    return redirect('/products')


# *************** CRUD ORDENADORES ***************


@login_required
def product_list(request):
    data = {
        "products": Product.objects.all(),  # recupera libros de db,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_list.html", context=data)


@login_required
def product_new(request):
    data = {
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_load(request, id):
    data = {
        "product": Product.objects.get(id=id), # recuperamos el producto
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request, "products/product_edit.html", context=data)


@login_required
def product_save(request):
    creation = not request.POST.get("id")
    manufacturers = request.POST.getlist('manufacturers')

    category_id_str = request.POST.get("category_id")
    category_id = int(category_id_str) if category_id_str else None

    if creation:
        product = Product.objects.create(
            # manufacturer=request.POST.get("manufacturer"),
            model=request.POST.get("model"),
            ram=request.POST.get("ram"),
            description=request.POST.get("description"),
            price=float(request.POST.get("price")),
            image=request.POST.get("image"),
            category_id=category_id
        )
        product.manufacturers.set(manufacturers)
    else:
        # Editar un producto existente
        id_product = int(request.POST.get("id"))
        product = Product.objects.get(id=id_product)

        # product.manufacturer = request.POST.get("manufacturer")
        product.model = request.POST.get("model")
        product.ram = request.POST.get("ram")
        product.description = request.POST.get("description")
        product.price = float(request.POST.get("price"))
        product.image = request.POST.get("image")
        product.category_id = category_id
        product.manufacturers.set(manufacturers)

        product.save()
    return HttpResponseRedirect("/products/{}/view".format(product.id))


@login_required
def product_filter(request):
    category_id_str = request.GET.get("category_id")
    manufacturers = request.GET.getlist("manufacturers")
    category_id = int(category_id_str) if category_id_str else None

    products = None
    if category_id and len(manufacturers) >= 1:
        products = Product.objects.filter(category_id=category_id, manufacturers__id__in=manufacturers).distinct()
    elif category_id:
        products = Product.objects.filter(category_id=category_id)
    elif len(manufacturers) >= 1:
        products = Product.objects.filter(manufacturers__id__in=manufacturers).distinct()
    else:
        products = Product.objects.all()

    data = {
        "products": products,
        "categories": Category.objects.all(),
        "manufacturers": Manufacturer.objects.all(),
        # Seleccionados en el filtro
        "category_id": category_id,
        "manufacturers_filtered": Manufacturer.objects.filter(id__in=manufacturers)
    }

    return render(request, "products/product_list.html", context=data)


@login_required
def product_view(request, id):
    product = Product.objects.get(id=id)
    data = {
        "product": product,
        "manufacturers": product.manufacturers.all()
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


# ************** OPERACIONES CARRITO ***************

def cart_add_product(request, product_id):
    product = Product.objects.get(id=product_id)
    lista = []
    lista = request.session["cart"]
    lista.append(product)
    print(lista)
    request.session["cart"] = lista
    return render(request, "products/product_list.html")


def cart_delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    pass

def cart_reduce_product(request, product_id):
    pass


def cart_clean(request, product_id):
    pass
