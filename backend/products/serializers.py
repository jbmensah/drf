from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer

from .models import Product
from . import validators


class ProductInlineSerializer(serializers.Serializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='product-detail',
		lookup_field='pk',
		read_only=True
	)
	title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
	owner = UserPublicSerializer(source='user', read_only=True)
	related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
	my_user_data = serializers.SerializerMethodField(read_only=True)
	my_discount = serializers.SerializerMethodField(read_only=True)
	edit_url = serializers.SerializerMethodField(read_only=True)
	url = serializers.HyperlinkedIdentityField(
		view_name='product-detail',
		lookup_field='pk')
	# email = serializers.EmailField(source='user.email', read_only=True)
	title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
	# name = serializers.CharField(source='title', read_only=True)

	class Meta:
		model = Product
		fields = [
			'owner',
			'url',
			'edit_url',
			# 'email',
			# 'name',
			'id',
			'title',
			'content',
			'price',
			'sale_price',
			'my_discount',
			'my_user_data',
			'related_products'
		]

	def get_my_user_data(self, obj):
		return {
			"username":obj.user.username
		}

	# def validate(self, data):
	def validate_title(self, value):
		# if len(value) < 10:
		# 	raise serializers.ValidationError("Title is too short!")
		request = self.context.get('request')
		user = request.user
		print(user)
		qs = Product.objects.filter(user=user, title__iexact=value)
		if qs.exists():
			raise serializers.ValidationError(f"{value} is already a product name!")
		return value

	# def create(self, validated_data):
	# 	# return Product.objects.create(**validated_data)
	# 	# email = validated_data.pop('email')
	# 	obj = super().create(validated_data)
	# 	# print(email, obj)
	# 	return obj

	# def update(self, instance, validated_data):
	# 	instance.title = validated_data.get('title')
	# 	# instance.content = validated_data.get('content')
	# 	# instance.price = validated_data.get('price')
	# 	# instance.save()
	# 	email = validated_data.pop('email')
	# 	# print(email)
	# 	# return super().update(instance, validated_data)
	# 	return instance

	def get_edit_url(self, obj):
		request = self.context.get('request')
		if request is None:
			return None
		return reverse('product-edit', kwargs={'pk': obj.id}, request=request)

	def get_my_discount(self, obj):
		if not hasattr(obj, 'id'):
			return None
		if not isinstance(obj, Product):
			return None
		return obj.get_discount()