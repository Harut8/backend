CREATE TABLE temp_company(
	
	t_id serial primary key,
	t_c_pass varchar(20) not null,
	t_c_name text not null,
	t_c_contact_name text not null,
	t_c_phone text not null,
	t_c_email text not null,
	t_c_verify_link text not null,
	t_c_inn text,
	t_c_kpp text,
	t_c_k_schet text,
	t_c_r_schet text,
	t_c_bik text,
	t_c_bank_name text,
	t_c_address text
	
)