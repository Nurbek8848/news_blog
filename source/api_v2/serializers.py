from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from articles.models import Tag, Comment
from articles.models.article import Article


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title"]
        read_only_fields = ["id"]

class ArticleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title']
        read_only_fields = fields


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
        read_only_fields = ["id"]


class ArticleSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    likes = LikesSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'tags', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        data['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return data


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
