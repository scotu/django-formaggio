# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.conf import settings


class FormaggioForm(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'form'

    def __unicode__(self):
        return u"{0}".format(self.get_short_desc())

    def get_short_desc(self):
        return self.title

    def save_result(self, result_fields, user=None, contact_info=None):
        if not contact_info:
            contact_info = user.email
        fr = FormaggioFormResult(
            form=self,
            user=user,
            contact_info=contact_info,
            answered_date=datetime.datetime.utcnow()
        )
        fr.save()
        for field in FormaggioField.objects.filter(
            id__in=[int(x) for x in result_fields.keys()]
        ):
            field.save_value(result_fields[str(field.id)], fr)
        fr.valid = True
        fr.save()
        return fr


class FormaggioFormResult(models.Model):
    form = models.ForeignKey('FormaggioForm', null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    contact_info = models.CharField(max_length=255, null=False, blank=False)
    answered_date = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'form result'


class FormaggioField(models.Model):
    FIELDS_TO_SAVE = [
        'index',
        'label',
        'kind',
        'hint',
        'extra',
        'mandatory'
    ]

    KIND_TEXT_TEXT = 'text'
    KIND_TEXT_VALUE = 'TEXT_FIELD'
    KIND_NUMBER_TEXT = 'number'
    KIND_NUMBER_VALUE = 'TEXT_FIELD_NUM'
    KIND_PHONE_TEXT = 'phone'
    KIND_PHONE_VALUE = 'TEXT_FIELD_PHONE'
    KIND_EMAIL_TEXT = 'email'
    KIND_EMAIL_VALUE = 'TEXT_FIELD_MAIL'
    KIND_NAME_TEXT = 'name'
    KIND_NAME_VALUE = 'TEXT_FIELD_NAME'
    KIND_CHECKBOX_TEXT = 'checkbox'
    KIND_CHECKBOX_VALUE = 'CHECKBOX'
    KIND_TEXTAREA_TEXT = 'textarea'
    KIND_TEXTAREA_VALUE = 'TEXT_AREA'
    KIND_CHOICES = (
        (KIND_TEXT_VALUE, KIND_TEXT_TEXT,),
        (KIND_NUMBER_VALUE, KIND_NUMBER_TEXT,),
        (KIND_PHONE_VALUE, KIND_PHONE_TEXT,),
        (KIND_EMAIL_VALUE, KIND_EMAIL_TEXT,),
        (KIND_NAME_VALUE, KIND_NAME_TEXT,),
        (KIND_CHECKBOX_VALUE, KIND_CHECKBOX_TEXT,),
        (KIND_TEXTAREA_VALUE, KIND_TEXTAREA_TEXT,),
    )
    active = models.BooleanField(default=True)

    form = models.ForeignKey('FormaggioForm', null=False, blank=False)
    # common fields with FieldValue model
    index = models.BigIntegerField()
    label = models.TextField(null=False, blank=False)
    kind = models.CharField(
        max_length=100,
        choices=KIND_CHOICES,
        null=False,
        blank=False
    )
    hint = models.TextField(null=False, blank=True)
    extra = models.TextField(null=False, blank=True)
    mandatory = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'form field'

    def __unicode__(self):
        return self.get_short_desc()

    def get_short_desc(self):
        return u"field: \"{0}\" (form: \"{1}\")".format(
            self.label,
            self.form.get_short_desc()
        )

    def save_value(self, value, form_result):
        fv = FormaggioFieldValue(
            value=value,
            form_result=form_result,
            field=self
        )
        for item in FormaggioField.FIELDS_TO_SAVE:
            setattr(fv, "original_{0}".format(item), getattr(self, item))
        fv.save()


class FormaggioFieldValue(models.Model):
    # common fields with Field model
    original_index = models.BigIntegerField()
    original_label = models.TextField(null=False, blank=False)
    original_kind = models.CharField(max_length=100, null=False, blank=False)
    original_hint = models.TextField(null=False, blank=True)
    original_extra = models.TextField(null=False, blank=True)
    original_mandatory = models.BooleanField(default=False)
    # FieldValue specific fields
    field = models.ForeignKey('FormaggioField', null=False, blank=False)
    form_result = models.ForeignKey(
        'FormaggioFormResult',
        null=False,
        blank=False
    )
    value = models.TextField()

    class Meta:
        verbose_name = 'form value'
