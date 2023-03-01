from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from secrets import token_hex


class DatabaseManipulatorLICENSE:

    @staticmethod
    def add_license_to_table(add_info: AddLicenseModel):
        try:
            with DBConnection.create_cursor() as cursor:
                license_key_ = token_hex(32)
                cursor.execute("""
                select
case 
	when (sum(cass_stantion_count)-
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
	and order_state = true""", {'unique_id': add_info.unique_code,
                                'product_id': add_info.product_id})
                if cursor.fetchone()['state_of_license'] != True:
                    return
                cursor.execute(""" insert into uniqunes_product(device_code, product_id)
                                   VALUES(%(device_code)s, %(product_id_fk)s);
                                   insert into licenses(license_key, product_id_fk, unique_id_cp)
                                   VALUES(%(lc_key)s, %(product_id_fk)s, %(unique_id_cp)s );
                                   INSERT INTO device_info(device_code, device_license_key)
                                   VALUES(%(device_code)s, %(device_lc_key)s);
                                   INSERT INTO device_port(unique_id_cp, license_key_fk)
                                   VALUES(%(unique_id_cp)s, %(lc_key)s) 
                                   on conflict(unique_id_cp) do
                                   UPDATE SET unique_id_cp = excluded.unique_id_cp where 
                                   device_port.unique_id_cp = %(unique_id_cp)s
                                   returning port;
                                   """, {
                    'lc_key': license_key_,
                    'product_id_fk': add_info.product_id,
                    'unique_id_cp': add_info.unique_code,
                    'device_code': add_info.device_code,
                    'device_lc_key': license_key_
                })
                port_ = cursor.fetchone()
                DBConnection.commit()
                return port_ | {'ip': '192.168.0.206', 'license_key': license_key_}
        except Exception as e:
            DBConnection.rollback()
            print(e)
            return
