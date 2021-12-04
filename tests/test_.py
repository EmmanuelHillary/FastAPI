from app.calculations import BankAccount, add_func, subtract_func, InsufficientFunds
import pytest

@pytest.fixture
def initialize_bank_account():
    return BankAccount()

@pytest.mark.parametrize("x, y, z", [(1,2,3), (4,5,9), (10,11,21)])
def test_add_func(x,y,z):
    assert add_func(x, y) == z

@pytest.mark.parametrize("x, y, z", [(3,2,1), (9,5,4), (21,11,10)])
def test_subtract_func(x,y,z):
    assert subtract_func(x, y) == z

@pytest.mark.parametrize("deposit, withdraw, f_balance, b_interest",[
    (50, 10, 40, 44),
    (60, 10, 50, 55),
    (70, 10, 60, 66)
])
def test_bank_account(initialize_bank_account, deposit, withdraw, f_balance, b_interest):
    default_balance = initialize_bank_account.default_balance
    initialize_bank_account.deposit(deposit)
    deposited_balance = initialize_bank_account.default_balance
    initialize_bank_account.withdraw(withdraw)
    final_balance = initialize_bank_account.default_balance
    interest = initialize_bank_account.interest()

    assert default_balance == 0
    assert deposited_balance == deposit
    assert final_balance == f_balance
    assert round(interest, 3) == b_interest

def test_insufficient_funds(initialize_bank_account):
    with pytest.raises(InsufficientFunds):
        initialize_bank_account.withdraw(400)