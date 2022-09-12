from django.shortcuts import render,redirect
from employer.models import Jobs
from django.views.generic import CreateView,TemplateView,UpdateView,DetailView,ListView,View
from candidate.models import Applications,CandidateProfile
from django.contrib import messages
from candidate.forms import CandidateProfileForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from employer.decorators import signin_required
from candidate.filters import JobFilterCandidate
from datetime import date
@method_decorator(signin_required,name="dispatch")
class CandidateHome(View):
    def get(self,request,*args,**kwargs):
        qs=Jobs.objects.all()
        f=JobFilterCandidate(request.GET,queryset=Jobs.objects.all().order_by("-create_date"))
        context={'jobs':qs,"filter":f,"today":date.today()}
        return render(request,'cand_home.html',context)
class JobView(DetailView):
    model = Jobs
    template_name = "detailjob.html"
    pk_url_kwarg = "id"
    context_object_name = "job"
    def get(self, request, *args, **kwargs):
        id=kwargs['id']
        qs = self.model.objects.get(id=id)
        context = {"job": qs}
        return render(request, self.template_name, context)
@method_decorator(signin_required, name="dispatch")
class AddCandidateProfile(CreateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "profile.html"
    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.candidate = request.user
            profile.save()
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})
@method_decorator(signin_required,name="dispatch")
class CandidateProfileView(DetailView):
    model = CandidateProfile
    template_name = "profiledetail.html"
    def get(self, request, *args, **kwargs):
        qs = self.model.objects.get(candidate=self.request.user)
        context = {"profile":qs}
        return render(request, self.template_name,context)
@method_decorator(signin_required,name="dispatch")
class EditCandidateProfileView(UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "editprofile.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "id"
@method_decorator(signin_required, name="dispatch")
class CreateApplication(View):
    def get(self, request,*args,**kwargs):
        id = kwargs['id']
        job = Jobs.objects.get(id=id)
        candidate =CandidateProfile.objects.get(candidate=request.user)
        qs=Applications.objects.filter(candidate=candidate,job=job)
        if qs:
            messages.success(request, "You are already applied for the job")
            return redirect("home")
        else:
            application = Applications(candidate=candidate,job=job)
            application.save()
            messages.success(request,"You are successfully applied for the job")
            return redirect("home")
@method_decorator(signin_required,name="dispatch")
class ViewApplications(ListView):
    model = Applications
    template_name = "applications.html"
    context_object_name = "applications"
    def get(self,request,object_list=None, **kwargs):
        candidate=CandidateProfile.objects.get(candidate=request.user)
        applications=Applications.objects.filter(candidate=candidate).order_by("-submitted_date")
        return render(request,self.template_name,{"applications":applications})



