from datetime import timedelta, datetime as dt
from typing import Union

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import COLUMN_COUNT, ROW_COUNT, SHEET_ID, TIME_FORMAT


def _format_duration(duration: Union[float, int]) -> str:
    """Преобразует дни в строку формата 'X days, HH:MM:SS.microseconds'."""
    return str(timedelta(days=duration))


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = dt.now().strftime(TIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет от {now_date_time}',
            'locale': 'ru-RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': SHEET_ID,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': ROW_COUNT, 'columnCount': COLUMN_COUNT
                }
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list[dict[str, Union[str, float]]],
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = dt.now().strftime(TIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
    ]
    if not projects:
        table_values.append(['В фонде нет закрытых проектов'])
    else:
        table_values.append(['Название проекта', 'Время сбора', 'Описание'])
        for project in projects:
            new_row = [
                project['name'],
                _format_duration(project['duration']),
                project['description'],
            ]
            table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
