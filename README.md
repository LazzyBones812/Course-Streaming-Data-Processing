# Course-Streaming-Data-Processing
The project for the course "Streaming data processing"

**Цель проекта**: получать новостные данные о популярных ценных бумагах с финансового новостного агрегатора (в данном случае это Yahoo Finance) и отправлять их в топик Kafka

**Библиотеки**
 - Scrapy - для получения данных с новостных источников
 - schedule - для того, чтобы паук Scrapy запускался через определенное время
 - confluent_kafka - для взаимодействия с Kafka

В *parse_fin_data\spiders* хранится файл yahoo_finance.py, в котором описана работа паука Scrapy. В этом файле в переменной lst хранится список тикетов ценных бумаг, информацию о которых паук получает. 

В файле main.py описана работа schedule. Цель этой программы - запускать паука Scrapy через каждую минуту.

В файл results.json записываются промежуточные результаты, которые получил паук Scrapy

Для запуска нужно в директории parse_fin_data запустить файл main.py
 - python main.py

Для запуска docker-compose - docker compose -f docker-compose-kafka.yml up
