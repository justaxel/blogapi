import pytest
import random
import string

from src.database.verification import AccountDataVerification

from src.utils.custom_errors import (
    NoDataFound,
    SomeDataMightBeEmpty,
    MaxNumberOfCharactersReached,
)


def test_general_data_validation():

    # ideal account data
    T_account_data1 = {
        'username': 'my_username123',
        'email': 'myusername@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify1 = AccountDataVerification(T_account_data1)
    assert verify1.is_data_valid() is True

    # passwords do not match
    T_account_data2 = {
        'username': 'my_username123',
        'email': 'myusername@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'totallysecurepassword123'
    }

    verify2 = AccountDataVerification(T_account_data2)
    # if passwords do not match return False without raising exception
    assert verify2.is_data_valid() is False

    # username contains invalid characters
    T_account_data3 = {
        'username': 'Not_a_valid_username123!',
        'email': 'thisisavalidemail@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify3 = AccountDataVerification(T_account_data3)
    # if username is not valid return, False without raising exception
    assert verify3.is_data_valid() is False
    
    # generate random string with 251 characters
    random_substring_ascii = ''.join(random.choice(string.ascii_letters) for _ in range(125))
    random_substring_digits = ''.join(random.choice(string.digits) for _ in range(125))
    random_string = random_substring_ascii + random_substring_digits + '_'

    # username contains too many characters
    T_account_data4 = {
        'username': random_string,
        'email': 'mynormalemail@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'   
    }

    verify4 = AccountDataVerification(T_account_data4)
    # if username has more than 250 characters, return False without raising exception
    assert verify4.is_data_valid() is False

    T_account_data5 = {
        'email': 'myemail@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify5 = AccountDataVerification(T_account_data5)
    # if account data does not have all required fields, raise NoDatafound excetion
    with pytest.raises(NoDataFound) as e_info:
        verify5.is_data_valid()
    assert str(e_info.value) == (
        "It appears that 'username' is missing. "
        "Please check that you have all required data. "
        "Here is a hint: username, email, password, password_confirm."
    )

    T_account_data6 = {
        'username': 'myusername',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify6 = AccountDataVerification(T_account_data6)
    # if account data does not have all required fields, raise NoDatafound excetion
    with pytest.raises(NoDataFound) as e_info:
        verify6.is_data_valid()
    assert str(e_info.value) == (
        "It appears that 'email' is missing. "
        "Please check that you have all required data. "
        "Here is a hint: username, email, password, password_confirm."
    )

    T_account_data7 = {
        'username': 'myusername',
        'email': 'myemail@email.com',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify7 = AccountDataVerification(T_account_data7)
    # if account data does not have all required fields, raise NoDatafound excetion
    with pytest.raises(NoDataFound) as e_info:
        verify7.is_data_valid()
    assert str(e_info.value) == (
        "It appears that 'password' is missing. "
        "Please check that you have all required data. "
        "Here is a hint: username, email, password, password_confirm."
    )

    T_account_data8 = {
        'username': '',
        'email': 'myemail@email.com',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify8 = AccountDataVerification(T_account_data8)
    # if account data has some empty field's value raise SomeDataMightBeEmpty exception.
    with pytest.raises(SomeDataMightBeEmpty) as e_info:
        verify8.is_data_valid()
    assert str(e_info.value) == (
        f"It appears that 'username' field is empty. "
         "Please check that all required data has a valid value"
    )

    T_account_data9 = {
        'username': 'myusername',
        'email': '',
        'password': 'mytotallysecurepassword123',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify9 = AccountDataVerification(T_account_data9)
    # if account data has some empty field's value raise SomeDataMightBeEmpty exception.
    with pytest.raises(SomeDataMightBeEmpty) as e_info:
        verify9.is_data_valid()
    assert str(e_info.value) == (
        f"It appears that 'email' field is empty. "
         "Please check that all required data has a valid value"
    )

    T_account_data10 = {
        'username': 'myusername',
        'email': 'myemail@email.com',
        'password': '',
        'password_confirm': 'mytotallysecurepassword123'
    }

    verify10 = AccountDataVerification(T_account_data10)
    # if account data has some empty field's value raise SomeDataMightBeEmpty exception.
    with pytest.raises(SomeDataMightBeEmpty) as e_info:
        verify10.is_data_valid()
    assert str(e_info.value) == (
        f"It appears that 'password' field is empty. "
         "Please check that all required data has a valid value"
    )

def test_username_validation():
    """
    Test for AccountDataVerification.is_username_valid() function.
    """
    
    # ideal account data
    T_account_data1 = {
        'username': 'my_username123'
    }

    verify1 = AccountDataVerification(T_account_data1)
    assert verify1.is_username_valid(T_account_data1['username']) is True

    T_account_data2 = {
        'username': 'Not_a_valid_username123!'
    }

    verify2 = AccountDataVerification(T_account_data2)
    with pytest.raises(TypeError) as e_info:
        verify2.is_username_valid(T_account_data2['username'])
    assert str(e_info.value) == (
        'The username can only contain letters (a-Z), numbers (0-9) and underscores. '
        f"Please check your input: Not_a_valid_username123!."
    )
    
    # generate random string with 251 characters
    random_substring_ascii = ''.join(random.choice(string.ascii_letters) for _ in range(125))
    random_substring_digits = ''.join(random.choice(string.digits) for _ in range(125))
    random_string = random_substring_ascii + random_substring_digits + '_'

    T_account_data3 = {
        'username': random_string
    }

    verify3 = AccountDataVerification(T_account_data3)
    with pytest.raises(MaxNumberOfCharactersReached) as e_info:
        verify3.is_username_valid(T_account_data3['username'])
    assert str(e_info.value) == (
        'A username can only be 250 or less characters long. '
        f"The one provided has 251 characters."
    )
