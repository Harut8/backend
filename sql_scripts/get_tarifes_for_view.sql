CREATE OR REPLACE FUNCTION public.get_tarifes_for_view()
 RETURNS TABLE(tarif_id integer, tarif_names character varying[], cassa_names character varying[], tarif_month_prices integer, cassa_counts integer, manager_names character varying[], manager_counts integer, web_names character varying[], web_counts integer, mobile_cassa_names text[], mobile_cassa_counts integer, tarifes_others text[])
 LANGUAGE plpgsql
AS $function$
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
join web_manager_field wmf
on tc.t_c_web_id  = wmf.w_m_f_id 
join mobile_cassa_field mcf
on mcf.m_c_f_id  = tc.t_c_mobile_c_id  order by t_month_price limit 4;
--return tarifes_table_for_return;
end; 
$function$
;
