CREATE TABLE client_tarif(
	c_t_id int not null primary key,
	c_t_tarif_id int not null primary key,
	foreign key(c_t_id) references company(c_id),
	foreign key(c_t_tarif_id) references tarif(t_id),
)