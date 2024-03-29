import unittest

from transform.transformers.common_software.acas.acas_transformer import perform_transforms


class TestAcasTransforms(unittest.TestCase):

    def test_perform_transforms(self):
        response_data = {
            "9999": "Yes, I can report for this period",
            "9998": "Yes",
            "150": "123456",
            "151": "23543",
            "152": "20210",
            "153": "5000",
            "154": "72456",
            "155": "27543",
            "156": "12474",
            "9997": "Yes",
            "159": "20543",
            "160": "42631",
            "161": "9582",
            "162": "1932",
            "163": "12654",
            "164": "22344",
            "165": "35210",
            "166": "32000",
            "167": "54109",
            "168": "32281",
            "169": "12000",
            "170": "22821",
            "171": "43354",
            "172": "22358",
            "173": "1500",
            "9996": "Yes",
            "200": "12000",
            "201": "22364",
            "202": "16345",
            "203": "45754",
            "204": "4567",
            "205": "123",
            "206": "5467",
            "207": "742",
            "208": "55667",
            "209": "22765",
            "210": "12456",
            "211": "54737",
            "212": "0",
            "213": "0",
            "214": "0",
            "215": "0",
            "218": "5000",
            "219": "7250",
            "220": "355",
            "221": "563",
            "9995": "Yes",
            "225": "Other Transport Assets",
            "226": "54210",
            "227": "65783",
            "9994": "No",
            "9991": "Yes",
            "300": "54360",
            "301": "12021",
            "302": "12000",
            "303": "0",
            "304": "1243",
            "305": "423",
            "306": "500",
            "307": "0",
            "308": "750",
            "309": "0",
            "310": "235.50",
            "311": "75.54",
            "9990": "Yes",
            "315": "56212",
            "316": "78000",
            "317": "56.43",
            "318": "122.87",
            "319": "102.65",
            "320": "12.34",
            "321": "75",
            "322": "56.23",
            "9989": "Yes",
            "400": "4523",
            "401": "65.12",
            "402": "22234",
            "403": "12652",
            "404": "7654",
            "405": "31278.54",
            "406": "596",
            "407": "12.50",
            "408": "11053",
            "409": "230",
            "410": "576",
            "411": "224",
            "412": "745",
            "413": "12.99",
            "414": "9.99",
            "415": "0",
            "416": "1943",
            "417": "72.45",
            "418": "12.43",
            "419": "1.50",
            "420": "234",
            "421": "56",
            "9988": "Yes",
            "500": "4310",
            "501": "5647",
            "502": "22450",
            "503": "12345",
            "504": "3456",
            "505": "8765",
            "506": "78943",
            "507": "22345",
            "508": "45764",
            "509": "6321",
            "510": "65853",
            "511": "6548",
            "512": "765",
            "513": "12",
            "514": "12350",
            "515": "6754",
            "516": "4372",
            "517": "87",
            "518": "432",
            "519": "785",
            "9987": "Yes",
            "601": "4536",
            "602": "742",
            "603": "7542",
            "604": "6543",
            "605": "22357",
            "606": "6542",
            "607": "232546",
            "608": "45675",
            "609": "765",
            "610": "20.54",
            "611": "12000",
            "612": "0",
            "613": "3541",
            "614": "654",
            "615": "6543",
            "616": "653",
            "617": "74265",
            "618": "6532",
            "9986": "Yes",
            "700": "6542",
            "701": "543",
            "702": "9754",
            "703": "43",
            "704": "5785",
            "705": "543",
            "706": "12000",
            "707": "1023",
            "708": "654",
            "709": "3",
            "710": "543",
            "711": "43",
            "712": "22.88",
            "713": "12.20",
            "714": "643",
            "715": "43",
            "9985": "Yes",
            "800": "6546",
            "801": "432",
            "802": "7658",
            "803": "654",
            "804": "4325",
            "805": "532",
            "806": "7657",
            "807": "876",
            "9984": "Yes",
            "811": "Widgets",
            "812": "76543",
            "813": "1245",
            "9983": "Yes",
            "814": "More widgets",
            "815": "6546",
            "816": "432",
            "9982": "No",
            "9978": "Yes",
            "901": "54356",
            "9977": "Yes",
            "904": "8",
            "905": "6",
            "146": "Excellent survey!",
            "906": "0",
            "907": "30"
        }
        actual = perform_transforms(response_data)
        expected = {'146': 1,
                    '150': 123,
                    '151': 24,
                    '152': 20,
                    '153': 5,
                    '154': 72,
                    '155': 28,
                    '156': 12,
                    '157': 2,
                    '158': 227,
                    '159': 21,
                    '160': 43,
                    '161': 10,
                    '162': 2,
                    '163': 13,
                    '164': 22,
                    '165': 35,
                    '166': 32,
                    '167': 54,
                    '168': 32,
                    '169': 12,
                    '170': 23,
                    '171': 43,
                    '172': 22,
                    '173': 2,
                    '174': 2,
                    '175': 188,
                    '176': 178,
                    '200': 12,
                    '201': 22,
                    '202': 16,
                    '203': 46,
                    '204': 5,
                    '205': 0,
                    '206': 5,
                    '207': 1,
                    '208': 56,
                    '209': 23,
                    '210': 12,
                    '211': 55,
                    '212': 0,
                    '213': 0,
                    '214': 0,
                    '215': 0,
                    '218': 5,
                    '219': 7,
                    '220': 0,
                    '221': 1,
                    '222': 2,
                    '223': 163,
                    '224': 103,
                    '225': 1,
                    '226': 54,
                    '227': 66,
                    '228': 2,
                    '231': 2,
                    '234': 2,
                    '237': 2,
                    '238': 54,
                    '239': 66,
                    '300': 54,
                    '301': 12,
                    '302': 12,
                    '303': 0,
                    '304': 1,
                    '305': 0,
                    '306': 1,
                    '307': 0,
                    '308': 1,
                    '309': 0,
                    '310': 0,
                    '311': 0,
                    '312': 2,
                    '313': 69,
                    '314': 12,
                    '315': 56,
                    '316': 78,
                    '317': 0,
                    '318': 0,
                    '319': 0,
                    '320': 0,
                    '321': 0,
                    '322': 0,
                    '323': 2,
                    '324': 56,
                    '325': 78,
                    '400': 5,
                    '401': 0,
                    '402': 22,
                    '403': 13,
                    '404': 8,
                    '405': 31,
                    '406': 1,
                    '407': 0,
                    '408': 11,
                    '409': 0,
                    '410': 1,
                    '411': 0,
                    '412': 1,
                    '413': 0,
                    '414': 0,
                    '415': 0,
                    '416': 2,
                    '417': 0,
                    '418': 0,
                    '419': 0,
                    '420': 0,
                    '421': 0,
                    '422': 2,
                    '423': 51,
                    '424': 44,
                    '500': 4,
                    '501': 6,
                    '502': 22,
                    '503': 12,
                    '504': 3,
                    '505': 9,
                    '506': 79,
                    '507': 22,
                    '508': 46,
                    '509': 6,
                    '510': 66,
                    '511': 7,
                    '512': 1,
                    '513': 0,
                    '514': 12,
                    '515': 7,
                    '516': 4,
                    '517': 0,
                    '518': 0,
                    '519': 1,
                    '520': 2,
                    '521': 237,
                    '522': 70,
                    '601': 5,
                    '602': 1,
                    '603': 8,
                    '604': 7,
                    '605': 22,
                    '606': 7,
                    '607': 233,
                    '608': 46,
                    '609': 1,
                    '610': 0,
                    '611': 12,
                    '612': 0,
                    '613': 4,
                    '614': 1,
                    '615': 7,
                    '616': 1,
                    '617': 74,
                    '618': 7,
                    '619': 2,
                    '620': 366,
                    '621': 70,
                    '700': 7,
                    '701': 1,
                    '702': 10,
                    '703': 0,
                    '704': 6,
                    '705': 1,
                    '706': 12,
                    '707': 1,
                    '708': 1,
                    '709': 0,
                    '710': 1,
                    '711': 0,
                    '712': 0,
                    '713': 0,
                    '714': 1,
                    '715': 0,
                    '716': 2,
                    '717': 38,
                    '718': 3,
                    '800': 7,
                    '801': 0,
                    '802': 8,
                    '803': 1,
                    '804': 4,
                    '805': 1,
                    '806': 8,
                    '807': 1,
                    '808': 2,
                    '809': 27,
                    '810': 3,
                    '811': 1,
                    '812': 77,
                    '813': 1,
                    '814': 1,
                    '815': 7,
                    '816': 0,
                    '817': 2,
                    '820': 2,
                    '823': 2,
                    '826': 2,
                    '829': 2,
                    '830': 84,
                    '831': 1,
                    '900': 2,
                    '901': 54,
                    '902': 1,
                    '903': 2,
                    '904': 8,
                    '905': 6}

        self.assertEqual(expected, actual)

    def test_perform_transforms_with_no_comment(self):
        response_data = {
            "9999": "Yes, I can report for this period",
            "9998": "Yes",
            "150": "-20",
            "151": "23543",
            "152": "20210",
            "153": "5000",
            "154": "72456",
            "155": "27543",
            "156": "12474",
            "9997": "Yes",
            "159": "20543",
            "160": "42631",
            "161": "9582",
            "162": "1932",
            "163": "12654",
            "164": "22344",
            "165": "35210",
            "166": "32000",
            "167": "54109",
            "168": "32281",
            "169": "12000",
            "170": "22821",
            "171": "43354",
            "172": "22358",
            "173": "1500",
            "9996": "Yes",
            "200": "12000",
            "201": "22364",
            "202": "16345",
            "203": "45754",
            "204": "4567",
            "205": "123",
            "206": "5467",
            "207": "742",
            "208": "55667",
            "209": "22765",
            "210": "12456",
            "211": "54737",
            "212": "0",
            "213": "0",
            "214": "0",
            "215": "0",
            "218": "5000",
            "219": "7250",
            "220": "355",
            "221": "563",
            "9995": "Yes",
            "225": "Other Transport Assets",
            "226": "54210",
            "227": "65783",
            "9994": "No",
            "9991": "Yes",
            "300": "54360",
            "301": "12021",
            "302": "12000",
            "303": "0",
            "304": "1243",
            "305": "423",
            "306": "500",
            "307": "0",
            "308": "750",
            "309": "0",
            "310": "235.50",
            "311": "75.54",
            "9990": "Yes",
            "315": "56212",
            "316": "78000",
            "317": "56.43",
            "318": "122.87",
            "319": "102.65",
            "320": "12.34",
            "321": "75",
            "322": "56.23",
            "9989": "Yes",
            "400": "4523",
            "401": "65.12",
            "402": "22234",
            "403": "12652",
            "404": "7654",
            "405": "31278.54",
            "406": "596",
            "407": "12.50",
            "408": "11053",
            "409": "230",
            "410": "576",
            "411": "224",
            "412": "745",
            "413": "12.99",
            "414": "9.99",
            "415": "0",
            "416": "1943",
            "417": "72.45",
            "418": "12.43",
            "419": "1.50",
            "420": "234",
            "421": "56",
            "9988": "Yes",
            "500": "4310",
            "501": "5647",
            "502": "22450",
            "503": "12345",
            "504": "3456",
            "505": "8765",
            "506": "78943",
            "507": "22345",
            "508": "45764",
            "509": "6321",
            "510": "65853",
            "511": "6548",
            "512": "765",
            "513": "12",
            "514": "12350",
            "515": "6754",
            "516": "4372",
            "517": "87",
            "518": "432",
            "519": "785",
            "9987": "Yes",
            "601": "4536",
            "602": "742",
            "603": "7542",
            "604": "6543",
            "605": "22357",
            "606": "6542",
            "607": "232546",
            "608": "45675",
            "609": "765",
            "610": "20.54",
            "611": "12000",
            "612": "0",
            "613": "3541",
            "614": "654",
            "615": "6543",
            "616": "653",
            "617": "74265",
            "618": "6532",
            "9986": "Yes",
            "700": "6542",
            "701": "543",
            "702": "9754",
            "703": "43",
            "704": "5785",
            "705": "543",
            "706": "12000",
            "707": "1023",
            "708": "654",
            "709": "3",
            "710": "543",
            "711": "43",
            "712": "22.88",
            "713": "12.20",
            "714": "643",
            "715": "43",
            "9985": "Yes",
            "800": "6546",
            "801": "432",
            "802": "7658",
            "803": "654",
            "804": "4325",
            "805": "532",
            "806": "7657",
            "807": "876",
            "9984": "Yes",
            "811": "Widgets",
            "812": "76543",
            "813": "1245",
            "9983": "Yes",
            "814": "More widgets",
            "815": "6546",
            "816": "432",
            "9982": "No",
            "9978": "Yes",
            "901": "54356",
            "9977": "Yes",
            "904": "8",
            "905": "6",
            "906": "0",
            "907": "30"
        }
        actual = perform_transforms(response_data)
        expected = {'146': 2,
                    '150': 99999999999,
                    '151': 24,
                    '152': 20,
                    '153': 5,
                    '154': 72,
                    '155': 28,
                    '156': 12,
                    '157': 2,
                    '158': 104,
                    '159': 21,
                    '160': 43,
                    '161': 10,
                    '162': 2,
                    '163': 13,
                    '164': 22,
                    '165': 35,
                    '166': 32,
                    '167': 54,
                    '168': 32,
                    '169': 12,
                    '170': 23,
                    '171': 43,
                    '172': 22,
                    '173': 2,
                    '174': 2,
                    '175': 188,
                    '176': 178,
                    '200': 12,
                    '201': 22,
                    '202': 16,
                    '203': 46,
                    '204': 5,
                    '205': 0,
                    '206': 5,
                    '207': 1,
                    '208': 56,
                    '209': 23,
                    '210': 12,
                    '211': 55,
                    '212': 0,
                    '213': 0,
                    '214': 0,
                    '215': 0,
                    '218': 5,
                    '219': 7,
                    '220': 0,
                    '221': 1,
                    '222': 2,
                    '223': 163,
                    '224': 103,
                    '225': 1,
                    '226': 54,
                    '227': 66,
                    '228': 2,
                    '231': 2,
                    '234': 2,
                    '237': 2,
                    '238': 54,
                    '239': 66,
                    '300': 54,
                    '301': 12,
                    '302': 12,
                    '303': 0,
                    '304': 1,
                    '305': 0,
                    '306': 1,
                    '307': 0,
                    '308': 1,
                    '309': 0,
                    '310': 0,
                    '311': 0,
                    '312': 2,
                    '313': 69,
                    '314': 12,
                    '315': 56,
                    '316': 78,
                    '317': 0,
                    '318': 0,
                    '319': 0,
                    '320': 0,
                    '321': 0,
                    '322': 0,
                    '323': 2,
                    '324': 56,
                    '325': 78,
                    '400': 5,
                    '401': 0,
                    '402': 22,
                    '403': 13,
                    '404': 8,
                    '405': 31,
                    '406': 1,
                    '407': 0,
                    '408': 11,
                    '409': 0,
                    '410': 1,
                    '411': 0,
                    '412': 1,
                    '413': 0,
                    '414': 0,
                    '415': 0,
                    '416': 2,
                    '417': 0,
                    '418': 0,
                    '419': 0,
                    '420': 0,
                    '421': 0,
                    '422': 2,
                    '423': 51,
                    '424': 44,
                    '500': 4,
                    '501': 6,
                    '502': 22,
                    '503': 12,
                    '504': 3,
                    '505': 9,
                    '506': 79,
                    '507': 22,
                    '508': 46,
                    '509': 6,
                    '510': 66,
                    '511': 7,
                    '512': 1,
                    '513': 0,
                    '514': 12,
                    '515': 7,
                    '516': 4,
                    '517': 0,
                    '518': 0,
                    '519': 1,
                    '520': 2,
                    '521': 237,
                    '522': 70,
                    '601': 5,
                    '602': 1,
                    '603': 8,
                    '604': 7,
                    '605': 22,
                    '606': 7,
                    '607': 233,
                    '608': 46,
                    '609': 1,
                    '610': 0,
                    '611': 12,
                    '612': 0,
                    '613': 4,
                    '614': 1,
                    '615': 7,
                    '616': 1,
                    '617': 74,
                    '618': 7,
                    '619': 2,
                    '620': 366,
                    '621': 70,
                    '700': 7,
                    '701': 1,
                    '702': 10,
                    '703': 0,
                    '704': 6,
                    '705': 1,
                    '706': 12,
                    '707': 1,
                    '708': 1,
                    '709': 0,
                    '710': 1,
                    '711': 0,
                    '712': 0,
                    '713': 0,
                    '714': 1,
                    '715': 0,
                    '716': 2,
                    '717': 38,
                    '718': 3,
                    '800': 7,
                    '801': 0,
                    '802': 8,
                    '803': 1,
                    '804': 4,
                    '805': 1,
                    '806': 8,
                    '807': 1,
                    '808': 2,
                    '809': 27,
                    '810': 3,
                    '811': 1,
                    '812': 77,
                    '813': 1,
                    '814': 1,
                    '815': 7,
                    '816': 0,
                    '817': 2,
                    '820': 2,
                    '823': 2,
                    '826': 2,
                    '829': 2,
                    '830': 84,
                    '831': 1,
                    '900': 2,
                    '901': 54,
                    '902': 1,
                    '903': 2,
                    '904': 8,
                    '905': 6}

        self.assertEqual(expected, actual)
