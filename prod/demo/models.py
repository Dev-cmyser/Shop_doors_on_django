from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчство', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', unique=True, blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FILD = 'username'

    def full_name(self):
        return ' '.join([self.name, self.surname, self.patronymic])

    def __str__(self):
        return self.full_name()


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    date = models.DateTimeField( verbose_name='дата обновления', auto_now_add=True)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file,
                                   blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])
    year = models.IntegerField(verbose_name='Год производства', blank=True)
    coutry = models.CharField(max_length=254, verbose_name='Страна производства', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                     default=0.00)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField( max_length=254, verbose_name='Наименование', blank=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    count = models.IntegerField(verbose_name='Кол-во', blank=False, default=0)
    product = models.ForeignKey('Product', verbose_name='Продукта', on_delete=models.CASCADE)
    user = models.ForeignKey('User', verbose_name='Пользователя', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product) + " " + str(self.count)


class Order(models.Model):
    STATUS_CHOICES = [
                         ('confirmed', 'Подтверждённый'),
                         ('new', 'Новый'),
                         ('canseled', 'Отменённый')
                     ]
    date = models.DateTimeField(verbose_name='дата заказа', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES , default='new')
    rejectreason = models.TextField(verbose_name='Причина отказа', blank=True)
    user = models.ForeignKey('User', verbose_name='Пользователя', on_delete=models.CASCADE)
    product = models.ManyToManyField('Product', through='ItemInOrder', related_name='order')

    def count_product(self):
        count_product = 0
        for iteminorder in self.iteminorder_set.all():
            count_product += iteminorder.count
        return count_product

    def __str__(self):
        return str(self.date.ctime()) + ' | ' + self.user.full_name() + \
            ' | Количество: ' + str(self.count_product()) + ' | ' + self.user.username


class ItemInOrder(models.Model):
    count = models.IntegerField(verbose_name='Кол-во', blank=False, default=0)
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)

    def __str__(self):
        return str(self.product) + " " + str(self.count) + '(' + str(self.price) + ')'

# Create your models here.
