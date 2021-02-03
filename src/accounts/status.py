ACCOUNTS_STATUS_OPTS = [
    'active',
    'not active',
    'upon deletion',
    'deleted',
]


def set_status(status: str) -> str:
    """
    Sets the current status of the account. The options are established by
    ACCOUNTS_STATUS_OPTS constant:
    `active`, `not active`, `upon deletion`, and `deleted`.
    """

    _status = status.lower()
    if _status in ACCOUNTS_STATUS_OPTS:
        status = _status
        return status
    else:
        raise ValueError(
            f'{status} is not a valid account status. '
            'Please see the status module to find all available account status'
        )
