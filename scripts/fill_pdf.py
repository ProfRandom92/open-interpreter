import sys
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject

DATA = {
    "Vorname": "Alexander",
    "Nachname": "K\u00f6lnberger",
    "Geburtsdatum": "18.04.1992",
    "Adresse": "Goethestra\u00dfe 29, 69151 Neckargem\u00fcnd",
    "E-Mail": "alexanderkoelnberger@gmail.com",
    "Telefon": "0171 2345678",
    "Unterschrift": "Alexander K\u00f6lnberger",
    "Datum": "19.07.2025",
}

INPUT_PDF = "anmeldung.pdf"
OUTPUT_PDF = "ausgefuellt.pdf"

ANNOT_KEY = PdfName.Annots
SUBTYPE_KEY = PdfName.Subtype
WIDGET_SUBTYPE_KEY = PdfName.Widget
FIELD_KEY = PdfName.T
VALUE_KEY = PdfName.V


def fill_pdf(input_pdf: str, output_pdf: str, data: dict) -> None:
    pdf = PdfReader(input_pdf)
    if pdf.Root.AcroForm:
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
    found = set()

    for page in pdf.pages:
        annotations = page.get(ANNOT_KEY)
        if not annotations:
            continue
        for annot in annotations:
            if annot.get(SUBTYPE_KEY) == WIDGET_SUBTYPE_KEY and annot.get(FIELD_KEY):
                key = annot[FIELD_KEY][1:-1] if annot[FIELD_KEY].startswith("(") else annot[FIELD_KEY]
                if key in data:
                    annot.update(PdfDict(V=PdfObject(f"({data[key]})"), AP=None))
                    found.add(key)

    for key in data:
        if key not in found:
            print(f"Warnung: Feld '{key}' existiert nicht im PDF-Formular.")

    PdfWriter().write(output_pdf, pdf)


if __name__ == "__main__":
    fill_pdf(INPUT_PDF, OUTPUT_PDF, DATA)
    print(f"PDF gespeichert als {OUTPUT_PDF}")
