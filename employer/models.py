from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,email,phone,role,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            role=role,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,phone,role,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone=models.CharField(max_length=15)
    options=(("jobseeker","jobseeker"),
             ("employer","employer"))
    role=models.CharField(max_length=15,choices=options)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
class CompanyProfile(models.Model):
    company=models.OneToOneField(MyUser,on_delete=models.CASCADE,related_name="employer")
    company_name=models.CharField(max_length=20)
    company_logo = models.ImageField(upload_to="images",null=True)
    services = models.TextField(max_length=120)
    founded_date=models.DateField(null=True)
    website = models.CharField(max_length=50)

class Jobs(models.Model):
    company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    Designation=models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    experience=models.PositiveIntegerField()
    skills=models.CharField(max_length=200)
    vacancies=models.PositiveIntegerField()
    location=models.CharField(max_length=50)
    create_date=models.DateField(auto_now_add=True)
    end_date=models.DateField(null=True)
