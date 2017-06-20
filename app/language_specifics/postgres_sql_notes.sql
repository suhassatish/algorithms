\copy players from /Users/jackson/Downloads/players_data.csv csv header

-----------------
regular expression on string columns - 

select * 
from mining_mindshare_hackday07.sp_hackday_searches_hashed q
where q.query REGEXP '.*pregnant.*'

select q.query 
from mining_mindshare_hackday07.sp_hackday_searches_hashed q
where q.query LIKE '% not pregnant %'

LIKE is faster than REGEXP
---------------------

select count(distinct patient_id_hash) from sp_microsoft_claims_hashed;


query searches table had about 7 Million entries and was slow to join on or index


---------

postgres sql windowing function - 
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
avg is computed per department. 
depname  | empno | salary |          avg          
-----------+-------+--------+-----------------------
 develop   |     8 |   6000 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     3 |   4800 | 4866.6666666666666667

-------------
postgres DDL commands 
\d+ tablename ; --describe table
\da ; --list of aggregate functions
\db ; --list of tablespaces
\df ;  --list of functions
\dg ; --list of roles
\dC ; --list of casts
\di ; --list of indexes
\dl ; --list of large objects
\dn ; --display namespaces (schemas) in current database
\dn+ ; --display namespaces along with access privileges & description
\do ; --list of user-defined custom operators
\dp ; --access privileges
\dt ; --list of tables
\ds ; --list of sequences
\dS+ mvp_*; --displays all columns, datatypes, storage-types & modifiers of tables starting with mvp_ in all the namespaces in the `search_path`; `S` modifier lists system-defined objects as well (eg- pg_catalog)
\du ; --list of users' roles
\dv ; --list of views


delete from followings where id='3';

delete using join - does not use inefficient construct-- where id not in (select *)

delete
from rewards_program_participations rpp
    using rewards_blocked_providers rbp
where rpp.provider_id=rbp.id;

----------------------------
--escaping single quote like CONCAT("'",tax_id,"'")
array_to_string(ARRAY[E'\'', tax_id, E'\''], '')

-------
--to  convert to Title Case , postgres 8.1+ has function
--initcap(string)	text	Convert the first letter of each word to upper case and the rest to lower case. 
--Words are sequences of alphanumeric characters separated by non-alphanumeric characters.	initcap('hi THOMAS')	-> Hi Thomas


----------------
all column names in postgres are converted to lower case. to query by preserving Camel case, give in double quotes like - 
select * from following where "followeeID" = 2; 

select * from tweets where user_id in (select "followeeID" from followings where "userID"=1);

show databases - postgres 
\list

--show which database , host port is psql currently connected to ? 
select inet_server_addr( ), inet_server_port( );


clone database from template - 
CREATE DATABASE prov_dir_username WITH TEMPLATE prov_dir_template OWNER pd_user;

use database
\connect username_twitter_test

-------------
CIB low price discrepancy - 

select *
from
  (select *
     , count(is_provider_in_ticket or null) over (partition by pt_code) > 0 ticket_provider_has_pt
   from
     (select pt_code
        , pt_label
        , is_provider_in_ticket
        , count(*) claim_cnt
        , round(avg(allowed_amount),2) avg_allowed_amount
        , (now() - avg(age(service_begin_date)))::date avg_service_begin_date
      from
        (select *
           , provider_id = 2114351 is_provider_in_ticket
           , extract(epoch from age(service_begin_date) - avg(case provider_id when 2114351 then age(service_begin_date) end) over (partition by pt_code))/(3600*24) days_from_ticket_provider_claims
         from claims_with_priceable_type c
           join providers_specialties ps using (provider_id)
           join providers_locations_networks pln using (provider_id)
           join locations l on l.id = location_id
         where pt_label like 'cpt-992%'
               and specialty_id = 632
               and state = 'WI'
               and city = 'Madison'
               and allowed_amount > 0) v
      where is_provider_in_ticket or abs(days_from_ticket_provider_claims::numeric ) <= 180
      group by 1,2,3) t
  ) u
where ticket_provider_has_pt
order by 1,2,3
-------------
select 
count(*), pm.procedure_family_id, case when amount is null then 'null_bundle' else 'priced_bundle' end as priced_bundle, bucket_id, buckets.name
from 
  bundle_app_priceables bap
  inner join procedure_mappings pm on pm.id = bap.procedure_mapping_id
  inner join app_priceables ap on bap.id = ap.id
  inner join buckets on ap.bucket_id = buckets.id
where
  pm.procedure_family_id in (247, 249)
group by 
2,3,4,5
order by 4,5,2,3
;
------------------------------------

windowing function for rank - beware the sub-query. it slows down operations in MySQL by 100X. use indexed joins instead. 


select top3.user_name, top3.text 
from
(select u.id, u.user_name, text, rank() over (partition by user_id order by t.created_at desc) as rank
from tweets t
  join users u on u.id = t.user_id
  join followings f on f."followeeID" = t.user_id
  where f."userID" = 2)top3
where rank<4;

------------------
common table expression (CTE) - use WITH instead of sub-queries. with is evaluated only once, at the beginning, instead of for every row as in the case of a sub-query. 
disadvantage: filter predicates from outer (parent) query are  pushed down into the child (inner) query for optimization. that kind of predicate pushdown doesnt happen for withs. so an inefficient WITH may pull lots of data, but postgres limits the returned results based on amount of fetched data and stops early. 


WITH regional_sales AS (
        SELECT region, SUM(amount) AS total_sales
        FROM orders
        GROUP BY region
     ), top_regions AS (
        SELECT region
        FROM regional_sales
        WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
     )
SELECT region,
       product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;

-----------
The queries:

SELECT * FROM t1 WHERE id NOT IN (SELECT id FROM t2);
SELECT * FROM t1 WHERE NOT EXISTS (SELECT id FROM t2 WHERE t1.id=t2.id);
Can be rewritten as:

SELECT table1.*
  FROM table1 LEFT JOIN table2 ON table1.id=table2.id
  WHERE table2.id IS NULL;

http://dev.mys.com/doc/refman/5.0/en/rewriting-subqueries.html
--------------------------

postgres syntax error - 
copy reference.phase_versions, reference.wh_versions (version,version_name) to STDOUT

try
copy reference.phase_versions, reference.wh_versions to STDOUT
------

$RVNG_HOME/sql_utils.dump_table_via_stdout throws the following error - 
RuntimeError: Failed to load file, error:  (no COPY in progress
)
	from /Users/username/Projects/Ventana/revenge/lib/database/sql_utils.rb:1309:in `raise_on_pg_error_status!'
	from /Users/username/Projects/Ventana/revenge/lib/database/sql_utils.rb:663:in `ensure in dump_table_via_stdout'
	from /Users/username/Projects/Ventana/revenge/lib/database/sql_utils.rb:663:in `dump_table_via_stdout'
	from /Users/username/Projects/Ventana/revenge/lib/continuous_integration.rb:226:in `block in dump_phase_version'
	from /Users/username/Projects/Ventana/revenge/lib/ssh_utils.rb:79:in `call'
	from /Users/username/Projects/Ventana/revenge/lib/ssh_utils.rb:79:in `with_ssh_session'
	from /Users/username/Projects/Ventana/revenge/lib/continuous_integration.rb:218:in `dump_phase_version'
	from (irb):3
	from /Users/username/.rvm/rubies/ruby-1.9.3-p551/bin/irb:12:in `<main>'
------
to see which is the currently connected to DB
select current_database();

similarly,
select current_user;
------------
--full text search of a table name and find out which schema its in 



--find all tables which have a particular column name

select distinct table_name, ordinal_position from information_schema.columns where column_name = 'procedure_mapping_id';

--find all column names from a table - 

select column_name from information_schema.columns where
table_name='captor_prime_aggregates';


---------------
schema owners are stored in 
information_schema.schemata.schema_owner 

select *
FROM information_schema.table_privileges
where grantee ilike 'pd_user';
--even grantor granteee table access permissions ownership is stored here 
---------
recursively change ownership of all tables in postgres- 

CREATE OR REPLACE FUNCTION change_owner(source_schema text, original_owner text, new_owner text) RETURNS void AS
$BODY$
DECLARE
  objeto text;
  buffer text;
BEGIN
    FOR objeto IN
        SELECT TABLE_NAME::text
        FROM information_schema.TABLES
        WHERE table_schema = source_schema          
    LOOP
        buffer := objeto;
        EXECUTE 'alter TABLE ' || buffer || ' owner to ' || new_owner;
    END LOOP;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;


SELECT change_owner('mncm','username','pd_user');

----
ARRAY_ADD is a group_by - use it as a windowing function when need arises

----------
once inside DB, 
set role dev;

this can then run admin commands. 

connect as some other user to increase database connection limit - 
RAILS_ENV=other_db_full OVERRIDE_DB=ssaneinejad_full DB_USER=ssaneinejad script/dbconsole
these options are there in database.yml

Sql.disconnect_users "bam_full"
now drop username_full

drop database release_palladium1;
ERROR:  database "release_palladium1" is being accessed by other users
set role dev; 
select pg_terminate_backend(procpid) from pg_stat_activity where datname='prov_dir_username';

select procpid from pg_stat_activity where datname='prov_dir_username';
--get procpid from pg_stat_activity

select * from pg_stat_activity where usename='username';
tells you where the queries are stuck, eg - coe_cartels had huge difference in row estimates (0) vs actual #rows materialized. so join was blowing up 

--drop auto increment from primary key column - 
ALTER TABLE providers DROP PRIMARY KEY, CHANGE id id int(11), ADD PRIMARY KEY (id);

change or modify table name - 

alter database username_full connection limit 10;

alter table `table_name` rename to `new_table_name`
alter schema clustering rename to clustering_bk;
-----------------------
show all schemas that exist - 
select * from information_schema.schemata;
-----------------
select e.name as employer_name, claims.*
from 
(SELECT
  employer_id,  count(*) as claims_count_per_employer
FROM claims
WHERE insurance_company_id NOT IN (19, 46)
      AND
      employer_id NOT IN (22, 46, 43, 64, 83, 86, 13, 121, 123, 140, 155, 166, 150, 36)
GROUP BY employer_id)claims
join employers e on e.id = claims.employer_id
order by claims_count_per_employer desc;

------------------------
random sampling in postgres 8.4 - 

SELECT * FROM myTable
WHERE attribute = 'myValue'
ORDER BY random()
LIMIT 1000;

--this may not be enough, sometimes u need stratified sampling; example - netflix most important devices are smart TVs and iphone in USA, 
--not someone in Australia on a gaming console;

--sampling proportions should be sensitive to these inherent data distributions (example - more male gamers  than females )
--------------------
dump postgres sql query result to csv or tsv - can redirect output to tsv file just before this command - 

psql -c "COPY (<select query>) TO STDOUT WITH CSV"

psql -c "COPY (<select query>) TO STDOUT WITH NULL AS ''"
copy (select * from claims_denorm_dump3 limit 100000) to stdout with null as '';


tolerate bad rows - max_error_rows
\copy flight_times from '/Users/username/data_science/allyears2k.csv' with csv NULL as 'NA' header segment reject limit 100 rows;
Last error was: invalid byte sequence for encoding "UTF8": 0xe4e22c

\copy employee_geographies from '/data02/tmp/employee_geographies.txt' NULL as 'NULL' header 
-- note: with \copy, dont put a semi colon at the end, it gives a syntax error

forcibly converting encoding to utf8 works - 
iconv -f ISO88592 -t utf-8 < demandforce_reviews.txt > demandforce_reviews_utf8.txt

show client_encoding;
show server_encoding;

e' character is not recognized with sedula. somehow find a workaround for it. 

---
\copy demandforce_reviews from '/home/username/duplo_data/dental/demandforce_raw_20151006T2103_20151119T0021/demandforce_reviews.txt' NEWLINE [ AS ] 'LF' | 'CR' | 'CRLF'
this dataset had newlines as \$ and $, as seen in vim on linux, have to pick the $ case only as newline.
------------------------------
copy an entire table as csv - 
COPY products_273 TO '/tmp/products_199.csv' DELIMITER ',' CSV HEADER;
delimiter: default is tab ascii character (\t)
header: tells that the first line is names of columns on output, and on input, first line is ignored.

dump an entire table as tsv - 
COPY products_273 TO '/tmp/products_199.tsv'  HEADER;

-------------------------

ERROR:  must be superuser to COPY to or from a file
HINT:  Anyone can COPY to stdout or from stdin. psql's \copy command also works for anyone.
ERROR:  relative path not allowed for COPY to file

/home/username/shared/revenge-sync

create table safeway_zips(zip char(5), eligible int, eligible_and_launched int, registered int);
COPY mytable FROM '/path/to/csv/file' WITH CSV HEADER; -- must be superuser
the path should be local to the database server machine, eg- bam_full  on bam0.ch.int

ERROR:  duplicate key violates unique constraint "pg_type_typname_nsp_index"
you get this error if you have concurrent sessions trying to create the same table name simultaneously. 


create  table analysis.ncct_collected_price_ranges (like ncct_location_query_price_ranges including defaults)
-------------------------------------------
load DATA pipe-separated '|' into postgresQL database - 
set role dev; 
path specified should exist on database server machine, ie zap-master01 or bam0

copy RSTR1_STRNGTH_DESC from '/home/username/RSTR1_STRNGTH_DESC' delimiter '|' ;
-------------------------
to see the roles in the DB- 
SELECT rolname FROM pg_roles;

CREATE ROLE name;
DROP ROLE name;

alter table locations_482xx  owner to pd_user;
alter table facility_test_data rename street_address to address;

this works for anyone - 
\copy locations_482xx from /home/username/data/locations_482xx.tsv header;

------------

on table claims_denorm_dump3, distribute by imported_claim_id 

its faster than creating index as it prioritizes spatial locality.

create table claims_dump4 as (select * from claims) 
distributed by (imported_claim_id);

create table iris_wheader(sepal_len numeric(4,2), sepal_wid numeric(4,2), petal_len numeric(4,2), petal_wid numeric(4,2), class varchar) distributed by(class);
--------------------
to display indexes 
select * from pg_indexes where tablename = 'claims_denorm_distributed';
---------------
--size on disk
select sosdnsp, (sosdschematablesize+sosdschemaidxsize)/1024/1024/1024 GB
from gp_toolkit.gp_size_of_schema_disk order by 1;

--find total table size on disk (including index) - 
SELECT pg_size_pretty(pg_total_relation_size('big_table'));

--see all DB sizes
select datname, pg_size_pretty(pg_database_size(datname)) from pg_database order by 2 desc;

--see sum of size of all tables within a schema
SELECT pg_size_pretty(SUM(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))::BIGINT)
FROM pg_tables
WHERE schemaname = 'matcher_prod';

--how to see each table size within a postgre DB ? this query shows the top 20 tables by size 
SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  ORDER BY pg_relation_size(C.oid) DESC
  LIMIT 20;

--to see the total size of your database - 
SELECT pg_size_pretty( pg_database_size( current_database() ) ) AS your_db_size;

--size of top 20 tables in all schemas by size
select
schemaname,
tablename,
pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as size_p,
pg_total_relation_size(schemaname || '.' || tablename) as siz,
pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size_p,
pg_total_relation_size(schemaname || '.' || tablename) - pg_relation_size(schemaname || '.' || tablename) as index_size,
(100*(pg_total_relation_size(schemaname || '.' || tablename) - pg_relation_size(schemaname || '.' || tablename)))/case when pg_total_relation_size(schemaname || '.' || tablename) = 0 then 1 else pg_total_relation_size(schemaname || '.' || tablename) end || '%' as index_pct
from pg_tables
order by siz desc limit 20;

--how to see the last table creation/modification timestamp in greenplum (operation not supported in vanilla postgres)
select * 
from pg_stat_last_operation
where objid = 'acr_imaging_quality_vy.aim_pl_subset'::regclass
order by statime;
-------------------
to create a unique index on column id (remove unique keyword to remove uniqueness constraint)- 
CREATE unique INDEX hphc_imported_claims_pkey ON hphc_imported_claims USING btree (id)

creates btree index or hash index_type - 
CREATE INDEX test_index ON numbers using hash (num);

CREATE TABLE stage_provider_affiliations (
    id serial,
    provider_id integer DEFAULT NULL,
    parent_provider_id integer DEFAULT NULL,
    affiliation_type varchar check(affiliation_type in ('HOSPITAL','SOLO PRACTICE','PRACTICE')) DEFAULT NULL,
    source varchar(20) DEFAULT NULL,
    active_flag varchar check(active_flag in ('ACTIVE','INACTIVE')) DEFAULT NULL,
    created_at timestamp DEFAULT NULL,
    updated_at timestamp DEFAULT NULL,    
    UNIQUE (provider_id,parent_provider_id,affiliation_type)
) distributed by (provider_id);
--unique and primary key cannot appear together in greenplum
--when unique and distributed by appear toegether, the distributed by must be a left subset of the unique columns

create table raw_provider_directory(
provider_id integer
, address_sha1 bytea
, network_id integer
,other_columns varchar
,UNIQUE (provider_id, address_sha1, network_id)
) distributed by (provider_id);
------------------------
redirect postgres query output to a file - 

# \o output_file
# SELECT * FROM pg_class;

to re-enable stdout, 
\o

------
PostgreSQL data types are divided into base types, composite types, domains, and pseudo-types.

--------
Second maximum value of a column
# SELECT MAX(num) from number_table where num  < ( select MAX(num) from number_table );

----------
Following example gives the total number of rows with a specific column value is not null.
# select count(col_name) from table;

------------
 How to find the largest table size in the postgreSQL database?
SELECT relname, relpages FROM pg_class ORDER BY relpages DESC;


analyze [table] [column]

will generate key distribution histogram for a table column and store it in pg_statistic. This will be used to optimize query plans during joins. 


ALTER TABLE distributors TO NODE (dn1, dn7), DISTRIBUTE BY HASH(dist_id);
this is in examples but doesnt work without the nodes as below - 
ALTER TABLE claims_denorm_dump3 DISTRIBUTE BY HASH(dist_id);
--------------
analyze providers_locations_networks_optimized (source,active_flag,provider_id,location_id,network_id,type);

distributed  by query example- 

CREATE TABLE my_table AS 
SELECT state, count(*) AS counter
FROM customer
GROUP BY state
DISTRIBUTED BY (state);
--Statistics will be gathered automatically only if the number of rows is 1M or more.


------------------

UPDATE table
SET column1 = value1,
 column2 = value2 ,...
WHERE
	condition;

example - 
update claims_denorm_distributed 
set insurance_company_id=2 
where imported_claim_id=26754381;

greenplum cannot update distribution column (by default is primary key)
update temp1_aetna set id=94457308;
ERROR:  Cannot parallelize an UPDATE statement that updates the distribution columns
--------------

union all example - 

create table claims_denorm_all AS
  select * from 
  (select a,b,c,...
from claims_denorm
limit 1000000)t1 
union ALL (select * from claims_denorm2 limit 1000000)
union all (select * from claims_denorm3  limit 1000000);
----------

insert table as select - 

INSERT into foo_bar (foo_id, bar_id) ( 
  SELECT foo.id, bar.id FROM foo CROSS JOIN bar 
    WHERE type = 'name' AND name IN ('selena', 'funny', 'chip') 
);

this works - 
insert into rx_claims_denorm_short select * from rx_claims_denorm r where r.insurance_company_id=43 and r.imported_claim_id > 1500000 and r.imported_claim_id < 2500000;G

LIMITATION! - cannot insert into only selected columns and not all! if you want to do selective column update, use update..command 
-----
mysql has str_to_date() function but postgres doesnt; so instead use the following in postgres in client application - 
SELECT to_char("date", 'DD/MM/YYYY') FROM mytable;
----------------------


distinct queries on 3 different columns only, and still non-distinct ones on others.

select distinct on (p,l,n) , a 
from ...


the distinct on should match the order by 

example - 
select distinct on  (provider_id, specialty_id) provider_id, specialty_id
from providers_specialties_with_name
order by provider_id, specialty_id ASC 
limit 10;
------------
create table with array type - 
alter table esi_variance_by_pharmacy135_1833981
    add column p1_ndc_array text[]
    ,add column id int;

where clause on array of character_varying data type - 
select *  
from procedures 
WHERE cpt= ANY(ARRAY['97802', '97803', '97804', '98960']);


select *
from procedure_mapping_export_filters
where 693=ANY(required_spec_ids);
---------------
date aggregate by month - 

select to_char(payment_date,'MM') as Mon, 
  extract(year from payment_date) as yyyy,
  count(*) as Number_of_claims

from nutrition_claims nc
group by 1,2
order by 2 desc, 1 desc;

select extract(year from created_at)
from provider_matches;
------------------------

providers_specialties_with_name = view that has super-set of all 
providers and specialties, including the ones from whom we have claims. 

----------------

claims_with_pricable_type.pt_label gives description of procedure.

--------------------
co-occuring procedure cpt-codes for claim_groups bundling 

--substr(string, from [, count])
--where FROM is the 1-indexed start index, inclusive
--and COUNT is the number of letters in the substring 

  select *
    from
  (select substring(member_id,1,10) member
  , service_begin_date b
  , service_end_date e
  , provider_id
  , provider_name
    , allowed_amount
  , label
  , short_description
  , *
--     , count(case when label = 'cpt-59400' then 1 end) over (partition by member_id) is_pregnancy
  , count(label =
          'revenue-0126' 
--          'cpt-59400' 
          or null) over (partition by member_id) is_detector
--     , count(label = 'cpt-59400' or null) over (partition by member_id) is_pregnancy
from claims
  join priceable_types using (procedure_label_id)) t
    where is_detector > 0
  order by 1,2,3,4,5,6
  limit 1000


---------

top co-occuring claim cpt-codes for nutrition_claims along for the same members on the same service_begin_dates

select label, count(*)
from nutrition_claims nc 
join claims_with_priceable_type c2 on (nc.service_begin_date = c2.service_begin_date 
                                       and nc.member_id = c2.member_id 
                                        and c2.label not in ('cpt-97802', 'cpt-97803', 'cpt-97804', 'cpt-98960') )
group by label
order by count desc;

-------
postgres date add - functions - 

http://www.postgresql.org/docs/9.1/static/functions-datetime.html

Operator	Example	Result
+	date '2001-09-28' + integer '7'	date '2001-10-05'
+	date '2001-09-28' + interval '1 hour'	timestamp '2001-09-28 01:00:00'
+	date '2001-09-28' + time '03:00'	timestamp '2001-09-28 03:00:00'
+	interval '1 day' + interval '1 hour'	interval '1 day 01:00:00'
+	timestamp '2001-09-28 01:00' + interval '23 hours'	timestamp '2001-09-29 00:00:00'
+	time '01:00' + interval '3 hours'	time '04:00:00'
-	- interval '23 hours'	interval '-23:00:00'
-	date '2001-10-01' - date '2001-09-28'	integer '3' (days)
-	date '2001-10-01' - integer '7'	date '2001-09-24'
-	date '2001-09-28' - interval '1 hour'	timestamp '2001-09-27 23:00:00'
-	time '05:00' - time '03:00'	interval '02:00:00'
-	time '05:00' - interval '2 hours'	time '03:00:00'
-	timestamp '2001-09-28 23:00' - interval '23 hours'	timestamp '2001-09-28 00:00:00'
-	interval '1 day' - interval '1 hour'	interval '1 day -01:00:00'
-	timestamp '2001-09-29 03:00' - timestamp '2001-09-27 12:00'	interval '1 day 15:00:00'
*	900 * interval '1 second'	interval '00:15:00'
*	21 * interval '1 day'	interval '21 days'
*	double precision '3.5' * interval '1 hour'	interval '03:30:00'
/	interval '1 hour' / double precision '1.5'	interval '00:40:00'

example date range query - 

join claims_with_priceable_type c2 on ( c2.service_begin_date >= (nc.service_begin_date - integer '1')
                                      and c2.service_begin_date <= (nc.service_begin_date + integer '3')
                                        and nc.member_id = c2.member_id 
----
rounding to 2 decimal places taking percentages % 

 round((count(label) ::decimal /45402 ::decimal)*100,2) as cnt

----------
select any in a char array [] type of column in a database - 

SELECT
  distinct provider_network_id
FROM warehouse.insurance_plans_with_product_codes ip
  join warehouse.insurance_plan_network_mappings ipnm
    on ipnm.external_plan_network_mapping_code = any(ip.product_code_array)
WHERE plan_key ILIKE '%anthem%'
      AND employer_id = 175;

--how to do the inverse of this where you want to select a varchar column and typecast into a text[] olumn?
alter table A alter column type text[] using array[column1];
--The optional USING clause specifies how to compute the new column value from the old; If omitted, the default conversion is the same as an assignment cast from old data type to new. A USING clause must be provided if there is no implicit or assignment cast from old to new type.


--below works fully correctly by declaring an empty array in postgres as '{}'
array_append('{}',board_web_desc::text)::text[];

alter table hospitals alter column hosp_id set default nextval('hospitals_id_seq'::regclass);
--makes a non-serial id column into serial
--------------
--sample query using serial and inserting auto-increment column automatically in postgres - 
--NOTE that id column is missing in bracket of insert statement; I didnt find a less cumbersome way to do it and get it working

insert into practitioner_test_data2(test_set_id,first_name,last_name,middle_name,medical_degrees,specialty_names,phone_nums,address,city,state,zip,npis,medical_school,grad_yr,provider_id,location_id,source_table_host_db_schema,source_reference_column_name,source_table_id)
      (select
    --nextval(test_data.practitioner_test_data2_id_seq.last_value)
    -1::integer
    ,lower(first_name)
    ,regexp_replace(lower(last_name),'''|-',' ')
    ,lower(middle_name)
    ,NULL
    ,array_append('{}',board_web_desc::text)::text[] --specialty
    ,NULL --phone_nums
    ,COALESCE(org1,'') || ' ' || COALESCE(line_1, '') || ' ' || COALESCE(line_2, '') || ' ' || COALESCE(line_3, '') --address
    ,city
    ,state_prov
    ,substr(us_zip,1,5)
    ,array_append('{}',npi::text)::text[]
    ,NULL --medical_school
    ,NULL --grad_yr
    ,NULL --provider_id
    ,NULL --location_id
    ,'biog.biog_nbr'::varchar
    ,biog_nbr
  from abms.biog b
    join abms.cert c using (biog_nbr)
    join abms.address a using (biog_nbr)
  limit 1);
----------

use coalesce function to impute first value in arguments which is not null

here, it actually see if pra.start_date is null, then it puts rp.start_date

SELECT rp.key, ip.insurance_company_id, ip.employer_id, alm.layer_id,
  rp.start_date, rp.end_date, pra.rewardable_activity_key, COALESCE(pra.start_date, rp.start_date), COALESCE(pra.end_date, rp.end_date)
FROM rewards_programs rp
  JOIN insurance_plans ip
    ON ip.id = rp.insurance_plan_id
  JOIN program_rewardable_activities pra
    ON pra.rewards_program_key = rp.key
  JOIN active_layer_mappings alm
    ON alm.insurance_company_id = ip.insurance_company_id
       AND alm.employer_id = ip.employer_id
WHERE pra.rewardable_activity_key like 'CLAIMS%';
----------
 split over each code 

create table nutriction_claims_by_code_monthly as 
select nc.code, to_char(service_begin_date,'MM') as Mon,
                extract(year from service_begin_date) as yyyy,
                count(*) over (partition by code) as Number_of_claims

from nutrition_claims2 nc
group by 1,2,3
order by 3 desc, 2 desc;

code,month,year,number_of_claims
97802	01	2015	100
97803	01	2015	98
G0108	01	2015	100
98960	01	2015	92
G0109	01	2015	88
G0109	12	2014	88
98960	12	2014	92
97802	12	2014	100
G0108	12	2014	100
97803	12	2014	98
97804	12	2014	85
97804	11	2014	85
97803	11	2014	98
G0108	11	2014	100
G0109	11	2014	88
97802	11	2014	100
98960	11	2014	92
98960	10	2014	92
97802	10	2014	100
97803	10	2014	98
G0109	10	2014	88
-----------------------------

now partition over 2 columns - cant do it, so take md5 hash over concatenated column of code and year  - 

select distinct on (yyyy, code) yyyy, code as year, 
  avg(number_of_claims) over (partition by md5(concat(code::text, yyyy::text))) as avg_yearly_number_of_claims 
from nutriction_claims_by_code_monthly
order by yyyy desc, code desc;
-------------------------------
set difference - using the except keyword  - makes it very slow
using  "where not in" () filter;

union, intersect and except operations are very slow
----------------------------
\! clear()

postgres  cumulative counts frequency distribution - 

select tmp.*, sum(num_emp) over (order by num_emp desc)
FROM 
(
  select cbsa, sum(count) as num_emp
  from current_employee_geographies ceg
    join zip_codes zc on (ceg.zip= zc.zip_code)
  where employer_id=84
  group by 1   
)tmp
order by 2 desc;
--------------------

create  table aetna.aetna_cbsa_pl_price_curve  as       select
        erpl.rbb_region_id,
        eg.n_employees,
        ncct_treatment_category,
        procedure_mapping_id,
        count(*) cnt_price,
        min(erpl.price_expected) min_price,
        max(erpl.price_expected) max_price,
        avg(erpl.price_expected) avg_price,
        percentile_disc(0.10) within group (order by erpl.price_expected) price10,
        percentile_disc(0.20) within group (order by erpl.price_expected) price20,
        percentile_disc(0.30) within group (order by erpl.price_expected) price30,
        percentile_disc(0.40) within group (order by erpl.price_expected) price40,
        percentile_disc(0.50) within group (order by erpl.price_expected) price50,
        percentile_disc(0.60) within group (order by erpl.price_expected) price60,
        percentile_disc(0.70) within group (order by erpl.price_expected) price70,
        percentile_disc(0.80) within group (order by erpl.price_expected) price80,
--
another way - 
select
    synonymous_subgroups_id
  ,employer_id
  --,ntile(10) over (PARTITION BY synonymous_subgroups_id, employer_id order by unit_drug_price) decile
  ,percentile_disc(0.1) within group (order by unit_drug_price) as employer_unit_drug_price_10
  ,median(unit_drug_price) as employer_unit_drug_price_median
  ,percentile_disc(0.9) within group (order by unit_drug_price) as employer_unit_drug_price_90
  --,unit_drug_price
from rx_claims_with_ss_id rxs
where prescription_service_date>=2015-01-19
group by
  synonymous_subgroups_id
  ,employer_id
-----------------
postgres operator -    <> or !=

---------

to see how many imaging_facfill prices finally made it into the app_priceables table - 

select count(distinct apu.id)
from app_priceable_units apu
  join providers_locations_networks pln on pln.id = apu.provider_participation_id
  join candidate_priceable_procedure_mappings using (procedure_mapping_id)
  join priceables pb using (priceable_type_id)
  join cartel_plns using (cartel_id, provider_id)
  join priceable_prices pp on pb.id = pp.priceable_id
  join prices pr on (pr.price_method='imaging_facfill' and pr.id = pp.price_id);
----------------

aggregate boolean and in postgres - 

create table priceable_claim_group_distribution AS 
select pb.id, count(distinct icg.id), not bool_and(icg.is_valid) as has_invalid_cg
from priceables pb 
join imaging_claim_groups icg using (priceable_type_id, cartel_id)
group by 1;
-----------------

my sql CTAS query with auto incrementing primary key - 

CREATE TABLE `user_mv` (id INT AUTO_INCREMENT PRIMARY KEY) SELECT `user`.`firstname` as 
   `firstname`,
   `user`.`lastname` as `lastname`,
   `user`.`lang` as `lang`,
   `user`.`name` as `user_name`,
   `group`.`name` as `group_name`
from `user`
  inner join `user_groups` on (`user`.`user_id`=`user_groups`.`user_id`)
  left  join `group` on (`group`.`group_id`=`user_groups`.`group_id`)
where `user`.`lang`=`group`.`lang`;
----
exact equivalent doesnt exist in postgres, so you need to use nextval(id_seq)
---------
postgres regular expresion - replace space with underscore  - 

similar - ltrim, rtrim, btrim - left trim, right trim, both trim 

SELECT trim(regexp_replace(mystring, '[\s]+', ' ', 'g')) as mystring FROM t1;

select distinct on (pd)
replace(pd, ' ', '_') as pd
from rndc14_ndc_mstr rndc;

select distinct on (pd)
regexp_replace(rndc.pd, '\\s+', '_','g') as pd
from rndc14_ndc_mstr rndc;

regexp_matches - 

-------------------------------
to see all the functions in the database in any schema-
--??
---------------
to see all the functions in the database - 

"\df <schema>.*"

information_schema.routines table and the information_schema.parameters tables. Using those, one can construct a query for this purpose.

SELECT routines.routine_name, parameters.data_type, parameters.ordinal_position
FROM information_schema.routines
    JOIN information_schema.parameters ON routines.specific_name=parameters.specific_name
WHERE routines.specific_schema='my_specified_schema_name'
ORDER BY routines.routine_name, parameters.ordinal_position;

SELECT format('%I.%I(%s)', ns.nspname, p.proname, oidvectortypes(p.proargtypes)) 
FROM pg_proc p INNER JOIN pg_namespace ns ON (p.pronamespace = ns.oid)
WHERE ns.nspname = 'my_namespace';

------
to delete a function from database - 

drop function tofloat(text);
---------------------------------------
Here are the dump commands: 
 
pg_dump  -s -S postgres "db_name" |gzip > "db_name.shema.sql" 
pg_dump -S postgres -a -Fc "db_name" > "db_name.data.dump" 
 
So restore twice the schema with the following command: 
 
psql -e "db_name" < "db_name.shema.sql" 
psql -e "db_name" < "db_name.shema.sql" 
 
pg_restore -v
------
to use ilike on more than 1 value , use similar to - 

select
  drug_name
  , form_long
  , strength
  , num_claims
from drugs_with_ndc
where form_long similar to '(TABLET|CAPSULE)%'  
group by 1,2,3,4
order by 1,2,3,4;
------------------
sort ordering - 

in order by 1 asc, 2 desc
null is considered as the highest value in ascending order. 

but max() and min() exclude the null values during computation
---------
select drug_name,
  form_long,
  strength,
  num_claims,
  dense_rank() over (partition by 1,2,3 order by num_claims desc)

dense_rank() window function gives a rank of 1 to NULL and a rank of 5763 to the actual winner which is the entry with 271 claims.

so obviously its not working properly. 

MAX() with awindowing function was picking only 1 window with the HIGHEST CLAIMS. this is obviously different from what we wanted in this context.
-----------

example of HAVING query - having condition should always be a boolean and should appear after group by and before order by

select drug_name,
  form_long,
  strength,
  max(num_claims)
from drugs_with_ndc
where form_long similar to '(TABLET|CAPSULE)%' and not is_obsolete
group by 1,2,3
having max(num_claims) is null
order by 1,2,3;
------

1) in postgres: 
left join with 1 of the join keys in the left table is null causes all entries from right table to be nulled out. 
eg: even when we have num_claims=null , we want to pick non-null ndc from the right table. 

2) its picking the wrong ndc when doing the join based on num_claims when num_claims is not included in the join. 

if including num_claims in the join, 

3) greenplum_functions.sql - review new function 
----------------

SELECT gp_segment_id, count(*)
FROM app_priceable_units
GROUP BY gp_segment_id
ORDER BY 2;

This will give an idea of the skew between the segments. It should be really minimal, as that column has a high degree cardinality.
-----------
when you dont want to group by certain columns like drug_ndc but you still want it in the rolled up result  to reconstruct later, 
use arrag_agg() function.  its a very memory intensive operation though. 

example usage - 

select drug_ndc_code, 
   count(*) as num_claims,
   array_agg(prescription_days_supply)
from rx_claims
group by 1;
--------------
get first element from array - 
select ndc_array[1] as ndc

------------
create sequence ssg start with 1;
-------
CASE statement - when none of the when conditions match and there is no else, default value is NULL
-------

is there  a way to use WITH...UPDATE together as a CTE? 

this works but maybe inefficient with 2 nested sub-selects - 
update tmp_rx_esi_all_data
set is_default=true
from (select ndc_array[1] as ndc
      from
        (select drug_name, max(num_claims), array_agg(ndc order by num_claims desc) as ndc_array
         from tmp_rx_esi_all_data
         group by 1)tmp
      where max>0)default_drug_group_ndc
where tmp_rx_esi_all_data.ndc=default_drug_group_ndc.ndc;

but this doesnt - 
with default_drug_group_ndc as (
select ndc_array[1] as ndc
from 
(select drug_name, max(num_claims), array_agg(ndc order by num_claims desc) as ndc_array
from tmp_rx_esi_all_data
group by 1)tmp
where max>0)
  update tmp_rx_esi_all_data    
  set is_default=true
  where tmp_rx_esi_all_data.ndc=default_drug_group_ndc.ndc;

postgres 9.1 has a new statement UPSERT (update/insert) but we use postgres 8.4
-----------------
postgres foregin key specification example - automatically throws error to maintain database referential integrity if the foreign key entry row doesnt exist in the primary table. 

CREATE TABLE weather (
        city      varchar(80) references cities(city),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
--------
for cumulative distribution - 
cume_dist() over (order by #{numeric_col}

min(#{numeric_col}) over (partition by #{numeric_col}_octile)
--------
UNION ALL doesnt guarantee distinct in the 2 sets. 

UNION ensures different sets dont have duplicates and is hence slower.
---------
EXISTS vs IN - 
if there are 100 entries in the IN array, use exists instead. 


 Correlated EXISTS subquery

SELECT * FROM t1 WHERE 
            EXISTS (SELECT 1 FROM t2 WHERE t2.x = t1.x);
Greenplum Database uses one of the following methods to run CSQs:

Unnest the CSQ into join operations--This method is most efficient, and it is how Greenplum Database runs most CSQs, including queries from the TPC-H benchmark.
Run the CSQ on every row of the outer query--This method is relatively inefficient, and it is how Greenplum Database runs queries that contain CSQs in the SELECT list or are connected by OR conditions.

http://gpdb.docs.pivotal.io/4320/admin_guide/query.html
examples on how to re-write them - 

--original query
SELECT T1.a,
      (SELECT COUNT(DISTINCT T2.z) FROM t2 WHERE t1.x = t2.y) dt2 
FROM t1;

--rewritten query 
SELECT t1.a, dt2 FROM t1 
       LEFT JOIN 
        (SELECT t2.y AS csq_y, COUNT(DISTINCT t2.z) AS dt2 
              FROM t1, t2 WHERE t1.x = t2.y 
              GROUP BY t1.x) 
       ON (t1.x = csq_y);
-----
CSQs connected by OR Clauses can be re-written with UNION
--original query 
SELECT * FROM t1 
WHERE 
x > (SELECT COUNT(*) FROM t2 WHERE t1.x = t2.x) 
OR x < (SELECT COUNT(*) FROM t3 WHERE t1.y = t3.y)

--rewritten query 
SELECT * FROM t1 
WHERE x > (SELECT count(*) FROM t2 WHERE t1.x = t2.x) 
UNION 
SELECT * FROM t1 
WHERE x < (SELECT count(*) FROM t3 WHERE t1.y = t3.y)
--NOTE - Subplan nodes in the query plan indicate that the query will run on every row of the outer query, and the query is a candidate for rewriting.


------------
EXPLAIN and ANALYSE - executes the query to see how long each piece takes, 
but EXPLAIN is just an estimate. 

if stats are off, EXPLAIN estimates can be way off. 

-- EXPLAIN ANALYZE runs the statement in addition to displaying its plan. This is useful for determining how close the planner’s estimates are to reality.
EXPLAIN ANALYZE SELECT * FROM names WHERE id=22;

--Cost is measured in disk I/O, shown as units of disk page fetches.
---------------
--using regexp matches to convert type cast from text to boolean for use in where clause - use the ~ operator 

select * from table where name ~ 'foo'
--The '~' operator produces a boolean result for whether the regex matches or not rather than extracting the matching subgroups.
-----------------

custom sort order (untested) - 

ORDER BY idx(array['Nails','Bolts','Washers','Screws','Staples','Nuts'], s.type)
This is much easier to follow. Nails will be sorted first and nuts sorted last.

----------------------------
this works for what i want - 

select tmp.drug_name, form_long, package_size, strength, 
  row_number() over (partition by drug_name 
 order by form_long,package_size, strength 
 ) as rank   
from tmp_rx_esi_all_data tmp
join singleton_form_drugs using (drug_name)
group by 1,2,3,4
order by 1,2,3,4;


now just take care of ordering.
----------

adding a SERIAL rownumber() column in postgres - 

alter table drug_form_priority add priority serial;
alter table drug_form_priority add primary key (priority);

ALTER FUNCTION name ( [ [ argmode ] [ argname ] argtype [, ...] ] )
SET SCHEMA new_schema;

alter function array_enumerate(anyarray) set schema reference;
alter function array_enumerate(anyarray) rename to array_enumerate_v1;
-------------
trying to use fuzzy string matching using postgres function levenshtein distance - in revenge code - there is a sql ddl cmd to create it - - 

on bam0, sudo su - gpadmin 
cd /usr/local/greenplum-db/share/postgresql/contrib/fuzzystrmatch-gp-4.0.4.0
psql -f fuzzystrmatch.sql -d username_full (by default goes to public schema, might want to put it in different schema by setting/modifying `search_path` in *.sql file)

from dbconsole, (for all tables including employers in config_master)
set role dev; GRANT ALL PRIVILEGES ON table warehouse.buckets TO username;
alter table buckets owner to username;

--changing ownership of a sequence in postgres 8.3

--below dont work
--alter table provider_affiliations alter sequence provider_affiliations_id_seq owner to pd_user;
--alter table provider_affiliations owner to pd_user cascade;
--alter sequence provider_affiliations_id_seq owner to pd_user;

--how to detach sequence from  a table definition?
ALTER TABLE dtab ALTER COLUMN i DROP DEFAULT;
ALTER SEQUENCE dtab_i_seq OWNED BY NONE;
DROP SEQUENCE dtab_i_seq;
--------
select postgis_version();
select version(); --finds the greenplum versionn; on gp3m2 we have 
--PostgreSQL 8.2.15 (Greenplum Database 4.3.5.3 build 2) on x86_64-unknown-linux-gnu, compiled by GCC gcc (GCC) 4.4.2 compiled on Aug 14 2015 16:50:26
--bam upgrading to 4.3.4.2

create table strength_float as 
select ndc, replace(unnest(regexp_matches(tmp1.strength, E'[\\d+\|\.|,]*')), ',', '') as str_float, tmp2.strength 
  from tmp_rx_esi_all_data tmp1
join tmp_rx_esi_all_data tmp2 using (ndc);

select 
  ndc
  ,case when length(str_float)=0 then 0::numeric(12,5
) else tonumeric(str_float)::numeric(12,5) end as strength_float, strength
from strength_float;

select ndc,to_number(str_float), strength
  from strength_float
order by 2;
  ---------------------

select esi.drug_name, unnest(regexp_matches(esi.strength, E'[\\d+\|\.]*')), esi.package_size, array_agg(ndc)
from tmp_rx_esi_all_data esi
join   
(select tmp.drug_name
from
(select
  drug_name
  ,count(distinct form_long) as num_forms
from tmp_rx_esi_all_data
where drug_name not in
      (
        select drug_name from tmp_rx_esi_all_data where is_default
      )
group by 1
order by 1)tmp
where num_forms=1)singleton_forms using (drug_name)
group by 1,2,3
order by 1,2,3;

-----------------
create table singleton_form_drugs as 
select drug_name 
from 
(select 
  drug_name
  ,count(distinct form_short) as num_forms
from tmp_rx_esi_all_data
where drug_name not in (
  select drug_name
  from tmp_rx_esi_all_data
  where is_default
) 
group by 1)tmp
where num_forms=1;


--experimenting  with ranking functions, this works. 
update tmp_rx_esi_all_data
set is_default=true
from(
select tmp.drug_name, form_long, package_size, strength, 
  row_number() over (partition by drug_name 
 order by form_long,package_size, strength 
 ) as rank, 
  lowmem_array_agg(ndc order by form_long,package_size, strength) as ndc
from tmp_rx_esi_all_data tmp
join singleton_form_drugs using (drug_name)
group by 1,2,3,4)tmp 
where rank=1 and tmp.ndc[1]=tmp_rx_esi_all_data.ndc;
----------
update #{staging_table_name}
set is_default=true
from 
(select 
  tmp.drug_name
  , priority
  , package_size
  , strength_indicator
  ,dense_rank() over (partition by drug_name
    order by priority,package_size,strength_indicator
    ) as rank,
  lowmem_array_agg(ndc order by priority,package_size, strength) as ndc
from rx_esi_staging tmp 
  join drug_form_priorities using (form_long)
where drug_name not in
      (select drug_name
       from rx_esi_staging
      where is_default)  
group by 1,2,3,4)w
where rank=1
  and w.ndc[1]=#{staging_table_name}.ndc;
-----------
drop table public.ndcs cascade;

CREATE INDEX "idx_drug_name" ON "drugs" ("drug_name");

CREATE INDEX "idx_ss_id" ON "ndcs" ("ss_id");

CREATE INDEX "idx_ssg_id" ON "synonymous_subgroups" ("ss_id");

CREATE INDEX "idx_rx_ss_id" ON "rx_esi_web_services_form_options" ("ss_id");

CREATE INDEX "idx_rx_drug_name" ON "rx_esi_web_services_form_options" ("drug_name");
------------------
greatest() and least() in postgres. 

,case when dwn.is_pill
          then prescription_days_supply* least(10, prescription_quantity_dispensed/prescription_days_supply)

        else
          case when prescription_quantity_dispensed<=10
            then prescription_quantity_dispensed
            else greatest(least(10, floor(prescription_quantity_dispensed/dwn.package_size)),1)
          end
        end as estimated_quantity

------------------------
to restart gpfdist server - 
gpfdist -d /data/gpfdist -p 8081 -l /data/gpfdist/gpfdist_2.log &

------
dump table from postgres to csv - 
SqlUtils.dump_via_gpfdist_or_copy :rx_esi_web_services_form_options, "/home/username/rx_esi_tables_data/v3/rx_esi_web_services_form_options.csv"

COPY rx_esi_form_options TO '/home/username/rx_esi/v4/rx_esi_form_options.csv' DELIMITER ',' CSV HEADER;
COPY rx_esi_drugs TO '/home/username/rx_esi/v4/rx_esi_drugs.csv' DELIMITER ',' CSV HEADER;
COPY rx_esi_ndcs TO '/home/username/rx_esi/v4/rx_esi_ndcs.csv' DELIMITER ',' CSV HEADER;
COPY rx_esi_synonymous_subgroups TO '/home/username/rx_esi/v4/rx_esi_synonymous_subgroups.csv' DELIMITER ',' CSV HEADER;

dump postgres table  sorted to tsv with header - 
copy (select * from test order by a,b) to '/tmp/rbb_price_lists.tsv' HEADER;


if you want to escape quotes - it works only in csv mode - 
\copy deduped_providers_482xx from /home/username/data/deduped_providers_482xx.tsv quote '''' header;

\copy deduped_providers_482xx to '/home/username/data/dumped_deduped_providers_482xx.tsv' header null as '';
instead of \N as null, its represented as empty string
-----------
to find the aggregate mode - 

  def self.aggregate_mode_of_rx_parameter rx_claim_column_name
    table_name="#{rx_claim_column_name}_by_ndc"
    Sql.create_temporary_table_as table_name, <<-EOSQL
      select
        drug_ndc_code
        ,#{rx_claim_column_name}
      from(
        select
           tmp.*
           ,row_number() over (partition by drug_ndc_code order by cnt desc)
        from(
           select
              drug_ndc_code
              ,#{rx_claim_column_name}
              ,count(*) as cnt
           from rx_claims
           where #{rx_claim_column_name}>0
           group by 1,2)tmp
      )t2
      where row_number=1;
    EOSQL
  end
--------------
CREATE OR REPLACE FUNCTION min_date_greater_than(date, date, date)
  returns date as $$
declare 
  tmp_date1 date;
  tmp_date2 date;
  date1 alias for $1;
  date2 alias for $2;
  cutoff_date alias for $3;
  return_date date;
begin
  tmp_date1 = case when date1<=cutoff_date or date1 is null then null else date1 end;
  tmp_date2 = case when date2<=cutoff_date or date2 is null then null else date2 end;
  select least(tmp_date1, tmp_date2) into return_date;
  return return_date;
end;
$$ language 'plpgsql' immutable;
----------------

insert into rx_fdb_pkg_description_mappings
    values ('AER_REF', 'Aerosol, Refill Unit'), ('AER_W/ADAP','Aerosol with Adapter');

to insert null value into an integer column - 
insert into test values (NULL);

although while reading from a tsv file \N is considered as a NULL;
----------------
postgres/greenplum on mac - 

There's a 'pg_config' executable that postgres uses to properly configure compilation, and after installing greenplum, you now have one for your postgres client (not sure where yours is, but mine is in /opt/local/lib/postgresql84/bin/pg_config) and one for the greenplum server (which  should be in /usr/local/greenplum-db-4.2.1.0/bin/pg_config).
Irritatingly, the server one seems to not work properly when compiling some things, so in order to get that 'working' I've had to take the configuration that it comes up with and modify it slightly by hand.
------------------
WITH statement with self join  - 

-- can different ndcs within sg be OTC and non-OTC ? 
select distinct synonymous_subgroups_id from (
with t1 as (
  select 
    dwn.ndc
    ,dwn.expiry_date
    ,dwn.is_over_the_counter
    ,synonymous_subgroups_id
  from drugs_with_ndc dwn
    join rx_esi_ndcs ren using (ndc)
    join rx_esi_staging using (ndc) 
  where is_default)
select *
from t1
  join t1 as t2 using (synonymous_subgroups_id)
where t1.ndc!=t2.ndc
  and t1.is_over_the_counter 
  and not t2.is_over_the_counter)t3;
--------
select decile*10 decile, max(unit_drug_price) as unit_drug_price, count(*) as num_claims
from
(select unit_drug_price
  ,ntile(10) over (partition by synonymous_subgroups_id
  order by unit_drug_price) decile
from rx_claims_sg_variance
where 
  synonymous_subgroups_id='4088'
  and prescription_service_date>='2015-01-01'
  and pharmacy_ncpdp_id='1562760')tmp
group by 1;

--problem statement : table has 2 columns - (term,frequency)
-- calculate percentile_frequency of term from 0 to 100 where 0 is least frequent and 100 is most frequent;
select
  term
  ,frequency
  ,ntile(100) over (order by frequency) as frequency_percentile
from term_frequency
order by frequency desc;
-----------
installing new greenplum modules - 
to find where to install lib modules - as gpadmin, 

pg_config --pkglibdir

usually above returns a path like 
/usr/local/greenplum-db/lib/postgresql

---------------
matching hidden ascii characters like \r \n \t in postgres char-varying columns - 

\r has ascii code 13 and is found in most of the places as the last character. 

select
  drug_name
  ,ascii(substring(drug_name,length(drug_name)))
from rx_esi_staging

--------
this works as wel to strip the strings of \r endings -
select 
  drug_name
  ,length(drug_name)
  ,rtrim(drug_name,'\r')
  ,length(rtrim(drug_name,'\r'))
from rx_esi_staging
where drug_name ilike '%adenosine%'; 

drug_name	length	rtrim	length
"ADENOSINE"	10	ADENOSINE	9
--------------------
you can kinda transpose columns and rows using the database concept of pivot table, supported using greenplum 9.1 module tablefunc(), function crosstab()

or you can use the following query and get the same effect without that module
SELECT section,
       SUM(CASE status WHEN 'Active' THEN count ELSE 0 END) AS active,
       SUM(CASE status WHEN 'Inactive' THEN count ELSE 0 END) AS inactive
FROM t
GROUP BY section;

another example - 
id | class | a1 | a2 | a3 
----+-------+----+----+----
  1 | C1    |  1 |  2 |  3
  2 | C1    |  1 |  4 |  3
  3 | C2    |  0 |  2 |  2
  4 | C1    |  1 |  2 |  1
  5 | C2    |  1 |  2 |  2
  6 | C2    |  0 |  1 |  3

to convert above table to the form below
 id | class | attr | value
----+-------+------+-------
  2 | C1    | A1   |     1
  2 | C1    | A2   |     2
  2 | C1    | A3   |     1
  4 | C2    | A1   |     1
  4 | C2    | A2   |     2
  4 | C2    | A3   |     2
  6 | C2    | A1   |     0

CREATE view class_example_unpivot AS
SELECT id, class, unnest(array['A1', 'A2', 'A3']) as attr, 
unnest(array[a1,a2,a3]) as value FROM class_example; 


--unnest() returns its output in the same order as the input.

--Performance of regexp_split_to_table() degrades with long strings. unnest(string_to_array(...)) scales better

--parallel unnesting is guaranteed to be in sync (as long as all arrays have the same number of elements)".  It's just the order of the rows (each row taken as a whole) that's arbitrary.
http://stackoverflow.com/questions/23830991/parallel-unnest-and-sort-order-in-postgresql
------------------
how to check the greenplum master hostname - 
select distinct hostname from gp_segment_configuration where content = -1;

----------
named windowing functions are possible in greenplum/postgres - 

WINDOW correlated_sequences AS (PARTITION BY correlation_key, priceable_type_id, price_sequence_id)

and then just use it with a windowing function: MAX(...) OVER (correlated_sequences)
--------
to find out the schema that a table name belongs to - 
select * from pg_tables where tablename like '%xyz%';
-------
--create new schema 
CREATE SCHEMA myschema;
----------------------
full text search index - 
create index post_tsidx on post using gin(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')));

---------------
operation | total_size_in_mem | total_size_on_disk | size_per_segment | skew
-----------+-------------------+--------------------+------------------+------
 Sort      | 1871 kB           | 6729 MB            | 224 MB           | 0.14
 Hash Join | 1866 kB           | 1406 MB            | 47 MB            | 0.03

Previously
 operation | total_size_in_mem | total_size_on_disk | size_per_segment | skew
-----------+-------------------+--------------------+------------------+------
 Sort      | 932 kB            | 1572 GB            | 52 GB            | 0.1

------------------------

clone schema - may not copy functions and views. 

CREATE OR REPLACE FUNCTION clone_schema(source_schema text, dest_schema text) RETURNS void AS
$BODY$
DECLARE 
  objeto text;
  buffer text;
BEGIN
    EXECUTE 'CREATE SCHEMA ' || dest_schema ;
 
    FOR objeto IN
        SELECT TABLE_NAME::text FROM information_schema.TABLES WHERE table_schema = source_schema
    LOOP        
        buffer := dest_schema || '.' || objeto;
        EXECUTE 'CREATE TABLE ' || buffer || ' (LIKE ' || source_schema || '.' || objeto || ' INCLUDING CONSTRAINTS INCLUDING INDEXES INCLUDING DEFAULTS)';
        EXECUTE 'INSERT INTO ' || buffer || '(SELECT * FROM ' || source_schema || '.' || objeto || ')';
    END LOOP;
 
END;
$BODY$
LANGUAGE plpgsql VOLATILE;
Execution is simple:

SELECT clone_schema('old_schema','new_schema');

-------------------------------------------
dump tables from 1 databse and copy it into another database 
pg_dump -t <schema-name.source-table-name> -h <source-host-name> <source-database-name> | psql -h <destination-host-name> -U <destination-user> -p <destination-port> <destination-database>

pg_dump -t table_to_copy source_db | psql target_db

example -
pg_dump -h <SERVER_FQDN> -p 5432 -t provider_master_prod_v5_10.locations prov_dir | psql -h <SERVER_FQDN> -p 5432 -d provider_directory -w


pg_dump -p 5432 -h <SERVER_FQDN> -U username -t provider_master_prod_v5_10.groups prov_dir | psql -p 5432 -h <SERVER-FQDN> -U username -d prov_dir_username

note:  if destination schema (namespace) does not exist of the same name as source schema (namespace), then copied tables are put in public namespace of the destination DB

then change the schema from public to your desired schema using the command below - 
ALTER TABLE name SET SCHEMA new_schema;
--------
create table  aetna_deduped.locations (like public.locations INCLUDING CONSTRAINTS INCLUDING INDEXES INCLUDING DEFAULTS);

--using comma separated column split to postgres array data type and then SQL query to  access them element-wise 


create table practitioner_componentized as
select
  tmp.id
  ,tmp.display_name
  ,tmp.a[1] as last_name
  ,tmp.a[2] as first_middle
  ,tmp.a[3] as degree_postscript  
  ,tmp.a[4] as additional_degrees
from (
    select
      regexp_split_to_array(display_name, ',') as a
      ,p.id
      ,p.display_name
    from providers p
    where p.provider_type='practitioner'
) tmp;
------
regexp_split_to_array(display_name, ',')
array_length
array_append
array_prepend
array_cat

--next challenge - how to compress different columns like phon_number1, fax into array elements without doing a group-by ?
--how to do the opposite which is accumulate primary_phone, secondary_phone, fax from multiple columns 
--as comma separated values in 1 column - 
string_to_array((COALESCE(primary_phone,'') || ',' || COALESCE(secondary_phone, '') || ',' || COALESCE(fax, '')),',')
--------

or use 
SELECT concat(col_a, col_b);
http://www.postgresql.org/docs/current/interactive/functions-string.html#FUNCTIONS-STRING-OTHER
------------------------------------
--above is not-supported in our version of postgres 8.2 (8.4?); 
--try to back-port stored-procedure from postgres 9.1 into our version of greenplum 

/*
The concat, concat_ws and format functions are variadic, so it is possible to pass the values to be concatenated 
or formatted as an array marked with the VARIADIC keyword (see Section 35.4.5). The array's elements are treated as 
if they were separate ordinary arguments to the function. If the variadic array argument is NULL, concat and concat_ws 
return NULL, but format treats a NULL as a zero-element array. */

/*
concat_ws
'ws' means 'with separator'.
Feature	code	PostgreSQL 9.1	behaviour summary - 
non-text args	| concat_ws(',', 'a', 123)	           | a,123
NULL args	    | concat_ws(',', 'a', NULL)	           | a	
3+ args	      | concat_ws(',', 'a', 'b', 'c')        | a,b,c	
NULL separator|	concat_ws(NULL, 'a', 'b')	           | NULL
all combos    | concat_ws(',', 'abcde', 2, NULL, 22) | abcde,2,22
*/

create or replace function concat_ws(separator text, variadic text[], out concat_str text) returns text as $$
begin
    select into concat_str array_to_string($2, separator);
end;
$$ language plpgsql;

------------------
define array_enumerate - 
CREATE OR REPLACE FUNCTION array_enumerate(IN a anyarray,
  OUT i integer, OUT e anyelement)
  RETURNS SETOF record AS
$BODY$
/**
 *  Unnests array into a table together with element indexes
 */
 /* -- testing
     select * from array_enumerate(ARRAY['a', 'b', 'c']) as u
  */
select s.i, ($1)[s.i] from generate_subscripts( $1, 1 ) as s(i)
$BODY$
  LANGUAGE 'sql' IMMUTABLE STRICT;


use it as - 

select ARRAY(
  select s.e
    from utils.array_enumerate(ARRAY[0,4,2,5,4,1,6,9,8,7]) as s(i,e)
   where s.i % 2 = 0
   order by s.i
);
-----------------
--drugs_with_ndc is loaded once, hardly updated ever and frequently used in analytical querying, its the perfect candidate for append-only storage instead of heap storage in greenplum GPDB

--plns table distribute by provider_id (can use local joins if providers table is also distributed by id), partition by ACTIVE/INACTIVE;
--partitioning greenplum tables examples and fundaes
--http://gpdb.docs.pivotal.io/4350/admin_guide/ddl/ddl-partition.html


--ERROR:  PRIMARY KEY and DISTRIBUTED BY definitions incompatible
--HINT:  When there is both a PRIMARY KEY (pln.id), and a DISTRIBUTED BY (pln.provider_id) clause, the DISTRIBUTED BY clause must be equal to or a left-subset of the PRIMARY KEY

SELECT partitionboundary, partitiontablename, partitionname, 
partitionlevel, partitionrank 
FROM pg_partitions 
WHERE tablename='sales';

--providers_locations_networks_optimized
CREATE TABLE "providers_locations_networks" (
  "id" serial NOT NULL,
  "source" varchar DEFAULT 'MASTER'::character varying,
  "active_flag" character varying(8) check( active_flag in ('ACTIVE','INACTIVE')) DEFAULT 'ACTIVE'::character varying,
  "provider_id" integer,
  "location_id" integer,
  "network_id" integer,
  "contact_id" integer,
  "type" character varying(8) check( type in ('','BILLING','PRACTICE')) DEFAULT ''::character varying,
  "created_at" timestamp without time zone,
  "updated_at" timestamp without time zone
  --CONSTRAINT providers_locations_networks_pkey PRIMARY KEY("id")
)WITHOUT OIDS
  distributed by (provider_id)
  partition by list(active_flag)
  ( PARTITION pln_active VALUES ('ACTIVE'),
  PARTITION pln_inactive VALUES ('INACTIVE'));

child tables 
-----------
select split_part(one_column, ' ', 1),split_part(one_column, ' ', 2)
to split on space in string
-----------------
--phone numbers, fax normalizing using translate function in postgres

select 
  phone
  ,translate(phone, '()- ', '') as normalized_phone
from 
(select 
  provider_id
  ,unnest(phone_nums) as phone
from test_phone_num
where provider_id=364)t  
where provider_id=364;
---------------------------------

--having a boolean true in join on condition will do a cross-join, you can create temp table within the join clause on the fly for tiny joins - 

   SELECT DISTINCT
        sswpt.synonymous_subgroups_id,
        dpg.insurance_company_id,
        dpg.employer_id,
        mo.mail_order,
        MAX(CASE WHEN qa.quantized_days_supply = 30 THEN
            COALESCE(#{coalesce_args}) END) AS unit_drug_price_30day,
        MAX(CASE WHEN qa.quantized_days_supply = 90 THEN
            COALESCE(#{coalesce_args}) END) AS unit_drug_price_90day
      FROM rx_esi_synonymous_subgroups_with_priceable_types sswpt
        -- Duplicate across mail_order values
        INNER JOIN (VALUES (TRUE), (FALSE)) mo(mail_order) ON TRUE
        -- Duplicate across days_supply values
        INNER JOIN (VALUES (30), (90)) qa(quantized_days_supply) ON TRUE
        -- Duplicate across drug plan groupings
        INNER JOIN drug_plan_groupings dpg
          ON dpg.employer_id IN (#{Db.current_layer.employers.map(&:id).to_commad_s});
---------------------------------
--For compressed data, an index access method means only the necessary rows are uncompressed.
--  http://gpdb.docs.pivotal.io/4350/admin_guide/ddl/ddl-index.html

--below some greenplum specifics about EXPLAIN ANALYZE and reading query plans
http://gpdb.docs.pivotal.io/4320/admin_guide/query.html
/*
The first estimate in explain analyze is the start-up cost of getting the first row and the second is the total cost of cost of getting all rows. The total cost assumes all rows will be retrieved, which is not always true; for example, if the query uses LIMIT, not all rows are retrieved.

In Greenplum Database, a gather motion is when segments send rows to the master.

Gather Motion 2:1 (slice1)
means that there are two segment instances that send to one master instance. This operation is working on slice1 of the parallel query execution plan. A query plan is divided into slices so the segments can work on portions of the query plan in parallel.

cost=0.00..20.88
means that The estimated startup cost for this plan is 00.00 (no cost) and a total cost of 20.88 disk page fetches.

optimizing join ordering 
make sure that the planner chooses the most selective join order. Joins that eliminate the largest number of rows should be done earlier in the plan so fewer rows move up the plan tree.

Question: when to use append-optimized storage vs columnar storage in greenplum? 


answer:
 Append-only
table storage favors denormalized fact tables in a data warehouse environment, which
are typically the largest tables in the system. 

Moving large fact tables to an append-only storage model eliminates the storage
overhead of the per-row update visibility information (about 20 bytes per row is
saved). This allows for a leaner and easier-to-optimize page structure. Append-only 
tables do not allow UPDATE and DELETE operations. 

The storage model of append-only
tables is optimized for bulk data loading. Single row INSERT statements are not
recommended.

Source: Creating and Managing Tables 72
Greenplum Database Administrator Guide 4.0 – Chapter 9: Defining Database Objects

default = heap storage (vs append-only), row-oriented (vs columnar) storage
*/

 CREATE TABLE bar (a int, b text)
 WITH (appendonly=true)
 DISTRIBUTED BY (a);

--to create columnar storage 
CREATE TABLE bar (a int, b text)
 WITH (appendonly=true, orientation=column)
 DISTRIBUTED BY (a);
-------------------------
Use the following query to see the data skew for your table

SELECT gp_segment_id, count(*)
FROM schema.table
GROUP BY gp_segment_id;
------------------
--Use the following command to clear the memory accumulated by the table after DELETE or TRUNCATE
Alter table schemaname.tablename set with (reorganize=true);

--I guess the gp_autostats_mode  is not set to on_change.
Make sure the ANALYZE is done on regular basis for all the frequently used tables so that the plan chosen would be optimal.
----------
using madlib term_frequency function - 

set search_path to suhas,demandforce_madlib;

create table tmp_madlib_tf_test(provider_name varchar
,docid integer, words text[]);

insert into tmp_madlib_tf_test
select
  provider_name
  ,1
  ,regexp_split_to_array(lower(provider_name),' ')
from demandforce_providers;

select
  madlib.term_frequency('tmp_madlib_tf_test','docid','words', 'document_tf');
--1 row retrieved starting from 1 in 13s 508ms (execution: 13s 505ms, fetching: 3ms)

select *
from document_tf;

-------------------
MASTER_DATA_DIRECTORY=/data/master/gpseg-1
export MASTER_DATA_DIRECTORY
----------------------

--STEP 1.5 -convert address string to term array
select
  pln_id
  ,array_agg(word) as term_array
from(
  select
    pln_id
    ,unnest(string_to_array(phrase,' '))as word
  from
    (select
      pln_id
      ,unnest(string_to_array(address,','))as phrase
    from tmp_practitioners_boston_cbsa
    where pln_id='161398415')phrases
)words
where length(word)>0
group by 1;
-----------------

select
    c.column_name,
    c.data_type,
    c.character_maximum_length as data_length,
    e.data_type as element_type
from
    information_schema.columns c
    left join information_schema.element_types e on (
        c.table_catalog = e.object_catalog and
        c.table_schema = e.object_schema and
        c.table_name = e.object_name and
        'TABLE' = e.object_type and
        c.dtd_identifier = e.collection_type_identifier
    )
where
    c.table_name = 'mvp_prov_dir' and
    c.table_schema = 'mvp'
order by c.ordinal_position;
----------------
create external table in greenplum - 

   create external table _gpfdist.mvp_prov_dir
                ( insurer_specific_uniq_prov_identifier character varying(14))
            location (
                'gpfdist://den-<SERVER>.ch.int:<PORT>/whdata/my_file.csv'
                )
            format 'csv' (header delimiter as ',' fill missing fields);
--------------------
change/switch  database connection from within psql shell to another database - 
\c prov_dir_username

-------------------------
SELECT max(octet_length(mailing_address_sha1)) from npi_raw;
tells how many bytes each sha1 column value occupies
-----------
python util/dev_plntest_restore.py --mode=single_table --schema=provider_master_prod_pre_v5_12 --table_file_path=/data/gpfdist/username_real/insurance_networks.txt --table_name=insurance_networks --gpfdist_url=gpfdist://den-<SERVER-FQDN>:8081 --gpfdist_path=/data/gpfdist/
---------------

--pivotal greenplum query optimization works for correlated subqueries also, (CSQ) which are queries where the inner query references the outer query's tables like below example - 

SELECT * 
FROM part p1
WHERE price > (SELECT avg(price) 
							 FROM part p2 
							 WHERE  p2.brand = p1.brand);

--CSQ can also be used in select clause as follows - 
SELECT *,
 (SELECT min(price) 
  FROM part p2 
  WHERE p1.brand = p2.brand) AS foo
provider_participation_attributes is missing in the greenplum export and needs to be there;
FROM part p1;
---------------------------
--search for table name and schema name in all schemas 
select table_schema 
from information_schema.tables 
where table_name = 'master_facility_preprocessed';
-----------------------
--handling multi-line json records dumped with mysqldump have '\' line continuation character which is actually \\n
--and true row ending is a \n. inserting this into postgres requires some vim pre-processing to find and replace \\n with a whitespace charcter
--followed by gpfdist load.
%s/\\\n/ /gc

have to unix-parallelize the above find and replace now using sed or awk wrapped in python
---------------------
--new in postgres 9.1 to be compatible with mysql - its not in the SQL standard

DO $$
DECLARE lastid int;
BEGIN
insert into data_source(
  data_source_name
  ,data_source_display_name
  ,active_flag
  ,created_by
  ,created_at
  ,modified_by
  ,modified_at) VALUES(
  'bte'
  ,'Bte'
  ,1
  ,'username'
  ,NOW()
  ,'username'
  ,NOW()) 
  RETURNING data_source_id INTO lastid;

  SELECT * FROM data_source WHERE data_source_id = lastid;
END $$;
------------------------
--postgres - restart sequence from max id by default to avoid this error on serial id columns- 
--IntegrityError: duplicate key violates unique constraint "insurance_company_data_files_pkey"  (seg2 den-gp2-seg02:40000 pid=7385)
SELECT setval('hospitals_hosp_id_seq', (SELECT MAX(hosp_id) FROM hospitals));

--unique constraint vs unique index
No need to create an index explicitly for the primary key columns. Greenplum Database automatically creates an index for each unique constraint or primary key constraint to enforce uniqueness.)
http://www.greenplumdba.com/greenplum-database-users-faq/dosanddontsforgreenplumdatabaseusers

-------------------------
--To add a (multicolumn) unique constraint to a table:
ALTER TABLE distributors ADD CONSTRAINT dist_id_zipcode_key UNIQUE (dist_id, zipcode);

--add not null constraint
alter table hospitals alter column hosp_id set not null;

ALTER TABLE your_table DROP CONSTRAINT constraint_name;

select setval('seqname',select max(id) from tablename))
-------------
--postgres rules for on duplicate update or ignore syntax in mysql which exists in psql 9.5+ only

CREATE RULE "my_table_on_duplicate_ignore" AS ON INSERT TO "my_table"
  WHERE EXISTS(SELECT 1 FROM my_table 
                WHERE (pk_col_1, pk_col_2)=(NEW.pk_col_1, NEW.pk_col_2))
  DO INSTEAD NOTHING;
INSERT INTO my_table SELECT * FROM another_schema.my_table WHERE some_cond;
DROP RULE "my_table_on_duplicate_ignore" ON "my_table";

create rule
"t_anti_transparency_providers_on_duplicate_ignore"
as on insert to "t_anti_transparency_providers"
  where exists(select 1
               from t_anti_transparency_providers
               where (bucket_id, provider_id)=(NEW.bucket_id, NEW.provider_id))
   DO INSTEAD NOTHING;
--NEW is a keyword which can be used only within rules as an alias for the future to-be-inserted values

drop rule practitioner_test_data_on_duplicate_ignore on practitioner_test_data;
-----------------------------------------
find_in_set function is specific to mysql and returns index of matching entry in arg1 when queried for arg0; if not found, returns 0. works on comma separated varchar. 
JOIN bucket_lists bl ON FIND_IN_SET(bm.bucket_id,bl.rate_bucket_ids)
      AND b.name = bl.key

equivalent in postgres is - 
JOIN bucket_lists bl ON (b.name = bl.key and bm.bucket_id = ANY(string_to_array(bl.rate_bucket_ids, ',')))
---------
BEGIN;
CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER;
REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins;
COMMIT;

GRANT EXECUTE ON FUNCTION pymax(a integer, b integer) TO pd_user;
-------------------
--using serial gets value for each gp segment from a sequence server which has a network overhead. use cache 20 to optimize performance and minimize network overhead 

http://engineering.pivotal.io/post/SERIAL_Datatype_Performance_in_Greenplum_Database/
ALTER SEQUENCE id_sequence CACHE 20;
--this will retrieve the next 20 values from sequence server for each gp_segment server (having a segment DB) and store it in the segment server.
-----------------
--copying entire schemas from 1 DB into another using gputils (not pg_dump or gpdump) 
--gpcrondump is just a wrapper using gp_dump under the hood
gpcrondump -x prov_dir_stage -s public -u /data/backup/prov_dir_stage_dbs/medcost_mysql_v6_04
gpcrondump -x prov_dir_stage --schema-file='/home/gpadmin/username/provider_matching_schemas_to_copy.txt' -u /data/backup/provider_matching
gpcrondump -x prov_dir_username -t ska_raw_20160607t1303.preprocessed_facilities -t ska_raw_20160607t1303.ska_provider -u /data/backup/provider_matching

gpcrondump -x pd_production --table-file='/home/gpadmin/tables_to_copy.txt' -u /data02/tmp/
--tables_to_copy.txt can specify schema as below 
--provider_master_prod_pre_y2017_w23.providers
gpdbrestore -u /data02/tmp -s prov_dir_ssatish --noanalyze

edit /data/backup/prov_dir_stage_dbs/medcost_mysql_v6_04/db_dumps/<TS>/gp_cdatabase_<TS> prov_dir_username

gpdbrestore -u /data/backup/prov_dir_stage_dbs/medcost_mysql_v6_04 -s prov_dir_username --noanalyze
gpdbrestore -u /data/backup/provider_matching -s provider_matching --noanalyze

--schema-file=filename (copies all schemas)

--you can do the same as above without needing gpadmin priveleges using the cmd below 
pg_dump -t unlabeled_test_data.data_source -h den-<SERVER-FQDN> -U user_name prov_dir_username | psql -h den-<SERVER-FQDN> -U user_name prov_dir_user_name

----------------------
--alternate way of doing same thing as above
now copy data from 1 DB to another with pgdump or gpdump as follows - 
gp_dump prov_dir_username -n provider_master_prod_pre_v5_12_end_to_end_npi --gp-d=end-to-end-schema –s

gpcrondump -x prov_dir_username -s npi_raw_20160309t1855 -u /tmp/username_testing/

/tmp/username_testing/db_dumps/20160311/gp_cdatabase_1_1_20160311010607
CREATE DATABASE prov_dir_username WITH TEMPLATE = template0 ENCODING = 'UTF8' OWNER = pd_user;
gpdbrestore -u /tmp/username/ -s prov_dir_username —no-analyze
-----------------------
--to check storage space on each and every segment, login as gpadmin to gp2-master01 and run
gpssh -f /home/gpadmin/hostfile-seg 'df -h /data'


--to clean up historical gpperfmon data 
https://discuss.zendesk.com/hc/en-us/articles/203309923-Script-Cleanup-Maintenance-script-for-historical-gpperfmon-data
----------
--to reduce table bloat, whenevery large DML operations on a table, do
Alter table schemaname.tablename set with (reorganize=true); --redistributeing table removes table bloat
Analyze schemaname.tablename;

ALTER TABLE SET with (REORGANIZE=false) DISTRIBUTED randomly; -- only "marks" the table, but does not move rows. Finishes instantly.
ALTER TABLE SET with (REORGANIZE=true) DISTRIBUTED BY (<column name1>, <column name2>); -- rewrites the data files. As the distribution actually never changes on data file level, rewrite happens locally without sending rows over network.
------
--in greenplum updates are treated as delete + insert (multi version concurrency control) and no space is marked as free until you run the VACUUM command after all DML operations. 
--this dead space can be reclaimed as free space with vacuum

/*Full vacuum will lock tables and thus requires a downtime. However, vacuum
table is an online operation. It will not return free space to disk but
mark it to be available for reuse by future INSERTs. So we recommend that
you vacuum table along with your UPDATE and DELETE transactions periodically. */


gp_toolkit.gp_bloat_diag -- this view shows tables with moderate and significant amount of bloat
--Columns:
bdirelid -- Object ID of the table (pg_class.oid)
bdinspname -- table schema name
bdirelname -- table name
bdirelpages -- number of pages currently in table data files
bdiexppages --number of pages expected according to current statistics
bdidiag -- diagnosis of bloat (bdirelpages/bdiexppages  ratio from 1 to 3 -> no bloat, ratio from 4 to 10 -> moderate bloat, ratio > 10 -> significant bloat)

select * from gp_toolkit.gp_bloat_diag;

select * from gp_toolkit.gp_bloat_expected_pages limit 5;
 btdrelid | btdrelpages | btdexppages 
----------+-------------+-------------
    10789 |           1 |           1
btdrelid -- Object ID of the table (pg_class.oid)
btdrelpages -- number of pages currently in table data files
btdexppages -- number of pages expected according to current statistics

VACUUM FULL <schema-name>.<table-name>;
VACUUM FULL command -- This command compacts the table data by moving it at the front of the data file and truncates the unused space on the tail (from deletes).
VACUUM FULL compacts rows one by one and therefore is slow for big tables and also takes exclusive lock on the table.
VACUUM FULL execution is recommended in maintenance window and with careful consideration of the run-time and effects.
VACUUM FULL command should not be terminated by user once started.
Better alternative to VACUUM FULL for user tables is to "redistribute" the table (cannot be performed on system tables). This effectively rebuilds the table getting rid of the bloat in the process.

--to remove bloat on index, use below
REINDEX INDEX <index-name>;
REINDEX TABLE <bloated-table-name>;
------------------------
--3rd method CTAS (create table as select) exists to remove table bloat. This does not apply table level lock unlike 
--(a) vacuum and (b) redistribute  by above. Steps are below - 

pg_dump -s -t tt1  --this is to dump DDL of table, view, or sequence with full information about indexes, constraints, ownership, ACL etc in cascade 

INSERT INTO <schema-name>.<new-table-name> SELECT * FROM <schema-name>.<bloated-table-name>;
ALTER TABLE <schema-name>.<bloated-table-name> RENAME TO <old-table-name>;
ALTER TABLE <schema-name>.<new-table-name> RENAME TO <bloated-table-name>;
-- Once users confirm everything is good.
DROP TABLE <schema-name>.<bloated-table-name>;
-----------------------
--as gpadmin, you can login to master and delete data from any/all segment servers .
gpssh –f /home/gpadmin/hostfile-seg
--Then do 
cd /data
-------------
Use Bitmap indexes for low selectivity columns. The Greenplum Database Bitmap index type is not available in regular PostgreSQL. See About Bitmap Indexes.

Bitmap indexes are most effective for queries that contain multiple conditions in the WHERE clause. Rows that satisfy some, but not all, conditions are filtered out before the table is accessed. This improves response time, often dramatically.

number of unique values of a column/total number of rows = selectivity.
for unique index selectivity = 1 which is the best possible scenario to use regular b-tree indexes
for low selectivity columns, use a bitmap index.

Columns with fewer than 100 distinct values, such as a gender column with two distinct values (male and female), usually do not benefit much from any type of index. On a column with more than 100,000 distinct values, the performance and space efficiency of a bitmap index decline.

Bitmap indexes can improve query performance for ad hoc queries. AND and OR conditions in the WHERE clause of a query can be resolved quickly by performing the corresponding Boolean operations directly on the bitmaps before converting the resulting bitmap to tuple ids. If the resulting number of rows is small, the query can be answered quickly without resorting to a full table scan.

Bitmap indexes are not suitable for OLTP applications with large numbers of concurrent transactions modifying the data.

Use bitmap indexes sparingly. Test and compare query performance with and without an index. Add an index only if query performance improves with indexed columns.


-------------------
update test_lag_lead tll
set end_date=tmp.fixed_date
from
  (select lead(start_date,1,end_date) over(partition by location_id order by start_date) as fixed_date
      ,t.location_id
      ,t.start_date
   from test_lag_lead t
  )tmp
where tmp.location_id=tll.location_id
  and tmp.start_date=tll.start_date;

syntax- lead(column_name to see the lead of,step_size, default_value from the current step)
-------------------
--table DML audit information storing user_name or user_id from AD/LDAP who's connected to the DB (not role)
select current_user; --drawback: if role is set to pd_user, it returns the role. we dont want the role, but want the actual user
select current_database();
--------
--using multiple windowing fuctions in 1 query 
create table term_frequency_tradeoffs as
  select *
    , round(missed_pls / total_pls:: numeric, 4) frac_missed
    , round(redundant_terms / total_terms:: numeric, 4) frac_redundant
  from
    (select
       *,
       count(is_rarest_name_term or null) over (fwd) missed_pls,
       sum(case when is_next_rarest_term then num_terms end) over (rev) redundant_terms
     from term_ranks
     window w as (partition by cbsa, is_practitioner)
       , fwd as (w order by frequency desc, term )
       , rev as (w order by frequency, term desc )
    ) t
    join
    (select
       cbsa,
       is_practitioner,
       count(1) total_terms
     from cbsa_pl_terms
     group by 1, 2
    ) u using (cbsa, is_practitioner);
---------------------------
deterministic sequence - 
select setseed(0.5);
select 
   random()
from 
   generate_series(1,20);
-------
-- add id column to table with an integer not null sequence
create sequence practitioner_pairs_id_seq start with 1 cache 10000;
alter table practitioner_pairs add column id integer not null default nextval('practitioner_pairs_id_seq');

-----------
--to find the OID of a function in postgres, 
SELECT 'normalize_address_be493(text,text,text,text)'::regprocedure::oid;

--then dump only that function with
pg_dump -Fc -s | pg_restore -P 'normalize_address_be493(text,text,text,text)'
-----------
--to turn on query runtime display in psql console - 
\timing

------
--lpad zip code to 5 digits by prefixing 0 
lpad(zip_code, 5, '0')
------------------------
--copy greenplum table from 1 cluster to another 
pg_dump -t provider_master_prod.provider_affiliations -h den-<SERVER-FQDN> -U username pd_production -f /data02/backup/provider_affiliations_for_ska_run.sql
prov_dir_username=> \i /data02/backup/provider_affiliations_for_ska_run.sql
-------------------
--remove data from gp segment servers
gpssh -f hostfile-seg rm –rf /data/backup/gp5/* 
------------------------
--to start gpfdist server 
gpfdist -d /data02/gpfdist-username -p 8095 -l /data02/gpfdist-username/gpfdist.log

with aetna_providers as (
  select provider_id
  from aetna.layer_joined_plns
  group by 1
),
npc as (
  select pc.*
  from (
    SELECT pc.cluster_provider_id
    FROM warehouse.provider_clusters pc
      JOIN aetna_providers ap
      USING (provider_id)
    WHERE pc.source = 'MATCHERIZE'
    GROUP BY 1
    HAVING count(*) > 1
  ) a
    join warehouse.provider_clusters pc
      using (cluster_provider_id)
)
select count(distinct cartel_id) cartels,
       count(distinct provider_id) providers,
       count(distinct case when claim_count > 0 then cartel_id else null end) cartels_with_claims,
       count(distinct case when claim_count > 0 then provider_id else null end) providers_with_claims,
       sum(claim_count) total_claims,
       avg(provider_count) avg_provider_count,
       count(*) total
from (
  SELECT cartel_id,
    provider_id,
    provider_count,
    count(cg.id) claim_count
  FROM (
         SELECT DISTINCT
           cpln.cartel_id,
           cpln.provider_id,
           count(DISTINCT cpln.provider_id)
           OVER (PARTITION BY cpln.cartel_id) provider_count
         FROM aetna.cartel_plns cpln
           JOIN npc pc
             ON pc.provider_id = cpln.provider_id
           JOIN warehouse.providers p
             ON p.id = pc.provider_id
         WHERE pc.source = 'MATCHERIZE'
               AND p.provider_type = 'practitioner') a
    LEFT JOIN aetna.claim_groups_for_full_pricing cg
      USING (cartel_id, provider_id)
  group by 1,2,3) b;
