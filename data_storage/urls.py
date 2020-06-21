import json

from django.urls import path, include
from . import models
from rest_framework import routers, serializers, viewsets


def load_json_from_str(ret, field):
    if field in ret:
        try:
            ret[field] = json.loads(ret[field])
        except json.JSONDecodeError:
            ret.pop(field)


class NeuralModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NeuralModel
        fields = '__all__'


class NeuralModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.NeuralModel.objects.all()
    serializer_class = NeuralModelSerializer


class UserInputSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserInput
        fields = '__all__'


class UserInputViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserInput.objects.all()
    serializer_class = UserInputSerializer


class TrainingTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TrainingTask
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ('error_message', 'result_url', 'metrics'):
            if not ret[field]:
                ret.pop(field)
        load_json_from_str(ret, 'metrics')
        return ret


class TrainingTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TrainingTask.objects.all()
    serializer_class = TrainingTaskSerializer


class EvalTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.EvalTask
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ('error_message', 'result'):
            if not ret[field]:
                ret.pop(field)
        load_json_from_str(ret, 'result')
        return ret


class EvalTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EvalTask.objects.all()
    serializer_class = EvalTaskSerializer


router = routers.DefaultRouter()
router.register(r'neural-models', NeuralModelViewSet)
router.register(r'user-input', UserInputViewSet)
router.register(r'training-tasks', TrainingTaskViewSet)
router.register(r'eval-tasks', EvalTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
