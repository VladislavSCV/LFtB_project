from django import forms


CHOICES = [
    ('theme1', 'Синяя тема'),
    ('theme2', 'Темная тема'),
    ('theme3', 'Фиолетовая тема'),
]


class select_theme(forms.Form):
    usernameSET = forms.CharField(label="Имя:", required=False)
    description = forms.CharField(label="Описание:", required=False)
    user_photo_url = forms.URLField(label="Ссылка на фото профиля:", required=False)
    user_theme = forms.ChoiceField(label="Выберите тему:", choices=CHOICES, widget=forms.RadioSelect, required=False)


class userFormREG(forms.Form):
    user_name_ = forms.CharField(label="Name", max_length=30)
    user_email_ = forms.EmailField(label="Email")
    password_ = forms.CharField(label="Password", widget=forms.PasswordInput())


class userSearchEngine(forms.Form):
    search_engine = forms.CharField(label="")


class userFormAUTH(forms.Form):
    _user_name = forms.CharField(label="Name", max_length=30)
    _password = forms.CharField(label="Password", widget=forms.PasswordInput())
    

class bank_card(forms.Form):
    cardNumber = forms.CharField(label="Номер карты:")
    cardholderName = forms.CharField(label="Имя владельца:")
    expiryDate = forms.CharField(label="Срок действия:")
    cvv = forms.CharField(label="CVV:")



