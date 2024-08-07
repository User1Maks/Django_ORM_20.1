from django.shortcuts import render
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from catalog.models import Category, Product, Blog, Version
from django.views.generic import (
    ListView,
    DetailView,
    View,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.conf import settings
from catalog.services import get_products_from_cache, get_category_list_cache
from django.core.cache import cache


class GetContextMixin:
    def get_context_data(self, **kwargs):
        """
        Метод добавляет поле 'current_version' в контекст шаблона.
        """
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm,
                                               extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Метод сохраняет данные формы по "formset" """
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class CategoryListView(ListView):
    """Контролер для вывода списка категорий"""
    model = Category

    def get_queryset(self):
        """
        Подключает функцию get_category_list_cache() из файла services.py для
        работы с контролером
        """
        return get_category_list_cache()


class ProductsListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for obj in context['object_list']:
            try:

                if len(obj.versions.filter(current_version=True)) > 1:
                    obj.active_version = obj.versions.filter(
                        current_version=True).last()
                else:
                    obj.active_version = obj.versions.get(current_version=True)
            except ObjectDoesNotExist:
                obj.active_version = "Версия продукта не указана"
        return context

    def get_queryset(self):
        """
        Подключает функцию get_products_from_cache() из файла services.py для
        работы с контролером
        """
        return get_products_from_cache()

    # app_name/<model_name>_<action>
    # catalog/product_list.html


# def products_list(requests):
#     product_list = Product.objects.all()
#     context = {
#         'object_list': product_list
#     }
#     return render(requests, "products_list.html", context)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        GetContextMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = "catalog.add_product"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, GetContextMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse("catalog:product_detail",
                       args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_edit_is_published") and user.has_perm(
                "catalog.can_edit_description") and user.has_perm(
            "catalog.can_edit_category"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDetailView(DetailView):
    model = Product
    permission_required = "catalog.product_detail"

    # Кеширование контроллера через views.py.
    # В данном проекте кеширование реализованно через urls.py
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     if settings.CACHES_ENABLED:
    #         key = f"product_list_{self.object.pk}"
    #         product_list = cache.get(key)
    #         if product_list is None:
    #             product_list = self.object.product_set.all()
    #             cache.set(key, product_list)
    #     else:
    #         product_list = self.object.product_set.all()
    #
    #     context_data['subjects'] = product_list
    #     return context_data


# def products_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         "product": product
#     }
#     return render(request, 'product_detail.html', context)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        DeleteView):
    model = Product
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy("catalog:product_list")


class ContactsView(View):
    def get(self, requests):
        return render(requests, "catalog/contacts.html")


# def contacts(requests):
#     if requests.method == "POST":
#         name = requests.POST.get("name")
#         phone = requests.POST.get("phone")
#         message = requests.POST.get("message")
#         print(f"{name}: {phone}\n {message}")
#
#     return render(requests, "catalog/contacts.html")


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("catalog:blog_base")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            user = self.request.user
            new_blog.owner = user
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("catalog:blog_base")

    def get_success_url(self):
        return reverse("catalog:blog_detail",
                       args=[self.kwargs.get("pk")])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("catalog:blog_base")
