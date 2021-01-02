import pytest
import random, string

from ..utils.account import Account
from ..utils.database import get_db_data

from ..utils.custom_errors import MaxNumberOfCharactersReached


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


def test_username_checker(account_instance):

    account = account_instance
    # wrong because of bad chars
    bad_username = ''.join(random.choice(string.printable) for _ in range(20))
    
    with pytest.raises(TypeError) as e_info:
        account.check_username(bad_username)
    assert str(e_info.value) == f"""\
                        The username can only contain letters (a-Z), numbers (0-9) and underscores.\
                        Please check {bad_username}.\
                    """.rstrip()
    bad_username2 = ''.join(random.choice(string.ascii_letters) for _ in range(251))

    with pytest.raises(MaxNumberOfCharactersReached) as e_info2:
        account.check_username(bad_username2)
    assert str(e_info2.value) == f"""\
                    The username can only be 250 or less characters long.\
                    The one provided has: 251 characters.\
                """.rstrip()
    bad_username3 = ''.join(random.choice(string.whitespace) for _ in range(20))
    
    with pytest.raises(TypeError) as e_info3:
        account.check_username(bad_username3)
    assert str(e_info3.value) == f"""\
                        The username can only contain letters (a-Z), numbers (0-9) and underscores.\
                        Please check {bad_username3}.\
                    """.rstrip()


def test_status_setter(account_instance):

    account = account_instance
    status = 'active'
    assert account.set_status(status) == status.upper()
    bad_status = 'I AM NOT A VALID STATUS'
    with pytest.raises(NameError) as e_info:
        account.set_status(bad_status)
    assert str(e_info.value) == f"""\
                    {bad_status} is not a valid status. Please use one of the following\
                    status options: 'ACTIVE, NOT ACTIVE, DELETED'.\
                """.rstrip()


def test_correct_db():

    assert get_db_data('THIS IS NOT ACTUAL DATA', is_test=False) == 'THIS IS NOT ACTUAL DATA'
    assert get_db_data('THIS IS NOT ACTUAL DATA EITHER', is_test=True) == 'TEST_THIS IS NOT ACTUAL DATA EITHER'
    ctrl_res = ''.join(random.choice(string.printable) for _ in range(20))
    assert not get_db_data('I EXIST TO NOT BE CONTROLLED') == ctrl_res