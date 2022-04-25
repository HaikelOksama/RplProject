from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('create/', views.createOrg, name='create'),

    path("organisasi/", views.organisasiList, name="organisasi"),
    path('organisasi/<str:name>/', views.organisasiDetail, name='detail'),
    path('update/<str:pk>', views.editOrg, name='update'),

    path("organisasi/<str:organisasi>/create-event/", views.createEvent, name="create-event"),
    path('event/<str:pk>', views.eventDetail, name='event'),
    path('event/<str:pk>/edit', views.editEvent, name='eventEdit'),
    path('event/<str:pk>/delete', views.deleteEvent, name='eventDelete'),

    path('rekomendasi/', views.rekomendasiList, name='rekomendasi'),

    path("organisasi/<str:organisasi>/new-feed/", views.createFeed, name="create-feed"),
    path("delete/<str:pk>", views.deleteFeed, name="delete_feed"),

    path("profile/<str:username>/", views.profileView, name="profile"),
    path("profile/update/<str:username>/", views.updateProfile, name="profile_update"),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerView, name='register'),

    
]


