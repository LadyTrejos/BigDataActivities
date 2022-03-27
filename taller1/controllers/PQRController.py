from taller1.managers.PQRManager import PQRManager


class PQRController(object):
    @staticmethod
    def get_pqr(id):
        return PQRManager.get_pqr(id)

    @staticmethod
    def insert_pqr(cod_motesp, riesgo_vida, pet_cod_mpio, pet_cod_depto):
        PQRManager.insert_pqr(cod_motesp, riesgo_vida, pet_cod_mpio, pet_cod_depto)
