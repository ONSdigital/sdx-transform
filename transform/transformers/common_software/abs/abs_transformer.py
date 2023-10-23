from sdx_gcp.app import get_logger

from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.survey_transformer import DelegatedImageTransformer

logger = get_logger()


class ABSTransformer(DelegatedImageTransformer):
    """Perform the transforms and formatting for the ABS survey."""

    # a dictionary mapping the instrument id to the sector id required downstream
    inst_map = {'1802': '053',
                '1804': '051',
                '1808': '050',
                '1810': '055',
                '1812': '052',
                '1814': '052',
                '1818': '052',
                '1820': '052',
                '1824': '052',
                '1826': '052',
                '1862': '001',
                '1864': '001',
                '1874': '001',
                '1805': '054',
                '1875': '001',
                '1865': '001',
                '1863': '001',
                '1819': '052',
                '1825': '052',
                '1806': '054',
                '1815': '052',
                '1827': '052',
                '1821': '052',
                '1867': '001',
                '1869': '001',
                '1871': '001',
                '1877': '001',
                '1879': '001',
                '1801': '053',
                '1803': '051',
                '1807': '050',
                '1809': '055',
                '1811': '052',
                '1813': '052',
                '1817': '052',
                '1823': '052',
                '1861': '001',
                '1873': '001',
                }

    def get_pck_name(self) -> str:
        sector_id = self.inst_map[self.survey_response.instrument_id]
        pck_name = CSFormatter.pck_name(sector_id, self.survey_response.tx_id)
        return pck_name
