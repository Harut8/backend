create  table tarif_content(
	t_c_id serial primary key,
	t_c_cassa_id int unique not null,
	t_c_manager_id int unique not null,
	t_c_sklad_id int unique not null,
	t_c_other TEXT[],
	foreign key(t_c_cassa_id) references cassa_field(c_f_id),
	foreign key(t_c_manager_id) references manager_field(m_f_id),
	foreign key(t_c_sklad_id) references sklad_field(s_f_id)
)