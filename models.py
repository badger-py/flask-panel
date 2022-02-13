from typing import Optional
from pydantic import BaseModel, ValidationError


class Positions(BaseModel):
    id: Optional[int]
    name: str
    price: int

    def get_name():
        return "positions"


# registr all models there
models_list = [
    Positions
]

if __name__ == "__main__":
    table = models_list[0]
    columns = list(dict(table.__dict__)['__annotations__'].keys())
    print(f"Table is {table.get_name()}")
    print(f"Columns = {columns}")

    data_to_validate = {
        "id": 1,
        "name": "Milk",
        "price": "25"
    }
    try:
        data = table.parse_obj(data_to_validate)
        print(data)
        print(data.json(exclude={'id'}))
    except ValidationError as v_error:
        for error in v_error.errors():
            print(f"Error in {error['loc'][0]}: {error['msg']}")
