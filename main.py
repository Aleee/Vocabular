from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise
import re
from types import SimpleNamespace
import lovely_logger as log


doc = load_file(r"C:\Users\Aleee\Desktop\lesen.pdf")
#visualise(file, show_info=True)

file = doc.get_page(1)

ns = SimpleNamespace()

ns.wordtype = SimpleNamespace()
ns.wordtype.verb = 1

ns.searchmethod = SimpleNamespace()
ns.searchmethod.contains = 1

class PdfParser:

    def __init__(self):
        self.doc = None
        self.page = None
        self.wordtype = None

        log.init("log.log")

    def open_pdf(self, path: str, word_type: int = ns.wordtype.verb):
        self.doc = load_file(path)
        # visualise(file, show_info=True)
        self.page = doc.get_page(1)
        self.wordtype = word_type

    def parse_save(self):
        if self.wordtype == ns.wordtype.verb:
            self.parse_save_verb()


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

    def parse_save_verb(self):

        verb_elements = {
            #search_method, search_params, single (None)/match position (int), db_table (str, optional), db_field (str, optional)
            "verbs_ind_presens": (ns.searchmethod.contains, "Презенс", 0),
            "verbs_ind_preterium": (ns.searchmethod.contains, "Претеритум", None),
            "verbs_ind_perfect": (ns.searchmethod.contains, "Перфект", 0),
            "verbs_ind_plusquamperfect": (ns.searchmethod.contains, "Плюсквамперфект", None),
            "verbs_ind_futurum1": (ns.searchmethod.contains, "Футурум I", 0),
            "verbs_ind_futurum2": (ns.searchmethod.contains, "Футурум I", 1),
            "verbs_con_conj1": (ns.searchmethod.contains, "Конъюнктив I", 0),
            "verbs_con_conj2": (ns.searchmethod.contains, "Конъюнктив I", 1),
            "verbs_con_perfect": (ns.searchmethod.contains, "Перфект конъюнктив", None),
            "verbs_con_plusquamperfect": (ns.searchmethod.contains, "Плюсквам. конъюнк.", None),
            "verbs_con_futurum1": (ns.searchmethod.contains, "Футурум I конъюнктив", None),
            "verbs_con_futurum2": (ns.searchmethod.contains, "Футурум II конъюнктив", None),
            "verbs_inf_inf1": (ns.searchmethod.contains, "Инфинитив I", 0),
            "verbs_inf_inf2": (ns.searchmethod.contains, "Инфинитив I", 1),
            "verbs_par_part1": (ns.searchmethod.contains, "Партицип I", 0),
            "verbs_par_part2": (ns.searchmethod.contains, "Партицип I", 1),
            "verbs_imp_presens": (ns.searchmethod.contains, "Презенс", 1)
        }

        for elem_name, el_params in verb_elements.items():
            elem_searchmethod = el_params[0]
            elem_searchparams = el_params[1]
            elem_matchposition = el_params[2]
            try:
                elem_dbtable = el_params[3]
                elem_dbfield = el_params[4]
            except IndexError:
                elem_dbtable, elem_dbfield = self.extract_dbtablefield_names(elem_name)

            match elem_searchmethod:
                case ns.searchmethod.contains:
                    pass





        # verbs_ind_presens = file.elements.filter_by_text_contains(text="Презенс")[0]
        # verbs_ind_preterium = file.elements.filter_by_text_contains(text="Претеритум").extract_single_element()
        # verbs_ind_perfect = file.elements.filter_by_text_contains(text="Перфект")[0]
        # verbs_ind_plusquamperfect = file.elements.filter_by_text_contains(text="Плюсквамперфект").extract_single_element()
        # verbs_ind_futurum1 = file.elements.filter_by_text_contains(text="Футурум I")[0]
        # verbs_ind_futurum2 = file.elements.filter_by_text_contains(text="Футурум I")[1]
        # verbs_con_conj1 = file.elements.filter_by_text_contains(text="Конъюнктив I")[0]
        # verbs_con_conj2 = file.elements.filter_by_text_contains(text="Конъюнктив I")[1]
        # verbs_con_perfect = file.elements.filter_by_text_contains(text="Перфект конъюнктив").extract_single_element()
        # verbs_con_plusquamperfect = file.elements.filter_by_text_contains(
        #     text="Плюсквам. конъюнк.").extract_single_element()
        # verbs_con_futurum1 = file.elements.filter_by_text_contains(text="Футурум I конъюнктив").extract_single_element()
        # verbs_con_futurum2 = file.elements.filter_by_text_contains(text="Футурум II конъюнктив").extract_single_element()
        # verbs_inf_inf1 = file.elements.filter_by_text_contains(text="Инфинитив I")[0]
        # verbs_inf_inf2 = file.elements.filter_by_text_contains(text="Инфинитив I")[1]
        # verbs_par_part1 = file.elements.filter_by_text_contains(text="Партицип I")[0]
        # verbs_par_part2 = file.elements.filter_by_text_contains(text="Партицип I")[1]
        # verbs_imp_presens = file.elements.filter_by_text_contains(text="Презенс")[1]





parser = PdfParser()
parser.open_pdf(r"C:\Users\Aleee\Desktop\lesen.pdf", word_type=ns.wordtype.verb)
parser.parse_save()


