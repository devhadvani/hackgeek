from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models




class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    email = models.EmailField(max_length=100,unique=True)
    is_host = models.BooleanField(default=False)
    is_part = models.BooleanField(default=False)

    role =(
        ('is_host','Host'),
        ('is_part','Participate')
        )
    roles = models.CharField(max_length=10, choices=role,default=is_part)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Participants(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    is_student = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    # college = models.CharField(max_length=300)
    # organization = models.CharField(max_length=300)
    role =(
        ('is_student','Student'),
        ('is_employee','Employee')
        )
    roles = models.CharField(max_length=20, choices=role,default=is_student)
    
class Hosts(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    organization = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    
class Host_hack(models.Model):
    # hack_id = models.IntegerField(null=True)
    image = models.FileField(upload_to="images",null = True, blank=True)
    host_name = models.ForeignKey(User,on_delete=models.SET_NULL,null = True)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    org_name = models.CharField(max_length=200)
    org_desc = models.TextField()
    from_date=  models.DateField(auto_now=False, auto_now_add=False,null=True)
    end_date=  models.DateField(auto_now=False, auto_now_add=False,null=True)


class Tags(models.Model):
    project_id = models.CharField(max_length=100,null=True)

class Details(models.Model):
    title = models.CharField(max_length=100,null=True)
    project_id = models.CharField(max_length=100,null=True)
    team_id = models.AutoField(primary_key=True)
    team_leader = models.CharField(max_length=100,null=True)
    team_m2 = models.CharField(max_length=100,null  =True)
    team_m3 = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.team_leader

class Data(models.Model):
    user = models.CharField(null = True,max_length=100)
    files = models.FileField(upload_to="images",null = True, blank=True)
    project_id = models.CharField(max_length=100,null=True)
    team_id = models.IntegerField(null=True)

class Winner(models.Model):
    POSITION_CHOICES = (
        ('1', 'First Place'),
        ('2', 'Second Place'),
        ('3', 'Third Place'),
    )

    team = models.OneToOneField(Details, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=100)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)

    def __str__(self):
        return f"Winner: {self.team.team_leader} - Position: {self.get_position_display()} - Project ID: {self.project_id}"