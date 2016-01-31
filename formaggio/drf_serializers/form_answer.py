# -*- coding: utf-8 -*-
from formaggio.models import get_formaggio_form_model
from rest_framework import serializers
from ..models import FormaggioFormResult, FormaggioFieldValue
FormaggioForm = get_formaggio_form_model()

import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


# Custom image field - handles base 64 encoded images
class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            file_format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = file_format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64FileField, self).to_internal_value(data)


class FormaggioFieldValueSerializer(serializers.ModelSerializer):
    file_value = Base64FileField(required=False)
    class Meta:
        model = FormaggioFieldValue
        fields = (
            'field',
            'value',
            'file_value',
        )


class FormaggioFormResultSerializer(serializers.ModelSerializer):
    field_values = FormaggioFieldValueSerializer(many=True, write_only=True)
    form = serializers.PrimaryKeyRelatedField(
            many=False,
            read_only=False,
            queryset=FormaggioForm.objects.all()
        )

    class Meta:
        model = FormaggioFormResult
        fields = (
            'form',
            'contact_info',
            'field_values',
        )

    def create(self, validated_data):
        try:
            form_definition = validated_data['form']  # TODO: make sure it belongs to the current app
        except FormaggioForm.DoesNotExist as dne:
            raise serializers.ValidationError({
                "form": "the form id provided didn't correspond to a valid form"
            })
        else:
            # FIXME: some more error handling needed in this block
            request = self.context.get('request')

            if request and hasattr(request, 'user'):
                user = request.user
            else:
                user = None

            result_fields = {}
            for item in validated_data['field_values']:
                if item['field'].form == form_definition:
                    result_fields[str(item['field'].id)] = (item.get('value', ""), item.get('file_value'),)
            return form_definition.save_result(
                result_fields=result_fields,
                user=user,
                contact_info=validated_data.get('contact_info')
            )

