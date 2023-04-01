from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from DB_dir.db_manipulator_license import DatabaseManipulatorLICENSE


class ServiceManipulatorLICENSE:

    @staticmethod
    def add_license(add_model: AddLicenseModel):
        info_ = DatabaseManipulatorLICENSE.add_license_to_table(add_model)
        if info_ is not None:
            return info_
        return

    @staticmethod
    def check_license(check_model: CheckLicenseModel):
        info_ = DatabaseManipulatorLICENSE.check_license(check_model)
        if info_ is not None:
            return info_
        return

    @staticmethod
    def get_license_type(license_key):
        info_ = DatabaseManipulatorLICENSE.get_license_type(license_key)
        if info_ is not None:
            return info_
        return None

    @staticmethod
    def get_port_for_suro(u_id, lc_key):
        info_ = DatabaseManipulatorLICENSE.get_port_for_suro(u_id, lc_key)
        if info_ is not None:
            return info_
        return None
