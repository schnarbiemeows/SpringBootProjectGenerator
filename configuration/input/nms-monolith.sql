drop view if exists workout_steps;
drop view if exists workout_cardio_vw;
drop view if exists quick_ingredient_list;
drop view if exists ingredient_type_mappings;
drop view if exists recipe_type_mappings;
drop view if exists manual_food_items_vw;
drop table if exists manual_food_items;
drop table if exists daily_journal;
drop table if exists body_measurements;
drop table if exists blood_pressure;
drop table if exists unsynced;
drop table if exists rda;
drop table if exists favorite_ingredients;
drop table if exists favorite_recipes;
drop table if exists favorite_brands;
drop table if exists favorite_spices;

drop table if exists graph_relation_indexes;
drop table if exists graph_relations;
drop table if exists user_calendar;
drop table if exists message_types;
drop table if exists messages;
drop table if exists notifications;
drop table if exists goal_event;
drop table if exists events_table;
drop table if exists period_ext;
drop table if exists periods;
drop table if exists period_type;
drop table if exists goal_groups;
drop table if exists goal_categories;
drop table if exists goals;
drop table if exists goal_types;

drop table if exists steps;
drop table if exists lift_set;
drop table if exists workout_lift;
drop table if exists weight_workout_type;
drop table if exists workouts;
drop table if exists lift_steps;
drop table if exists lift_lift_eqp;
drop table if exists lift_equip;
drop table if exists lift_muscle;
drop table if exists lifts;
drop table if exists exercise_type;
drop table if exists muscles;
drop table if exists muscle_groups;
drop table if exists cardio_type;

drop table if exists bldst_table;
drop table if exists daily_diet;
drop table if exists daily_diet_totals;
drop table if exists daily_weight;
drop table if exists daily_dietary_notes;

drop table if exists payment;
drop table if exists payment_type;

drop table if exists rec_equip_join;
drop table if exists rec_eq_type;
drop table if exists recipe_equip;
drop table if exists recipe_steps;
drop table if exists recipe_ingredients;
drop table if exists recipe_spices;
drop table if exists recipes;

drop table if exists recipe_type;
drop table if exists ingredients;
drop table if exists brand_ingr_type;
drop table if exists ingredient_types;
drop table if exists brands;
drop table if exists spices;
drop table if exists serving_type_options;
drop table if exists serving_type_ratios;
drop table if exists serving_types;

drop table if exists user_config;
drop table if exists rsrc_type;
drop table if exists resources;
drop table if exists roles_hist;
drop table if exists roles;
drop table if exists grp_user_hist;
drop table if exists grp_user;
drop table if exists groups_hist;
drop table if exists groups;
drop table if exists users_hist;
drop table if exists users_temp;
drop table if exists users;
drop table if exists password_reset;
drop table if exists action_type;
drop table if exists limitter_settings;
######################################################################
# account tables
######################################################################

##################
# rate limiter settings
#
# see the bottom for a list of insert statements
##################
create table if not exists limitter_settings(setting_id mediumint not null auto_increment primary key,
url varchar(1000) NOT NULL COMMENT 'URL',
domain varchar(1000) NOT NULL COMMENT 'domain',
permissions varchar(1000) NOT NULL COMMENT 'permissions',
totNumReqPerSec mediumint NOT NULL COMMENT 'total number of requests per second',
wndwForRateLmtInMs mediumint NOT NULL COMMENT 'total Window For Rate Limit In Milliseconds',
totalMaxBucketSize mediumint NOT NULL COMMENT 'totalMaxBucketSize',
ipTotNumReqPerSec mediumint NOT NULL COMMENT 'number Of Requests Per Second Per Ip Address',
ipWndwRtLmt mediumint NOT NULL COMMENT 'window For Rate Limit In Milliseconds Per Ip Address',
ipMaxWndw mediumint NOT NULL COMMENT 'max Bucket Size Per Ip Address',
environment varchar(10) comment 'what environment is this for?');
alter table limitter_settings
add constraint unique_lmst UNIQUE(url,domain);
create index lmst_env_idx on limitter_settings(environment);

create table if not exists graph_relation_indexes(graph_relation_index_id mediumint not null auto_increment primary key,
index_desc varchar(100) not null comment "should be table_name or (parent table) --> (child table)",
actv varchar(1) comment "is this relation active(Y or N)?");

# graph join table - used for things like:
# - the recipe_type hierarchical structure, which is used in the
# 	recipe type navbar when trying to find recipes
create table if not exists graph_relations(graph_relations_id mediumint not null auto_increment primary key,
parent_node mediumint comment "parent relation(for all tables that have a mediumint PK)",
child_node mediumint not null comment "child relation(for all tables that have a mediumint PK)",
edge_val varchar(100) comment "if we want to use weighted edges, or if we want each edge to have some value",
edge_fk mediumint comment "if we want to use a table record reference that contains the edge data",
graph_relation_index_id mediumint not null comment "child relation(for all tables that have a mediumint PK)",
foreign key GRI_FK1(graph_relation_index_id) references graph_relation_indexes(graph_relation_index_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this relation active(Y or N)?");
# create index graph_relations_idx on graph_relations(graph_relation_index_id); --> not needed because
# MySQL requires that foreign key columns be indexed; if you create a table with a foreign key constraint but no index on a given column, an index is created.

# action_type table - 2 purposes:
# 1. for the historical tables, tells what the action was
# that was performed on the record(action_type fields)
# 2. for the roles table - tells us what actions are allowable
create table if not exists action_type(action_type_id mediumint not null auto_increment primary key,
action_type_cde varchar(5) not null comment "action type code" ,
action_type_desc varchar(100) comment "action description",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists password_reset(password_reset_id int NOT NULL AUTO_INCREMENT primary key,
unique_id varchar(255) NOT NULL,
email_addr varchar(255) DEFAULT NULL,
created_date datetime DEFAULT NULL);

# users table - all users of the system have a record in this table
create table if not exists users(user_id mediumint NOT NULL AUTO_INCREMENT primary key,
username varchar(256) NOT NULL COMMENT 'unique username',
email varchar(300) NOT NULL COMMENT 'unique email address',
password varchar(256) NOT NULL COMMENT 'password should be encrypted',
age smallint DEFAULT NULL COMMENT 'age in years; we don''t want to store the user''s DOB',
lst_logd_in datetime DEFAULT NULL COMMENT 'when did the user last log in?',
phone varchar(10) DEFAULT NULL COMMENT 'user''s phone number, required for message notifications',
actv bit(1) NOT NULL DEFAULT b'1',
authorizations blob,
first_name varchar(255) DEFAULT NULL,
last_name varchar(255) DEFAULT NULL,
user_not_locked bit(1) NOT NULL DEFAULT b'1',
join_date datetime DEFAULT NULL,
last_login_date_display datetime DEFAULT NULL,
profile_image varchar(255) DEFAULT NULL,
roles varchar(255) DEFAULT NULL,
user_identifier varchar(255) DEFAULT NULL);

CREATE TABLE if not exists user_temp(user_temp_id int NOT NULL AUTO_INCREMENT primary key,
username varchar(255) DEFAULT NULL,
email varchar(255) DEFAULT NULL,
phone varchar(10) DEFAULT NULL,
first_name varchar(255) DEFAULT NULL,
last_name varchar(255) DEFAULT NULL,
age smallint DEFAULT NULL,
actv bit(1) NOT NULL,
authorizations blob,
user_not_locked bit(1) NOT NULL,
created_date datetime DEFAULT NULL,
join_date datetime DEFAULT NULL,
last_login_date datetime DEFAULT NULL,
last_login_date_display datetime DEFAULT NULL,
password varchar(255) DEFAULT NULL,
profile_image varchar(255) DEFAULT NULL,
roles varchar(255) DEFAULT NULL,
user_identifier varchar(255) DEFAULT NULL,
unique_id varchar(255) NOT NULL);

create table if not exists user_config(users_config_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKUC1(user_id) references users(user_id)
on update cascade on delete cascade,
property_key varchar(75) not null comment "name of the property",
property_value varchar(300) comment "value of the property");
create index user_config_idx on user_config(user_id);

# users_hist table - history of transactions on the users table
create table if not exists users_hist(users_hist_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKUH1(user_id) references users(user_id)
on update cascade on delete cascade,
username varchar(256) not null comment "username",
email varchar(300) not null comment "email address",
password varchar(256) not null comment "password should be encrypted",
age smallint comment "age in years; we don't want to store the user's DOB",
lst_logd_in	datetime comment "when did the user last log in?",
action_type_id mediumint not null comment "what action was performed on this record?",
foreign key FKUH2(action_type_id) references action_type(action_type_id)
on update cascade on delete cascade,
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id mediumint not null comment "who did this action?, FK to the users.user_id field",
foreign key FKUH3(evnt_oper_id) references users(user_id)
on update cascade on delete cascade);
create index users_hist_idx on users_hist(user_id);

# groups table - basic members, premium members, admins, etc...
# each user can only belong to one group_type at a time
create table if not exists groups(grp_id mediumint not null auto_increment primary key,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description");

# groups_hist - history table for group
create table if not exists groups_hist(grp_hist_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to groups.grp_id field",
foreign key FKGH1(grp_id) references groups(grp_id)
on update cascade on delete cascade,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description",
action_type_id mediumint not null comment "what action was performed on this record?",
foreign key FKGH2(action_type_id) references action_type(action_type_id)
on update cascade on delete cascade,
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id mediumint not null comment "who did this action?, FK to the users.user_id field",
foreign key FKGH3(evnt_oper_id) references users(user_id)
on update cascade on delete cascade);
create index groups_hist_idx on groups_hist(grp_id);

# grp_user - table to "connect" all users with all groups
create table if not exists grp_user(grp_user_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field",
foreign key FKGU1(grp_id) references groups(grp_id)
on update cascade on delete cascade,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKGU2(user_id) references users(user_id)
on update cascade on delete cascade);
create index grp_user_idx on grp_user(grp_id);
create index user_grp_idx on grp_user(user_id);

# grp_user_hist - history table for grp_user
create table if not exists grp_user_hist(grp_user_hist_id mediumint not null auto_increment primary key,
grp_user_id mediumint not null comment "FK to the grp_user.grp_user_id field",
foreign key FKGUH1(grp_user_id) references grp_user(grp_user_id)
on update cascade on delete cascade,
grp_id mediumint not null comment "FK to the groups.grp_id field",
foreign key FKGUH2(grp_id) references groups(grp_id)
on update cascade on delete cascade,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKGUH3(user_id) references users(user_id)
on update cascade on delete cascade,
action_type_id mediumint not null comment "what action was performed on this record?",
foreign key FKGUH4(action_type_id) references action_type(action_type_id)
on update cascade on delete cascade,
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id mediumint not null comment "who did this action?, FK to the users.user_id field",
foreign key FKGUH5(evnt_oper_id) references users(user_id)
on update cascade on delete cascade);
create index grp_user_hist_idx on grp_user_hist(grp_user_id);

# resource_type table - just for the resource table, what resource types there are, pages, tables, etc..
create table if not exists rsrc_type(rsrc_type_id mediumint not null auto_increment primary key,
rsrc_type varchar(30) not null comment "resource type code",
rsrc_type_desc varchar(100) comment "resource type description",
actv varchar(1) comment "is this record active(Y or N)?");

# resources table - a list of all the different resources(screens, tables, etc..) that there are
create table if not exists resources(rsrc_id mediumint not null auto_increment primary key,
rsrc_type_id mediumint not null comment "FK to the rsrc_type.rsrc_type_id field", foreign key FKRES1(rsrc_type_id) references rsrc_type(rsrc_type_id)
on update cascade on delete cascade,
rsrc_desc varchar(100) comment "description of the resource",
actv varchar(1) comment "is this record active(Y or N)?");

# roles table - table that shows what groups have what permissions(action_types) on what resources
create table if not exists roles(role_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field", foreign key FKROL1(grp_id) references groups(grp_id)
on update cascade on delete cascade,
rsrc_id mediumint not null comment "FK to the resources.rsrc_id field", foreign key FKROL2(rsrc_id) references resources(rsrc_id)
on update cascade on delete cascade,
action_type_id mediumint not null comment "FK to the action_type.action_type_id field", foreign key FKROL3(action_type_id) references action_type(action_type_id)
on update cascade on delete cascade);

# roles_hist table - history table for the roles table
create table if not exists roles_hist(role_hist_id mediumint not null auto_increment primary key,
role_id mediumint not null comment "FK to the roles.role_id field",
foreign key FKROLH1(role_id) references roles(role_id)
on update cascade on delete cascade,
grp_id mediumint not null comment "FK to the groups.grp_id field",
foreign key FKROLH2(grp_id) references groups(grp_id)
on update cascade on delete cascade,
rsrc_id mediumint not null comment "FK to the resources.rsrc_id field",
foreign key FKROLH3(rsrc_id) references resources(rsrc_id)
on update cascade on delete cascade,
action_type_id mediumint not null comment "what action was performed on this record?",
foreign key FKROLH4(action_type_id) references action_type(action_type_id)
on update cascade on delete cascade,
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id mediumint not null comment "who did this action?, FK to the users.user_id field",
foreign key FKROLH5(evnt_oper_id) references users(user_id)
on update cascade on delete cascade);


# favorite_ingredients
# ------------------------
create table if not exists favorite_ingredients(favorite_ingredient_id mediumint not null auto_increment primary key,
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field or the local_ingredients.ingr_id field",
is_local boolean default false comment "is the ingr_id FK a local ingr_id?",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");
create index favorite_ingredients_idx on favorite_ingredients(user_id);

# favorite_recipes
# -----------------
create table if not exists favorite_recipes(favorite_recipe_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field or the local_recipes.recipe_id field",
is_local boolean default false comment "is the recipe_id FK a local recipe_id?",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");
create index favorite_recipes_idx on favorite_recipes(user_id);

# favorite_brands
# ---------------
create table if not exists favorite_brands(favorite_brand_id mediumint not null auto_increment primary key,
brand_id mediumint not null comment "FK to the brands.brand_id field or the local_brands.brand_id field",
is_local boolean default false comment "is the brand_id FK a local brand_id?",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");
create index favorite_brands_idx on favorite_brands(user_id);

# favorite_spices
# ---------------
create table if not exists favorite_spices(favorite_spice_id mediumint not null auto_increment primary key,
spice_id mediumint not null comment "FK to the spices.spice_id field or the local_spices.spice_id field",
is_local boolean default false comment "is the spice_id FK a local spice_id?",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");
create index favorite_spices_idx on favorite_spices(user_id);

create table if not exists rda(rda_id mediumint not null auto_increment primary key,
rda_name varchar(100) comment "name of the recommended daily allowance",
rda_value decimal(6,2) not null comment "the amount of grams or milligrams per day",
user_id mediumint not null comment "FK to the user.user_id field",
foreign key FKRDA1(user_id) references users(user_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");
create index rda_userid_idx on rda(user_id);

######################################################################
# nms-ingr and nms-types tables
######################################################################

create table if not exists image_loc(image_loc_id mediumint not null auto_increment primary key,
img_desc varchar(700) not null comment "description of the image",
img_path varchar(300) comment "file path to the image");

create table if not exists serving_types(serv_type_id mediumint not null auto_increment primary key,
serv_type_cde varchar(10) not null comment "short code for the serving type",
serv_type_desc varchar(50) not null comment "longer description of the serving type",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKST3(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

# conversion factors between each different servings types
create table if not exists serving_type_ratios(serv_type_ratio_id mediumint not null auto_increment primary key,
serv_type_id_1 mediumint not null, foreign key FKST1(serv_type_id_1) references serving_types(serv_type_id)
on update cascade on delete cascade,
serv_type_id_2 mediumint not null, foreign key FKST2(serv_type_id_2) references serving_types(serv_type_id)
on update cascade on delete cascade,
ratio decimal(6,6) comment "conversion factor from serv_type_id_1 to serv_type_id_2");

create table if not exists serving_type_options(serv_type_opt_id mediumint not null auto_increment primary key,
serv_type_id mediumint not null, foreign key FKST5(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade,
menu_option mediumint not null, foreign key FKST6(menu_option) references serving_types(serv_type_id)
on update cascade on delete cascade);

# list of spices
create table if not exists spices(spice_id mediumint not null auto_increment primary key,
spice_name varchar(100) comment "name of the spice",
actv varchar(1) comment "is this record active(Y or N)?",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKSP1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade);


create table if not exists brands(brand_id mediumint not null auto_increment primary key,
brand_type varchar(1) comment "brand type(N = name, G = generic, S = store)",
brand_name varchar(100) comment "name of the brand",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKBR1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists ingredient_types(ingr_type_id mediumint not null auto_increment primary key,
prnt_ingr_type mediumint comment "FK to the ingredient_types.ingr_type_id field of this type's parent type",
ingr_type_desc varchar(100) not null comment "description of the ingredient type",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKINGT1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists brand_ingr_type(brand_ingr_type_id mediumint not null auto_increment primary key,
brand_id mediumint not null, foreign key FKBTIT1(brand_id) references brands(brand_id)
on update cascade on delete cascade,
ingr_type_id mediumint not null, foreign key FKBTIT2(ingr_type_id) references ingredient_types(ingr_type_id)
on update cascade on delete cascade,
prnt_ingr_type mediumint not null, foreign key FKBTIT3(prnt_ingr_type) references ingredient_types(ingr_type_id)
on update cascade on delete cascade);

create table if not exists ingredients(ingr_id mediumint not null auto_increment primary key,
ingr_desc varchar(256) comment "description of the ingredient",
ingr_type_id mediumint not null comment "FK to the ingredient_types.ingr_type_id field",
foreign key INGR1(ingr_type_id) references ingredient_types(ingr_type_id)
on update cascade on delete cascade,
brand_id mediumint not null comment "FK to the brands.brand_id field",
foreign key INGR2(brand_id) references brands(brand_id)
on update cascade on delete cascade,
serv_sz	decimal(6,2) not null comment "the size of an individual serving",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
foreign key INGR3(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade,
kcalories decimal(6,2) not null comment "total killocalories per serving",
tot_fat	decimal(6,2) not null comment "total fat in grams  per serving",
sat_fat	decimal(6,2) comment "total saturated fat in grams  per serving",
trans_fat decimal(6,2) comment "total trans fat in grams  per serving",
poly_fat decimal(6,2) comment "total polyunsaturated fat in grams per serving",
mono_fat decimal(6,2) comment "total monounsaturated fat in grams per serving",
choles decimal(6,2) not null comment "total cholesterol in milligrams per serving",
sodium mediumint not null comment "total sodium in milligrams per serving",
tot_carbs decimal(6,2) not null comment "total carbohydrates in grams per serving",
tot_fiber decimal(6,2) not null comment "total fiber in grams per serving",
tot_sugars decimal(6,2) not null comment "total sugars in grams per serving",
tot_protein decimal(6,2) not null comment "total protein in grams per serving",
glyc_indx decimal(6,2) comment "the glycemic index of this ingredient",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key INGR4(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists recipe_type(recipe_type_id mediumint not null auto_increment primary key,
recipe_type_desc varchar(100) comment "description of the recipe type",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists recipes(recipe_id mediumint not null auto_increment primary key,
recipe_name varchar(100) comment "name of the recipe",
recipe_type_id mediumint not null comment "FK to the recipe_type.recipe_type_id field",
foreign key REC_TYP1(recipe_type_id) references recipe_type(recipe_type_id)
on update cascade on delete cascade,
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field of this recipe's listing",
foreign key REC1(ingr_id) references ingredients(ingr_id)
on update cascade on delete cascade,
recipe_desc varchar(256) comment "description of the recipe",
recipe_link varchar(256) comment "hyperlink to the recipe",
num_srv decimal(6,2) comment "number of servings this recipe makes",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists recipe_spices(recipe_spice_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
foreign key RS1(recipe_id) references recipes(recipe_id)
on update cascade on delete cascade,
spice_id mediumint not null comment "FK to the spices.spice_id",
foreign key RS2(spice_id) references spices(spice_id)
on update cascade on delete cascade,
serv_sz	decimal(6,3) not null comment "the size of an individual serving",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
foreign key RS3(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists recipe_steps(recipe_step_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
foreign key FKRES1(recipe_id) references recipes(recipe_id)
on update cascade on delete cascade,
step_num smallint not null comment "the step order",
step_desc varchar(3000) comment "step description",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKRES2(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists rec_eq_type(rec_eq_type_id mediumint not null auto_increment primary key,
rec_eq_cde varchar(5) not null comment "short code for equipment type (APP = applicance, etc...)",
rec_eq_desc varchar(50) not null comment "short description of the equipment type",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists recipe_equip(recipe_equip_id mediumint not null auto_increment primary key,
rec_eq_type_id mediumint not null comment "FK to the rec_eq_type.rec_eq_type_id field",
foreign key FKRE1(rec_eq_type_id) references rec_eq_type(rec_eq_type_id)
on update cascade on delete cascade,
equip_desc varchar(75) comment "short description of the equipment",
equip_long_desc varchar(300) comment "long description of the equipment",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKRE2(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists rec_equip_join(rec_equip_join_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
foreign key FKREJ1(recipe_id) references recipes(recipe_id)
on update cascade on delete cascade,
recipe_equip_id mediumint not null comment "FK to the recipe_equip.recipe_equip_id field",
foreign key FKREJ2(recipe_equip_id) references recipe_equip(recipe_equip_id)
on update cascade on delete cascade);

create table if not exists recipe_ingredients(recipe_ingr_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
foreign key RI1(recipe_id) references recipes(recipe_id)
on update cascade on delete cascade,
rec_or_ingr_id mediumint not null comment "FK to either the ingredients.ingr_id field or the recipes.recipe_id field",
recipe_flg varchar(1) comment "is rec_or_ing_id another recipe(Y or N)?",
serv_sz	decimal(6,2) not null comment "the size of an individual serving",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
foreign key RI2(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

######################################################################
# nms-pay tables
######################################################################

create table if not exists payment_type(payment_type_id mediumint not null auto_increment primary key,
payment_type_cde varchar(10) not null comment "short code for the payment type",
payment_type_desc varchar(50) not null comment "longer description of the payment type",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKPAYT1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists payment(payment_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKPAY1(user_id) references users(user_id)
on update cascade on delete cascade,
payment_type_id mediumint not null comment "FK to the payment_type.payment_type_id field",
foreign key FKPAY2(payment_type_id) references payment_type(payment_type_id),
payment_amt decimal(6,2) not null comment "payment amount",
payment_desc varchar(100) comment "payment description",
actv varchar(1) comment "is this record active(Y or N)?");

######################################################################
# nms-daily-diet tables
######################################################################

create table if not exists bldst_table(bldst_table_id mediumint not null auto_increment primary key,
bldst_cde varchar(3) not null comment "B = breakfast, L = lunch, etc...",
bldst_desc varchar(30) not null comment "breakfast,lunch, etc...",
actv varchar(1) comment "is this record active(Y or N)?");
#insert into bldst_table(bldst_cde,bldst_desc,actv) values("B","Breakfast","Y");
#insert into bldst_table(bldst_cde,bldst_desc,actv) values("L","Lunch","Y");
#insert into bldst_table(bldst_cde,bldst_desc,actv) values("D","Dinner","Y");
#insert into bldst_table(bldst_cde,bldst_desc,actv) values("S","Snack","Y");
#insert into bldst_table(bldst_cde,bldst_desc,actv) values("T","Total","Y");

create table if not exists daily_diet(daily_total_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDAYD1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
ingr_id mediumint not null comment "FK to ingredients.ingr_id or local_ingredients.ingr_id field",
is_recipe boolean comment "is this a recipe(Y or N)?",
is_local boolean comment "is this a local recipe or ingredient?",
bldst_id mediumint comment "FK to the bldst_table.bldst_table_id field",
foreign key FKDAYD3(bldst_id) references bldst_table(bldst_table_id)
on update cascade on delete cascade,
num_srv decimal(6,2) not null comment "the number of servings of this item eaten",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
foreign key LRI2(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade,
time_eaten time comment "at what time of the day was this item eaten");
create index daily_diet_idx on daily_diet(user_id);


create table if not exists daily_diet_totals(daily_diet_total_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDDT1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
bldst_id mediumint comment "FK to the bldst_table.bldst_table_id field",
foreign key FKDDT2(bldst_id) references bldst_table(bldst_table_id)
on update cascade on delete cascade,
kcalories decimal(6,2) not null comment "total killocalories",
tot_fat	decimal(6,2) not null comment "total fat in grams",
sat_fat	decimal(6,2) comment "total saturated fat in grams",
trans_fat decimal(6,2) comment "total trans fat in grams",
poly_fat decimal(6,2) comment "total polyunsaturated fat in grams",
mono_fat decimal(6,2) comment "total monounsaturated fat in grams",
choles decimal(6,2) not null comment "total cholesterol in milligrams",
sodium mediumint not null comment "total sodium in milligrams",
tot_carbs decimal(6,2) not null comment "total carbohydrates in grams",
tot_fiber decimal(6,2) not null comment "total fiber in grams",
tot_sugars decimal(6,2) not null comment "total sugars in grams",
tot_protein decimal(6,2) not null comment "total protein in grams");
create index daily_diet_totals_idx on daily_diet_totals(user_id);
alter table daily_diet_totals
add constraint unique_ddt UNIQUE(user_id,calendar_date,bldst_id);

create table if not exists daily_weight(daily_weight_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDW1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date date not null comment "the calendar date(date only, no time)",
weight decimal(6,2) not null comment "person's weight on this given day");
create index daily_weight_idx on daily_weight(user_id);
create index dw_user_cal_idx on daily_weight(user_id,calendar_date);
create unique index dw_unique_indx on daily_weight(user_id,calendar_date);
# daily dietary notes table - a list of notes about your diet
create table if not exists daily_dietary_notes(ddn_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDDN1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
daily_notes varchar(3000) comment "daily notes about your diet");
create index daily_dietary_idx on daily_dietary_notes(user_id);
alter table daily_dietary_notes
add constraint unique_ddn UNIQUE(user_id,calendar_date);

# daily dietary exclusions table - a list of days that we want to exclude when computing
# or considering daily dietary aggregates(stuff like cheat days OR days that we are using
# as templates!
create table if not exists daily_dietary_exclusions(daily_dietary_exclusion_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDDE1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)");
alter table daily_dietary_exclusions
add constraint unique_dde UNIQUE(user_id,calendar_date);

# dietary templates table
create table if not exists dietary_templates(dietary_template_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDT1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
template_name varchar(100) comment "name of the template");
create index dietary_template_idx on dietary_templates(user_id);

######################################################################
# nms-exer tables
######################################################################

create table if not exists muscle_groups(muscle_group_id mediumint not null auto_increment primary key,
muscle_grp_name varchar(100) not null comment "description of the muscle group",
actv varchar(1) default "Y" comment "is this record active(Y or N)?");

create table if not exists muscles(muscle_id mediumint not null auto_increment primary key,
muscle_group_id mediumint not null comment "FK to the muscle_groups.muscle_group_id field",
foreign key FKMUSC1(muscle_group_id) references muscle_groups(muscle_group_id)
on update cascade on delete cascade,
muscle_name varchar(75) not null comment "description of the ingredient type",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKMUSC2(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) default "Y" comment "is this record active(Y or N)?");

create table if not exists exercise_type(exercise_type_id mediumint not null auto_increment primary key,
prnt_exercise_type mediumint comment "FK to the exercise_type.exercise_type_id field of this type's parent type",
exercise_type_desc varchar(100) not null comment "description of the exercise type",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKEXTYP1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");
insert into exercise_type(exercise_type_desc,actv) values("Cardio","Y");
insert into exercise_type(exercise_type_desc,actv) values("Strength Training","Y");
insert into exercise_type(exercise_type_desc,actv) values("Low Impact","Y");

create table if not exists lifts(lift_id mediumint not null auto_increment primary key,
lift_desc varchar(100) not null comment "lift description",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKLIFTS2(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?",
muscle_group_id mediumint comment "FK to the muscle_group table",
foreign key FKLMG1(muscle_group_id) references muscle_groups(muscle_group_id)
ON DELETE CASCADE ON UPDATE CASCADE
);

create table if not exists weight_workout_type(weight_workout_type_id mediumint not null auto_increment primary key,
workout_id mediumint not null comment "FK to the workouts.workout_id field",
foreign key FKWRKREC4(workout_id) references workouts(workout_id)
on update cascade on delete cascade,
muscle_group_id mediumint comment "FK to the muscle_group table",
foreign key FKLMG2(muscle_group_id) references muscle_groups(muscle_group_id)
ON DELETE CASCADE ON UPDATE CASCADE);

create table if not exists lift_muscle(lift_muscle_id mediumint not null auto_increment primary key,
lift_id mediumint not null comment "FK to the lifts.lift_id field",
foreign key FKLIFTS3(lift_id) references lifts(lift_id)
on update cascade on delete cascade,
muscle_id mediumint not null comment "FK to the muscles.muscle_id field",
foreign key FKLIFTS4(muscle_id) references muscles(muscle_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists lift_steps(lift_step_id mediumint not null auto_increment primary key,
lift_id mediumint not null comment "FK to the lifts.lift_id field",
foreign key FKLIST1(lift_id) references lifts(lift_id)
on update cascade on delete cascade,
step_num smallint not null comment "the step order",
step_desc varchar(300) comment "step description",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKLIST2(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade);

create table if not exists lift_equip(lift_equip_id mediumint not null auto_increment primary key,
equip_desc varchar(75) comment "short description of the equipment",
equip_long_desc varchar(300) comment "long description of the equipment",
image_loc mediumint comment "FK to the image_loc.image_loc_id field",
foreign key FKLIEQ1(image_loc) references image_loc(image_loc_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists lift_lift_eqp(lift_lift_eqp_id mediumint not null auto_increment primary key,
lift_id mediumint not null comment "FK to the lifts.lift_id field",
foreign key FKLILIEQ1(lift_id) references lifts(lift_id)
on update cascade on delete cascade,
lift_equip_id mediumint not null comment "FK to the lift_equip.lift_equip_id field",
foreign key FKLILIEQ2(lift_equip_id) references lift_equip(lift_equip_id)
on update cascade on delete cascade);

create table if not exists cardio_type(cardio_type_id mediumint not null auto_increment primary key,
description varchar(100) comment "what type of cardio is it?",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists workouts(workout_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKWORK1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
exercise_type_id mediumint comment "FK to the exercise_type.exercise_type_id field",
foreign key FKWORK2(exercise_type_id) references exercise_type(exercise_type_id)
on update cascade on delete cascade,
duration mediumint comment "length of workout, in minutes",
rating decimal(2,1) comment "user's statisfaction with their workout 0.0 - 10.0 rating",
notes varchar(500) comment "any particular observations on this workout?",
actv varchar(1) comment "is this record active(Y or N)?");
create index workouts_idx on workouts(user_id,actv);

create table if not exists workout_cardio(workout_cardio_id mediumint not null auto_increment primary key,
workout_id mediumint not null comment "FK to the workouts.workout_id field",
foreign key FKWRKCARD1(workout_id) references workouts(workout_id)
on update cascade on delete cascade,
cardio_type_id mediumint comment "FK to the cardio_type.cardio_type_id field",
foreign key FKWRKCARD2(cardio_type_id) references cardio_type(cardio_type_id)
on update cascade on delete cascade);
create index workout_cardio_idx on workout_cardio(workout_id);

create table if not exists workout_lift(workout_lift_id mediumint not null auto_increment primary key,
workout_id mediumint not null comment "FK to the workouts.workout_id field",
foreign key FKWRKREC3(workout_id) references workouts(workout_id)
on update cascade on delete cascade,
lift_id mediumint comment "FK to the lifts.lift_id field",
foreign key FKWRKREC4(lift_id) references lifts(lift_id)
on update cascade on delete cascade);
create index workout_lift_idx on workout_lift(workout_id);

create table if not exists lift_set(lift_set_id mediumint not null auto_increment primary key,
workout_lift_id mediumint not null comment "FK to the workouts.workout_id field",
foreign key FKLFTSETREC1(workout_lift_id) references workout_lift(workout_lift_id)
on update cascade on delete cascade,
weight decimal(4,1) comment "weight",
reps smallint comment "number of reps");
create index lift_set_idx on lift_set(workout_lift_id);

create table if not exists steps(step_id mediumint not null auto_increment primary key,
workout_id mediumint not null comment "FK to the workouts.workout_id field",
foreign key FKWRKREC1(workout_id) references workouts(workout_id)
on update cascade on delete cascade,
steps mediumint comment "how many steps",
actv varchar(1) comment "is this record active(Y or N)?"
);

create or replace view workout_steps as
select w.workout_id, w.user_id, w.calendar_date, s.steps
from workouts w, steps s
where w.workout_id = s.workout_id
order by w.calendar_date;
select * from workout_steps;

create or replace view workout_cardio_vw as
select w.workout_id, w.user_id, w.calendar_date, ct.description
from workouts w, workout_cardio wc, cardio_type ct
where w.workout_id = wc.workout_id
and wc.cardio_type_id = ct.cardio_type_id
order by w.calendar_date;
######################################################################
# goals and messages tables
######################################################################

-- goal types, drop down table
create table if not exists goal_types(goal_type_id mediumint not null auto_increment primary key,
goal_type_cde varchar(3) not null comment "WEI(weight), EXR(exercise),DIE(diet), FIN(financial)",
goal_type_desc varchar(20) not null comment "description of the goal_type_cde");

-- message types, drop down table
create table if not exists message_types(message_type_id mediumint not null auto_increment primary key,
message_type_cde varchar(1) not null comment "D(dashboard), C(Calendar),T(text message), E(email message)",
message_type_desc varchar(20) not null comment "description of the message_type_cde");

-- period types, drop down table
create table if not exists period_type(period_type_id mediumint not null auto_increment primary key,
period_type_cde varchar(1) not null comment "O(one-time),Y(yearly),Q(quarterly),S(semi-yearly),M(monthly),W(weekly),D(daily),2(twice a day),4(4 times a day),H(hourly)",
period_type_desc varchar(20) not null comment "description of the period_type_cde");

-- one-time or recurring periodic specs
create table if not exists periods(period_id mediumint not null auto_increment primary key,
period_type_id mediumint not null comment "FK to the period_type.period_type_id field",
foreign key FKPER1(period_type_id) references period_type(period_type_id)
on update cascade on delete cascade,
one_time_date datetime comment "for the O(one-time) option, calendar date and time of event",
day_of_year tinyint comment "for the Y(yearly) option 0-365 day of the year",
day_of_month tinyint comment "for the M(monthly) option, the day of the month",
day_of_week varchar(2) comment "day of the week, M,Tu,W,Th,F,Sa,Su",
actv varchar(1) comment "is this record active(Y or N)?");

-- for the 2, 4, Q, and S period_types, this table stores records specifying the exact dates
-- and/or times for the actual events_table
create table if not exists period_ext(period_ext_id mediumint not null auto_increment primary key,
period_id mediumint not null comment "FK to the periods.period_id field",
foreign key FKPER1(period_id) references periods(period_id)
on update cascade on delete cascade,
specific_date date comment "specific date",
specific_time time comment "sepcific time");

-- core events_table table
create table if not exists events_table(event_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKEVNT1(user_id) references users(user_id)
on update cascade on delete cascade,
event_name varchar(75) not null comment "short name of the event",
event_desc varchar(300) comment "longer description of the event",
period_id mediumint not null comment "FK to the periods.period_id field",
foreign key FKEVNT2(period_id) references periods(period_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");
create index events_table_idx on events_table(user_id,actv);

-- notifications table: go through this table every hour to send off notifications
create table if not exists notifications(notification_id mediumint not null auto_increment primary key,
event_id mediumint not null comment "FK to the events_table.event_id field",
foreign key FKNOTF1(event_id) references events_table(event_id)
on update cascade on delete cascade,
notif_time time not null comment "time of day to send notification",
next_notif_date datetime comment "(null if there is none, or set to actv = False when done, or move to history table)",
attempts tinyint not null comment "how many times did we attempt to send out the notifcation?",
delivered varchar(1) not null default "N" comment "was this message delivered?");

-- messages table, the messages associated with an event
create table if not exists messages(message_id mediumint not null auto_increment primary key,
event_id mediumint not null comment "FK to the events_table.event_id field",
foreign key FKMESS1(event_id) references events_table(event_id)
on update cascade on delete cascade,
message_type_id mediumint not null comment "FK to the message_types.message_type_id field",
foreign key FKMESS2(message_type_id) references message_types(message_type_id)
on update cascade on delete cascade,
message_txt varchar(1024) not null comment "message text");

-- calendar table for displaying events on a calendar
create table if not exists user_calendar(user_calendar_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKCLDR1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date date not null comment "calendar date",
calendar_time time comment "calendar time",
event_id mediumint not null comment "FK to the events_table.event_id field",
foreign key FKCLDR2(event_id) references events_table(event_id)
on update cascade on delete cascade);
create index user_calendar_idx on user_calendar(user_id);

-- goal categories: we will provide set goals for the user, which can be
-- tracked and messages set when the goals are achieved. OR they can chose
-- the Custom, non-trackable goal if they just want a goal that will appear on
-- their dashboard.
create table if not exists goal_categories(gc_id mediumint not null auto_increment primary key,
goal_type_id mediumint not null comment "FK to the goal_types.goal_type_id field",
foreign key FKGOCAT1(goal_type_id) references goal_types(goal_type_id)
on update cascade on delete cascade,
gc_desc varchar(100) not null comment "description of the goal category",
actv varchar(1) comment "is this record active(Y or N)?");

-- core goals table
create table if not exists goals(goal_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKGOAL1(user_id) references users(user_id)
on update cascade on delete cascade,
goal_name varchar(250) not null comment "short name of the goal",
gc_id mediumint not null comment "FK to the goal_categories.gc_id field",
foreign key FKGOAL3(gc_id) references goal_categories(gc_id)
on update cascade on delete cascade,
comparator varchar(3) comment "eq = equals, LT = less than, LEQ = less than or equals, GT, GTE, etc...",
comp_fld varchar(20) comment "what field(weight, calories) or stat are we comparing to?",
num_times smallint default 1 comment "how many times do we need to satisfy the comparison for the goal to be reached?",
times_met smallint default 0 comment "how many times have we currently satisfied the comparison?",
conseq varchar(1) comment "Y or N, do we have to meet this comparison num_times in a row, or just num_times total times?",
renew varchar(1) comment "Y or N, should we renew this goal once it's met?",
achieved varchar(1) not null default "N" comment "Y or N, have we achieved this goal?",
actv varchar(1) default "Y" comment "is this record active(Y or N)?");
create index goals_idx on goals(user_id,actv);

create table if not exists goal_groups(goal_group_id mediumint not null auto_increment primary key,
goal_id_1 mediumint not null comment "FK to the goals.goal_id field",
foreign key FKGOGR1(goal_id_1) references goals(goal_id)
on update cascade on delete cascade,
goal_id_2 mediumint not null comment "FK to the goals.goal_id field",
foreign key FKGOGR2(goal_id_2) references goals(goal_id)
on update cascade on delete cascade,
relation varchar(3) comment "AND or OR, how are these 2 goals related?");

create table if not exists goal_event(goal_event_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKGOEV1(user_id) references users(user_id)
on update cascade on delete cascade,
goal_id mediumint not null comment "FK to the goals.goal_id field",
foreign key FKGOEV2(goal_id) references goals(goal_id)
on update cascade on delete cascade,
event_id mediumint not null comment "FK to the events_table.event_id field",
foreign key FKGOEV3(event_id) references events_table(event_id)
on update cascade on delete cascade);
create index goal_ev_idx on goal_event(event_id);
create index goal_ev_idx2 on goal_event(user_id);

create table if not exists unsynced(unsynced_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key UDAYD1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)");
create index unsynced_idx on unsynced(user_id,calendar_date);

create table if not exists blood_pressure(blood_pressure_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key BLPR1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date date not null comment "the calendar date(date only, no time)",
systolic mediumint comment "systolic pressure(mm Hg)",
diastolic mediumint comment "diastolic pressure(mm Hg)",
pulse mediumint comment "pulse",
actv varchar(1) comment "is this record active(Y or N)?");
create index blood_pressure_idx on blood_pressure(user_id,actv);

drop view if exists recipe_type_mappings;
create view recipe_type_mappings as
select x.id, x.parent_id, x.parent_desc, x.child_id
from
(
	select q.id, q.parent_id, q.parent_desc, GROUP_CONCAT(q.child_id order by q.child_id asc) as child_id
	from
	(
		select a.graph_relations_id as id,
		case
			when a.parent_node is null then 0
            else a.parent_node
		end as parent_id,
		b.recipe_type_desc as parent_desc,
		a.child_node as child_id
		from graph_relations a
		left join recipe_type b on a.parent_node = b.recipe_type_id,
		recipe_type c
		where
		a.child_node = c.recipe_type_id
		and
		a.graph_relation_index_id=1
		group by a.parent_node, a.child_node
		order by a.parent_node, a.child_node
	) q
	group by q.parent_id
	UNION
	select r.id, r.parent_id, r.parent_desc, r.child_id
	from
	(
		select a.graph_relations_id as id,
		a.child_node as parent_id,
		b.recipe_type_desc as parent_desc,
		null as child_id
		from graph_relations a, recipe_type b
		where a.child_node = b.recipe_type_id
		and
		a.child_node NOT IN (select distinct parent_node from graph_relations where graph_relation_index_id=1 and parent_node is not null)
		and a.graph_relation_index_id=1
		order by a.child_node
	) r
) x
order by x.parent_id;

	create view ingredient_type_mappings as
	select x.id, x.parent_id, x.parent_desc, x.child_id
	from
	(
	select q.id, q.parent_id, q.parent_desc, GROUP_CONCAT(q.child_id order by q.child_id asc) as child_id
	from
	(
	select a.graph_relations_id as id,
	a.parent_node as parent_id,
	b.ingr_type_desc as parent_desc,
	a.child_node as child_id
	from graph_relations a
	left join ingredient_types b on a.parent_node = b.ingr_type_id,
	ingredient_types c
	where
	a.child_node = c.ingr_type_id
	and
	a.graph_relation_index_id=2
	group by a.parent_node, a.child_node
	order by a.parent_node, a.child_node
	) q
	group by q.parent_id
	UNION
	select r.id, r.parent_id, r.parent_desc, r.child_id
	from
	(
	select a.graph_relations_id as id,
	a.child_node as parent_id,
	b.ingr_type_desc as parent_desc,
	null as child_id
	from graph_relations a, ingredient_types b
	where a.child_node = b.ingr_type_id
	and
	a.child_node NOT IN (select distinct parent_node from graph_relations where graph_relation_index_id=2 and parent_node is not null)
	and a.graph_relation_index_id=2
	order by a.child_node
	) r
) x
order by x.parent_id;

drop view if exists quick_ingredient_list;
create view quick_ingredient_list as
select
innertable.id,
innertable.meal_type,
innertable.ingredient_id,
innertable.ingredient_desc,
innertable.local,
innertable.serv_type_id,
innertable.serv_type_cde,
innertable.quantity
from
(
	select
	qpq.quick_page_serving_qty_id as id,
	qpi.bldst_id as meal_type,
	i.ingr_id as ingredient_id,
	i.ingr_desc as ingredient_desc,
	false as local,
	st.serv_type_id as serv_type_id,
	st.serv_type_cde as serv_type_cde,
	qpq.qty as quantity
	from
	ingredients	i,
	quick_page_items qpi,
	quick_page_servings qps,
	quick_page_serving_qtys qpq,
	serving_types st
	where
	qpi.is_local = false
	and
	i.ingr_id = qpi.ingredient_id
	and
	qpi.quick_page_item_id = qps.quick_page_item_id
	and
	qps.quick_page_serving_id = qpq.quick_page_serving_id
	and
	qps.serv_type_id = st.serv_type_id
	UNION
	select
	qpq.quick_page_serving_qty_id as id,
	qpi.bldst_id as meal_type,
	li.ingr_id as ingredient_id,
	li.ingr_desc as ingredient_desc,
	true as local,
	st.serv_type_id as serv_type_id,
	st.serv_type_cde as serv_type_cde,
	qpq.qty as quantity
	from
	local_ingredients	li,
	quick_page_items qpi,
	quick_page_servings qps,
	quick_page_serving_qtys qpq,
	serving_types st
	where
	qpi.is_local = true
	and
	li.ingr_id = qpi.ingredient_id
	and
	qpi.quick_page_item_id = qps.quick_page_item_id
	and
	qps.quick_page_serving_id = qpq.quick_page_serving_id
	and
	qps.serv_type_id = st.serv_type_id
) innertable
order by meal_type,ingredient_id,serv_type_id;

create or replace view workouts_vw as
select w.workout_id, w.user_id, w.calendar_date, w.duration, w.rating, mg.muscle_grp_name
from workouts w, weight_workout_type wwt, muscle_groups mg
where w.workout_id = wwt.workout_id
and wwt.muscle_group_id = mg.muscle_group_id
and muscle_grp_name in('legs','Chest-Triceps','Back-Biceps','Shoulders-Traps-Forearms')
and w.actv='Y'
UNION
select w.workout_id, w.user_id, w.calendar_date, w.duration, w.rating, 'Cardio'
from workouts w
where w.exercise_type_id=1
and w.actv='Y'
order by calendar_date;

create table if not exists body_measurements(body_meas_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key BODM1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
calf_l decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
calf_r decimal(4,2) not null comment "right calf in inches, to the closest 1/4 inch",
thigh_l decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
thigh_r decimal(4,2) not null comment "right calf in inches, to the closest 1/4 inch",
waist decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
chest decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
bicep_l decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
bicep_r decimal(4,2) not null comment "right calf in inches, to the closest 1/4 inch",
forearm_l decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
forearm_r decimal(4,2) not null comment "right calf in inches, to the closest 1/4 inch",
shoulders decimal(4,2) not null comment "left calf in inches, to the closest 1/4 inch",
actv varchar(1) comment "is this record active(Y or N)?");
create index body_meas_idx on body_measurements(user_id,calendar_date);

create or replace view serving_type_options_vw as
select sto.serv_type_opt_id, sto.serv_type_id, sto.menu_option, st.serv_type_cde
from serving_type_options sto, serving_types st
where st.serv_type_id = sto.menu_option;

######################################################################
# views for the daily dietary totals
# to replace the daily_dietary_totals table along with the laborious
# buggy code that recalculates these records every time an ingredient
# or recipe gets changed or deleted
######################################################################


create or replace view daily_totals_inner_vw as
select USER_ID, BLDST_ID, CAL_DATE,
sum(CALORIES) as CALORIES, sum(TOT_FAT) as TOT_FAT, sum(TOT_CARBS) as TOT_CARBS,
sum(TOT_PROTEIN) as TOT_PROTEIN
from
(
	select USER_ID, BLDST_ID, CAL_DATE, ingr_desc, DD_srv_sz, DD_srv_type, I_srv_sz, I_srv_type,
	RATIO, ROUND(CALORIES*RATIO*DD_srv_sz/I_srv_sz,2) as CALORIES,
	ROUND(TOT_FAT*RATIO*DD_srv_sz/I_srv_sz,2) as TOT_FAT,
	ROUND(TOT_CARBS*RATIO*DD_srv_sz/I_srv_sz,2) as TOT_CARBS,
	ROUND(TOT_PROTEIN*RATIO*DD_srv_sz/I_srv_sz,2) as TOT_PROTEIN
	from
	(
		select dd.user_id as USER_ID, dd.bldst_id as BLDST_ID,
		dd.calendar_date as CAL_DATE, li.ingr_desc, dd.num_srv as DD_srv_sz, dd.serv_type_id as DD_srv_type, li.serv_sz as I_srv_sz, li.serv_type_id as I_srv_type, str.ratio as RATIO,
		li.kcalories as CALORIES, li.tot_fat as TOT_FAT, li.tot_carbs as TOT_CARBS, li.tot_protein as TOT_PROTEIN
		from
		daily_diet dd,
		local_recipes lr,
		serving_type_ratios str,
		local_ingredients li
		where
		dd.is_local = 1 and dd.is_recipe = 1
		and dd.ingr_id = lr.recipe_id
		and lr.ingr_id = li.ingr_id
		and str.serv_type_id_1 = dd.serv_type_id
		and str.serv_type_id_2 = li.serv_type_id

		UNION ALL

		select dd.user_id as USER_ID, dd.bldst_id as BLDST_ID,
		dd.calendar_date as CAL_DATE, i.ingr_desc, dd.num_srv as DD_srv_sz, dd.serv_type_id as DD_srv_type, i.serv_sz as I_srv_sz, i.serv_type_id as I_srv_type, str.ratio as RATIO,
		i.kcalories as CALORIES, i.tot_fat as TOT_FAT, i.tot_carbs as TOT_CARBS, i.tot_protein as TOT_PROTEIN
		from
		daily_diet dd,
		recipes r,
		serving_type_ratios str,
		ingredients i
		where
		dd.is_local = 0 and dd.is_recipe = 1
		and dd.ingr_id = r.recipe_id
		and r.ingr_id = i.ingr_id
		and str.serv_type_id_1 = dd.serv_type_id
		and str.serv_type_id_2 = i.serv_type_id

		UNION ALL

		select dd.user_id as USER_ID, dd.bldst_id as BLDST_ID,
		dd.calendar_date as CAL_DATE, li.ingr_desc, dd.num_srv as DD_srv_sz, dd.serv_type_id as DD_srv_type, li.serv_sz as I_srv_sz, li.serv_type_id as I_srv_type, str.ratio as RATIO,
		li.kcalories as CALORIES, li.tot_fat as TOT_FAT, li.tot_carbs as TOT_CARBS, li.tot_protein as TOT_PROTEIN
		from
		daily_diet dd,
		serving_type_ratios str,
		local_ingredients li
		where
		dd.is_local = 1 and dd.is_recipe = 0
		and dd.ingr_id = li.ingr_id
		and str.serv_type_id_1 = dd.serv_type_id
		and str.serv_type_id_2 = li.serv_type_id

		UNION ALL

		select dd.user_id as USER_ID, dd.bldst_id as BLDST_ID,
		dd.calendar_date as CAL_DATE, i.ingr_desc, dd.num_srv as DD_srv_sz, dd.serv_type_id as DD_srv_type, i.serv_sz as I_srv_sz, i.serv_type_id as I_srv_type, str.ratio as RATIO,
		i.kcalories as CALORIES, i.tot_fat as TOT_FAT, i.tot_carbs as TOT_CARBS, i.tot_protein as TOT_PROTEIN
		from
		daily_diet dd,
		serving_type_ratios str,
		ingredients i
		where
		dd.is_local = 0 and dd.is_recipe = 0
		and dd.ingr_id = i.ingr_id
		and str.serv_type_id_1 = dd.serv_type_id
		and str.serv_type_id_2 = i.serv_type_id
		## and dd.calendar_date = '2024-09-17' and dd.user_id=1
	) q
) Z
group by USER_ID, CAL_DATE, BLDST_ID
order by USER_ID, CAL_DATE desc, BLDST_ID;

create or replace view daily_totals_outer_vw as
select vw.USER_ID, 9 as BLDST_ID, vw.CAL_DATE,
sum(vw.CALORIES) as CALORIES, sum(vw.TOT_FAT) as TOT_FAT, sum(vw.TOT_CARBS) as TOT_CARBS,
sum(vw.TOT_PROTEIN) as TOT_PROTEIN, dw.weight
from daily_totals_inner_vw vw left join daily_weight dw
on
vw.USER_ID=1
and vw.user_id = dw.user_id
and vw.CAL_DATE = dw.calendar_date
group by USER_ID, CAL_DATE
order by USER_ID, CAL_DATE desc;

create table daily_journal(daily_journal_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key DAJO1(user_id) references users(user_id)
on update cascade on delete cascade,
calendar_date datetime not null comment "the calendar date(date only, no time)",
note varchar(8000) comment "daily journal entry",
actv varchar(1) comment "is this record active(Y or N)?");
create index daily_journal_idx on daily_journal(user_id,calendar_date);

create table if not exists manual_food_items(manual_food_item_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
foreign key FKDAYD11(user_id) references users(user_id)
on update cascade on delete cascade,
ingr_id mediumint not null comment "FK to ingredients.ingr_id or local_ingredients.ingr_id field",
is_recipe boolean comment "is this a recipe(Y or N)?",
is_local boolean comment "is this a local recipe or ingredient?",
bldst_id mediumint comment "FK to the bldst_table.bldst_table_id field",
foreign key FKDAYD31(bldst_id) references bldst_table(bldst_table_id)
on update cascade on delete cascade,
num_srv decimal(6,2) not null comment "the number of servings of this item eaten",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
foreign key LRI21(serv_type_id) references serving_types(serv_type_id)
on update cascade on delete cascade);
create index manual_food_items_idx on manual_food_items(user_id);

create or replace view manual_food_items_vw as
select q.manual_food_item_id, q.user_id, q.bldst_id, q.ingr_id, q.ingr_desc, q.total, q.is_recipe, q.is_local, q.num_srv,
st.serv_type_id, st.serv_type_cde from
(
select mfi.manual_food_item_id, mfi.user_id, mfi.bldst_id, mfi.ingr_id, ingr.ingr_desc, 1 as total, mfi.num_srv,
mfi.is_recipe, mfi.is_local, mfi.serv_type_id
from manual_food_items mfi
join ingredients ingr on mfi.ingr_id = ingr.ingr_id
where mfi.is_local=0 and mfi.is_recipe=0
group by mfi.bldst_id, mfi.ingr_id, mfi.serv_type_id, mfi.num_srv, mfi.is_recipe, mfi.is_local
UNION
select mfi.manual_food_item_id, mfi.user_id, mfi.bldst_id, mfi.ingr_id, ingr.ingr_desc, 1 as total, mfi.num_srv,
mfi.is_recipe, mfi.is_local, mfi.serv_type_id
from manual_food_items mfi
join local_ingredients ingr on mfi.ingr_id = ingr.ingr_id
where mfi.is_local=1 and mfi.is_recipe=0
## and mfi.calendar_date > date('2024-11-28 00:00:00')
group by mfi.bldst_id, mfi.ingr_id, mfi.serv_type_id, mfi.num_srv, mfi.is_recipe, mfi.is_local
UNION
select mfi.manual_food_item_id, mfi.user_id, mfi.bldst_id, mfi.ingr_id, ingr.recipe_name, 1 as total, mfi.num_srv,
mfi.is_recipe, mfi.is_local, mfi.serv_type_id
from manual_food_items mfi
join recipes ingr on mfi.ingr_id = ingr.recipe_id
where mfi.is_local=0 and mfi.is_recipe=1
group by mfi.bldst_id, mfi.ingr_id, mfi.serv_type_id, mfi.num_srv, mfi.is_recipe, mfi.is_local
UNION
select mfi.manual_food_item_id, mfi.user_id, mfi.bldst_id, mfi.ingr_id, ingr.recipe_name, 1 as total, mfi.num_srv,
mfi.is_recipe, mfi.is_local, mfi.serv_type_id
from manual_food_items mfi
join local_recipes ingr on mfi.ingr_id = ingr.recipe_id
where mfi.is_local=1 and mfi.is_recipe=1
group by mfi.bldst_id, mfi.ingr_id, mfi.serv_type_id, mfi.num_srv, mfi.is_recipe, mfi.is_local
) q,
serving_types st
where q.serv_type_id = st.serv_type_id
order by q.user_id, q.bldst_id, q.ingr_id, st.serv_type_cde, q.num_srv  ;

