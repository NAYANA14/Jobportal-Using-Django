from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,UpdateView,DetailView,ListView,View
from django.core.paginator import Paginator
from employer.models import CompanyProfile,Jobs
from candidate.models import CandidateProfile,Applications
from employer.forms import CompanyProfileForm,EmpLoginForm,EmpSignUpForm,JobForm,ApplicationStatusForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,logout,login
from employer.models import MyUser
from django.utils.decorators import method_decorator
from employer.decorators import signin_required
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control
from django.db.models import Q
from datetime import date
from django.core.paginator import Paginator
from django import forms
# Create your views here.
class SignUpView(CreateView):
    model = MyUser
    template_name = "register.html"
    form_class = EmpSignUpForm
    success_url = reverse_lazy("signin")
class SignInView(TemplateView):
    template_name = "login.html"
    form_class=EmpLoginForm
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context={"form":self.form_class}
        return context
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get("email")
            password=form.cleaned_data.get("password")
            role=form.cleaned_data.get("role")
            user=authenticate(request,email=email,password=password,role=role)
            if user:
                login(request,user)
                if user.role == "employer":
                    return render(request,"emp_home.html")
                else:
                    return redirect("home")
        else:
            context = {'form': form}
            return render(request,'login.html', context)
@cache_control(no_cache=True, must_revalidate=True)
def sign_out(request):
    logout(request)
    return redirect('index')
class ListAllCompanies(ListView):
    model=CompanyProfile
    template_name = "index_companies.html"
    context_object_name = "companies"
@method_decorator(signin_required,name="dispatch")
class Home(TemplateView):
    template_name="emp_home.html"
def index(request):
    return render(request,'index.html')
def Search(request,**kwargs):
    if request.method=="GET":
        query=request.GET.get('query')
        if query:
            jobs=Jobs.objects.filter(Q(location__icontains=query)|Q(Designation__contains=query)).order_by("-create_date")
            context={'jobs':jobs,"today":date.today()}
            return render(request, 'search.html',context)
        else:
            jobs=Jobs.objects.all().order_by("-create_date")
            context = {'jobs': jobs,"today":date.today()}
            return render(request,'search.html', context)
@method_decorator(signin_required,name="dispatch")
class AddCompanyProfile(CreateView):
    model=CompanyProfile
    form_class =CompanyProfileForm
    template_name = "add_company.html"
    def post(self,request):
        form=self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            companyprofile= form.save(commit=False)
            companyprofile.company=request.user
            companyprofile.save()
            return redirect("alljobs")
        else:
            return render(request,self.template_name,{"form":form})
@method_decorator(signin_required, name="dispatch")
class CompanyProfileView(DetailView):
    model = CompanyProfile
    template_name = "company_detail.html"
    def get(self, request, *args, **kwargs):
        qs = self.model.objects.get(company=self.request.user)
        context = {"profile":qs}
        return render(request, self.template_name,context)
@method_decorator(signin_required,name="dispatch")
class EditCompanyProfileView(UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = "editcompanyprofile.html"
    success_url = reverse_lazy("alljobs")
    pk_url_kwarg = "id"
@method_decorator(signin_required,name="dispatch")
class AddJobView(CreateView):
    model =Jobs
    form_class = JobForm
    template_name = "add_jobs.html"
    context_object_name = "job"
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            company=CompanyProfile.objects.get(company=request.user)
            job.company = company
            job.save()
            return redirect("alljobs")
        else:
            return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class AllJobsView(ListView):
    model=Jobs
    template_name = "list_jobs.html"
    def get(self, request, *args, **kwargs):
        company = CompanyProfile.objects.get(company=request.user)
        jobs= Jobs.objects.filter(company=company).order_by("-create_date")
        paginator = Paginator(jobs,5 )
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {  "page_obj":  page_obj,"today":date.today()})
class JobsDetailView(DetailView):
    model = Jobs
    template_name = "job_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "job"
    def get(self, request, *args, **kwargs):
        id=kwargs['id']
        qs = self.model.objects.get(id=id)
        context = {"job": qs}
        return render(request, self.template_name, context)
@method_decorator(signin_required,name="dispatch")
class EditJobView(UpdateView):
    model = Jobs
    form_class = JobForm
    template_name = "edit_jobs.html"
    context_object_name = "job"
    success_url = reverse_lazy("alljobs")
    pk_url_kwarg = "id"
@method_decorator(signin_required,name="dispatch")
class RemoveJobView(View):
    def get(self,request,**kwargs):
        id=kwargs.get("id")
        qs=Jobs.objects.get(id=id)
        qs.delete()
        jobs=Jobs.objects.all()
        context={"job":jobs}
        return render(request,"list_jobs.html",context)
@method_decorator(signin_required,name="dispatch")
class AllApplications(ListView):
    model=Applications
    template_name = "allapplications.html"
    context_object_name = "applications"
    def get(self, request, *args, **kwargs):
        company = CompanyProfile.objects.get(company=request.user)
        job = Jobs.objects.filter(company=company)
        applications=Applications.objects.filter(job__in=job).order_by("-submitted_date")
        paginator = Paginator(applications, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj":page_obj})
@method_decorator(signin_required,name="dispatch")
class InterViewCall(UpdateView):
    model = Applications
    pk_url_kwarg = "id"
    form_class = ApplicationStatusForm
    template_name = "app process.html"
    success_url = reverse_lazy("jobapplications")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.object
        return context
    def form_valid(self, form):
        self.object.status = "accepted"
        self.object = form.save()
        Interview_Date = form.cleaned_data.get('Interview_Date')
        message = 'Your Interview will be held on ' + str(Interview_Date)
        send_mail(
            'InterviewCall',
            message,
            'reciever@gmail.com',
            ['sender@gmail.com'],
            fail_silently=False,
        )
        return super().form_valid(form)

        html_content = render_to_string('email.html')
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            'InterviewCall',
            message,
            settings.EMAIL_HOST_USER,
            ['sender@gmail.com']
        )
@method_decorator(signin_required,name="dispatch")
class ApplicationStausReject(View):
    def get(self,request, **kwargs):
        id=kwargs['id']
        application=Applications.objects.get(id=id)
        application.status="rejected"
        application.save()
        return redirect("jobapplications")

@method_decorator(signin_required, name="dispatch")
class AllApplicants(ListView):
    model=Applications
    template_name = "applicants.html"
    context_object_name = "applications"
    paginate_by = 10
    page_kwarg = "applications"
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        job = Jobs.objects.get(id=id)
        applications=Applications.objects.filter(job=job).order_by("-submitted_date")
        return render(request, self.template_name, {"applications": applications})
@method_decorator(signin_required,name="dispatch")
class ApplicantProfileView(ListView):
    model = Applications
    template_name = "applicantprofile.html"
    context_object_name = "applications"
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        application=Applications.objects.get(id=id)
        return render(request, self.template_name, {"application": application})