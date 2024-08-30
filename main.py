import py_pdf_parser.loaders
from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise
import re
from types import SimpleNamespace
from typing import Optional


ns = SimpleNamespace()
ns.searchmethod = SimpleNamespace()
ns.searchmethod.contains = 1


class PdfParser:

    def __init__(self):
        self.doc: Optional[py_pdf_parser.loaders.PDFDocument] = None
        self.page = None

    def open_pdf(self, path: str):
        self.doc = load_file(path)
        #visualise(self.doc, show_info=True)
        self.page = self.doc.get_page(1)

    def parse_save(self):
        raise NotImplementedError

    @staticmethod
    def remove_redundant(text: str):
        result = re.sub(r'[\u2070-\u2079()]', '', text)
        return result

    @staticmethod
    def extract_dbtablefield_names(text: str):
        return text.split(sep="_", maxsplit=1)


    def split_block(self, text: str):
        splitted = []
        for line in text.splitlines():
            first, _, rest = line.partition(" ")
            text_to_append = rest or first
            pproc_text = self.remove_redundant(text_to_append)
            splitted.append(pproc_text)
        splitted.pop(0)
        return splitted


class VerbPdfParser(PdfParser):

    verb_elements = {
        # search_method, search_params, single (None)/match position (int), db_table (str), db_field (str)
        "verbs_ind_presens": (ns.searchmethod.contains, "Презенс", 0, "verb_forms", "ind_presens"),
        "verbs_ind_preterium": (ns.searchmethod.contains, "Претеритум", None, "verb_forms", "ind_preterium"),
        "verbs_ind_perfect": (ns.searchmethod.contains, "Перфект", 0, "verb_forms", "ind_perfect"),
        "verbs_ind_plusquamperfect": (ns.searchmethod.contains, "Плюсквамперфект", None, "verb_forms", "ind_plusquamperfect"),
        "verbs_ind_futurum1": (ns.searchmethod.contains, "Футурум I", 0, "verb_forms", "ind_futurum1"),
        "verbs_ind_futurum2": (ns.searchmethod.contains, "Футурум I", 1, "verb_forms", "ind_futurum2"),
        "verbs_con_conj1": (ns.searchmethod.contains, "Конъюнктив I", 0, "verb_forms", "con_conj1"),
        "verbs_con_conj2": (ns.searchmethod.contains, "Конъюнктив I", 1, "verb_forms", "con_conj2"),
        "verbs_con_perfect": (ns.searchmethod.contains, "Перфект конъюнктив", None, "verb_forms", "con_perfect"),
        "verbs_con_plusquamperfect": (ns.searchmethod.contains, "Плюсквам. конъюнк.", None, "verb_forms", "con_plusquamperfect"),
        "verbs_con_futurum1": (ns.searchmethod.contains, "Футурум I конъюнктив", None, "verb_forms", "con_futurum1"),
        "verbs_con_futurum2": (ns.searchmethod.contains, "Футурум II конъюнктив", None, "verb_forms", "con_futurum2"),
        "verbs_inf_inf1": (ns.searchmethod.contains, "Инфинитив I", 0, "verb_forms", "inf_inf1"),
        "verbs_inf_inf2": (ns.searchmethod.contains, "Инфинитив I", 1, "verb_forms", "inf_inf2"),
        "verbs_par_part1": (ns.searchmethod.contains, "Партицип I", 0, "verb_forms", "par_part1"),
        "verbs_par_part2": (ns.searchmethod.contains, "Партицип I", 1, "verb_forms", "par_part2"),
        "verbs_imp_presens": (ns.searchmethod.contains, "Презенс", 1, "verb_forms", "imp_presens")
    }

    def __init__(self):
        super().__init__()

    def parse_save(self):
        for elem_name, elem_params in VerbPdfParser.verb_elements.items():
            el_searchmethod = elem_params[0]
            el_searchparams = elem_params[1]
            el_matchposition = elem_params[2]
            el_dbtable = elem_params[3]
            el_dbfield = elem_params[4]

            match el_searchmethod:
                case ns.searchmethod.contains:
                    if el_matchposition is not None:
                        el = self.doc.elements.filter_by_text_contains(text=el_searchparams)[el_matchposition]
                    else:
                        try:
                            el = self.doc.elements.filter_by_text_contains(text=el_searchparams).extract_single_element()
                        except py_pdf_parser.exceptions.MultipleElementsFoundError as e:
                            print(f"Multiple occurences found: {el_searchparams}")
                            raise e

                case _:
                    return NotImplementedError

            print(el.text())



parser = VerbPdfParser()
parser.open_pdf(r"C:\Users\Aleee\Desktop\lesen.pdf")
parser.parse_save()


