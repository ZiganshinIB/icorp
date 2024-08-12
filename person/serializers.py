from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'phone_number', 'first_name', 'last_name', 'surname', 'birthday', 'password', 'email')
        read_only_fields = ('username', 'email')
