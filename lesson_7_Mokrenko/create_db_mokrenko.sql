
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS task_scheduled;
CREATE TABLE task_scheduled (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), comment VARCHAR (255), category INT, priority INT, isexecuted INT,  plandate DATE, plantime INT, facttime INT);
DROP TABLE IF EXISTS task_heaped;
CREATE TABLE task_heaped (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), comment VARCHAR (255), category INT, priority INT,  targetdate DATE);

insert into task_scheduled select 1, 'Сделать домашнее задание по курсу "Python"', 'Есть вопрос по ДЗ', 3, 2, 1, null, null, null;
insert into task_scheduled select 2, 'Заказать корм коту с наименьшей ценой', 'В почте есть промокод. Найти.', 2, 1, 0, null, null, null;
insert into task_scheduled select 3, 'Проверить личную почту', 'Жду письмо от ALiexpress', 1, 3, 0, null, null, null;
insert into task_scheduled select 4, 'Сходить и получить посылку №121232312323', 'Почта работает и в ВСК', 2, 2, 0, null, null, null;

insert into task_heaped select 5, 'Сделать домашнее задание к уроку 2', 'Предварительно должно быть сделано ДЗ к уроку 1', 3, 1, null;
insert into task_heaped select 6, 'Разобрать лоджию', 'Нужно дождаться тепла', 2, 3, null;

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
