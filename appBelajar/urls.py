from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("topics/", views.topics, name='topics'),
    path("chance/<int:pk>", views.chance, name='chance'),
    path("exercise1/<int:pk>/<int:number>/", views.exercise1, name='exercise1'),
    path("exercise2/<int:pk>/<int:number>/", views.exercise2, name='exercise2'),
    path("exercise3/<int:pk>/<int:number>/", views.exercise3, name='exercise3'),
    path("over1/<int:pk>/", views.exerciseOver1, name='exerciseOver1'),
    path("over2/<int:pk>/", views.exerciseOver2, name='exerciseOver2'),
    path("over3/<int:pk>/", views.exerciseOver3, name='exerciseOver3'),
    path("myResult1/<int:pk>/", views.myResult1, name='myResult1'),
    path("myResult2/<int:pk>/", views.myResult2, name='myResult2'),
    path("myResult3/<int:pk>/", views.myResult3, name='myResult3'),
    
    path("registerPage/", views.registerPage, name='registerPage'),
    path("loginPage/", views.loginPage, name='loginPage'),
    path("logoutPage/", views.logoutPage, name='logoutPage'),
    
    path("topicList/", views.topicList, name='topicList'),
    path("questionList/<int:pk>/", views.questionList, name='questionList'),
    
    path("createTopic/", views.createTopic, name='createTopic'),
    path("deleteTopic/<int:pk>/", views.deleteTopic, name='deleteTopic'),
    path("deleteQuestion/<int:pk>/", views.deleteQuestion, name='deleteQuestion'),
    path("updateQuestion/<int:pk>/", views.updateQuestion, name='updateQuestion'),
    
    path("studentsAnswer1/<int:pk>/", views.studentsAnswer1, name='studentsAnswer1'),
    path("studentsAnswer2/<int:pk>/", views.studentsAnswer2, name='studentsAnswer2'),
    path("studentsAnswer3/<int:pk>/", views.studentsAnswer3, name='studentsAnswer3'),
    path("downloadAnswers1/<int:pk>/", views.downloadAnswer1, name='downloadAnswers1'),
    path("downloadAnswers2/<int:pk>/", views.downloadAnswer2, name='downloadAnswers2'),
    path("downloadAnswers3/<int:pk>/", views.downloadAnswer3, name='downloadAnswers3'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)