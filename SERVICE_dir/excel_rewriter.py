from num2words import num2words
import dataclasses
from openpyxl import load_workbook
import datetime
from MODELS_dir.tarif_model import TarifModelForExcel
@dataclasses.dataclass
class ExcelAnketaRewriter:

    buyer: str = "ООО «{org_name}» ИНН {inn_num}, {address}"
    cheque_num: str = "№ {cheque_num}"
    cheque_datetime: str = "от {day} {month} {year} г."
    buyed_tarifes_and_summ: str = "{tarif_count}, на сумму {tarif_summ}"
    tarife_summ: str = "{tarif_summ}"
    summ_with_words: str = ""
    MonthDictRu = {'1': 'Январь',
                   '2': 'Февраль',
                   '3': 'Март',
                   '4': 'Апрель',
                   '5': 'Май',
                   '6': 'Июнь',
                   '7': 'Июль',
                   '8': 'Август',
                   '9': 'Сентябрь',
                   '10': 'Октябрь',
                   '11': 'Ноябрь',
                   '12': 'Декабрь'}

    @classmethod
    def set_buyer_info(cls, org_name=None, inn_num=None, address=None):
        if org_name and inn_num and address is not None:
            cls.buyer = cls.buyer.format(org_name=org_name, address=address, inn_num=inn_num)
        else:
            raise Exception("ERROR")

    @classmethod
    def set_order_info(cls, cheque_num=None, tarif_count=None, tarif_summ=None):
        try:

            #tarif_summ = tarif_summ.replace('$','')
            print(cheque_num, tarif_summ, tarif_count)
            if cheque_num and tarif_summ and tarif_count is not None:
                cls.cheque_num = cls.cheque_num.format(cheque_num=cheque_num)
                cls.tarife_summ = cls.tarife_summ.format(tarif_summ=tarif_summ)
                cls.buyed_tarifes_and_summ = cls.buyed_tarifes_and_summ.format(tarif_count=tarif_count, tarif_summ=tarif_summ)
                cls.summ_with_words = num2words(int(float(tarif_summ)),lang="ru")
                print(cls.summ_with_words)
            else:
                raise Exception("VALUE ERROR")
        except Exception as e:
            print(e)
            raise Exception("VALUE ERROR")

    @classmethod
    def set_datetime(cls):
        try:
            now__ = datetime.datetime.utcnow()
            cls.cheque_datetime = cls.cheque_datetime.format(
                month=cls.MonthDictRu[str(now__.month)],
                day=now__.day,
                year=now__.year)
            print(1)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def rewrite_excel(cls, order_id):
        try:
            # import os
            # print(os.getcwd())
            workbook = load_workbook(filename="SERVICE_dir/csv/schet.xlsx")
            # open workbook
            sheet = workbook.active


            # modify the desired cell
            sheet["B8"] = cls.cheque_num
            sheet["C8"] = cls.cheque_datetime
            sheet["B11"] = cls.buyer
            sheet["B18"] = cls.tarife_summ
            sheet["C17"] = cls.buyed_tarifes_and_summ
            sheet["A20"] = cls.summ_with_words
            workbook.save(filename=f"SERVICE_dir/csv/{order_id}.xlsx")
            print("CREATED EXCEL")
            return True
        except Exception as e:
            print(e)
            return None

    @classmethod
    def set_all_attributes(cls, info: TarifModelForExcel):
        try:
            cls.set_datetime()
            cls.set_buyer_info(info.c_name,info.c_inn,info.c_address)
            cls.set_order_info(info.order_id,info.count,info.order_summ)
            cls.rewrite_excel(info.order_id)
            return True
        except Exception as e:
            print(e)
            return None

