from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.constants import SECONDS_IN_HOUR, SECONDS_IN_MINUTE
from app.core.config import settings
from app.models.charity_project import CharityProject


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(settings.format_datetime)
    service = await wrapper_services.discover(
        'sheets',
        settings.google_sheets_api_version
    )
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': settings.sheets_locale},
        'sheets': [
            {'properties': {
                'sheetType': settings.sheet_type,
                'sheetId': settings.sheet_id,
                'title': settings.sheet_title,
                'gridProperties': {'rowCount': settings.row_count,
                                   'columnCount': settings.column_count}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': settings.permissions_type,
                        'role': settings.permissions_role,
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        'drive', settings.google_drive_api_version
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(settings.format_datetime)
    service = await wrapper_services.discover(
        'sheets',
        settings.google_sheets_api_version
    )
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            str(project.name),
            str(get_time_difference(project)),
            str(project.description)
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': settings.update_major_dimension,
        'values': table_values
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=settings.sheets_range,
            valueInputOption=settings.sheets_value_input_option,
            json=update_body
        )
    )
    return response


def get_time_difference(project: CharityProject) -> str:
    time_difference: timedelta = project.close_date - project.create_date
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, SECONDS_IN_HOUR)
    minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)
    return f'{days} days, {hours}:{minutes}:{seconds}'
