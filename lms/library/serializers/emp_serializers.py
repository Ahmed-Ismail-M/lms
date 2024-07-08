from rest_framework import serializers
from ..models import Employee
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = Employee
        fields = ['username', 'password', 'first_name',
                  'last_name', 'email']
    
    def create(self, validated_data):
        emp = self.Meta.model.objects.create(**validated_data)
        emp.set_password(validated_data['password'])
        group, created = Group.objects.get_or_create(name='Employee')
        group.save()
        emp.groups.add(group)
        emp.save()
        return emp
    
class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                print(user)
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [ 'id', 'username']