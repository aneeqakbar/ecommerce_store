from django.urls import path
from .views import (
    CategoryView,
    HomeView,
    ProductView,
)

app_name = 'core'

urlpatterns = [
    path('',HomeView.as_view(),name='HomeView'),
    path('product/<pk>/',ProductView.as_view(),name='ProductView'),
    path('category/<slug:category>/',CategoryView.as_view(),name='CategoryView')
]
