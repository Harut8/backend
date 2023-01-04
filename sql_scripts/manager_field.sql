create table manager_field(
	m_f_id serial primary key,
	m_f_name varchar(30) not null,
	m_per_price int not null default 0,
	m_inf_price int not null default 0
)