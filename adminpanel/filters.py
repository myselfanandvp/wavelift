import django_filters



from users.models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username',lookup_expr='icontains',label='User Name')
    is_active = django_filters.ChoiceFilter(
        field_name='is_active',
        label='Active Or Not',
        choices=[
            ('', 'All'),
            ('True', 'Active'),
            ('False', 'Not Active')
        ],
        empty_label=None  # Prevents an additional "---------" option
    )
    
    order_by = django_filters.OrderingFilter(fields=(
        ('created_at', 'created_at'),
        ('username', 'username'),
            ('email', 'email'),
            ('id', 'id'),
    ),field_labels={
            'created_at': 'Created At',
            'username': 'Username',
            'email': 'Email',
            'id': 'ID',
        },
        choices=[
            ('created_at', 'Created At (Ascending)'),
            ('-created_at', 'Created At (Descending)'),
            ('username', 'Username (Ascending)'),
            ('-username', 'Username (Descending)'),
            ('email', 'Email (Ascending)'),
            ('-email', 'Email (Descending)'),
            ('id', 'ID (Ascending)'),
            ('-id', 'ID (Descending)'),
        ],
        label='Order By'
        )
   
    class Meta:
        model = User
        fields = ["id",'username', 'email', 'is_active'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initializes FilterSet properly
        
        
        for field in   self.form.fields.values():
           field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': field.label, 
            })
           