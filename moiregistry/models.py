from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

import json


# Create your models here.
class ObjectRegistration(models.Model):
    moi = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)

    approved = models.BooleanField(default=False)

    type = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)

    modref = models.TextField()

    def __str__(self):
        return "MOI[{}]".format(self.moi)

    def clean(self):
        # make sure that the moderef is a valid json object
        try:
            json.loads(self.modref)
        except:
            raise ValidationError({
                'modref': ValidationError(
                    'modref needs to be a valid JSON object', code='invalid')
            })


class AdminObject(admin.ModelAdmin):
    search_fields = ('type', 'moi', 'user', 'keywords')
    list_display = ('moi', 'approved', 'type', 'note', 'keywords')
    list_filter = ('approved', 'type')


admin.site.register(ObjectRegistration, AdminObject)


class ObjectCitations(models.Model):
    object = models.ForeignKey(ObjectRegistration, unique=False, related_name='cite_object')
    subject = models.ForeignKey(ObjectRegistration, unique=False, related_name='cite_subject')

    class Meta:
        unique_together = (('object', 'subject'), )

    def __str__(self):
        return 'Cite[{}, {}]'.format(self.object, self.subject)


admin.site.register(ObjectCitations)
