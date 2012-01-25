from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
from django.utils.datetime_safe import date
from unidecode import unidecode

class Entry(models.Model):

    # Blog entry fields
    headline = models.CharField('Blog entry title',max_length=200)
    body = models.TextField('Blog Content')
    publishdate = models.DateField('Blog entry publishing date', default=date.today() )
    publish = models.BooleanField('Publish Blog entry',default=False )

    # Meta data
    slug = models.SlugField(editable=False) # the future
    author = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(editable=False,auto_now_add=True)
    updated = models.DateTimeField(editable=False,auto_now=True)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.headline))[:50]
        super(Entry, self).save(force_insert=True)

# admin stuff
site.register(Entry)