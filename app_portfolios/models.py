from portfolio_maker.tools import upload_image_path, upload_image_with_rand_num_name, get_file_ext
from django.contrib.auth.models import User
from django.db import models
from .model_managers import PortfolioManager


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="first name")
    last_name = models.CharField(max_length=50, blank=True, null=True,  verbose_name="last name")
    profile_image = models.ImageField(upload_to=upload_image_path, blank=True, null=True, verbose_name="image")
    user_skill_title = models.CharField(max_length=50, blank=True, null=True,  verbose_name="Your Skill Title")
    introduce = models.TextField(verbose_name="introduce", blank=True, null=True)
    about_me_title = models.CharField(max_length=200, blank=True, null=True,  verbose_name="title of about me page")
    work_experience = models.TextField(verbose_name="experience", blank=True, null=True)

    birthday = models.DateField(blank=True, null=True, verbose_name="birthday")
    website = models.CharField(max_length=150, blank=True, null=True, verbose_name="website")
    # email = models.CharField(max_length=50, unique=True, verbose_name="email")
    freelance = models.CharField(max_length=50, null=True, blank=True, verbose_name="freelance")

    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="phone")
    linkedin = models.CharField(max_length=50, blank=True, null=True, verbose_name="linkedin")
    instagram = models.CharField(max_length=50, blank=True, null=True, verbose_name="instagram")

    # categories = models.ManyToManyField(ProductCategories, blank=True, verbose_name="دسته بندی های اصلی")
    # sub_categories = models.ManyToManyField(Product_SubCategories, blank=True, verbose_name="دسته بندی های فرعی")
    # wisher_users = models.ManyToManyField(User, verbose_name="موجود در لیست علاقه مندی", blank=True)

    objects = PortfolioManager()

    class Meta:
        verbose_name_plural = "Portfolios"
        verbose_name = "Portfolio"

    def __str__(self):
        return self.owner.email

    # def get_amount_in_session(self):
    #     cart_items = EshopSessions.__new__(EshopSessions)
    #     return cart_items.get_amount_of_product_in_cart(the_product=give_me_the_product_by_id(self.id))


class Skill(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name="owner")
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name="title")
    skill_percent = models.IntegerField(default=0, verbose_name="skill percent")

    # showing to Django admin panel
    class Meta:
        verbose_name_plural = "skills"
        verbose_name = "skill"

    def __str__(self):
        return self.portfolio.owner.email


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name="owner")
    url = models.CharField(max_length=150, blank=True, null=True, verbose_name="link")
    image = models.ImageField(upload_to=upload_image_with_rand_num_name, verbose_name="image")

    # to show in Django admin page
    class Meta:
        verbose_name_plural = "Projects"
        verbose_name = "project"

    # modify showing type in Django admin panel
    def __str__(self):
        return self.portfolio.owner.email
