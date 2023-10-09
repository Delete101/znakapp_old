from .kn_kz_parser import parsing_kn_kz
from .krisha_kz_parser import parsing_krisha_kz
from .kz_m2bomber_com_parser import parsing_kz_m2bomber
from .nedvizhimostpro_kz_parser import parsing_nevdizhimostpro_kz
from .olx_kz_parser import parsing_olx_kz


def main(value: str):
    try:
        if "www.kn.kz" in value:
            parsing_kn_kz(value)  # Not clear, only parsing and input
        elif 'krisha.kz' in value:
            parsing_krisha_kz(value)  # Clear
        elif "kz.m2" in value:
            parsing_kz_m2bomber(value)  # Not clear, only pars
        elif "nedvizhimostpro.kz" in value:
            parsing_nevdizhimostpro_kz(value)  # Not clear, only pars
        elif "olx.kz" in value:
            parsing_olx_kz(value)  # Not clear, only pars
    except Exception as ex:
        print(f'Parsing error: {ex}')









