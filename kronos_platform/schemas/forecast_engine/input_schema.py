from dataclasses import dataclass


@dataclass
class ForecastDataSchema:
    """
    TODO complete docstring
    """

    client: str
    db: str
    schema: str
    table: str
    item_id: str
    target: str
    prediction: str
    month: str
    year: str
    day: str
    item_list: list

