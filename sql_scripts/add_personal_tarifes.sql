--alter table sklad_field alter column s_f_name set default array['Cklad','Sklad']

create or replace function add_personal_tarifes(
	cassa_count int,
	manager_count int,
	sklad_count int,
	client_id int)
returns int
language plpgsql
as $$
declare 
max_id_cassa int;
max_id_manager int;
max_id_sklad int;
max_id_tarif_content int;
max_id_tarif int;
begin
	SELECT max(c_f_id)+1,
		   max(m_f_id)+1,
		   max(s_f_id)+1,
		   max(t_c_id)+1,
		   max(t_id)+1 INTO
	max_id_cassa,
	max_id_manager,
	max_id_sklad,
	max_id_tarif_content,
	max_id_tarif
	FROM cassa_field,
		 manager_field,
		 sklad_field,
		 tarif_content,
		 tarif;
	INSERT INTO cassa_field(c_f_id,c_f_count) values(max_id_cassa, cassa_count);
	INSERT INTO manager_field(m_f_id, m_f_count) values(max_id_manager, manager_count);
	INSERT INTO sklad_field(s_f_id, s_f_count) values(max_id_sklad, sklad_count);
	INSERT INTO tarif_content(t_c_id,
							  t_c_cassa_id,
							  t_c_manager_id,
							  t_c_sklad_id)
	VALUES(max_id_tarif_content,
		   max_id_cassa,
		   max_id_manager,
		   max_id_sklad);
	
	INSERT INTO tarif(t_id,
				      t_month_price,
					  t_c_id_fk)
	VALUES(max_id_tarif, 10000, max_id_tarif_content);
	INSERT INTO client_tarife (c_t_id, c_t_tarif_id) VALUES(client_id, max_id_tarif);
	RETURN 1;
end;
$$