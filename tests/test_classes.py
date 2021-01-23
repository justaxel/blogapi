import pytest

from src.classes.accounts import Account
from src.database.verification import AccountDataVerification

from src.utils.custom_errors import (
    EmptyValue,
    EmptyPasswordNotAllowed
)


def test_account_set_status():

    T_username = 'myusername'
    T_email = 'myemail@email.com'
    T_password = 'mysecurepassword'

    T_account = Account(T_username, T_email, T_password)

    T_account.set_status('active')
    assert T_account.status == 'active'
    T_account.set_status('not active')
    assert T_account.status == 'not active'
    T_account.set_status('deleted')
    assert T_account.status == 'deleted'

    with pytest.raises(NameError) as e_info:
        T_account.set_status('not a valid status')
    assert str(e_info.value) == (
        'not a valid status is not a valid status. '
        'Please use one of the following status options: '
        "'active, not active, deleted'."
    )

    with pytest.raises(EmptyValue) as e_info:
        T_account.set_status('')

def test_account_hash_password():

    T_username = 'myusername'
    T_email = 'myemail@email.com'
    T_password = 'mysecurepassword'

    T_account = Account(T_username, T_email, T_password)

    T_account.hash_password()
    assert not T_account.password == T_password


    # set a status so spew_out_data() can return a dictionary with all the data
    T_account.set_status('active')
    T_data = T_account.spew_out_data()
    
    # set up an AccountDataVerification instance to be able to check if the
    # hash_password worked correctly
    verification = AccountDataVerification(T_data)
    assert verification.is_hashed_str_valid(T_password, T_account.password) is True

    # test hash_password with an empty password
    T_account.password = ''

    with pytest.raises(EmptyPasswordNotAllowed):
        T_account.hash_password()