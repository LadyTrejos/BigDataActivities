from taller1.managers.DepartamentoManager import DepartamentoManager


class DepartamentoController(object):
    @staticmethod
    def get_departamento(pet_cod_depto):
        return DepartamentoManager.get_departamento(pet_cod_depto)

    @staticmethod
    def insert_departamento(pet_cod_depto, pet_depto):
        departamento = DepartamentoController.get_departamento(pet_cod_depto)
        if not departamento:
            DepartamentoManager.insert_departamento(pet_cod_depto, pet_depto)
