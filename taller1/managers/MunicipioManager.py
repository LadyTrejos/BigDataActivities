import taller1.db as db
from taller1.models import Municipio


class MunicipioManager(object):
    @staticmethod
    def get_municipio(pet_cod_mpio):
        return (
            db.session.query(Municipio)
            .filter(Municipio.pet_cod_mpio == pet_cod_mpio)
            .first()
        )

    @staticmethod
    def insert_municipio(pet_cod_mpio, pet_mpio, pet_cod_depto):
        mpio = Municipio(
            pet_cod_mpio=pet_cod_mpio, pet_mpio=pet_mpio, pet_cod_depto=pet_cod_depto
        )
        db.session.add(mpio)
        db.session.commit()
