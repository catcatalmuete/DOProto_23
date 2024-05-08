import data.db_connect as dbc
from bson import ObjectId

RES_HALL = "res_hall"
ADDRESS = "address"
RES_HALL_ID = "_id"
RES_HALL_COLLECT = "Residence Halls"


def add_hall(res_hall: str, address: str):
    dbc.connect_db()
    found_user = dbc.fetch_one(RES_HALL_COLLECT, {RES_HALL: res_hall})
    if found_user:
        raise ValueError(f'This residence hall already exists: {res_hall}')
    new_res = {}
    new_res[RES_HALL] = res_hall
    new_res[ADDRESS] = address

    _id = dbc.insert_one(RES_HALL_COLLECT, new_res)
    return _id is not None


def get_all_res_add() -> dict:
    dbc.connect_db()
    resAdds = dbc.fetch_all_as_dict(RES_HALL, RES_HALL_COLLECT)
    return resAdds


def get_res_add(res_hall: str):
    dbc.connect_db()
    return dbc.fetch_one(RES_HALL_COLLECT, {RES_HALL: res_hall})


def delete_res_hall(res_id: str):
    res_id = ObjectId(res_id)
    dbc.connect_db()
    return dbc.del_one(RES_HALL_COLLECT, {RES_HALL_ID: res_id})
