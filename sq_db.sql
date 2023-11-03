CREATE TABLE ������������� (
  �������������_id integer PRIMARY KEY ,
  ����_������ DECIMAL(4,2) NOT NULL,
  ������_������� VARCHAR(20),
  ������_������ VARCHAR(20),
  ��������� VARCHAR(30),
  �������_id integer ,
  �������_����������� VARCHAR(30) NOT NULL,
  FOREIGN KEY (�������������_id) REFERENCES ��������(�������������_id)
);

CREATE TABLE ������ (
  ������_id integer PRIMARY KEY ,
  ��������_������ VARCHAR(20) NOT NULL,
  FOREIGN KEY (������_id) REFERENCES ��������(������_id)
);

CREATE TABLE ���������� (
  ����������_id integer PRIMARY KEY ,
  ��������_�������� VARCHAR(50) NOT NULL ,
  ��������_������� INT, --��
  ������� INT,
  ���_����� INT, --������������
  ����_����� INT, --������ ��� ������
  ����_����� INT, --������������ �������
  �����_����� INT, --
  FOREIGN KEY ( ����������_id) REFERENCES ��������(����������_id)
);

CREATE TABLE ������� (
 �������_id integer PRIMARY KEY ,
  ������� VARCHAR(30) NOT NULL,
  ��� VARCHAR(30) NOT NULL,
  �������� VARCHAR(30) NOT NULL,
  �����_id integer,
  FOREIGN KEY ( �������_id) REFERENCES �������������(�������_id)
);

CREATE TABLE �������� (
  ��������_id integer PRIMARY KEY ,
  ��������_�������� VARCHAR(50) NOT NULL,
  ������� integer,
  ���_����� integer,
  ����_����� integer,
  ����_����� integer,
  �����_����� integer,
  ����������_id integer  ,
  �������������_id integer  ,
  ������_id integer
);
