# -*- coding: utf-8 -*-
from formaggio.models import FormaggioForm
from rest_framework import serializers
from ..models import FormaggioFormResult, FormaggioFieldValue


class FormaggioFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaggioFieldValue
        fields = (
            'field',
            'value',
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
                    result_fields[str(item['field'].id)] = item['value']
            return form_definition.save_result(
                result_fields=result_fields,
                user=user,
                contact_info=validated_data['contact_info']
            )

