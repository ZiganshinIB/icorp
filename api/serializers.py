
# Example serializers
from rest_framework import serializers
from company.models import Company

# Sample serializers
# class CompanySerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()
#     count = serializers.IntegerField()
#
#     # Для добавления данных в базу данных
#     # во Views serializers.CompanySerializer(data).save()
#     # def create(self, validated_data):
#     #     return company.objects.create(**validated_data)
#
#     # Для обновления данных
#     # def update(self, instance, validated_data):
#     #     instance.title = validated_data.get('title', instance.title)
#     #     instance.content = validated_data.get('content', instance.content)
#     #     instance.count = validated_data.get('count', instance.count)
#     #     return instance
#
#     # Валидация данных
#     # https://django.fun/docs/django-rest-framework/3.12/api-guide/serializers/#field-level-validation
#     def validate_title(self, value):
#         if len(value) < 5:
#             raise serializers.ValidationError('Title is too short!')
#         return value
#
#     # Валидация данных на уровне объекта
#     # https://django.fun/docs/django-rest-framework/3.12/api-guide/serializers/#object-level-validation
#     def validate(self, data):
#         if data['title'] == data['content']:
#             raise serializers.ValidationError('Title and content must be different!')
#         return data


# Model serializers
# https://django.fun/docs/django-rest-framework/3.12/api-guide/serializers/#modelserializer
class CompanySerializer(serializers.ModelSerializer):
    # https://django.fun/docs/django-rest-framework/3.12/api-guide/serializers/#specifying-fields-explicitly
    my_field = serializers.CharField(source='title')

    class Meta:
        model = Company
        fields = '__all__'
        # exclude
        # depth = 1 - показать дочерние объекты
        # read_only_fields = ('title', 'content', 'count') - только для чтения

