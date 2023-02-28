from MODELS_dir.license_model import CheckLicenseModel, AddLicenseModel
from DB_dir.db_manipulator_license import DatabaseManipulatorLICENSE


class ServiceManipulatorLICENSE:

    @staticmethod
    def add_license(add_model: AddLicenseModel):
        info_ = DatabaseManipulatorLICENSE.add_license_to_table(add_model)
        if info_ is not None:
            return info_
        return
