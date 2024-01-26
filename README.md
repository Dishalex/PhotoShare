# PhotoShare
Team 6 python WEB FastAPI project

**Project architecture**
├── src
│  ├── conf
│  │   └── config.py
│  ├── database
│  │  └── db.py
│  ├── entity
│  │  └── models.py
│  ├── repository
│  │  ├── users.py
│  │  ├── photos.py
│  │  └── comments.py
│  ├── routes
│  │  ├── auth_routes.py
│  │  ├── user_routes.py
│  │  ├── photo_routes.py
│  │  └── comment_routes.py
│  ├── schemas
│  │  ├── user_schemas.py
│  │  ├── photo_schemas.py
│  │  └── comment_schemas.py
│  ├──services
│  │   ├── templates
│  │   │  └── verify_email.html
│  │   ├── auth_service.py
│  │   ├── email_service.py
│  │   └── role_service.py
│  ├──utils/messages.py
│  ├──static
│  └── templates
├── tests
├── docs
├── pyproject.toml
├── main.py
└── requirements.txt

‌

    src/conf/config.py: Файл для роботи зі змінними середовища через клас Settingns.
    src/database: Містить файли для роботи з базою даних.
    db.py: Файл для створення та керування з'єднанням з базою даних.
    src/entity/models.py: Представлення моделей для бази даних.
    src/repository: Зберігає файли, які відповідають за роботу з репозиторіями для різних сутностей.
    users.py: Операції репозиторія для користувачів.
    photos.py: Операції репозиторія для фотографій.
    comments.py: Операції репозиторія для коментарів.
    src/routes: Містить файли для опису маршрутів вашого застосунку.
    auth_routes.py: Операції репозиторія аутентифікації.
    user_routes.py: Маршрути, пов'язані з користувачами.
    photo_routes.py: Маршрути, пов'язані з фотографіями.
    comment_routes.py: Маршрути, пов'язані з коментарями.
    src/schemas: Містить файли з описом схем даних для валідації та роботи з даними.
    user_schemas.py: Схеми для користувачів.
    photo_schemas.py: Схеми для фотографій.
    comment_schemas.py: Схеми для коментарів.
    src/services: Містить файли з описом схем даних для валідації та роботи з даними.
    auth_service.py: Схеми для користувачів.
    email_service.py: Схеми для фотографій.
    role_service.py: Схеми для коментарів.
    utils/messages.py**:** репозиторій повідомлень і констант.
    tests і docs: для тестів і документації
    pyproject.toml: Файл конфігурації проекту.
    main.py: Основний файл, де розташовується точка входу для застосунку.
    requirements.txt: Файл, де перераховані залежності для встановлення.




