from taller1.managers.MotivoEspecificoManager import MotivoEspecificoManager


class MotivoEspecificoController(object):
    @staticmethod
    def get_motivo_especifico(cod_motesp):
        return MotivoEspecificoManager.get_motivo_especifico(cod_motesp)

    @staticmethod
    def insert_motivo_especifico(cod_motesp, motivo_especifico):
        motivo_especifico_ = MotivoEspecificoController.get_motivo_especifico(
            cod_motesp
        )
        if not motivo_especifico_:
            MotivoEspecificoManager.insert_motivo_especifico(
                cod_motesp, motivo_especifico
            )
