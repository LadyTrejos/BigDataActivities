import taller1.db as db
from taller1.models import PQR


class PQRManager(object):
    @staticmethod
    def get_pqr(id):
        return db.session.query(PQR).filter(PQR.id == id).first()

    @staticmethod
    def insert_pqr(cod_motesp, riesgo_vida, pet_cod_mpio, pet_cod_depto):
        pqr = PQR(
            cod_motesp=cod_motesp,
            riesgo_vida=riesgo_vida,
            pet_cod_mpio=pet_cod_mpio,
            pet_cod_depto=pet_cod_depto,
        )
        db.session.add(pqr)
        db.session.commit()
