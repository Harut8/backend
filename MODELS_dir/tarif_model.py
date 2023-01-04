from pydantic import BaseModel,validator

class InnerModelForTarif(BaseModel):
    """MODEL FOR INNER  CONTENT OF TARIF"""

    cassa_names: list[str] = None
    cassa_counts: int = None
    manager_names: list[str] = None
    manager_counts: int = None
    sklad_names: list[str] = None
    sklad_counts: int = None
    tarifes_others: list[str] = None

class TarifModelForView(BaseModel):
    """MODEL FOR TARIFES VIEW"""

    tarif_names: list[str] = None
    tarif_month_prices: int = None
    inner_content: InnerModelForTarif = None

    @validator('tarif_month_prices')
    def tarif_month_prices_check(cls, month_prices):
        print(month_prices)
        if month_prices <= 0:
            return "FREE"
        return month_prices
