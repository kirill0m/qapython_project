# Итоговый проект


## Тестируемое приложение
* Приложение представляет собой простую страничку-визитку с формой авторизации и возможностью зарегистрировать
нового пользователя. Есть поддержка управления пользователями через API, поставляется в docker-контейнере

## Что было сделано
1. Написан mock сервис для работы с айди пользователя, которое запрашивает приложение после авторизации
2. Написан docker-compose.yml для развертывания контейнеров приложения, базы данных, селеноида, mock сервиса и проекта для тестирования приложения
3. Написаны автотесты для тестирования страницы авторизации, регистрации, главной страницы и API приложения с использованием fixtures, PageObject, APIObject и ORM
4. Тесты запускаются параллельно и не конфликтуют между собой
5. Запуск тестов реализован через Jenkins: подготовлена сборка, после завершения тестирования к сборке аттачится Allure отчет
<details><summary>Пример отчета с тестовыми наборами</summary><img src="https://i.ibb.co/wBBZ4yZ/image.png"></details>

## Настройки сборки Jenkins
* В Build Environment активирована настройка для удаления папки с прошлыми отчетами
* В Build Steps выполняется батник

    `docker network create -d bridge ui-test_selenoid` - создаем сеть для корректной работы селеноида и контейнеров с браузерами

    `docker load -i C:\Users\Kirill\Desktop\final_project\app\myapp` - загружаем образ приложения, в данном случае локально с компа 

    `docker-compose up --abort-on-container-exit --exit-code-from test_myapp` - развертываем, система завершается с завершением работы тестового проекта

    `docker-compose down -v --rmi local` - останавливаем сервисы, удаляем контейнеры и сети
