from . import views
from django.urls import path

app_name = "homepage"

urlpatterns = [
    path('', views.home, name="homepage"),
    # path('plant_classify', views.post_plant_classify, name="plant_classify"),
]