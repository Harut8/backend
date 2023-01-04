from DB_dir.db_manipulator_tarifes import DatabaseManipulatorTARIFES
from MODELS_dir.tarif_model import TarifModelForView, InnerModelForTarif


class ServiceManipulatorTARIFES:
    """BUSINESS LOGIC FOR TARIFES"""

    @staticmethod
    def get_tarifes_for_view():
        """Returns tarifes table for view"""
        temp_ = DatabaseManipulatorTARIFES.get_tarifes_for_view()
        if temp_[0]:
            data_for_view = [
                TarifModelForView(
                    tarif_names=i['tarif_names'],
                    tarif_month_prices=i['tarif_month_prices'],
                    inner_content=InnerModelForTarif(
                        cassa_names=i['cassa_names'],
                        cassa_counts=i['cassa_counts'],
                        manager_names=i['manager_names'],
                        manager_counts=i['manager_counts'],
                        sklad_names=i['sklad_names'],
                        sklad_counts=i['sklad_counts'],
                        tarifes_others=i['tarifes_others'],)
                )
                for i in temp_[1]
            ]
            return True, data_for_view
        else:
            return False,
