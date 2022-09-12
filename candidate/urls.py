from candidate import views
from django.urls import path
urlpatterns = [
    path('jobs/path',views.CandidateHome.as_view(),name="home"),
    path('job/<int:id>',views.JobView.as_view(),name="job"),
    path('profile/add',views.AddCandidateProfile.as_view(),name="addprofile"),
    path('profile/edit/<int:id>',views.EditCandidateProfileView.as_view(),name="editprofile"),
    path('profile/view',views.CandidateProfileView.as_view(),name="viewprofile"),
    path('job/apply/<int:id>',views.CreateApplication.as_view(),name="createapplication"),
    path('applications/all',views.ViewApplications.as_view(),name="viewapplication"),

    ]