from sqlalchemy import Column, Integer, Text, String, ForeignKey, Sequence

import db as db


class Departamento(db.Base):
    __tablename__ = "departamento"
    pet_cod_depto = Column(Integer, primary_key=True)
    pet_depto = Column(Text)


class Municipio(db.Base):
    __tablename__ = "municipio"
    pet_cod_mpio = Column(Integer, primary_key=True)
    pet_mpio = Column(Text)
    pet_cod_depto = Column(Integer, ForeignKey("departamento.pet_cod_depto"))


class PQR(db.Base):
    __tablename__ = "pqr"
    id = Column(Integer, Sequence("pqr_id_seq"), primary_key=True)
    cod_motesp = Column(Integer, ForeignKey("motivo_especifico.cod_motesp"))
    riesgo_vida = Column(String(2))
    pet_cod_mpio = Column(Integer, ForeignKey("municipio.pet_cod_mpio"))
    pet_cod_depto = Column(Integer, ForeignKey("departamento.pet_cod_depto"))


class MotivoEspecifico(db.Base):
    __tablename__ = "motivo_especifico"
    cod_motesp = Column(Integer, primary_key=True)
    motivo_especifico = Column(Text)
