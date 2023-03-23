from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from secrets import token_hex


class DatabaseManipulatorLICENSE:

    @staticmethod
    def add_license_to_table(add_info: AddLicenseModel):
        try:
            product_id_table = {
                1: 'cass_stantion_count',
                2: 'mobile_cass_count',
                3: 'web_manager_count',
                4: 'mobile_manager_count'
            }
            with DBConnection.create_cursor() as cursor:
                license_key_ = token_hex(32)
                cursor.execute(f"""
                select
case 
	when (sum({product_id_table[add_info.product_id]})-
case
		when (
		select
			sum(product_id_fk)
		from
			licenses l
		where
			product_id_fk = %(product_id)s) is not null
	then (
		select
			sum(product_id_fk)
		from
			licenses l
		where
			product_id_fk = %(product_id)s)
		else 0
	end ) >0 then true 
	else false
end
 as state_of_license
from
	saved_order_and_tarif soat
where
	company_id = (
	select
		c_id
	from
		company c
	where
		c_unique_id = %(unique_id)s)
	and order_state = true """, {'unique_id': add_info.unique_code,
                                'product_id': add_info.product_id})
                if cursor.fetchone()['state_of_license'] != True:
                    return
                cursor.execute(""" select device_license_key from device_info where device_code = %(device_code)s """,{
                    "device_code": add_info.device_code
                })
                juts_ = cursor.fetchone()
                if juts_ is not None:
                    license_key_ = juts_['device_license_key']
                    cursor.execute("""select port, ip_of_client from device_port where unique_id_cp = %(uni)s """,
                                   {"uni": add_info.unique_code})
                    info_ = cursor.fetchone()
                    return {"port": info_["port"], "ip": info_["ip_of_client"], "license_key": license_key_}
                cursor.execute(""" insert into uniqunes_product(device_code, product_id)
                                   VALUES(%(device_code)s, %(product_id_fk)s);
                                   insert into licenses(license_key, product_id_fk, unique_id_cp)
                                   VALUES(%(lc_key)s, %(product_id_fk)s, %(unique_id_cp)s );
                                   INSERT INTO device_info(device_code, device_license_key)
                                   VALUES(%(device_code)s, %(device_lc_key)s);
                                   INSERT INTO device_port(unique_id_cp,ip_of_client )
                                   VALUES(%(unique_id_cp)s, (select ip_of_client from client_ip where ip_id = (select max(ip_id) from client_ip)))
                                   on conflict(unique_id_cp) do
                                   UPDATE SET unique_id_cp = excluded.unique_id_cp where
                                   device_port.unique_id_cp = %(unique_id_cp)s
                                   returning port, ip_of_client;
                                   """, {
                    'lc_key': license_key_,
                    'product_id_fk': add_info.product_id,
                    'unique_id_cp': add_info.unique_code,
                    'device_code': add_info.device_code,
                    'device_lc_key': license_key_
                })
                port_ip = cursor.fetchone()
                port_ = port_ip["port"]
                ip_ = port_ip["ip_of_client"]
                DBConnection.commit()
                return {'port': port_} | {'ip': ip_, 'license_key': license_key_}
        except Exception as e:
            DBConnection.rollback()
            print(e)
            return

    @staticmethod
    def check_license(check_info: CheckLicenseModel):
        try:
            product_id_table = {
                1: 'cass_stantion_count',
                2: 'mobile_cass_count',
                3: 'web_manager_count',
                4: 'mobile_manager_count'
            }
            with DBConnection.create_cursor() as cursor:
                cursor.execute(""" 
                select c_t_tarif_id as tarif_id, end_license::date>current_date as date_state  from client_tarif ct where c_t_id = 
                (select c_id
                from company c where c_unique_id =( select unique_id_cp  from licenses l
                where license_key = %(lc_key)s
                and %(dev_code)s = (select device_code from device_info di 
                where device_license_key = %(lc_key)s)))""", {
                    'lc_key': check_info.license_key,
                    'dev_code': check_info.device_code
                })
                tarif_id_and_date = cursor.fetchall()
                print(check_info)
                cursor.execute(f"""
                select tarif_id_fk as tarif_id,
                case 
                    when {product_id_table[check_info.product_id]} > 0 then true
                    else false
                end as state
                from saved_order_and_tarif soat where company_id = (
                select c_id from company c where c_unique_id =(
                select unique_id_cp  from licenses l where license_key = %(lc_key)s
                and %(dev_code)s = (select device_code from device_info di 
                where device_license_key = %(lc_key)s))) and order_state = true""", {
                    'lc_key': check_info.license_key,
                    'dev_code': check_info.device_code
                })
                tarif_id_and_count_of_product = cursor.fetchall()
                cursor.execute(""" 
                select port, ip_of_client  from device_port dp  where 
                unique_id_cp = (select unique_id_cp  from licenses l where license_key =%(lc_key)s)  """,
                               {'lc_key': check_info.license_key})
                info_ip_port = cursor.fetchone()
                info_of_id = [i['tarif_id'] for i in tarif_id_and_date if i['date_state'] is True]
                info_of_count = any(
                    [True for j in tarif_id_and_count_of_product if j['state'] is True and j['tarif_id'] in info_of_id])
                if info_of_count and info_of_id and info_ip_port is not None:
                    return {'state': info_of_count, 'ip': info_ip_port["ip_of_client"], 'port': info_ip_port["port"]}
                elif info_of_id and info_ip_port is not None:
                    return {'state': False, 'ip': info_ip_port["ip_of_client"], 'port': info_ip_port["port"]}
                return {'state': 0}

        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_license_type(license_key):
        try:
            with DBConnection.create_cursor() as cursor:
                cursor.execute("""
                SELECT 
                    case 
                        when (true in (select tarif_id_fk=1 from saved_order_and_tarif 
                        where company_id = (
                        select c_id from company
                        where c_unique_id = ( select distinct unique_id_cp from licenses where license_key = %(lic_key)s)
                        ) ))
                        then true
                    else
                        false
                    end as type_of
                    
                """, {
                    "lic_key": license_key
                })
                return cursor.fetchone()["type_of"]
        except Exception as e:
            print(e)
            return

