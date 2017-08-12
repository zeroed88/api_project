from lombards.serializers import PercentQuerySerializer as pqs
from django.contrib.auth.models import AnonymousUser as auser
from django.contrib.auth import authenticate
from main.serializers import UserSerializer
from main.models import User as sUser
from simple_email_confirmation.models import EmailAddress
from lombards.models import Filial
from lombards.serializers import FilialSerializer


def test_authenticateUser(username, password):
    return authenticate(username=username, password=password)

def test_PercentQuerySerializer(zalogNumber, lastName, user=auser):
    test_data = {'user': user.pk, 'lastName': lastName, 'zalogNumber': zalogNumber}
    s = pqs(data=test_data)
    if s.is_valid():
        r = s.save()
        return s

def test_UserCreate(username, email, password):
    input_data = {
        'email': email,
        'username': username,
        'password': password
    }
    import ipdb; ipdb.set_trace(context=5)
    s = UserSerializer(data=input_data)
    if s.is_valid():
        user = s.create(s.validated_data)
        return user

def test_UserSerialiser(**kwargs):
    s = UserSerializer(data=kwargs)
    return s

def test_GetConfirmKey(username):
    u = sUser.objects.get(username=username)
    return u.reset_email_confirmation(u.email)

def test_CheckConfirmationKey(username, myKey, newEmail):
    u = sUser.objects.get(username=username)
    import ipdb; ipdb.set_trace(context=5)
    if u.get_confirmation_key() != myKey:
        raise Exception('myKey is broken!')
    u.add_confirmed_email(newEmail)
    u.set_primary_email(newEmail)
    return u

def test_uniqUserName(username):
    try:
        u = sUser.objects.get(username=username)
        return False
    except:
        return True

def test_FilialSerialiser():
    filials = Filial.objects.filter(active=True)
    return FilialSerializer(filials, many=True)



if __name__ == '__main__':
    # record = test_PercentQuerySerializer(18344, 'Абдул Хамид')
    # record = test_UserCreate('ivan', 'ge52@mail.ru', '123')
    # record = test_UserSerialiser(username='Garry')
    # record = test_GetConfirmKey('Garry')
    # record = test_CheckConfirmationKey('Garry', 'jKE4qHtH6jXe', 'm@mail.ru')
    # record = test_uniqUserName('Garr')
    # record = test_authenticateUser('Garry123', '1234567A')
    record = test_FilialSerialiser()


