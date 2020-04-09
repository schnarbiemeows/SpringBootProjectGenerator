# groups table - basic members, premium members, admins, etc...
# each user can only belong to one group_type at a time
create table if not exists groups(grp_id mediumint not null auto_increment primary key,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description");

# groups_hist - history table for group
create table if not exists groups_hist(grp_hist_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to group.group_id",
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description",
action_type varchar(5) comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");