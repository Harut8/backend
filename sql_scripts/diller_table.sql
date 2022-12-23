CREATE TABLE diller(
	
	d_id serial primary key,
	d_pass varchar(20) not null,
	d_name text not null,
	d_contacname text not null,
	d_phone text not null,
	d_email text not null,
	d_inn text,
	d_kpp text,
	d_k_schet text,
	d_r_schet text,
	d_bik text,
	d_bank_name text,
	d_address text
)