from django.urls import path
from employer import views
urlpatterns = [
path('',views.index,name="index"),
    path("ehome",views.Home.as_view(),name="ehome"),
    path("companies",views.ListAllCompanies.as_view(),name="company"),
    path("search",views.Search,name="search"),
    path('signup',views.SignUpView.as_view(),name="signup"),
    path('signin',views.SignInView.as_view(),name="signin"),
    path('signout',views.sign_out,name="signout"),
    path('profile/add',views.AddCompanyProfile.as_view(),name="addcompany"),
    path('profile/edit/<int:id>', views.EditCompanyProfileView.as_view(), name="editcompany"),
    path('profile/view', views.CompanyProfileView.as_view(), name="viewcompany"),
    path('job/add/',views.AddJobView.as_view(),name="addjob"),
    path('job/change/<int:id>', views.EditJobView.as_view(), name="editjob"),
    path('job/view/<int:id>', views.JobsDetailView.as_view(), name="viewjob"),
    path('jobs/all',views.AllJobsView.as_view(),name="alljobs"),
    path('job/remove/<int:id>',views.RemoveJobView.as_view(),name="removejob"),
    path('job/applications/all',views.AllApplications.as_view(),name="jobapplications"),
    path('job/applicants/<int:id>',views.AllApplicants.as_view(),name="applicants"),
    path('job/applicants/profile/<int:id>', views.ApplicantProfileView.as_view(), name="applicantprofile"),
    path('job/application/accept/<int:id>',views.InterViewCall.as_view(),name="appstatus"),
    path('job/application/reject/<int:id>',views.ApplicationStausReject.as_view(),name="appreject"),
]