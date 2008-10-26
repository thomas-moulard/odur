#!/usr/bin/env python
# -*- coding: utf-8 -*-

#FIXME: replace country list by a real list with country codes.
#FIXME: search what means '.' in the second column.

# CURRENCY: (CURRENCY_CODE, DIGITS_AFTER_DOT, CURRENCY_NAME, COUNTRIES)
# See: http://en.wikipedia.org/wiki/ISO_4217
ISO_4217 = {
    'AED': (784, 2, 'United Arab Emirates dirham', 'United Arab Emirates'),
    'AFN': (971, 2, 'Afghani', 'Afghanistan'),
    'ALL': (  8, 2, 'Lek', 'Albania'),
    'AMD': ( 51, 2, 'Armenian dram', 'Armenia'),
    'ANG': (532, 2, 'Netherlands Antillean guilder', 'Netherlands Antilles'),
    'AOA': (973, 2, 'Kwanza', 'Angola'),
    'ARS': ( 32, 2, 'Argentine peso', 'Argentina'),
    'AUD': ( 36, 2, 'Australian dollar', 'Australia, Australian Antarctic Territory, Christmas Island, Cocos (Keeling) Islands, Heard and McDonald Islands, Kiribati, Nauru, Norfolk Island, Tuvalu'),
    'AWG': (533, 2, 'Aruban guilder', 'Aruba'),
    'AZN': (944, 2, 'Azerbaijanian manat', 'Azerbaijan'),
    'BAM': (977, 2, 'Convertible marks', 'Bosnia and Herzegovina'),
    'BBD': ( 52, 2, 'Barbados dollar', 'Barbados'),
    'BDT': ( 50, 2, 'Bangladeshi taka', 'Bangladesh'),
    'BGN': (975, 2, 'Bulgarian lev', 'Bulgaria'),
    'BHD': ( 48, 3, 'Bahraini dinar', 'Bahrain'),
    'BIF': (108, 0, 'Burundian franc', 'Burundi'),
    'BMD': ( 60, 2, 'Bermudian dollar (customarily known as Bermuda dollar)', 'Bermuda'),
    'BND': ( 96, 2, 'Brunei dollar', 'Brunei, Singapore'),
    'BOB': ( 68, 2, 'Boliviano', 'Bolivia'),
    'BOV': (984, 2, 'Bolivian Mvdol (funds code)', 'Bolivia'),
    'BRL': (986, 2, 'Brazilian real', 'Brazil'),
    'BSD': ( 44, 2, 'Bahamian dollar', 'Bahamas'),
    'BTN': ( 64, 2, 'Ngultrum', 'Bhutan'),
    'BWP': ( 72, 2, 'Pula', 'Botswana'),
    'BYR': (974, 0, 'Belarussian ruble', 'Belarus'),
    'BZD': ( 84, 2, 'Belize dollar', 'Belize'),
    'CAD': (124, 2, 'Canadian dollar', 'Canada'),
    'CDF': (976, 2, 'Franc Congolais', 'Democratic Republic of Congo'),
    'CHE': (947, 2, 'WIR euro (complementary currency)', 'Switzerland'),
    'CHF': (756, 2, 'Swiss franc', 'Switzerland, Liechtenstein'),
    'CHW': (948, 2, 'WIR franc (complementary currency)', 'Switzerland'),
    'CLF': (990, 0, 'Unidad de Fomento (funds code)', 'Chile'),
    'CLP': (152, 0, 'Chilean peso', 'Chile'),
    'CNY': (156, 2, 'Renminbi', 'Mainland China'),
    'COP': (170, 2, 'Colombian peso', 'Colombia'),
    'COU': (970, 2, 'Unidad de Valor Real', 'Colombia'),
    'CRC': (188, 2, 'Costa Rican colon', 'Costa Rica'),
    'CUP': (192, 2, 'Cuban peso', 'Cuba'),
    'CVE': (132, 2, 'Cape Verde escudo', 'Cape Verde'),
    'CZK': (203, 2, 'Czech koruna', 'Czech Republic'),
    'DJF': (262, 0, 'Djibouti franc', 'Djibouti'),
    'DKK': (208, 2, 'Danish krone', 'Denmark, Faroe Islands, Greenland'),
    'DOP': (214, 2, 'Dominican peso', 'Dominican Republic'),
    'DZD': ( 12, 2, 'Algerian dinar', 'Algeria'),
    'EEK': (233, 2, 'Kroon', 'Estonia'),
    'EGP': (818, 2, 'Egyptian pound', 'Egypt'),
    'ERN': (232, 2, 'Nakfa', 'Eritrea'),
    'ETB': (230, 2, 'Ethiopian birr', 'Ethiopia'),
    'EUR': (978, 2, 'Euro', '15 European Union countries, Andorra, Kosovo, Monaco, Montenegro, San Marino, Vatican; see eurozone'),
    'FJD': (242, 2, 'Fiji dollar', 'Fiji'),
    'FKP': (238, 2, 'Falkland Islands pound', 'Falkland Islands'),
    'GBP': (826, 2, 'Pound sterling', 'United Kingdom, Crown Dependencies (the Isle of Man and the Channel Islands), certain British Overseas Territories (South Georgia and the South Sandwich Islands, British Antarctic Territory and British Indian Ocean Territory)'),
    'GEL': (981, 2, 'Lari', 'Georgia'),
    'GHS': (936, 2, 'Cedi', 'Ghana'),
    'GIP': (292, 2, 'Gibraltar pound', 'Gibraltar'),
    'GMD': (270, 2, 'Dalasi', 'Gambia'),
    'GNF': (324, 0, 'Guinea franc', 'Guinea'),
    'GTQ': (320, 2, 'Quetzal', 'Guatemala'),
    'GYD': (328, 2, 'Guyana dollar', 'Guyana'),
    'HKD': (344, 2, 'Hong Kong dollar', 'Hong Kong Special Administrative Region'),
    'HNL': (340, 2, 'Lempira', 'Honduras'),
    'HRK': (191, 2, 'Croatian kuna', 'Croatia'),
    'HTG': (332, 2, 'Haiti gourde', 'Haiti'),
    'HUF': (348, 2, 'Forint', 'Hungary'),
    'IDR': (360, 2, 'Rupiah', 'Indonesia'),
    'ILS': (376, 2, 'Israeli new sheqel', 'Israel'),
    'INR': (356, 2, 'Indian rupee', 'Bhutan, India'),
    'IQD': (368, 3, 'Iraqi dinar', 'Iraq'),
    'IRR': (364, 2, 'Iranian rial', 'Iran'),
    'ISK': (352, 0, 'Iceland krona', 'Iceland'),
    'JMD': (388, 2, 'Jamaican dollar', 'Jamaica'),
    'JOD': (400, 3, 'Jordanian dinar', 'Jordan'),
    'JPY': (392, 0, 'Japanese yen', 'Japan'),
    'KES': (404, 2, 'Kenyan shilling', 'Kenya'),
    'KGS': (417, 2, 'Som', 'Kyrgyzstan'),
    'KHR': (116, 2, 'Riel', 'Cambodia'),
    'KMF': (174, 0, 'Comoro franc', 'Comoros'),
    'KPW': (408, 2, 'North Korean won', 'North Korea'),
    'KRW': (410, 0, 'South Korean won', 'South Korea'),
    'KWD': (414, 3, 'Kuwaiti dinar', 'Kuwait'),
    'KYD': (136, 2, 'Cayman Islands dollar', 'Cayman Islands'),
    'KZT': (398, 2, 'Tenge', 'Kazakhstan'),
    'LAK': (418, 2, 'Kip', 'Laos'),
    'LBP': (422, 2, 'Lebanese pound', 'Lebanon'),
    'LKR': (144, 2, 'Sri Lanka rupee', 'Sri Lanka'),
    'LRD': (430, 2, 'Liberian dollar', 'Liberia'),
    'LSL': (426, 2, 'Loti', 'Lesotho'),
    'LTL': (440, 2, 'Lithuanian litas', 'Lithuania'),
    'LVL': (428, 2, 'Latvian lats', 'Latvia'),
    'LYD': (434, 3, 'Libyan dinar', 'Libya'),
    'MAD': (504, 2, 'Moroccan dirham', 'Morocco, Western Sahara'),
    'MDL': (498, 2, 'Moldovan leu', 'Moldova'),
    'MGA': (969, '0.7', 'Malagasy ariary', 'Madagascar'),
    'MKD': (807, 2, 'Denar', 'The former Yugoslav Republic of Macedonia'),
    'MMK': (104, 2, 'Kyat', 'Myanmar'),
    'MNT': (496, 2, 'Tugrik', 'Mongolia'),
    'MOP': (446, 2, 'Pataca', 'Macau Special Administrative Region'),
    'MRO': (478, '0.7', 'Ouguiya', 'Mauritania'),
    'MUR': (480, 2, 'Mauritius rupee', 'Mauritius'),
    'MVR': (462, 2, 'Rufiyaa', 'Maldives'),
    'MWK': (454, 2, 'Kwacha', 'Malawi'),
    'MXN': (484, 2, 'Mexican peso', 'Mexico'),
    'MXV': (979, 2, 'Mexican Unidad de Inversion (UDI) (funds code)', 'Mexico'),
    'MYR': (458, 2, 'Malaysian ringgit', 'Malaysia'),
    'MZN': (943, 2, 'Metical', 'Mozambique'),
    'NAD': (516, 2, 'Namibian dollar', 'Namibia'),
    'NGN': (566, 2, 'Naira', 'Nigeria'),
    'NIO': (558, 2, 'Cordoba oro', 'Nicaragua'),
    'NOK': (578, 2, 'Norwegian krone', 'Norway'),
    'NPR': (524, 2, 'Nepalese rupee', 'Nepal'),
    'NZD': (554, 2, 'New Zealand dollar', 'Cook Islands, New Zealand, Niue, Pitcairn, Tokelau'),
    'OMR': (512, 3, 'Rial Omani', 'Oman'),
    'PAB': (590, 2, 'Balboa', 'Panama'),
    'PEN': (604, 2, 'Nuevo sol', 'Peru'),
    'PGK': (598, 2, 'Kina', 'Papua New Guinea'),
    'PHP': (608, 2, 'Philippine peso', 'Philippines'),
    'PKR': (586, 2, 'Pakistan rupee', 'Pakistan'),
    'PLN': (985, 2, 'Zloty', 'Poland'),
    'PYG': (600, 0, 'Guarani', 'Paraguay'),
    'QAR': (634, 2, 'Qatari rial', 'Qatar'),
    'RON': (946, 2, 'Romanian new leu', 'Romania'),
    'RSD': (941, 2, 'Serbian dinar', 'Serbia'),
    'RUB': (643, 2, 'Russian rouble', 'Russia, Abkhazia, South Ossetia'),
    'RWF': (646, 0, 'Rwanda franc', 'Rwanda'),
    'SAR': (682, 2, 'Saudi riyal', 'Saudi Arabia'),
    'SBD': ( 90, 2, 'Solomon Islands dollar', 'Solomon Islands'),
    'SCR': (690, 2, 'Seychelles rupee', 'Seychelles'),
    'SDG': (938, 2, 'Sudanese pound', 'Sudan'),
    'SEK': (752, 2, 'Swedish krona', 'Sweden'),
    'SGD': (702, 2, 'Singapore dollar', 'Singapore, Brunei'),
    'SHP': (654, 2, 'Saint Helena pound', 'Saint Helena'),
    'SKK': (703, 2, 'Slovak koruna', 'Slovakia'),
    'SLL': (694, 2, 'Leone', 'Sierra Leone'),
    'SOS': (706, 2, 'Somali shilling', 'Somalia'),
    'SRD': (968, 2, 'Surinam dollar', 'Suriname'),
    'STD': (678, 2, 'Dobra', 'São Tomé and Príncipe'),
    'SYP': (760, 2, 'Syrian pound', 'Syria'),
    'SZL': (748, 2, 'Lilangeni', 'Swaziland'),
    'THB': (764, 2, 'Baht', 'Thailand'),
    'TJS': (972, 2, 'Somoni', 'Tajikistan'),
    'TMM': (795, 2, 'Manat', 'Turkmenistan'),
    'TND': (788, 3, 'Tunisian dinar', 'Tunisia'),
    'TOP': (776, 2, 'Pa\'anga', 'Tonga'),
    'TRY': (949, 2, 'New Turkish lira', 'Turkey, Northern Cyprus'),
    'TTD': (780, 2, 'Trinidad and Tobago dollar', 'Trinidad and Tobago'),
    'TWD': (901, 2, 'New Taiwan dollar', 'Taiwan and other islands that are under the effective control of the Republic of China (ROC)'),
    'TZS': (834, 2, 'Tanzanian shilling', 'Tanzania'),
    'UAH': (980, 2, 'Hryvnia', 'Ukraine'),
    'UGX': (800, 2, 'Uganda shilling', 'Uganda'),
    'USD': (840, 2, 'US dollar', 'American Samoa, British Indian Ocean Territory, Ecuador, El Salvador, Guam, Haiti, Marshall Islands, Micronesia, Northern Mariana Islands, Palau, Panama, Puerto Rico, Timor-Leste, Turks and Caicos Islands, United States, Virgin Islands, Bermuda(as well as Bermudian Dollar)'),
    'USN': (997, 2, 'United States dollar (next day) (funds code)', 'United States'),
    'USS': (998, 2, 'United States dollar (same day) (funds code) (one source claims it is no longer used, but it is still on the ISO 4217-MA list)', 'United States'),
    'UYU': (858, 2, 'Peso Uruguayo', 'Uruguay'),
    'UZS': (860, 2, 'Uzbekistan som', 'Uzbekistan'),
    'VEF': (937, 2, 'Venezuelan bolívar fuerte', 'Venezuela'),
    'VND': (704, 2, 'Vietnamese đng', 'Vietnam'),
    'VUV': (548, 0, 'Vatu', 'Vanuatu'),
    'WST': (882, 2, 'Samoan tala', 'Samoa'),
    'XAF': (950, 0, 'CFA franc BEAC', 'Cameroon, Central African Republic, Congo, Chad, Equatorial Guinea, Gabon'),
    'XAG': (961, '.', 'Silver (one troy ounce)'),
    'XAU': (959, '.', 'Gold (one troy ounce)'),
    'XBA': (955, '.', 'European Composite Unit (EURCO) (bond market unit)'),
    'XBB': (956, '.', 'European Monetary Unit (E.M.U.-6) (bond market unit)'),
    'XBC': (957, '.', 'European Unit of Account 9 (E.U.A.-9) (bond market unit)'),
    'XBD': (958, '.', 'European Unit of Account 17 (E.U.A.-17) (bond market unit)'),
    'XCD': (951, 2, 'East Caribbean dollar', 'Anguilla, Antigua and Barbuda, Dominica, Grenada, Montserrat, Saint Kitts and Nevis, Saint Lucia, Saint Vincent and the Grenadines'),
    'XDR': (960, '.', 'Special Drawing Rights', 'International Monetary Fund'),
    'XFU': (0, '.', 'UIC franc (special settlement currency)', 'International Union of Railways'),
    'XOF': (952, 0, 'CFA Franc BCEAO', 'Benin, Burkina Faso, Côte d\'Ivoire, Guinea-Bissau, Mali, Niger, Senegal, Togo'),
    'XPD': (964, '.', 'Palladium (one troy ounce)'),
    'XPF': (953, 0, 'CFP franc', 'French Polynesia, New Caledonia, Wallis and Futuna'),
    'XPT': (962, '.', 'Platinum (one troy ounce)'),
    'XTS': (963, '.', 'Code reserved for testing purposes'),
    'XXX': (999, '.', 'No currency'),
    'YER': (886, 2, 'Yemeni rial', 'Yemen'),
    'ZAR': (710, 2, 'South African rand', 'South Africa'),
    'ZMK': (894, 2, 'Kwacha', 'Zambia'),
    'ZWD': (716, 2, 'Zimbabwe dollar', 'Zimbabwe'),
    }
