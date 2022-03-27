import taller1.db as db
from taller1.models import MotivoEspecifico


class MotivoEspecificoManager(object):
    @staticmethod
    def get_motivo_especifico(cod_motesp):
        return (
            db.session.query(MotivoEspecifico)
            .filter(MotivoEspecifico.cod_motesp == cod_motesp)
            .first()
        )

    @staticmethod
    def insert_motivo_especifico(cod_motesp, motivo_especifico):
        motivo_especifico_ = MotivoEspecifico(
            cod_motesp=cod_motesp, motivo_especifico=motivo_especifico
        )
        db.session.add(motivo_especifico_)
        db.session.commit()
