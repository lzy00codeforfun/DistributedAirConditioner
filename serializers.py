from  rest_framework import serializers
from polls.models import test

class TestSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    phone = serializers.IntegerField(default=-1)

    def create(self, validated_data):
        return test.objects.create(**validated_data)

    def update(self,instance,validated_data):
