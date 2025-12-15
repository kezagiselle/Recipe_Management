from django.urls import path
from .views import RecipeListCreate, RecipeDetail, CategoryList

urlpatterns = [
    path('', RecipeListCreate.as_view(), name='recipe-list-create'),
    path('<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
]
