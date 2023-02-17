from pydantic import BaseModel,validator

class InnerModelForTarif(BaseModel):
    """MODEL FOR INNER  CONTENT OF TARIF"""

    cassa_names: str = None
    cassa_counts: int = None
    manager_names: str = None
    manager_counts: int = None
    web_names: str = None
    web_counts: int = None
    mobile_cassa_names: str = None
    mobile_cassa_counts: int = None
    tarifes_others: list[str] = None


class TarifModelForView(BaseModel):
    """MODEL FOR TARIFES VIEW"""
    tarif_id: int = None
    tarif_names: str = None
    tarif_month_prices: int = None
    inner_content: InnerModelForTarif = None

    @validator('tarif_month_prices')
    def tarif_month_prices_check(cls, month_prices):
        print(month_prices)
        if month_prices <= 0:
            return "FREE"
        return month_prices


class PersonalTarifForClient(BaseModel):
    """MODEL FOR PERSONAL TARIF USED BY CLIENT"""
    cass_stantion_price: int | None = None
    mobile_cass_price: int | None = None
    mobile_manager_price: int | None = None
    web_manager_price: int | None = None


class TarifToClient(BaseModel):
    """MODEL FOR ADDING TO CLIENT"""
    tarif_id_or_info: int | None = None


class PersonalTarifInfo(BaseModel):
    cass_stantion_price: int | None = None
    mobile_cass_price: int | None = None
    mobile_manager_price: int | None = None
    web_manager_price: int | None = None
    cass_stantion_count: int | None = None
    mobile_cass_count: int | None = None
    mobile_manager_count: int | None = None
    web_manager_count: int | None = None
    tarif_month: int | None = 1


class PersonalTarifForView(PersonalTarifForClient):
    cass_stantion_name: str | None = None
    mobile_cass_name: str | None = None
    mobile_manager_name: str | None = None
    web_manager_name: str | None = None


class BuyTarifeByTransfer(BaseModel):
    order_summ: int
    cass_stantion_count: int
    mobile_cass_count: int
    mobile_manager_count: int
    web_manager_count: int
    client_token: str
    interval: int = 1


class TarifModelForExcel(BaseModel):
    order_id: int
    c_name: str
    c_inn: str
    c_address: str
    order_summ: str
    count: int
    csc: int
    mcc: int
    mmc: int
    wmc: int