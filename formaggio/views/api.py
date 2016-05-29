from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from ..models import FormaggioFormResult, FormaggioField
from ..drf_serializers.form_answer import FormaggioFormResultSerializer
from ..drf_serializers.form_builder import FormaggioFieldSerializer


class FormAnswerViewSet(CreateModelMixin, GenericViewSet):
    queryset = FormaggioFormResult.objects.all()
    serializer_class = FormaggioFormResultSerializer


class FormFieldEditorViewSet(ModelViewSet):
    queryset = FormaggioField.objects.all()
    serializer_class = FormaggioFieldSerializer
