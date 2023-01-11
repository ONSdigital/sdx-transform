import unittest

from transform.transformers.cora.ukis.ukis_transformer import perform_transforms
from transform.transformers.cora.ukis.ukis_transforms import ukis_transformations, checkbox_qcodes


class TestUkisTransforms(unittest.TestCase):

    def test_perform_transforms(self):
        response_data = {
            "2310": "New business practices for organising procedures or external relations",
            "2340": "Marketing methods for promotion, packaging, pricing, product placement or after sales services",
            "2370": "Methods for accounting or administrative operations",
            "1010": "Your business by itself",
            "1040": "Other businesses or organisations",
            "1310": "Yes",
            "1410": "10000",
            "1320": "Yes",
            "1420": "5000",
            "1330": "Yes",
            "1332": "Computer hardware",
            "1333": "Computer software",
            "1430": "2000",
            "1340": "Yes",
            "1440": "3000",
            "1350": "Yes",
            "1450": "7000",
            "1360": "Yes",
            "1460": "8050",
            "1370": "Yes",
            "1371": "Changes to product or service design",
            "1373": "Changes to marketing methods",
            "1470": "10000",
            "0510": "Yes",
            "0520": "Yes",
            "0602": "Your business with other businesses or organisations",
            "0603": "Your business by adapting or modifying processes originally developed by other businesses or organisations",
            "0710": "Yes",
            "0720": "Yes",
            "0810": "30",
            "0820": "67",
            "0840": "5",
            "1510": "Innovation activities were abandoned",
            "2657": "Medium importance",
            "2658": "High importance",
            "2659": "Low importance",
            "2660": "Not important",
            "2661": "High importance",
            "2662": "Medium importance",
            "2663": "Low importance",
            "2664": "Not important",
            "2665": "Not important",
            "2666": "Low importance",
            "2667": "Medium importance",
            "2678": "High importance",
            "2680": "Medium importance",
            "2681": "Low importance",
            "2682": "Not important",
            "1210": "High importance",
            "1211": "Medium importance",
            "1220": "Low importance",
            "1230": "Not important",
            "1240": "Low importance",
            "1250": "Medium importance",
            "1290": "High importance",
            "1260": "Not important",
            "1270": "Low importance",
            "1212": "Medium importance",
            "1213": "High importance",
            "1280": "Low importance",
            "1282": "Not important",
            "1281": "Medium importance",
            "1283": "High importance",
            "1601": "High importance",
            "1620": "Medium importance",
            "1631": "Low importance",
            "1632": "Not important",
            "1640": "High importance",
            "1650": "Medium importance",
            "1660": "Low importance",
            "1670": "Not important",
            "1680": "High importance",
            "1610": "Medium importance",
            "1611": "Low importance",
            "1690": "Not important",
            "1691": "High importance",
            "1692": "Medium importance",
            "2103": "Any other business activities",
            "1812": "UK",
            "1813": "EU or EFTA countries",
            "1823": "EU or EFTA countries",
            "1824": "All other countries",
            "1882": "UK",
            "1891": "We did not co-operate with clients or customers from the public sector",
            "1844": "All other countries",
            "1852": "UK",
            "1853": "EU or EFTA countries",
            "1854": "All other countries",
            "1862": "UK",
            "1863": "EU or EFTA countries",
            "2121": "Further than 15 miles from the physical sites of your business and within the UK",
            "1871": "We did not co-operate with government or public research institutes",
            "1877": "EU or EFTA countries",
            "1878": "All other countries",
            "1880": "UK",
            "1898": "We did not co-operate with regulatory bodies",
            "1902": "EU or EFTA countries",
            "2650": "40-90%",
            "2651": "Over 90%",
            "2652": "Less than 40%",
            "2654": "None",
            "2655": "Less than 40%",
            "2656": "40-90%",
            "2669": "UK central government",
            "2670": "European Union (EU) institutions or programmes",
            "2672": "Direct financial support",
            "2673": "Indirect financial support: Research and Development tax credits",
            "2450": "Yes",
            "2610": "10",
            "2620": "34",
            "2631": "Graphic arts, layout, advertising",
            "2633": "Multimedia, web design",
            "2634": "Software development, database management",
            "2636": "Mathematics, statistics",
            "2201": "Accountancy software",
            "2203": "Electronic invoicing (e-invoicing)",
            "2205": "HR management software",
            "2206": "Videoconferencing software",
            "2213": "Cloud based computing",
            "2214": "Computer aided design (CAD) software",
            "2215": "Internet of things (IoT)",
            "2220": "Yes",
            "2221": "No, they were not significant",
            "2222": "Yes",
            "2223": "Yes, they were significant",
            "2224": "Yes",
            "2225": "No, they were not significant",
            "2226": "No",
            "2228": "Yes",
            "2229": "No, they were not significant",
            "2230": "Yes",
            "2231": "Yes, they were significant",
            "2232": "Yes",
            "2233": "No, they were not significant",
            "2234": "No",
            "2236": "No",
            "2238": "Yes",
            "2239": "No, they were not significant",
            "2700": "Here is a comment about additional information",
            "2801": "1",
            "2800": "21",
            "2900": "Yes"
        }

        expected = {
             '0510': '10',
             '0520': '10',
             '0601': '',
             '0602': '1',
             '0603': '1',
             '0604': '',
             '0710': '10',
             '0720': '10',
             '0810': '30',
             '0820': '67',
             '0840': '5',
             '1010': '1',
             '1020': '',
             '1030': '',
             '1040': '1',
             '1210': '1000',
             '1211': '0100',
             '1212': '0100',
             '1213': '1000',
             '1220': '0010',
             '1230': '0001',
             '1240': '0010',
             '1250': '0100',
             '1260': '0001',
             '1270': '0010',
             '1280': '0010',
             '1281': '0100',
             '1282': '0001',
             '1283': '1000',
             '1290': '1000',
             '1310': '10',
             '1320': '10',
             '1330': '10',
             '1331': '',
             '1332': '1',
             '1333': '1',
             '1340': '10',
             '1350': '10',
             '1360': '10',
             '1370': '10',
             '1371': '1',
             '1372': '',
             '1373': '1',
             '1374': '',
             '1410': '10',
             '1420': '5',
             '1430': '2',
             '1440': '3',
             '1450': '7',
             '1460': '8',
             '1470': '10',
             '1510': '1',
             '1520': '',
             '1540': '',
             '1601': '1000',
             '1610': '0100',
             '1611': '0010',
             '1620': '0100',
             '1631': '0010',
             '1632': '0001',
             '1640': '1000',
             '1650': '0100',
             '1660': '0010',
             '1670': '0001',
             '1680': '1000',
             '1690': '0001',
             '1691': '1000',
             '1692': '0100',
             '1811': '',
             '1812': '1',
             '1813': '1',
             '1814': '',
             '1821': '',
             '1822': '',
             '1823': '1',
             '1824': '1',
             '1841': '',
             '1842': '',
             '1843': '',
             '1844': '1',
             '1851': '',
             '1852': '1',
             '1853': '1',
             '1854': '1',
             '1861': '',
             '1862': '1',
             '1863': '1',
             '1864': '',
             '1871': '1',
             '1872': '',
             '1873': '',
             '1874': '',
             '1875': '',
             '1876': '',
             '1877': '1',
             '1878': '1',
             '1879': '',
             '1880': '1',
             '1881': '',
             '1882': '1',
             '1883': '',
             '1884': '',
             '1885': '',
             '1886': '',
             '1891': '1',
             '1892': '',
             '1893': '',
             '1894': '',
             '1895': '',
             '1896': '',
             '1897': '',
             '1898': '1',
             '1901': '',
             '1902': '1',
             '1903': '',
             '1904': '',
             '2011': '',
             '2020': '',
             '2030': '',
             '2031': '',
             '2032': '',
             '2033': '',
             '2101': '',
             '2102': '',
             '2103': '1',
             '2104': '',
             '2121': 'temp answer',
             '2201': '1',
             '2202': '',
             '2203': '1',
             '2204': '',
             '2205': '1',
             '2206': '1',
             '2211': '',
             '2212': '',
             '2213': '1',
             '2214': '1',
             '2215': '1',
             '2216': '',
             '2220': '10',
             '2221': '01',
             '2222': '10',
             '2223': '10',
             '2224': '10',
             '2225': '01',
             '2226': '01',
             '2228': '10',
             '2229': '01',
             '2230': '10',
             '2231': '10',
             '2232': '10',
             '2233': '01',
             '2234': '01',
             '2236': '01',
             '2238': '10',
             '2239': '01',
             '2310': '1',
             '2320': '',
             '2330': '',
             '2340': '1',
             '2350': '',
             '2360': '',
             '2370': '1',
             '2380': '',
             '2450': '10',
             '2610': '10',
             '2620': '34',
             '2631': '1',
             '2632': '',
             '2633': '1',
             '2634': '1',
             '2635': '',
             '2636': '1',
             '2637': '',
             '2650': '0010',
             '2651': '0001',
             '2652': '0011',
             '2654': '0100',
             '2655': '0011',
             '2656': '0010',
             '2657': '0100',
             '2658': '1000',
             '2659': '0010',
             '2660': '0001',
             '2661': '1000',
             '2662': '0100',
             '2663': '0010',
             '2664': '0001',
             '2665': '0001',
             '2666': '0010',
             '2667': '0100',
             '2668': '',
             '2669': '1',
             '2670': '1',
             '2671': '',
             '2672': '1',
             '2673': '1',
             '2674': '',
             '2678': '1000',
             '2679': '',
             '2680': '0100',
             '2681': '0010',
             '2682': '0001',
             '2700': '1',
             '2801': '1',
             '2900': '10'
            }

        actual = perform_transforms(response_data, ukis_transformations, checkbox_qcodes)

        self.assertEqual(expected, actual)
