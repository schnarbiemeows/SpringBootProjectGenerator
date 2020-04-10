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

# grp_user - table to "connect" all users with all groups
create table if not exists grp_user(grp_user_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field",
user_id mediumint not null comment "FK to the users.user_id field");
create index grp_user_idx on grp_user(grp_id);
create index user_grp_idx on grp_user(user_id);

# grp_user_hist - history table for grp_user
create table if not exists grp_user_hist(grp_user_hist_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field",
user_id mediumint not null comment "FK to the users.user_id field",
action_type varchar(5) comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");