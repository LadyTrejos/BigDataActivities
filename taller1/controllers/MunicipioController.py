from taller1.managers.MunicipioManager import MunicipioManager


class MunicipioController(object):
    @staticmethod
    def get_municipio(pet_cod_mpio):
        return MunicipioManager.get_municipio(pet_cod_mpio)

    @staticmethod
    def insert_municipio(pet_cod_mpio, pet_mpio, pet_cod_depto):
        municipio = MunicipioController.get_municipio(pet_cod_mpio)
        if not municipio:
            MunicipioManager.insert_municipio(pet_cod_mpio, pet_mpio, pet_cod_depto)
