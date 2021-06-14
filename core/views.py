from django.contrib.auth.signals import user_logged_in
from django.http.response import Http404
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import Product
from shop.choices import CATEGORIES

# Create your views here.
def is_ajax(request):
    """
    This utility function is used, as `request.is_ajax()` is deprecated.

    This implements the previous functionality. Note that you need to
    attach this header manually if using fetch.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

class HomeView(View):
    def get(self, *args, **kwargs):
        # model = Product.objects.all().order_by('created_on')[:5]
        all_products = Product.objects.order_by('-pk')
        paginator = Paginator(all_products, per_page=12)
        page = self.request.GET.get('page',1)
        products = paginator.get_page(page)
        if self.request.META.get('CONTENT_TYPE') == 'application/json':
            try:
                products = paginator.page(page)
            except EmptyPage:
                raise Http404
            except PageNotAnInteger:
                products = paginator.page(1)
            return render(self.request, 'generate_products.html', {'products' : products})

        context = {'model': products.object_list, 'categories': CATEGORIES}
        return render(self.request, 'home.html', context)


class CategoryView(View):
    def get(self, *args, **kwargs):
        model = Product.objects.filter(category=kwargs['category'])
        context = {'model': model}
        return render(self.request, 'category_list.html', context)


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    # queryset = get_object_or_404(Product,pk=self.request.pk)


