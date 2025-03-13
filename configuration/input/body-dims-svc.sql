create table if not exists users(user_id mediumint not null auto_increment primary key,
username varchar(256) not null UNIQUE comment "username",
email varchar(300) not null UNIQUE comment "email address",
phone varchar(10) comment "user's phone number, required for message notifications",
password varchar(256) not null comment "password should be encrypted",
age smallint comment "age in years; we don't want to store the user's DOB",
lst_logd_in	datetime comment "when did the user last log in?");
create table if not exists body_dimensions(body_dimension_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key BLPR2(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date date not null comment "the calendar date(date only, no time)",
dimension decimal(6,2) comment "dimension in inches");
create index body_dimensions_idx on body_dimensions(calendar_date);