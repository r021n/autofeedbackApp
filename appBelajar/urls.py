from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("topics/", views.topics, name='topics'),
    path("exercise/<int:pk>/<int:number>/", views.exercise, name='exercise'),
    path("over/", views.exerciseOver, name='exerciseOver'),
    path("myResult/<int:pk>/", views.myResult, name='myResult'),
    
    path("registerPage/", views.registerPage, name='registerPage'),
    path("loginPage/", views.loginPage, name='loginPage'),
    path("logoutPage/", views.logoutPage, name='logoutPage'),
    
    path("topicList/", views.topicList, name='topicList'),
    path("questionList/<int:pk>/", views.questionList, name='questionList'),
    
    path("createTopic/", views.createTopic, name='createTopic'),
    path("deleteTopic/<int:pk>/", views.deleteTopic, name='deleteTopic'),
    path("deleteQuestion/<int:pk>/", views.deleteQuestion, name='deleteQuestion'),
    path("updateQuestion/<int:pk>/", views.updateQuestion, name='updateQuestion'),
    
    path("studentsAnswer/<int:pk>/", views.studentsAnswer, name='studentsAnswer'),
    path("downloadAnswers/<int:pk>/", views.downloadAnswer, name='downloadAnswers'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)