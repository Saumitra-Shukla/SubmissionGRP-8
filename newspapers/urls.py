from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='newspapers'

urlpatterns = [

			path('news/<int:pk>/',views.NewsDetailView.as_view(),name='news_detail'),
			path('newspaper/<int:pk>/', views.news_detail_view, name="newspaper_detail"),
			path('news/preriority',views.vader_sentiment,name='vader_sentiment'),
			path('news/latest',views.latest_news,name='latest'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
