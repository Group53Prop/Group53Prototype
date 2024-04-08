from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

USER_TYPE_CHOICES = [
        ('consultant', 'Consultant'),
        ('Line Manager', 'Manager'),
        ('financeteam', 'Accounts Payable'),
        ('admin', 'Admin')

    ]

class MyAccountManager(BaseUserManager):
    def create_user(self, email, userID, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not userID:
            raise ValueError("Users must have a userID")

        user = self.model(
            email=self.normalize_email(email),
            userID=userID
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, userID, password):

        user = self.create_user(
        email=self.normalize_email(email),
        password=password,
        userID=userID,
    )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)


class Account(AbstractBaseUser):
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
    userID       = models.IntegerField(unique=True)
    date_joined  = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login   = models .DateTimeField(verbose_name="last login", auto_now=True)
    is_admin     = models. BooleanField(default=False)
    is_active    = models. BooleanField(default=True)
    is_staff     = models. BooleanField(default=True)
    is_superuser = models. BooleanField(default=False)
    first_name   = models.CharField(max_length=30)
    last_name    = models.CharField(max_length=30)
    user_type    = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='consultant',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'userID' ,]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_full_name(self):
        # Adjust the following to concatenate your user's first and last names appropriately
        return f"{self.first_name} {self.last_name}"
