from operator import is_
import pytest
import random, string

from ..utils.account import Account
from ..utils.database import get_db_data, is_data_valid

from ..utils.custom_errors import (
    MaxNumberOfCharactersReached,
    SomeDataMightBeEmpty,
    NoDataFound
)

################# BEGINNING OF FIXTURES #################


@pytest.fixture
def account_instance():
    account = Account()
    return account


#################### END OF FIXTURES ####################


def test_hash(account_instance):

    account = account_instance
    raw_str = 'ThisIsNotTheBestPasswordInTheWorld1234'
    h_str = account.hash_password(raw_str)
    assert not raw_str == h_str

    another_raw_str = 'TotallyNotMyPassword0987'
    wrong_h_str = account.hash_password(another_raw_str)
    assert account.verify_password(raw_str, h_str) is True
    assert account.verify_password(raw_str, wrong_h_str) is False

    one_more_raw_str = 'ThisIsAPassword1234!"#$#"%$#%00¿¿'
    h_str1 = account.hash_password(one_more_raw_str)
    h_str2 = account.hash_password(one_more_raw_str)
    assert not h_str1 == h_str2


def test_username_checker(account_instance):

    account = account_instance
    # wrong because of bad chars
    bad_username = ''.join(random.choice(string.printable) for _ in range(20))
    
    with pytest.raises(TypeError) as e_info:
        account.is_username_valid(bad_username)
    assert str(e_info.value) == (
        "The username can only contain letters (a-Z), numbers (0-9) and underscores. "
        f"Please check your input: {bad_username}."
    )
    bad_username2 = ''.join(random.choice(string.ascii_letters) for _ in range(251))

    with pytest.raises(MaxNumberOfCharactersReached) as e_info2:
        account.is_username_valid(bad_username2)
    assert str(e_info2.value) == (
        "The username can only be 250 or less characters long. "
        "The one provided has: 251 characters."
    )
    bad_username3 = ''.join(random.choice(string.whitespace) for _ in range(20))
    
    with pytest.raises(TypeError) as e_info3:
        account.is_username_valid(bad_username3)
    assert str(e_info3.value) == (
        "The username can only contain letters (a-Z), numbers (0-9) and underscores. "
        f"Please check your input: {bad_username3}."
    )


def test_status_setter(account_instance):

    account = account_instance
    status = 'active'
    assert account.set_status(status) == status.upper()
    bad_status = 'I AM NOT A VALID STATUS'
    with pytest.raises(NameError) as e_info:
        account.set_status(bad_status)
    assert str(e_info.value) == (
        f"{bad_status} is not a valid status. "
        "Please use one of the following status options: 'ACTIVE, NOT ACTIVE, DELETED'."
    )


def test_correct_db():

    assert get_db_data('THIS IS NOT ACTUAL DATA', is_test=False) == 'THIS IS NOT ACTUAL DATA'
    assert get_db_data('THIS IS NOT ACTUAL DATA EITHER', is_test=True) == 'TEST_THIS IS NOT ACTUAL DATA EITHER'
    ctrl_res = ''.join(random.choice(string.printable) for _ in range(20))
    assert not get_db_data('I EXIST TO NOT BE CONTROLLED') == ctrl_res


def test_data_validation():

    # control data. It should always return true
    data1 = {
        'username': 'myusername',
        'email': 'myemail@email.com',
        'password': """MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    assert is_data_valid(data1) is True

    # username with bad characters
    data2 = {
        'username': """asdaksdñalkf0031!"$"#""¿''123123""",
        'email': 'myemail@email.com',
        'password': """"MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    assert is_data_valid(data2) is False

    # empty username
    data3 = {
        'username': '',
        'email': 'myemail@email.com',
        'password': """"MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    with pytest.raises(SomeDataMightBeEmpty) as e_info:
        is_data_valid(data3)
    assert str(e_info.value) == (
            "It appears that \"username\" field is empty. "
            "Please check that all required data has a valid value"
    )

    # no username
    data4 = {
        'email': 'myemail@email.com',
        'password': """"MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    with pytest.raises(NoDataFound) as e_info2:
        is_data_valid(data4)
    assert str(e_info2.value) == (
        "It appears that 'username' might be missing. "
        "Please check that you have input all required data."
    )

    #! TODO: email with bad chars

    # empty email
    data5 = {
        'username': 'myusername',
        'email': '',
        'password': """"MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    with pytest.raises(SomeDataMightBeEmpty) as e_info3:
        is_data_valid(data5)
    assert str(e_info3.value) == (
        "It appears that \"email\" field is empty. "
        "Please check that all required data has a valid value"
    ) 

    # no email
    data6 = {
        'username': 'myusername',
        'password': """"MyPassword1234!"=)#('""",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    with pytest.raises(NoDataFound) as e_info4:
        is_data_valid(data6)
    assert str(e_info4.value) == (
        "It appears that 'email' might be missing. "
        "Please check that you have input all required data."
    )

    # empty password
    data7 = {
        'username': 'myusername',
        'email': 'myemail@email.com',
        'password': "",
        'conf_password': """MyPassword1234!"=)#('"""
    }
    with pytest.raises(SomeDataMightBeEmpty) as e_info5:
        is_data_valid(data7)
    assert str(e_info5.value) == (
        "It appears that \"password\" field is empty. "
        "Please check that all required data has a valid value"
    )

    # no passwords
    data8 = {
        'username': 'myusername',
        'email': 'myemail@email.com'
    }
    with pytest.raises(NoDataFound) as e_info6:
        is_data_valid(data8)
    assert str(e_info6.value) == (
        "It appears that 'password' might be missing. "
        "Please check that you have input all required data."
    )
