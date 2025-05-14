# Test Task IOKA

## Ключевые пункты

- Регистрация пользователей
- Логин
- Создание банковских счетов с различными валютами
- Конвертация между счетов с учётом комиссии. Конвертация можжет быть как внутри одного аккаунта, так и между текущим и другими
- Вывод курсов валют

## Установка

git clone https://github.com/OPELsinus/test_task_ioka
```
pip install -r requirements.txt

poetry shell
```

## Запуск

```
uvicorn main:app --reload
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | POST | Регистрация |
| `/login` | POST | Вход в аккаунт |
| `/create_bank_account` | POST | Создание банковского счёта |
| `/exchange` | POST | Создание обмена |

## Конфиг

```
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

## Documentation

Visit `/docs` or `/redoc` after starting the server.

Примеры приложения:
![image](https://github.com/user-attachments/assets/74d39ce3-a021-4f16-97fe-fdfca342f16a)

![image](https://github.com/user-attachments/assets/211d2408-d695-4c2e-9a45-abcad7a6e069)
