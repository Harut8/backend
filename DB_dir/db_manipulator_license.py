from .db_connection import DatabaseConnection as DBConnection
from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from secrets import token_hex


class DatabaseManipulatorLICENSE:

    @staticmethod
    def add_license_to_table(add_info: AddLicenseModel):
        try:
            with DBConnection.create_cursor() as cursor:
                license_key_ = token_hex(32)
                cursor.execute(""" insert into uniqunes_product(device_code, product_id)
                                   VALUES(%(device_code)s, %(product_id_fk)s);
                                   insert into licenses(license_key, product_id_fk, unique_id_cp)
                                   VALUES(%(lc_key)s, %(product_id_fk)s, %(unique_id_cp)s );
                                   INSERT INTO device_info(device_code, device_license_key)
                                   VALUES(%(device_code)s, %(device_lc_key)s);
                                   INSERT INTO device_port(device_code_fk, license_key_fk)
                                   VALUES(%(device_code)s, %(lc_key)s) returning port
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
