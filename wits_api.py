# load required package
from xml.etree import ElementTree as ET 
import urllib.request as rq
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize as jnorm
import lxml.etree as et
import json, requests
# import pandasdmx as pdsx
# get data availability

def get_all_info(url):
    """

    :param url: url of xml
    :return: dataframe  of all info
    """

    xml_page = rq.urlopen(url)

    root = ET.fromstring(xml_page.read())

    result = []

    for child_l1 in root.getchildren():
        # level 1: indicators
        for child_l2 in child_l1:
            # level 2: indicator
            tmp = {}
            tmp = child_l2.attrib
            for child_l3 in child_l2.getchildren():
                # level 3 (last level)
                tmp[child_l3.tag.split('}')[1]] = child_l3.text
            result.append(tmp)

    data_frame_result = pd.DataFrame(result)

    return data_frame_result


if __name__ == '__main__':
    info = get_all_info('http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/indicator/ALL?format=JSON')

    print(info)

# For the country data availability http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/dataavailability/

# For product code: http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/product/all

# get available indicators

indi = rq.urlopen('http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/indicator/ALL?format=JSON')

test = et.parse(indi)
indi_list = et.tostring(test, pretty_print = True)

# define single countr-partner-year-indicator-prodcut parser
def trade_parser(json_url = "http://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/usa/year/all/partner/chn/product/Total/indicator/MPRT-TRD-VL?format=JSON"):
    response_totalimport = requests.get(json_url)
    json_totalimport = response_totalimport.json()
    
    df_obtained = pd.DataFrame({})
    # Loop for every partner country
    for par in range(len(json_totalimport['dataSets'][0]['series'])):
        # for each country:    
        # retrieve the values of indicator for all the years
        value_index = '0:0:' + str(par) + ':0:0'
        
        sv_obs = json_totalimport['dataSets'][0]['series'][value_index]['observations']

        # shape it into a pandas dataframe
        sl_obs = pd.DataFrame.from_dict(sv_obs,  orient = 'index') 
        obs_value = sl_obs[0]
        obs_value = obs_value.values
        sl_obs.rename(columns = {sl_obs.columns[0] : 'value'}, inplace = True)


        # retrieve all the available years
        sv_year = json_totalimport['structure']['dimensions']['observation'][0]['values']
        sl_year = pd.DataFrame.from_dict(sv_year, orient = 'columns')
        sl_year.rename(columns = {sl_year.columns[1] : 'year'}, inplace = True)

        # ------------------------------------------- #
        # report the params of this request for the specific country
        #freq =  annual
        sv_freq = json_totalimport['structure']['dimensions']['series'][0]['values'][0]['id']

        # Anchored the reporter, report its iso 3 code
        sv_reporter = json_totalimport['structure']['dimensions']['series'][1]['values'][0]['id']

        # Anchored the partner country, report its iso 3 code
        sv_partner = json_totalimport['structure']['dimensions']['series'][2]['values'][par]['id']

        # Anchored the product code, report its code which can be found in Trade: http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/product/all
        sv_prod = json_totalimport['structure']['dimensions']['series'][3]['values'][0]['id']

        # Anchored the indicator, which can be found in Trade: http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/indicator/ALL
        sv_indi = json_totalimport['structure']['dimensions']['series'][4]['values'][0]['id']

        # combine all the results
        # obtain a good shape dataframe as container
        df_combined = pd.DataFrame(pd.np.empty((sl_year.shape[0] , 7)), columns = {'year', 'value', 'freq', 'report', 'partner', 'prod', 'indi'})

        df_combined['year'] = sl_year['year']
        df_combined['report'] = sv_reporter
        df_combined['partner'] = sv_partner
        df_combined['prod'] = sv_prod
        df_combined['indi'] = sv_indi
        df_combined['freq'] = sv_freq

        # iterate to fill in the value
        for year in range(sl_year.shape[0]):
            if str(year) in sv_obs.keys():
                df_combined['value'][year] = sv_obs[str(year)][0]
            else:
                df_combined['value'][year] = 0

        # combine all the results to get one reporter - all partner - all yr
        df_obtained = df_obtained.append(df_combined, ignore_index = True)
    return(df_obtained)


def wits_trade(rpt = 'usa', ptn = 'chn', pcd = 'Total', idt = 'MPRT-TRD-VL', yr_def = 'all'): 
    #get the data
    # perform a country-partner-productcode-indicator with all years.
    # ideally to loop for country list and productcode.

    dashjoin = "/"
    preurl = "http://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade"
    rpurl = "reporter"
    yrurl = "year"
    pturl = "partner"
    pcurl = "product"
    idurl = "indicator"
    tail = "?format=JSON"

    # add this since there is no dash
    posturl = idt + tail

    full_url = dashjoin.join( (preurl, rpurl ,rpt , yrurl, yr_def, pturl , ptn, pcurl, pcd, idurl, posturl) )

    # response_totalimport = requests.get("http://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/usa/year/all/partner/all/product/Total/indicator/MPRT-TRD-VL?format=JSON")
    
    df_target = trade_parser(full_url)

    return(df_target)


# start the loop  for required data

# read the iso-3 list from disk
iso_all = pd.read_excel('D:/dropbox/Dropbox/LKY_RA/trilemma/WITS_API/iso_list.xlsx', header = 0)
iso3 = iso_all['iso3']
iso3.to_string

# or we may get the available country list from the server
# otherwise it is too slow
aval_country = get_all_info('http://wits.worldbank.org/API/V1/wits/datasource/tradestats-trade/dataavailability/')['iso3Code']

list_country = set(aval_country)
'USA' in list_country

# here we choose to match the available country we have in the FX-IR data, which amounts to 80. 

list_fx = pd.read_csv("d:/dropbox/Dropbox/InProgress/Data/Trilemma/fx_ir_source_data.csv")
country_fx = set(list_fx['Iso Country'])
country_fx.add('USA')

# list required product code
pcd_rqst = {'Total', 'UNCTAD-SoP1' , 'UNCTAD-SoP2', 'UNCTAD-SoP3', 'UNCTAD-SoP4'}

# define the indicator in request
idt_rqst = {'MPRT-TRD-VL','XPRT-TRD-VL' }

# set empty containers and counters
rn = 0
pn = 0
cn = 0
dn = 0
df_combined = pd.DataFrame({})

for rp_country in country_fx :
    rn = rn + 1
    for pt_country in country_fx:
        pn = pn + 1
        for pcdrq in pcd_rqst:
            cn = cn + 1
            for idtrq in idt_rqst:
                 dn = dn + 1
                 try: 
                     df_target = wits_trade(rp_country, pt_country , pcdrq, idtrq)
                 except Exception:
                     print(("something is wrong in " + rp_country + '-'+ pt_country + '-' + pcdrq  + '-' + idtrq))
                 else: 
                     df_combined = df_combined.append(df_target, ignore_index=True)
                     print("Successful: " + rp_country + '-'+ pt_country + '-' + pcdrq + '-' + idtrq)
                 finally:
                     print([rn, pn, cn, dn])
                 
                    

# write the data file to disk
df_combined.to_csv('D:/dropbox/Dropbox/LKY_RA/trilemma/WITS_API/test.csv')
            
