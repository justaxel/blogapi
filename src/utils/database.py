def get_db_data(db_data: str , is_test: bool = False) -> str:
    
    if is_test:
        request = f'TEST_{db_data}'
    else:
        request = f'{db_data}'
    return request

