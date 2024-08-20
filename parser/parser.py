import requests
from bs4 import BeautifulSoup
from loguru import logger


async def get_parsing(login, password, date):
    # URL для страницы авторизации
    login_url = 'https://p.vendista.ru/Auth/Login'
    results = []
    # Создаем сессию для обработки куков
    session = requests.Session()

    # Отправляем GET-запрос для получения страницы и извлечения токена
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    verification_token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')

    # URL и данные для аутентификации
    auth_url = 'https://p.vendista.ru/Auth/Login'
    login_data = {
        '__RequestVerificationToken': verification_token,
        'returnUrl': '',
        'Login': login,
        'Password': password,
    }

    # Отправляем POST-запрос для аутентификации
    response = session.post(auth_url, data=login_data)

    # URL для перехода после успешной авторизации
    report_url = (f'https://p.vendista.ru/Reports?OrderByColumn=0&OrderDesc=True&PageNumber=1&ItemsOnPage='
                  f'200&IsAfterSubmittingForm=true&DateFrom={date}+00%3A00&DateTo={date}+23%3A59&FilterText='
                  f'&OwnerIds=&DivisionId=&DivisionName=&ProcessingIds=&TermId=')

    # Отправляем GET-запрос для перехода по новому URL
    response_bonuses = session.get(report_url)

    # Проверяем результат перехода
    try:
        # Извлекаем данные из таблицы
        soup_bonuses = BeautifulSoup(response_bonuses.text, 'html.parser')

        # Найдите тело таблицы
        table_body = soup_bonuses.find('tbody')

        # Перебирать строки в теле таблицы
        for row in table_body.find_all('tr'):
            # Извлеките соответствующие данные из каждой строки
            columns = row.find_all('td')
            terminal_id = columns[0].text.strip()
            company_name = columns[1].text.strip()
            amount = columns[2].text.strip()
            quantity = columns[3].text.strip()

            results.append(f"#{company_name} <b>{amount}</b> - {quantity}")

        # Извлеките итоговую строку
        total_row = soup_bonuses.find('tfoot').find('tr')
        total_amount = total_row.find_all('td')[1].text.strip()
        total_quantity = total_row.find_all('td')[2].text.strip()
        results.append(f"Итого: {total_quantity} на сумму <b>{total_amount}</b>")

        return '\n'.join(results)

    except Exception as e:
        logger.exception('Аутентификация не прошла!', e)


if __name__ == "__main__":
    # Пример использования функции
    login_ = 'golana127@mail.ru'
    password_ = 'qrjyat'
    date_ = '11.12.2023'

    get_parsing(login_, password_, date_)
