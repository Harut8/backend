CREATE TABLE company(
	
	c_id serial primary key,
	c_unique_id int not null,
	c_diller_id int not null,
	c_pass varchar(20) not null,
	c_name text not null,
	c_contacname text not null,
	c_phone text not null,
	c_email text not null,
	c_inn text,
	c_kpp text,
	c_k_schet text,
	c_r_schet text,
	c_bik text,
	c_bank_name text,
	c_address text
)