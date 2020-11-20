-- noinspection SqlNoDataSourceInspectionForFile

-- noinspection SqlDialectInspectionForFile

# this table:
drop table if exists recipe_ingredients;
# has foreign keys to these 2 tables:
drop table if exists recipes;
drop table if exists ingredients;
# ingredients table has foreign keys to ingredient_types,serving_types, and brands
# this table:
drop table if exists brand_ingr_type;
# has foreign keys to these 2 tables:
drop table if exists ingredient_types;
drop table if exists brands;
drop table if exists brand_type;
# this table:
drop table if exists serving_type_ratios;
# has foreign keys to this table
drop table if exists serving_types;
#####################################################################################
#	CREATE TABLES
#####################################################################################
# list of all of the different serving types(ozs., cups, tbs, etc..)
create table if not exists serving_types(serv_type_id mediumint not null auto_increment primary key,
serv_type_cde varchar(10) not null comment "short code for the serving type",
serv_type_desc varchar(50) not null comment "longer description of the serving type",
img_loc varchar(200) comment "image details",
actv varchar(1) comment "is this record active(Y or N)?");
# conversion factors between each different servings types
create table if not exists serving_type_ratios(serv_type_ratio_id mediumint not null auto_increment primary key,
serv_type_id_1 mediumint not null, foreign key FKST1(serv_type_id_1) references serving_types(serv_type_id)
on update cascade on delete cascade,
serv_type_id_2 mediumint not null, foreign key FKST2(serv_type_id_2) references serving_types(serv_type_id)
on update cascade on delete cascade,
ratio decimal(6,2) comment "conversion factor from serv_type_id_1 to serv_type_id_2",
actv varchar(1) comment "is this record active(Y or N)?");

# list of name brands
create table if not exists brands(brand_id mediumint not null auto_increment primary key,
brand_type varchar(1) comment "brand type(N = name, G = generic, S = store)",
brand_name varchar(100) comment "name of the brand",
img_loc varchar(200) comment "image details",
actv varchar(1) comment "is this record active(Y or N)?");

# list of the types(vegetables, fruits, dairy) - recursive table, 3 levels
create table if not exists ingredient_types(ingr_type_id mediumint not null auto_increment primary key,
prnt_ingr_type mediumint comment "FK to the ingredient_types.ingr_type_id field of this type's parent type",
ingr_type_desc varchar(100) not null comment "description of the ingredient type",
img_loc varchar(200) comment "image details",
actv varchar(1) comment "is this record active(Y or N)?");

# connector table between brand and ingredient type
create table if not exists brand_ingr_type(brand_ingr_type_id mediumint not null auto_increment primary key,
brand_id mediumint not null, foreign key FKBTIT1(brand_id) references brands(brand_id)
on update cascade on delete cascade,
ingr_type_id mediumint not null, foreign key FKBTIT2(ingr_type_id) references ingredient_types(ingr_type_id)
on update cascade on delete cascade,
prnt_ingr_type mediumint not null, foreign key FKBTIT3(prnt_ingr_type) references ingredient_types(ingr_type_id)
on update cascade on delete cascade,
actv varchar(1) comment "is this record active(Y or N)?");

# this table is just for populating a dropdown on a web page
create table if not exists brand_type(brand_type_id mediumint not null auto_increment primary key,
brand_type varchar(1) comment "brand type(N = name, G = generic, S = store)",
brand_type_name varchar(100) comment "name of the brand");
insert into brand_type(brand_type,brand_type_name) values("N","Name Brand");
insert into brand_type(brand_type,brand_type_name) values("S","Store Brand");
insert into brand_type(brand_type,brand_type_name) values("G","Generic(No Brand)");

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
img_loc varchar(200) comment "image details",
actv varchar(1) comment "is this record active(Y or N)?");

# table of the aggregate characteristics of a recipe
create table if not exists recipes(recipe_id mediumint not null auto_increment primary key,
recipe_name varchar(100) comment "name of the recipe",
ingr_id mediumint not null comment "FK to the ingredients.ingr_id field of this recipe's listing",
foreign key REC1(ingr_id) references ingredients(ingr_id)
on update cascade on delete cascade,
recipe_desc varchar(256) comment "description of the recipe",
recipe_link varchar(256) comment "hyperlink to the recipe",
num_srv decimal(6,2) comment "number of servings this recipe makes",
actv varchar(1) comment "is this record active(Y or N)?");

# join table that joins recipes with their fundamental ingredients/recipes - recursive table
create table if not exists recipe_ingredients(recipe_ingr_id mediumint not null auto_increment primary key,
recipe_id mediumint not null comment "FK to the recipes.recipe_id field",
foreign key RI1(recipe_id) references recipes(recipe_id)
on update cascade on delete cascade,
rec_or_ingr_id mediumint not null comment "FK to either the ingredients.ingr_id field or the recipes.recipe_id field",
recipe_flg varchar(1) comment "is rec_or_ing_id another recipe(Y or N)?",
actv varchar(1) comment "is this record active(Y or N)?");

select * from serving_types;
delete from serving_types where serv_type_id=9;
select * from serving_type_ratios;
insert into serving_types(serv_type_cde,serv_type_desc,actv) values("tsp","teaspoons","Y");
insert into serving_type_ratios(serv_type_id_1,serv_type_id_2,ratio,actv) values(5,1,3.0,"Y");

create table if not exists payment_type(payment_type_id mediumint not null auto_increment primary key,
payment_type_cde varchar(10) not null comment "short code for the payment type",
payment_type_desc varchar(50) not null comment "longer description of the payment type",
img_loc varchar(200) comment "image details",
actv varchar(1) comment "is this record active(Y or N)?");

create table if not exists payment(payment_id mediumint not null auto_increment primary key,
payment_type_id mediumint not null comment "FK to the payment_type.payment_type_id field",
foreign key PT1(payment_type_id) references payment_type(payment_type_id),
payment_amt decimal(6,2) not null comment "payment amount",
payment_desc varchar(100) comment "payment description",
actv varchar(1) comment "is this record active(Y or N)?");