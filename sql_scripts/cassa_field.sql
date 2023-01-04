create table cassa_field(
	c_f_id serial primary key,
	c_f_name varchar(30) not null,
	c_per_price int not null default 0,
	c_inf_price int not null default 0
	
)
