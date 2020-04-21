drop table if exists users;
drop table if exists users_hist;
drop table if exists groups;
drop table if exists groups_hist;
drop table if exists grp_user;
drop table if exists grp_user_hist;
drop table if exists roles;
drop table if exists roles_hist;
drop table if exists action_type;
drop table if exists rsrc_type;
drop table if exists resources;

drop table if exists brands;
drop table if exists products;
drop table if exists recipe_ingredients;
drop table if exists recipes;
drop table if exists ingredient_types;
drop table if exists serving_types;
drop table if exists serving_type_ratios;
drop table if exists ingredients;

drop table if exists local_brands;
drop table if exists local_products;
drop table if exists local_recipe_ingredients;
drop table if exists local_recipes;
drop table if exists local_ingredient_types;
drop table if exists local_ingredients;

drop table if exists daily_totals;
drop table if exists user_date;
drop table if exists daily_weight;
drop table if exists daily_dietary_notes;

# action_type table - 2 purposes:
# 1. for the historical tables, tells what the action was
# that was performed on the record(action_type fields)
# 2. for the roles table - tells us what actions are allowable
xreate table action_type(action_type_id mediumint not null auto_increment primary key,
action_type varchar(5) not null comment "action code" ,
action_type_desc varchar(100) comment "action description",
actv varchar(1) comment "is this record active(Y or N)?");
insert into action_type(action_type, action_type_desc, actv) values("V","view","Y");
insert into action_type(action_type, action_type_desc, actv) values("S","select","Y");
insert into action_type(action_type, action_type_desc, actv) values("C","create","Y");
insert into action_type(action_type, action_type_desc, actv) values("U","update","Y");
insert into action_type(action_type, action_type_desc, actv) values("D","delete","Y");
insert into action_type(action_type, action_type_desc, actv) values("A","all permissions","Y");
#select * from action_type;


# users table - all users of the system have a record in this table
xreate table if not exists users(user_id mediumint not null auto_increment primary key,
username varchar(256) not null UNIQUE comment "unique username",
email varchar(300) not null UNIQUE comment "unique email address",
password varchar(256) not null comment "password should be encrypted",
age smallint comment "age in years; we don't want to store the user's DOB",
lst_logd_in	datetime comment "when did the user last log in?");

# users_hist table - history of transactions on the users table
xreate table if not exists users_hist(users_hist_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
username varchar(256) not null comment "unique username",
email varchar(300) not null comment "unique email address",
password varchar(256) not null comment "password should be encrypted",
age smallint comment "age in years; we don't want to store the user's DOB",
lst_logd_in	datetime comment "when did the user last log in?",
action_type_id mediumint not null comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");


# groups table - basic members, premium members, admins, etc...
# each user can only belong to one group_type at a time
xreate table if not exists groups(grp_id mediumint not null auto_increment primary key,
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description");

# groups_hist - history table for group
xreate table if not exists groups_hist(grp_hist_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to groups.grp_id field",
grp_name varchar(30) comment "brief name of the group",
grp_desc varchar(256) comment "group or membership type description",
action_type_id mediumint not null comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");


# grp_user - table to "connect" all users with all groups
xreate table if not exists grp_user(grp_user_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field",
user_id mediumint not null comment "FK to the users.user_id field");
create index grp_user_idx on grp_user(grp_id);
create index user_grp_idx on grp_user(user_id);

# grp_user_hist - history table for grp_user
xreate table if not exists grp_user_hist(grp_user_hist_id mediumint not null auto_increment primary key,
grp_user_id mediumint not null comment "FK to the grp_user.grp_user_id field",
grp_id mediumint not null comment "FK to the groups.grp_id field",
user_id mediumint not null comment "FK to the users.user_id field",
action_type_id mediumint not null comment "what action was performed on this record?",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");


# resource_type table - just for the resource table, what resource types there are, pages, tables, etc..
xreate table if not exists rsrc_type(rsrc_type_id mediumint not null auto_increment primary key,
rsrc_type varchar(30) not null comment "resource type code",
rsrc_type_desc varchar(100) comment "resource type description",
actv varchar(1) comment "is this record active(Y or N)?");
insert into rsrc_type(rsrc_type,rsrc_type_desc, actv) values("TABLE","database table name","Y");
insert into rsrc_type(rsrc_type,rsrc_type_desc, actv) values("WEBPAGE","web page or screen","Y");
insert into rsrc_type(rsrc_type,rsrc_type_desc, actv) values("ALL","all resource types","Y");

# resources table - a list of all the different resources(screens, tables, etc..) that there are
xreate table if not exists resources(rsrc_id mediumint not null auto_increment primary key,
rsrc_type_id mediumint not null comment "FK to the rsrc_type.rsrc_type_id field",
rsrc_desc varchar(100) comment "description of the resource",
actv varchar(1) comment "is this record active(Y or N)?");

# roles table - table that shows what groups have what permissions(action_types) on what resources
xreate table if not exists roles(role_id mediumint not null auto_increment primary key,
grp_id mediumint not null comment "FK to the groups.grp_id field",
rsrc_id mediumint not null comment "FK to the resources.rsrc_id field",
action_type_id mediumint not null comment "FK to the action_type.action_type field");

# roles_hist table - history table for the roles table
xreate table if not exists roles_hist(role_hist_id mediumint not null auto_increment primary key,
role_id mediumint not null comment "FK to the roles.role_id field",
grp_id mediumint not null comment "FK to the groups.grp_id field",
rsrc_id mediumint not null comment "FK to the resources.rsrc_id field",
action_type_id mediumint not null comment "what action was performed on this record?",
record_action_id mediumint not null comment "what action was performed on this record?(FK to the action_type.action_type field)",
evnt_tmestmp datetime comment "when did this action happen?",
evnt_oper_id varchar(256) comment "who did this action?, FK to the users.username field");

# list of name brands
xreate table if not exists brands(brand_id mediumint not null auto_increment primary key,
brand_name varchar(100) comment "name of the brand",
actv varchar(1) comment "is this record active(Y or N)?");

# list of brand name products
xreate table if not exists products(product_id mediumint not null auto_increment primary key,
brand_id mediumint not null comment "FK to the brands.brand_id field",
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field",
product_name varchar(100) comment "name of the product",
product_desc varchar(256) comment "description of the product",
actv varchar(1) comment "is this record active(Y or N)?");

# join table that joins recipes with their fundamental ingredients/recipes - recursive table
xreate table if not exists recipe_ingredients(recipe_ingr_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
rec_or_ingr_id mediumint not null comment "FK to either the ingredients.ingr_id field or the recipes.recipe_id field",
recipe_flg varchar(1) comment "is rec_or_ing_id another recipe(Y or N)?",
actv varchar(1) comment "is this record active(Y or N)?");

# table of the aggregate characteristics of a recipe
xreate table if not exists recipes(recipe_id mediumint not null auto_increment primary key,
recipe_name varchar(100) comment "name of the recipe",
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field of this recipe's listing",
recipe_desc varchar(256) comment "description of the recipe",
recipe_link varchar(256) comment "hyperlink to the recipe",
num_srv decimal(6,2) comment "number of servings this recipe makes",
actv varchar(1) comment "is this record active(Y or N)?");

# list of the types(vegetables, fruits, dairy) - recursive table, 3 levels
xreate table if not exists ingredient_types(ingr_type_id mediumint not null auto_increment primary key,
prnt_ingr_type mediumint comment "FK to the ingredient_types.ingr_type_id field of this type's parent type",
ingr_type_desc varchar(100) not null comment "description of the ingredient type",
table_name varchar(50) comment "FK to another table for later querying",
actv varchar(1) comment "is this record active(Y or N)?");

# list of all of the different serving types(ozs., cups, tbs, etc..)
xreate table if not exists serving_types(serv_type_id mediumint not null auto_increment primary key,
serv_type_cde varchar(10) not null comment "short code for the serving type",
serv_type_desc varchar(50) not null comment "longer description of the serving type",
actv varchar(1) comment "is this record active(Y or N)?");

# conversion factors between each different servings types
xreate table if not exists serving_type_ratios(serv_type_ratio_id mediumint not null auto_increment primary key,
serv_type_id_1 mediumint not null comment "FK to the serving_types.serv_type_id field",
serv_type_id_2 mediumint not null comment "FK to the serving_types.serv_type_id field",
ratio decimal(6,2) comment "conversion factor from serv_type_id_1 to serv_type_id_2",
actv varchar(1) comment "is this record active(Y or N)?");

xreate table if not exists ingredients(ingr_id mediumint not null auto_increment primary key,
ingr_desc varchar(256) comment "description of the ingredient",
ingr_type_id mediumint not null comment "FK to the ingredient_types.ingr_type_id field",
serv_sz	decimal(6,2) not null comment "the size of an individual serving",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
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
actv varchar(1) comment "is this record active(Y or N)?");

# list of name brands
xreate table if not exists local_brands(brand_id mediumint not null auto_increment primary key,
brand_name varchar(100) comment "name of the brand",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");

# list of brand name products
xreate table if not exists local_products(product_id mediumint not null auto_increment primary key,
brand_id mediumint not null comment "FK to the brands.brand_id field",
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field",
product_name varchar(100) comment "name of the product",
product_desc varchar(256) comment "description of the product",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");

# join table that joins recipes with their fundamental ingredients/recipes - recursive table
xreate table if not exists local_recipe_ingredients(recipe_ingr_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
rec_or_ingr_id mediumint not null comment "FK to either the ingredients.ingr_id field or the recipes.recipe_id field",
recipe_flg varchar(1) comment "is rec_or_ing_id another recipe(Y or N)?",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");

# table of the aggregate characteristics of a recipe
xreate table if not exists local_recipes(recipe_id mediumint not null auto_increment primary key,
recipe_name varchar(100) comment "name of the recipe",
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field of this recipe's listing",
recipe_desc varchar(256) comment "description of the recipe",
recipe_link varchar(256) comment "hyperlink to the recipe",
num_srv decimal(6,2) comment "number of servings this recipe makes",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");

# list of the types(vegetables, fruits, dairy) - recursive table, 3 levels
xreate table if not exists local_ingredient_types(ingr_type_id mediumint not null auto_increment primary key,
prnt_ingr_type mediumint comment "FK to the ingredient_types.ingr_type_id field of this type's parent type",
ingr_type_desc varchar(100) not null comment "description of the ingredient type",
table_name varchar(50) comment "FK to another table for later querying",
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");

xreate table if not exists local_ingredients(ingr_id mediumint not null auto_increment primary key,
ingr_desc varchar(256) comment "description of the ingredient",
ingr_type_id mediumint not null comment "FK to the ingredient_types.ingr_type_id field",
serv_sz	decimal(6,2) not null comment "the size of an individual serving",
serv_type_id mediumint not null comment "FK to the serving_types.serv_type_id field",
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
actv varchar(1) comment "is this record active(Y or N)?",
user_id mediumint not null comment "FK to the user.user_id field");
create index local_ingredients_idx on local_ingredients(user_id);

# list of food eaten by each user each day - BIG table!
xreate table if not exists daily_totals(daily_total_id mediumint not null auto_increment primary key,
user_date_id mediumint not null comment "FK to the user.user_id field",
item_id mediumint not null comment "FK to either ingredients, local_ingredients, recipes, or local_recipes tables",
is_recipe varchar(1) comment "is this a recipe(Y or N)?",
is_local_ingr varchar(1) comment "is this a local ingredient(Y or N)?",
num_srv decimal(6,2) not null comment "the number of servings of this item eaten",
time_eaten time comment "at what time of the day was this item eaten",
actv varchar(1) comment "is this record active(Y or N)?");
create index daily_totals_idx on daily_totals(user_date_id);

# join table that joins daily_totals with the users and calendar date, compund user/date index
create table if not exists user_date(user_date_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
calendar_date datetime not null comment "the caledar date(date only, no time)",
actv varchar(1) comment "is this record active(Y or N)?");
create index user_date_idx on user_date(user_id);

# daily weight table
create table if not exists daily_weight(daily_weight_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
calendar_date datetime not null comment "the caledar date(date only, no time)",
weight decimal(6,2) not null comment "person's weight on this given day",
actv varchar(1) comment "is this record active(Y or N)?");
create index daily_weight_idx on daily_weight(user_id);

# daily dietary notes table - a list of notes about your diet
create table if not exists daily_dietary_notes(ddn_id mediumint not null auto_increment primary key,
user_id mediumint not null comment "FK to the users.user_id field",
user_date_id mediumint not null comment "FK to the user.user_id field",
daily_note varchar(512) comment "daily note about your diet",
actv varchar(1) comment "is this record active(Y or N)?");
create index daily_dietary_idx on daily_dietary_notes(user_id);