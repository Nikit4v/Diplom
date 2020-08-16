# Дипломный проект по Django
### Установка
Скачать (clean ветку, не master) репозиторий, установить django, запустить следующие команды:
`python manage.py migrate`
`python manage.py loaddata db.json`

Всё! Проект готов к работе!

Для запуска используется команда:
`python manage.py runserver`

Доступ к **Django Administration** с помощью пользователя **admin**, пароль **admin**

Данные обычного пользователя: Логин: **std_user** Пароль: **Somepass12**

### Дополнительно
В базе данных есть дополнительные обьекты, не предоставленные изначально. Они по умолчанию скрыты, чтобы их увидеть нужно поменять их **visible status** в **Django Administration** на **Visible**. Это можно сделать для каждого объекта отдельно, а можно при помощи действия **Make objects visible**

Так же в `settings.py` есть два дополнительных параметра (расположены в самом конце файла), это `DATA_MULTIPLIER = 1` и `OBJECTS_PER_PAGE = 4`, удобные для тестов. Певрый параметр уравляет множителем данных, если нужно больше данных для тестирования, можно повысить данное значение и все обьекты будут включены в пагинацию несколько раз. Второй параметр управляет количеством объектов на странице, но важно, что за единицу принимается не 1, а 3 объекта!    