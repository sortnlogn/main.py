CREATE TABLE Преподаватель (
  Преподаватель_id integer PRIMARY KEY ,
  Доля_ставки DECIMAL(4,2) NOT NULL,
  Ученая_степень VARCHAR(20),
  Ученое_звание VARCHAR(20),
  Должность VARCHAR(30),
  Персона_id integer ,
  Условия_привлечения VARCHAR(30) NOT NULL,
  FOREIGN KEY (Преподаватель_id) REFERENCES Нагрузка(преподаватель_id)
);

CREATE TABLE Группа (
  Группа_id integer PRIMARY KEY ,
  Название_группы VARCHAR(20) NOT NULL,
  FOREIGN KEY (Группа_id) REFERENCES Нагрузка(Состав_id)
);

CREATE TABLE Дисциплина (
  Дисциплина_id integer PRIMARY KEY ,
  Название_предмета VARCHAR(50) NOT NULL ,
  Зачетные_еденицы INT, --ЗЕ
  Семестр INT,
  Лаб_часов INT, --лабораторные
  Лекц_часов INT, --лекции без потока
  Прак_часов INT, --Практические занятия
  Итого_часов INT, --
  FOREIGN KEY ( Дисциплина_id) REFERENCES Нагрузка(Дисциплина_id)
);

CREATE TABLE Персона (
 Персона_id integer PRIMARY KEY ,
  Фамилия VARCHAR(30) NOT NULL,
  Имя VARCHAR(30) NOT NULL,
  Отчество VARCHAR(30) NOT NULL,
  Логин_id integer,
  FOREIGN KEY ( Персона_id) REFERENCES Преподаватель(Персона_id)
);

CREATE TABLE Нагрузка (
  Нагрузка_id integer PRIMARY KEY ,
  Название_предмета VARCHAR(50) NOT NULL,
  Семестр integer,
  Лаб_часов integer,
  Лекц_часов integer,
  Прак_часов integer,
  Итого_часов integer,
  Дисциплина_id integer  ,
  преподаватель_id integer  ,
  Состав_id integer
);
