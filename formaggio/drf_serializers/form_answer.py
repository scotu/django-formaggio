# -*- coding: utf-8 -*-
import base64
import six
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from ..models import get_formaggio_form_model
from ..models import FormaggioFormResult, FormaggioFieldValue
FormaggioForm = get_formaggio_form_model()


class Base64FileField(serializers.FileField):
    """
    source: http://stackoverflow.com/a/28036805/150932

    A Django REST framework field for handling image-uploads through raw post
    data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64FileField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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
                    value = item.get('value', "")
                    file_value = item.get('file_value')
                    result_fields[str(item['field'].id)] = (value, file_value,)
            return form_definition.save_result(
                result_fields=result_fields,
                user=user,
                contact_info=validated_data.get('contact_info')
            )

