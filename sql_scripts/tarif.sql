create TABLE tarif(
	
	t_id serial primary key,
	t_name varchar(30) not null,
	t_month_price int not null,
	t_inf_price int default 0,
	t_c_id_fk int unique,
	foreign key(t_c_id_fk) references tarif_content(t_c_id)
)