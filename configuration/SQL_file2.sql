drop table if exists question;
drop table if exists answer;
drop table if exists question_category;
drop table if exists question_level;
create table question_category(question_category_id mediumint not null auto_increment primary key,
question_category_desc varchar(100), is_actv boolean, evnt_tmestmp DATETIME(2), evnt_oper_id varchar(10));
create table question_level(question_level_id mediumint not null auto_increment primary key,
question_level_desc varchar(100), is_actv boolean, evnt_tmestmp DATETIME(2), evnt_oper_id varchar(10));
create table answer(answer_id mediumint not null auto_increment primary key,
answer_txt varchar(1024), is_actv boolean, evnt_tmestmp DATETIME(2), evnt_oper_id varchar(10));
create table question(question_id mediumint not null auto_increment primary key,
question_category_id mediumint not null, foreign key QCK_1(question_category_id) references question_category(question_category_id)
on update cascade on delete cascade,
question_level_id mediumint not null, foreign key QLK_1(question_level_id) references question_level(question_level_id)
on update cascade on delete cascade,
answer_id mediumint, foreign key ANS_1(answer_id) references answer(answer_id)
on update cascade on delete cascade,
question_txt varchar(256), is_actv boolean, evnt_tmestmp DATETIME(2), evnt_oper_id varchar(10));

insert into question_level(question_level_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("EASY",true,sysdate(), 'admin');
insert into question_level(question_level_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("MEDIUM",true,sysdate(), 'admin');
insert into question_level(question_level_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("HARD",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Java - Core",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Java - Data Structures",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Java - Threading",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Java - Java 8",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Linux",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Kafka - Core",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Kafka - Streaming",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Hadoop - Core",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Hive",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("PySpark",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Sqoop",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Spark - Core",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Spark - Scala",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Spark - Streaming",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("SQL",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Python",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Java - Spring",true,sysdate(), 'admin');
insert into question_category(question_category_desc,is_actv,evnt_tmestmp,evnt_oper_id) values ("Scala",true,sysdate(), 'admin');
