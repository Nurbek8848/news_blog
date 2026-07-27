from django.core.exceptions import ValidationError
from rest_framework import serializers

from articles.models import Tag
from articles.models.article import status_choices, Article


# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=200, required=True)
#     content = serializers.CharField(max_length=3000, required=True)
#     author = serializers.PrimaryKeyRelatedField(read_only=True)
#     status = serializers.ChoiceField(choices=status_choices, required=False)
#     tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'tags', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        return super().validate(data)

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError('error text')
        return value


    # def create(self, validated_data):
    #     tags = validated_data.pop('tags', [])
    #     article = super().create(validated_data)
    #     article.tags.set(tags)
    #     return article
    #
    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('tags', [])
    #
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     instance.tags.set(tags)
    #     return instance
