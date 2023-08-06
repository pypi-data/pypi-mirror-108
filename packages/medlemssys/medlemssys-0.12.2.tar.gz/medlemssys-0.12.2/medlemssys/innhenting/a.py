# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 expandtab ai

import datetime

import mod10

TRANSAKSJONSTYPE = {
    "10": "Giro belasta konto",
    "11": "Faste oppdrag",
    "12": "Direkte remittering",
    "13": "Bedriftsterminalgiro (BTG)",
    "14": "Skrankegiro",
    "15": "AvtaleGiro",
    "16": "TeleGiro",
    "17": "Giro - betalt kontant",
    "18": "Nettgiro - reversering m KID",
    "19": "Nettgiro - kjøp m KID",
    "20": "Nettgiro - reversering m fritekst",
    "21": "Nettgiro - kjøp m fritekst",
}

def _parse(ocr_data):
    for row in ocr_data:
        row = row.strip()
        if row[0:8] == "NY000010":
            # Startrecord for sending
            #forsendelsesnr = row[16:23]
            break
    else:
        raise OCRError('Fann ikkje startrecord for sending')

    data = []
    for row in ocr_data:
        row = row.strip()

        if row[0:6] == "NY0900":
            if row[6:8] == "20":
                # Startrecord for oppdrag
                pass
            elif row[6:8] == "88":
                # Sluttrecord for oppdrag
                pass
            else:
                raise OCRError("Forstår ikkje kode {0} ({1})!".format(row[6:8], row))
            continue

        elif row[0:4] == "NY09":
            if row[6:8] != "30":
                raise OCRError("Venta startrecord 30, fekk {0}. ({1})!".format(row[6:8], row))

            # Transaksjon
            trans = TRANSAKSJONSTYPE[row[4:6]]
            dato = row[15:21]
            dato = datetime.date(2000 + int(dato[4:6]), int(dato[2:4]), int(dato[0:2]))
            belop = int(row[32:49])/100.0
            kid = row[49:74].strip()
            if not mod10.check_number(kid.strip()):
                raise OCRError("KID-nummer validerte ikkje ({0})".format(kid))

            row2 = ocr_data.next()
            oppdr_dato = row2[41:47]
            fra_konto = row2[47:58]

            fritekst = ""
            if row[4:6] == "20" or row[4:6] == "21":
                row3 = ocr_data.next()
                fritekst = row3[15:55]

            data.append(dict(
                        transaksjon=trans,
                        dato=dato,
                        belop=belop,
                        kid=kid,
                        oppdragsdato=oppdr_dato,
                        fra_konto=fra_konto,
                        fritekst=fritekst,
                    ))
    return data

if __name__ == '__main__':
    import fileinput
    import pprint

    data = _parse(fileinput.input())
    pprint.pprint(data)
