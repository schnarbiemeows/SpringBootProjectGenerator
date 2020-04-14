create table action_type(action_type_id mediumint not null auto_increment primary key,
action_type varchar(5) not null ,
action_type_desc varchar(100) comment "action description",
actv varchar(1) comment "is this record active(Y or N)?");
insert into action_type(action_type, action_type_desc, actv) values("V","view","Y");
insert into action_type(action_type, action_type_desc, actv) values("S","select","Y");
insert into action_type(action_type, action_type_desc, actv) values("C","create","Y");
insert into action_type(action_type, action_type_desc, actv) values("U","update","Y");
insert into action_type(action_type, action_type_desc, actv) values("D","delete","Y");
select * from action_type;
# groups table - basic members, premium members, admins, etc...
# each user can only belong to one group_type at a time
create table if not exists groups(grp_id mediumint not null auto_increment primary key,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description");

# groups_hist - history table for group
create table if not exists groups_hist(grp_hist_id mediumint not null auto_increment primary key,
grp_id mediumint not null,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description",
action_type varchar(5) comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");