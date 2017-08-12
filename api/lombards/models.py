from __future__ import unicode_literals
from main.models import User
from django.core.validators import MinValueValidator

from django.db import models
from utils.api import getPercent
from utils.utils import get_date


WEEKDAYS = (
    ('ПН', 'Понедельник'),
    ('ВТ', 'Вторник'),
    ('СР', 'Среда'),
    ('ЧТ', 'Четверг'),
    ('ПТ', 'Пятница'),
    ('СБ', 'Суббота'),
    ('ВС', 'Воскресенье')
)

class Filial(models.Model):
    name = models.CharField('Имя', max_length=75)
    address = models.TextField('Адрес', max_length=400)
    phone = models.CharField('Телефон', max_length=11)
    shop = models.BooleanField('Магазин', default=False)
    active = models.BooleanField('Активный', default=False)
    image = models.ImageField('Изображение', upload_to='filials')
    start_time = models.TimeField('Начало работы', blank=False)
    end_time = models.TimeField('Окончание работы', blank=False)
    long = models.FloatField(
        'Longitude(долгота)', 
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    lat = models.FloatField(
        'Latitude(широта)', 
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    end_day = models.CharField(
        'Последний рабочий день недели', 
        choices=WEEKDAYS, 
        blank=True,
        max_length=2,
        help_text='Если оставить пустым то без выходных')

    def getWorkTime(self):
        return '{}-{}'.format(self.start_time.strftime('%H:%M'), self.end_time.strftime('%H:%M'))
    getWorkTime.short_description = 'Рабочее время'
    workTime = property(getWorkTime)

    def getWorkInterval(self):
        return 'Без выходных' if (self.end_day == '') else 'ПН-{}'.format(self.end_day)
    getWorkInterval.short_description = 'Рабочие дни'
    daysInterval = property(getWorkInterval)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'filials'
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


MARKS = (
	(375, 375),
	(500, 500),
	(583, 583),
	(585, 585),
	(750, 750),
	(900, 900),
	(958, 958),
	)

class GoldMark(models.Model):
    mark = models.IntegerField('Проба', choices=MARKS, unique=True, blank=False)
    price = models.IntegerField('Цена', default=0, blank=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.getName()

    def getName(self):
        return '{} {}'.format(self.mark, 'проба')
    getName.short_description = 'Наименование'
    name = property(getName)


    class Meta:
        db_table = 'gold_prices'
        verbose_name = 'Цена пробы'
        verbose_name_plural = 'Цены проб золота'


class PercentQuery(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    percent = models.DecimalField('Процент', max_digits=10, decimal_places=2, blank=True, null=True)
    lastName = models.CharField('Фамилия', max_length=85)
    user = models.ForeignKey(User, verbose_name='Пользователь', null=True)
    zalogNumber = models.IntegerField('Номер ЗБ')
    ip = models.GenericIPAddressField('ip', blank=True, null=True)
    serverAnswer = models.TextField('Ответ сервера')
    relizDate = models.DateField('Дата реализации', blank=True, null=True)

    def __str__(self):
        return 'Query {}'.format(self.zalogNumber)

    def save(self, *args, **kwargs):
        serverAnswer = getPercent(self.zalogNumber, self.lastName)
        self.serverAnswer = serverAnswer
        if type(serverAnswer) is dict:
            self.percent = serverAnswer['percents']
            self.relizDate = get_date(serverAnswer['relizDate'])
        
        super(PercentQuery, self).save(*args, **kwargs)

    class Meta:
        db_table = 'percents_queries'
        verbose_name = 'Запрос процентов'
        verbose_name_plural = 'Запросы процентов'


