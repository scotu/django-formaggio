from rest_framework import serializers
from ..models import FormaggioForm, FormaggioField


class FormaggioFieldReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaggioField
        fields = (
            'id',
            'index',
            'label',
            'kind',
            'hint',
            'extra',
            'mandatory',
        )

class FormaggioFormReadSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField(method_name='get_fields_field')

    class Meta:
        model = FormaggioForm
        fields = (
            'id',
            'title',
            'fields',
        )

    def get_fields_field(self, form):
        queryset = FormaggioField.objects.filter(form=form)
        return FormaggioFieldReadSerializer(
            instance=queryset,
            many=True,
            read_only=True
        ).data
