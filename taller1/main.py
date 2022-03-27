import csv
import sys

import db as db
from taller1.controllers.DepartamentoController import DepartamentoController
from taller1.controllers.MotivoEspecificoController import MotivoEspecificoController
from taller1.controllers.MunicipioController import MunicipioController
from taller1.controllers.PQRController import PQRController

if __name__ == "__main__":
    db.Base.metadata.create_all(db.motor)
    try:
        for idx, line in enumerate(sys.stdin):
            if idx > 0:
                line = list(csv.reader([line]))[0]

                pet_cod_depto = line[6]
                pet_depto = line[7]
                pet_cod_mpio = line[8]
                pet_mpio = line[9]
                cod_motesp = line[37]
                motivo_especifico = line[38]
                riesgo_vida = line[44]

                if pet_depto != "NA" and pet_mpio != "NA":
                    if pet_depto == "BOGOTÁ D.C.":
                        pet_cod_depto = "25"
                        pet_depto = "CUNDINAMARCA"
                    DepartamentoController.insert_departamento(pet_cod_depto, pet_depto)
                    MunicipioController.insert_municipio(
                        pet_cod_mpio, pet_mpio, pet_cod_depto
                    )
                    MotivoEspecificoController.insert_motivo_especifico(
                        cod_motesp, motivo_especifico
                    )
                    PQRController.insert_pqr(
                        cod_motesp, riesgo_vida, pet_cod_mpio, pet_cod_depto
                    )
    except Exception as e:
        print(e)
