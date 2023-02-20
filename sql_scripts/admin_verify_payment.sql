--select date_part('day', k.sb)  from (select order_ending -order_date as sb  from saved_order_and_tarif soat) as k
DO
$func$
declare 
order_id_ int:=70;
state_checker bool;
count_row record;
t_c_id_ int;
m_c_f_id_ int;
m_f_id_ int;
w_m_f_id_ int;
c_f_id_ int;
tarif_id int;
begin
	select order_state  into state_checker from saved_order_and_tarif;
	if state_checker = TRUE then
		raise Exception 'error';
	end if;
	SELECT cass_stantion_count,
		   mobile_cass_count,
		   web_manager_count,
		   mobile_manager_count,
		   order_summ,
		   company_id,
		   date_part('day',order_ending -order_date) as sb_date
		   into count_row
	from saved_order_and_tarif soat where order_id = order_id_;
    INSERT INTO mobile_cassa_field(m_c_count) values(count_row.mobile_manager_count) returning m_c_f_id into m_c_f_id_;
    INSERT INTO manager_field (m_f_count) values(count_row.mobile_cass_count) returning m_f_id into m_f_id_;
    INSERT INTO web_manager_field  (w_m_count) values(count_row.web_manager_count) returning w_m_f_id into w_m_f_id_;
    INSERT INTO cassa_field  (c_f_count) values(count_row.cass_stantion_count) returning c_f_id into c_f_id_;
   --raise notice '%', c_f_id_;
    INSERT INTO tarif_content(t_c_cassa_id,
                              t_c_manager_id,
                              t_c_web_id,
                              t_c_mobile_c_id,
                              t_c_month)
    VALUES(c_f_id_,
           m_f_id_,
           w_m_f_id_,
           m_c_f_id_,
           count_row.sb_date
           ) RETURNING tarif_content.t_c_id into t_c_id_;
          --raise notice '%',t_c_id_;
    INSERT INTO tarif(t_month_price, t_c_id_fk) values(count_row.order_summ,t_c_id_)returning t_id into tarif_id;
    INSERT INTO client_tarif(c_t_id, c_t_tarif_id) values(count_row.company_id,tarif_id);
    update saved_order_and_tarif set order_state = TRUE; 
end;
$func$