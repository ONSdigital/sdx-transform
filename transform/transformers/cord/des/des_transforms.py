from enum import Enum


class Transform(Enum):
    VALUE = 1
    CHECKBOX = 2
    RADIO = 3
    MULTI_RADIO = 4
    THOUSANDS = 5
    COMMENT = 6


# The following dictionary defines the transformations to perform.
# The key is the qcode, the value is a list describing the transform
# and any arguments to pass.

transformations = {
    "022": [Transform.VALUE],
    "356": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "277": [
        Transform.MULTI_RADIO,
        {
            "Less than 2Mbps": {
                "qcode": "277",
                "ticked": "1",
                "unticked": "0"
            },
            "2Mbps or more, but less than 10Mbps": {
                "qcode": "278",
                "ticked": "1",
                "unticked": "0"
            },
            "10Mbps or more, but less than 30Mbps": {
                "qcode": "279",
                "ticked": "1",
                "unticked": "0"
            },
            "30Mbps or more, but less than 100Mbps": {
                "qcode": "280",
                "ticked": "1",
                "unticked": "0"
            },
            "100Mbps or more, but less than 500Mbps": {
                "qcode": "497",
                "ticked": "1",
                "unticked": "0"
            },
            "500Mbps or more, but less than 1000Mbps (1Gbps)": {
                "qcode": "498",
                "ticked": "1",
                "unticked": "0"
            },
            "1000Mbps (1Gbps) or more": {
                "qcode": "499",
                "ticked": "1",
                "unticked": "0"
            },
            "Don't know": {
                "qcode": "029",
                "ticked": "1",
                "unticked": "0"
            }
        }
    ],
    "452": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "600": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "601": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "602": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "603": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "604": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "605": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "607": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "608": [Transform.THOUSANDS],
    "609": [Transform.THOUSANDS],
    "610": [Transform.THOUSANDS],
    "611": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "612": [Transform.THOUSANDS],
    "613": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "614": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "615": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "616": [Transform.THOUSANDS],
    "617": [Transform.THOUSANDS],
    "618": [Transform.THOUSANDS],
    "619": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "620": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "621": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "622": [Transform.THOUSANDS],
    "623": [Transform.THOUSANDS],
    "624": [Transform.THOUSANDS],
    "625": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "626": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "627": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "628": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "629": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "630": [Transform.THOUSANDS],
    "631": [Transform.THOUSANDS],
    "632": [Transform.THOUSANDS],
    "633": [Transform.THOUSANDS],
    "634": [Transform.THOUSANDS],
    "635": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "636": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "637": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "638": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "639": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "640": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "641": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "642": [Transform.THOUSANDS],
    "643": [Transform.THOUSANDS],
    "644": [Transform.THOUSANDS],
    "645": [Transform.THOUSANDS],
    "646": [Transform.THOUSANDS],
    "647": [Transform.THOUSANDS],
    "648": [Transform.THOUSANDS],
    "649": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "650": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "651": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "652": [Transform.THOUSANDS],
    "653": [Transform.THOUSANDS],
    "654": [Transform.THOUSANDS],
    "655": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "656": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "657": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "658": [Transform.THOUSANDS],
    "659": [Transform.THOUSANDS],
    "660": [Transform.THOUSANDS],
    "661": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "662": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "663": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "664": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "665": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "666": [Transform.THOUSANDS],
    "667": [Transform.THOUSANDS],
    "668": [Transform.THOUSANDS],
    "669": [Transform.THOUSANDS],
    "670": [Transform.THOUSANDS],
    "671": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "672": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "673": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "674": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "675": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "676": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "677": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "678": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "679": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "680": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "681": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "682": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "683": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "684": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "685": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "686": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "687": [Transform.THOUSANDS],
    "688": [Transform.THOUSANDS],
    "689": [Transform.THOUSANDS],
    "690": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "691": [Transform.THOUSANDS],
    "692": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "693": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "694": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "695": [Transform.THOUSANDS],
    "696": [Transform.THOUSANDS],
    "697": [Transform.THOUSANDS],
    "698": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "699": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "700": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "701": [Transform.THOUSANDS],
    "702": [Transform.THOUSANDS],
    "703": [Transform.THOUSANDS],
    "704": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "705": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "706": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "707": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "708": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "709": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "710": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "711": [Transform.THOUSANDS],
    "712": [Transform.THOUSANDS],
    "713": [Transform.THOUSANDS],
    "714": [Transform.THOUSANDS],
    "715": [Transform.THOUSANDS],
    "716": [Transform.THOUSANDS],
    "717": [Transform.THOUSANDS],
    "718": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "719": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "720": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "721": [Transform.THOUSANDS],
    "722": [Transform.THOUSANDS],
    "723": [Transform.THOUSANDS],
    "724": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "725": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "726": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "727": [Transform.THOUSANDS],
    "728": [Transform.THOUSANDS],
    "729": [Transform.THOUSANDS],
    "730": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "731": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "732": [Transform.THOUSANDS],
    "733": [Transform.THOUSANDS],
    "734": [Transform.THOUSANDS],
    "736": [Transform.THOUSANDS],
    "738": [Transform.THOUSANDS],
    "739": [Transform.THOUSANDS],
    "740": [Transform.THOUSANDS],
    "741": [Transform.THOUSANDS],
    "742": [Transform.THOUSANDS],
    "743": [Transform.THOUSANDS],
    "744": [Transform.THOUSANDS],
    "745": [Transform.THOUSANDS],
    "746": [Transform.THOUSANDS],
    "747": [Transform.THOUSANDS],
    "748": [Transform.THOUSANDS],
    "749": [Transform.THOUSANDS],
    "750": [Transform.THOUSANDS],
    "751": [Transform.THOUSANDS],
    "752": [Transform.THOUSANDS],
    "753": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "754": [Transform.THOUSANDS],
    "755": [Transform.THOUSANDS],
    "756": [Transform.THOUSANDS],
    "757": [Transform.THOUSANDS],
    "758": [Transform.THOUSANDS],
    "759": [Transform.THOUSANDS],
    "760": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "761": "\u00a3's",
    "762": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "763": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "190": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "764": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "765": [Transform.THOUSANDS],
    "766": [Transform.THOUSANDS],
    "767": [Transform.THOUSANDS],
    "768": [Transform.THOUSANDS],
    "769": [Transform.THOUSANDS],
    "365": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "364": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "359": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "363": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "361": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "360": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "362": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "770": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "771": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "431": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "432": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "433": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "434": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "772": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "515": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "516": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "517": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "773": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "774": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "775": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "776": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "777": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "778": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "780": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "781": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "782": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "783": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "518": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "495": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "784": [Transform.THOUSANDS],
    "785": [
        Transform.RADIO,
        {
            "Yes": "10",
            "No": "01"
        }
    ],
    "786": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "787": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "788": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "789": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "790": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "791": [
        Transform.CHECKBOX,
        "10",
        "01"
    ],
    "792": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "793": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "794": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "795": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "796": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "797": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "484": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "483": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "486": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "487": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "481": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "275": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "274": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "272": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "482": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "485": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "798": [
        Transform.CHECKBOX,
        "1",
        "0"
    ],
    "500": [
        Transform.COMMENT,
        "1",
        "0"
    ]
}
