# Intro for the WITS api and Retrieved Data
## Import and Export Data
* Folder: /InProgress/Data/Trilemma/trade_wits/: 'combined_total.csv'

Record format: index-freq-indicator-inflow-outflow-total-value-year


Field   | Def
---     | --
Freq    | A = Annual
Partner | for import: outflow; for export: inflow
Report  | for import: inflow; for export: outflow 
year    | availabilty varies 
value   | Trade value in '000 USD
prod    | productcode, now it's only total*
indi    | indicator, MPRT-TRD-VL:import trade value;  XPRT-TRD-VL: export trade value.


* Pls refer to [UNCTAD-SoP](https://wits.worldbank.org/product-metadata.aspx?lang=en)

* Included Countries: ['ABW', 'AFG', 'AGO', 'AIA', 'ALB', 'AND', 'ANT', 'ARE', 'ARG', 'ARM', 'ASM', 'ATA', 'ATF', 'ATG', 'AUS', 'AUT', 'AZE', 'BAT', 'BDI', 'BEL', 'BEN', 'BES', 'BFA', 'BGD', 'BGR', 'BHR', 'BHS', 'BIH', 'BLM', 'BLR', 'BLX', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'BRN', 'BTN', 'BUN', 'BVT', 'BWA', 'CAF', 'CAN', 'CCK', 'CHE', 'CHL', 'CHN', 'CIV', 'CMR', 'COG', 'COK', 'COL', 'COM', 'CPV', 'CRI', 'CSK', 'CUB', 'CUW', 'CXR', 'CYM', 'CYP', 'CZE', 'DDR', 'DEU', 'DJI', 'DMA', 'DNK', 'DOM', 'DZA', 'EAS', 'ECS', 'ECU', 'EGY', 'ERI', 'ESH', 'ESP', 'EST', 'ETF', 'ETH', 'FIN', 'FJI', 'FLK', 'FRA', 'FRE', 'FRO', 'FSM', 'GAB', 'GBR', 'GEO', 'GHA', 'GIB', 'GIN', 'GLP', 'GMB', 'GNB', 'GNQ', 'GRC', 'GRD', 'GRL', 'GTM', 'GUF', 'GUM', 'GUY', 'HKG', 'HMD', 'HND', 'HRV', 'HTI', 'HUN', 'IDN', 'IND', 'IOT', 'IRL', 'IRN', 'IRQ', 'ISL', 'ISR', 'ITA', 'JAM', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'KHM', 'KIR', 'KNA', 'KOR', 'KWT', 'LAO', 'LBN', 'LBR', 'LBY', 'LCA', 'LCN', 'LKA', 'LSO', 'LTU', 'LUX', 'LVA', 'MAC', 'MAR', 'MCO', 'MDA', 'MDG', 'MDV', 'MEA', 'MEX', 'MHL', 'MKD', 'MLI', 'MLT', 'MMR', 'MNG', 'MNP', 'MNT', 'MOZ', 'MRT', 'MSR', 'MTQ', 'MUS', 'MWI', 'MYS', 'MYT', 'NAC', 'NAM', 'NCL', 'NER', 'NFK', 'NGA', 'NIC', 'NIU', 'NLD', 'NOR', 'NPL', 'NRU', 'NZE', 'NZL', 'OAS', 'OMN', 'PAK', 'PAN', 'PCE', 'PCN', 'PER', 'PHL', 'PLW', 'PNG', 'POL', 'PRK', 'PRT', 'PRY', 'PSE', 'PYF', 'QAT', 'REU', 'ROM', 'RUS', 'RWA', 'SAS', 'SAU', 'SDN', 'SEN', 'SER', 'SGP', 'SGS', 'SHN', 'SLB', 'SLE', 'SLV', 'SMR', 'SOM', 'SPE', 'SPM', 'SSD', 'SSF', 'STP', 'SUD', 'SUR', 'SVK', 'SVN', 'SVU', 'SWE', 'SWZ', 'SXM', 'SYC', 'SYR', 'TCA', 'TCD', 'TGO', 'THA', 'TJK', 'TKL', 'TKM', 'TMP', 'TON', 'TTO', 'TUN', 'TUR', 'TUV', 'TZA', 'UGA', 'UKR', 'UMI', 'UNS', 'URY', 'USA', 'USP', 'UZB', 'VAT', 'VCT', 'VEN', 'VGB', 'VNM', 'VUT', 'WLD', 'WLF', 'WSM', 'YDR', 'YEM', 'YUG', 'ZAF', 'ZAR', 'ZMB', 'ZWE']

