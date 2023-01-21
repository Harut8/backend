--drop function get_tarifes_for_view();
--drop type tarifes_table;

CREATE OR REPLACE FUNCTION get_tarifes_for_view()
RETURNS table(
	   tarif_id int,
	   tarif_names varchar(60)[],
	   cassa_names varchar(60)[],
	   tarif_month_prices int,
	   cassa_counts int,
	   manager_names varchar(60)[],
	   manager_counts int,
	   sklad_names varchar(60)[],
	   sklad_counts int,
	   mobile_cassa_names text[],
	   mobile_cassa_counts int,
	   tarifes_others text[])
language plpgsql
as $$
--declare 
--tarifes_table_for_return tarifes_table;
begin 
return query SELECT t_id,
	   t_name,
	   c_f_name,
	   t_month_price, 
	   c_f_count,
	   m_f_name,
	   m_f_count,
	   s_f_name,
	   s_f_count,
	   m_c_f_name,
	   m_c_count,
	   t_c_other
	   --into tarifes_table_for_return
	   FROM 
tarif t
join tarif_content tc 
on t.t_c_id_fk = tc.t_c_id 
join cassa_field cf 
on tc.t_c_cassa_id = cf.c_f_id 
join manager_field mf
on tc.t_c_manager_id = mf.m_f_id 
join sklad_field sf
on tc.t_c_sklad_id = sf.s_f_id 
join mobile_cassa_field mcf
on mcf.m_c_f_id  = tc.t_c_mobile_c_id  order by t_month_price limit 4;
--return tarifes_table_for_return;
end; 
$$ 