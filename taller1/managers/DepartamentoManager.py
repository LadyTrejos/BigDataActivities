import taller1.db as db
from taller1.models import Departamento


class DepartamentoManager(object):
    @staticmethod
    def get_departamento(pet_cod_depto):
        return (
            db.session.query(Departamento)
            .filter(Departamento.pet_cod_depto == pet_cod_depto)
            .first()
        )

    @staticmethod
    def insert_departamento(pet_cod_depto, pet_depto):
        dpto = Departamento(pet_cod_depto=pet_cod_depto, pet_depto=pet_depto)
        db.session.add(dpto)
        db.session.commit()

    @staticmethod
    def insert_departamentos(data):
        for item in data:
            dpto = Departamento(
                pet_cod_depto=item["pet_cod_depto"],
                pet_depto=item["pet_depto"],
            )
            db.session.add(dpto)
        db.session.commit()
