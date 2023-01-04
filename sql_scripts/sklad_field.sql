create table sklad_field(
	s_f_id serial primary key,
	s_f_name varchar(30) not null,
	s_per_price int not null default 0,
	s_inf_price int not null default 0
)