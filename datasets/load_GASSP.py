from .models import Dataset, MeasurementFile, MeasurementDataset, MeasurementVariable, \
    CCNMeasurementVariable, Campaign
from datetime import datetime
import itertools
from os.path import join
from os.path import expanduser

home = expanduser("~")
local_data = join(home, "Local data")

old_data_path = join(local_data, 'gassp_data', 'Level_2')
data_path = join(local_data, 'gassp_data', 'Level_2_1')


def new_platform(region, platform, label=None, **kwargs):
    # Flatten the various measurement campaigns
    measurements = [m for k, ml in kwargs.items() for m in ml if ml is not None]
    cp = Dataset(region=region, platform=platform, label=label)
    cp.save()
    cp.measurementdataset_set.add(*measurements)
    # cp.measurement_campaigns = measurements
    return cp


# Campaign constructor
def new_Campaign(name=None, region=None, platform=None, **kwargs):
    campaign = Campaign(label=name)
    campaign.save()
    cp = new_platform(region, platform, **kwargs)
    campaign.dataset_set.add(cp)
    return campaign


# Campaign constructor
def new_Campaign_with_multiple_platforms(platforms, name=None, **kwargs):
    campaign = Campaign(label=name)
    campaign.save()
    campaign.campaign_platforms = platforms
    return campaign


def CNMeasurementDataset(files, variables):
    # v = [MeasurementVariable(name=var) for var in variables.split(",")]
    c = MeasurementDataset(files=files, type='cn')
    # c.measurement_variables = v
    return c


def SO4MeasurementDataset(files, variables):
    v = [MeasurementVariable(name=var) for var in variables.split(",")]
    c = MeasurementDataset(files=files, type='so4')
    c.measurement_variables = v
    return c


def BCMeasurementDataset(files, variables, campaign_platform):
    v = [MeasurementVariable(name=var) for var in variables.split(",")]
    c = MeasurementDataset(files=files, type='bc')
    c.measurement_variables = v
    c.campaign_platform = campaign_platform
    return c


def NSDMeasurementDataset(files, variables, campaign_platform):
    v = [MeasurementVariable(name=var) for var in variables.split(",")]
    c = MeasurementDataset(files=files, type='nsd')
    c.measurement_variables = v
    c.campaign_platform = campaign_platform
    return c


def CCNMeasurementDataset(files, variables, fixed_ss=None, ss_variable=None):
    if ss_variable is not None:
        v = [CCNMeasurementVariable(name=var, fixed_ss=fixed_ss, ss_variable=ss_var) for var, ss_var in
             zip(variables.split(","), ss_variable.split(","))]
    else:
        v = [CCNMeasurementVariable(name=var, fixed_ss=fixed_ss) for var in variables.split(",")]
    c = MeasurementDataset(files=files, type='ccn')
    c.measurement_variables = v
    return c


def CCN_with_multiple_variables(files, variables):
    c = MeasurementDataset(files=files, type='ccn')
    c.measurement_variables = variables
    return c


# # Note that there is also a MMR in here
# # This is measured at Standard Atmosphere and Pressure. It also has volume and mass mixing ratios (at SAP)

ace1_cn = CNMeasurementDataset(files=join(data_path, "ACE1", "ACE1_CPC*.nc"), variables="N3")
ace1_cn_ship = CNMeasurementDataset(files=join(data_path, "ACE1", "ACE1_atm.nc"), variables="N3")
ace2_cn_ship = CNMeasurementDataset(files=join(data_path, "ACE2", "ACE2_atm.nc"), variables="N3")
aceasia_cn_air = CNMeasurementDataset(files=join(data_path, "ACEASIA", "ACEASIA_CPC*.nc"), variables="N3")
aceasia_cn_ship = CNMeasurementDataset(files=join(data_path, "ACEASIA", "ACEASIA_atmchem_v11.nc"), variables="N3")
aforce_cn = CNMeasurementDataset(files=join(data_path, "A-FORCE", "CPC_A-FORCE_*.nc"), variables="N10")

appraise_cn = CNMeasurementDataset(files=join(data_path, "APPRAISE", "faam-3786cpc*.nc"), variables="N3")

arctas_cn_pc3 = CNMeasurementDataset(files=join(data_path, "ARCTAS", "ARCTAS_CPC*.nc"), variables="N3")
arctas_cn_dc8 = CNMeasurementDataset(files=join(data_path, "ARCTAS", "NAerosol_CPC*.nc"), variables="N10")
arcpac_cn = CNMeasurementDataset(files=join(data_path, "ARCPAC2008", "NAerosol_*.nc"), variables="N4")
calnex_cn = CNMeasurementDataset(files=join(data_path, "CALNEX", "NAerosol*NP3*"), variables="N4")
calnex_cn_ship = CNMeasurementDataset(files=join(data_path, "CALNEX", "CNpmel*.nc"), variables="N5")
caribic_cn = CNMeasurementDataset(files=join(data_path, "CARIBIC", "CPC_CARIBIC2_*.nc"), variables="N4_12,N12")
dc3_cn_falcon = CNMeasurementDataset(files=join(data_path, "DC3", "NAerosol_CPC_mrg60-falcon*.nc"), variables="N5")
dc3_cn_dc8 = CNMeasurementDataset(files=join(data_path, "DC3", "NAerosol_CPC_mrg60-dc8*.nc"), variables="N3")
intexa_cn = CNMeasurementDataset(files=join(data_path, "INTEX-A", "INTEX-A_CPC*.nc"), variables="N3,N7,N10_NONVOL,N10_VOLATILE")
intexb_cn = CNMeasurementDataset(files=join(data_path, "INTEX-B", "NAerosol_CPC*.nc"), variables="N3")

goamazon_cn = CNMeasurementDataset(files=join(data_path, "GoAmazon", "CPC_AERMERGE_*.nc"), variables="N3,N10")
mirage_cn = CNMeasurementDataset(files=join(data_path, "MIRAGE", "MIRAGE_CPC*.nc"), variables="N3")
icealot_cn = CNMeasurementDataset(files=join(data_path, "ICEALOT", "CNpmel*.nc"), variables="N5")
indoex_cn = CNMeasurementDataset(files=join(data_path, "INDOEX", "INDOEX_CPC_*.nc"), variables="N3,N10")
pase_cn = CNMeasurementDataset(files=join(data_path, "PASE", "PASE_CPC*.nc"), variables="N3")

pem_tropics_a_cn = CNMeasurementDataset(files=join(data_path, "PEMTropicsA", "CN_mrg*.nc"), variables="N4,N15")
pem_tropics_a_cn_p3 = CNMeasurementDataset(files=join(data_path, "PEMTropicsA", "PEMTropicsA_CPC*.nc"), variables="N3,N10,N11")

pem_tropics_b_cn = CNMeasurementDataset(files=join(data_path, "PEMTropicsB", "CN_mrg*.nc"), variables="N8,N15")
pem_tropics_b_cn_p3 = CNMeasurementDataset(files=join(data_path, "PEMTropicsB", "PEMTropicsB_CPC*.nc"), variables="N3,N10")

pem_west_a_cn = CNMeasurementDataset(files=join(data_path, "PEMWestA", "AerDen*.nc"), variables="N120,N500")

# NOTE that these both look to be N3 rather than N20...
# pride_cn = CNMeasurementDataset(files=join(data_path, "PRIDE_PRD", "NSD*.nc"), variables="N20")
# care_beijing_cn = CNMeasurementDataset(files=join(data_path, "CAREBeijing", "NSD*.nc"), variables="N20")

ronoco_cn = CNMeasurementDataset(files=join(data_path, "RONOCO", "faam-3786cpc*.nc"), variables="N3")

trace_p_cn = CNMeasurementDataset(files=join(data_path, "TRACEP", "CN_mrg60-p3b_*.nc"), variables="N13")
trace_p_ucn = CNMeasurementDataset(files=join(data_path, "TRACEP", "UCN_*.nc"), variables="N3")
trace_p_cn_dc8 = CNMeasurementDataset(files=join(data_path, "TRACEP", "CN_mrg60-dc8_*.nc"), variables="N4")

texaqs_cn = CNMeasurementDataset(files=join(data_path, "TEXAQS2006", "NAerosol*NP3*"), variables="N4")
seac4rs_cn = CNMeasurementDataset(files=join(data_path, "SEAC4RS", "NAerosol_CPC*.nc"), variables="N3")
texaqs_cn_ship = CNMeasurementDataset(files=join(data_path, "TEXAQS2006", "CNpmel*.nc"), variables="N5")
trace_a_cn = CNMeasurementDataset(files=join(data_path, "TRACEA", "AerDen*.nc"), variables="N120,N500")
vocals_cn = CNMeasurementDataset(files=join(data_path, "VOCALS", "VOCALS_CPC*.nc"), variables="N3")
vocals_cn_faam = CNMeasurementDataset(files=join(data_path, "VOCALS", "faam-3786cpc*.nc"), variables="N3")
vocals_cn_ship = CNMeasurementDataset(files=join(data_path, "VOCALS", "CNpmel*.nc"), variables="N5")

cn_campaigns = [ace1_cn, appraise_cn, arctas_cn_pc3, arctas_cn_dc8, calnex_cn, calnex_cn_ship, dc3_cn_falcon,
                dc3_cn_dc8, intexa_cn, intexb_cn, mirage_cn, pem_tropics_a_cn, pem_tropics_a_cn_p3, pem_tropics_b_cn_p3, pem_tropics_b_cn,
                icealot_cn, pase_cn, texaqs_cn, texaqs_cn_ship, vocals_cn, pem_west_a_cn, ronoco_cn, trace_a_cn,
                trace_p_cn, trace_p_ucn, trace_p_cn_dc8]

ace1_ccn = [
    # We actually only have RF11-28 - which causes problems when comparing to CN...
    CCN_with_multiple_variables(files=join(data_path, "ACE1", "ACE1_CCN*.nc"),
                               variables=[CCNMeasurementVariable(name="CCN0_02", fixed_ss=0.02),
                                          CCNMeasurementVariable(name="CCN0_08", fixed_ss=0.08),
                                          CCNMeasurementVariable(name="CCN0_2", fixed_ss=0.2),
                                          CCNMeasurementVariable(name="CCN0_6", fixed_ss=0.6)])]

amaze_ccn = [CCNMeasurementDataset(files=join(data_path, "AMAZE-08", "CCN*.nc"), variables="TOTAL_CCN",
                                    ss_variable="S")]

appraise_ccn = [CCNMeasurementDataset(files=join(data_path, "APPRAISE", "faam-ccnrack*.nc"),
                                       variables="CCN_COLA,CCN_COLB", ss_variable="SS_COLA,SS_COLB")]

arcpac_ccn = [CCNMeasurementDataset(files=join(data_path, "ARCPAC2008", "CCN*.nc"),
                                     variables="NUMBER_CONCENTRATION", ss_variable="SUPERSATURATION")]

arctas_ccn_pc3 = [
    CCN_with_multiple_variables(files=join(data_path, "ARCTAS", "ARCTAS_CCN*.nc"),
                                variables=[CCNMeasurementVariable(name="CCN_LT0_08", fixed_ss=0.04),
                                           CCNMeasurementVariable(name="CCN0_08TO0_23", fixed_ss=0.155),
                                           CCNMeasurementVariable(name="CCN0_23TO0_43", fixed_ss=0.33),
                                           CCNMeasurementVariable(name="CCN0_43TO0_65", fixed_ss=0.54)])]

arctas_ccn_dc8 = [
    CCNMeasurementDataset(files=join(data_path, "ARCTAS", "CCN*.nc"),
                           variables="CCN_NUMBER_CONCENTRATION", ss_variable="SUPERSATURATION")]
# This isn't in all the files by the looks of it...
# arctas_ccn.append(Campaign(files=join(data_path,"ARCTAS","ARCTAS_CCN*.nc"), variables="CCN_GT0_65", fixed_ss=1.0, platform="aircraft", region="NA"))

calnex_ccn_air = [
    CCNMeasurementDataset(files=join(data_path, "CALNEX", "CCN_*.nc"), variables="CCN_CONCENTRATION",
                           ss_variable="SUPERSATURATION")]
calnex_ccn_ship = [
    CCNMeasurementDataset(files=join(data_path, "CALNEX", "CCNpmel*.nc"), variables="CCN_N",
                           ss_variable="CCNSS")]

care_beijing_ccn = [
    CCNMeasurementDataset(files=join(data_path, "CAREBeijing", "CCN*.nc"), variables="TOTAL_CCN",
                           ss_variable="S")]

carriba_ccn = [CCNMeasurementDataset(files=join(data_path, "CARRIBA", "CCN*.nc"), variables="CCN", fixed_ss=0.26)]

clace_ccn = [
    CCNMeasurementDataset(files=join(data_path, "CLACE6", "CCN*.nc"), variables="TOTAL_CCN", ss_variable="S")]

dc3_ccn_dc8 = [CCNMeasurementDataset(files=join(data_path, "DC3", "CCN*.nc"), variables="CCNCONC_AMB",
                                      ss_variable="CCNINST_SUPERSATURATION")]

em25_ccn = [
    CCNMeasurementDataset(files=join(data_path, "EM25", "faam-ccnrack*.nc"), variables="CCN_COLA,CCN_COLB",
                           ss_variable="SS_COLA,SS_COLB")]

eucaari_ccn = [CCNMeasurementDataset(files=join(data_path, "EUCAARI", "faam-ccnrack*.nc"),
                                      variables="CCN_COLA,CCN_COLB", ss_variable="SS_COLA,SS_COLB")]

goamazon_ccn = [CCNMeasurementDataset(files=join(data_path, "GoAmazon", "CCN*.nc"),
                                       variables="CCNA_CNC,CCNB_CNC", ss_variable="CCNA_SS,CCNB_SS")]

intexb_ccn = [
    CCNMeasurementDataset(files=join(data_path, "INTEX-B", "CCN*.nc"), variables="NCCN", ss_variable="SSC")]

indoex_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "INDOEX", "INDOEX_CCN*.nc"),
                                variables=[CCNMeasurementVariable(name="CCN0_02_MEASURED", fixed_ss=0.02),
                                           CCNMeasurementVariable(name="CCN0_08_MEASURED", fixed_ss=0.08),
                                           CCNMeasurementVariable(name="CCN0_2_MEASURED", fixed_ss=0.2),
                                           CCNMeasurementVariable(name="CCN0_6_MEASURED", fixed_ss=0.6)])]

mirage_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "MIRAGE", "MIRAGE_CCN*.nc"),
                                variables=[CCNMeasurementVariable(name="CCN0_08TO0_13", ss_variable="SSC_PERCENT"),
                                           CCNMeasurementVariable(name="CCN0_13TO0_18", ss_variable="SSC_PERCENT"),
                                           CCNMeasurementVariable(name="CCN0_18TO0_23", ss_variable="SSC_PERCENT")])]

icealot_ccn = [CCNMeasurementDataset(files=join(data_path, "ICEALOT", "CCNpmel*.nc"), variables="CCN_N",
                                      ss_variable="CCNSS")]

pase_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "PASE", "PASE_CCN*.nc"),
                                variables=[CCNMeasurementVariable(name="CCN0_2", fixed_ss=0.2),
                                           CCNMeasurementVariable(name="CCN0_04", fixed_ss=0.04)])]

polarstern_ccn = [
    CCNMeasurementDataset(files=join(data_path, "Polarstern", "CCN*.nc"), variables="CCN", ss_variable="D50")]

pride_ccn = [
    CCNMeasurementDataset(files=join(data_path, "PRIDE_PRD", "CCN*.nc"), variables="TOTAL_CCN",
                           ss_variable="S")]

ronoco_ccn = [CCNMeasurementDataset(files=join(data_path, "RONOCO", "faam-ccnrack*.nc"),
                                     variables="CCN_COLA,CCN_COLB", ss_variable="SS_COLA,SS_COLB")]

seac4rs_ccn = [
    CCNMeasurementDataset(files=join(data_path, "SEAC4RS", "CCN_*.nc"), variables="NUMCONC_AMB_CCN",
                           ss_variable="SUPERSATURATION_CCN")]

texaqs_ccn_air = [CCNMeasurementDataset(files=join(data_path, "TEXAQS2006", "CCN_*.nc"),
                                     variables="NUMBER_CONCENTRATION", ss_variable="SUPERSATURATION")]
texasqs_ccn_ship = [CCNMeasurementDataset(files=join(data_path, "TEXAQS2006", "CCNpmel*.nc"),
                                     variables="CCN_N", ss_variable="CCNSS")]

trompex_ccn = [CCNMeasurementDataset(files=join(data_path, "TROMPEX", "faam-ccnrack*.nc"),
                                      variables="CCN_COLA,CCN_COLB", ss_variable="SS_COLA,SS_COLB")]

vocals_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "VOCALS", "VOCALS_CCN*.nc"),
                                variables=[CCNMeasurementVariable(name="CCNLT0_3", fixed_ss=0.15),
                                           CCNMeasurementVariable(name="CCNGT0_8", fixed_ss=1.0)])]

vocals_faam_ccn = [
    CCNMeasurementDataset(files=join(data_path, "VOCALS", "faam-ccnrack*.nc"), variables="CCN_COLA,CCN_COLB",
                           ss_variable="SS_COLA,SS_COLB")]

ccn_campaigns = list(
    itertools.chain(ace1_ccn, amaze_ccn, appraise_ccn, arcpac_ccn, arctas_ccn_dc8, arctas_ccn_pc3, calnex_ccn_air,
                    care_beijing_ccn, carriba_ccn, ronoco_ccn,
                    clace_ccn, dc3_ccn_dc8, em25_ccn, eucaari_ccn, goamazon_ccn, intexb_ccn, mirage_ccn, icealot_ccn,
                    pase_ccn, polarstern_ccn, pride_ccn, seac4rs_ccn, texaqs_ccn_air, trompex_ccn, vocals_ccn, vocals_faam_ccn))


# All the SO4 data for which we also have CCN data
ace1_so4_ship = SO4MeasurementDataset(files=join(data_path, "ACE1", "ACE1_aero_an.nc"), variables="SO4_PM1")
ace2_so4_ship = SO4MeasurementDataset(files=join(data_path, "ACE2", "ACE2_aero_an.nc"), variables="SO4_PM1")

aceasia_so4_air = SO4MeasurementDataset(files=join(data_path, "ACEASIA", "ACEASIA_PILS_*.nc"), variables="SO4")
aceasia_so4_ship = SO4MeasurementDataset(files=join(data_path, "ACEASIA", "ACEASIA_aero_an.nc"), variables="SO4_PM1")

accacia_so4 = SO4MeasurementDataset(files=join(data_path, "ACCACIA", "AMS_ACCACIA*FAAM*.nc"), variables="SO4")
accacia_so4_ship = SO4MeasurementDataset(files=join(data_path, "ACCACIA", "AMS_ACCACIA*Ship*.nc"), variables="SO4")
aegean_game_so4 = SO4MeasurementDataset(files=join(data_path, "AEGEAN-GAME", "AMS_AG*.nc"), variables="SO4")
amma_so4 = SO4MeasurementDataset(files=join(data_path, "AMMA", "AMS_AMMA*.nc"), variables="SO4")
arcpac_so4 = SO4MeasurementDataset(files=join(data_path, "ARCPAC2008", "AMS_*.nc"), variables="SO4")

arctas_so4_dc8 = SO4MeasurementDataset(files=join(data_path, "ARCTAS", "AMS*.nc"), variables="SO4")
arctas_so4_pc3 = SO4MeasurementDataset(files=join(data_path, "ARCTAS", "ARCTAS_AMS*.nc"), variables="SO4")
bortas_so4 = SO4MeasurementDataset(files=join(data_path, "BORTAS", "AMS_BORTAS_*.nc"), variables="SO4")
calnex_so4 = SO4MeasurementDataset(files=join(data_path, "CALNEX", "AMS_*.nc"), variables="SO4")
calnex_so4_ship = SO4MeasurementDataset(files=join(data_path, "CALNEX", "AMSpmel*.nc"), variables="SO4")
cope_so4 = SO4MeasurementDataset(files=join(data_path, "COPE", "AMS_COPE_*.nc"), variables="SO4")
dc3_so4 = SO4MeasurementDataset(files=join(data_path, "DC3", "AMS*.nc"), variables="SO4")
discoveraq_so4 = SO4MeasurementDataset(files=join(data_path, "DISCOVERAQ", "PILS_*.nc"), variables="SO4")
eucaari_so4 = SO4MeasurementDataset(files=join(data_path, "EUCAARI", "AMS_EUCAARI_*.nc"), variables="SO4")
intexa_so4 = SO4MeasurementDataset(files=join(data_path, "INTEX-A", "INTEX-A_PILS*.nc"), variables="SO4")
intexb_so4 = SO4MeasurementDataset(files=join(data_path, "INTEX-B", "AMS*.nc"), variables="SO4")
icealot_so4 = SO4MeasurementDataset(files=join(data_path, "ICEALOT", "AMSpmel*.nc"), variables="SO4")
mirage_so4 = SO4MeasurementDataset(files=join(data_path, "MIRAGE", "MIRAGE_AMS*.nc"), variables="SO4")
op3_so4 = SO4MeasurementDataset(files=join(data_path, "OP3", "AMS_OP3*.nc"), variables="SO4")
pase_ams = SO4MeasurementDataset(files=join(data_path, "PASE", "PASE_AMS*.nc"), variables="SO4")
pem_tropics_a_so4 = SO4MeasurementDataset(files=join(data_path, "PEMTropicsA", "SolIons_mrg*.nc"), variables="SO4")
pem_west_a_so4 = SO4MeasurementDataset(files=join(data_path, "PEMWestA", "AerComp*.nc"), variables="SO4")
pem_west_b_so4 = SO4MeasurementDataset(files=join(data_path, "PEMWestB", "AerComp*.nc"), variables="SO4")
ronoco_so4 = SO4MeasurementDataset(files=join(data_path, "RONOCO", "AMS_RONOCO*.nc"), variables="SO4")
seac4rs_so4 = SO4MeasurementDataset(files=join(data_path, "SEAC4RS", "AMS_*.nc"), variables="SO4")
texaqs_so4 = SO4MeasurementDataset(files=join(data_path, "TEXAQS2006", "AMS_*.nc"), variables="SO4")
texaqs_so4_ship = SO4MeasurementDataset(files=join(data_path, "TEXAQS2006", "AMSpmel*.nc"), variables="SO4")
vocals_so4_faam = SO4MeasurementDataset(files=join(data_path, "VOCALS", "AMS_VOCALS*.nc"), variables="SO4")
vocals_so4_c130 = SO4MeasurementDataset(files=join(data_path, "VOCALS", "VOCALS_AMS*.nc"), variables="SO4")
vocals_so4_ship = SO4MeasurementDataset(files=join(data_path, "VOCALS", "AMSpmel*.nc"), variables="SO4")

so4_campaigns = [accacia_so4, accacia_so4_ship, arctas_so4_dc8, arctas_so4_pc3, aegean_game_so4, amma_so4, bortas_so4, calnex_so4, calnex_so4_ship, dc3_so4, intexb_so4, icealot_so4, texaqs_so4, texaqs_so4_ship,
                 vocals_so4_faam, vocals_so4_c130, vocals_so4_ship, intexa_so4, mirage_so4, pem_tropics_a_so4, pem_west_a_so4, pem_west_b_so4]


ace1_ship = new_platform(region="NA", platform="ship", CN=[ace1_cn_ship], SO4=[ace1_so4_ship])
ace1_air = new_platform(region="NA", platform="aircraft", CN=[ace1_cn], CCN=ace1_ccn)
ace1 = new_Campaign_with_multiple_platforms([ace1_air, ace1_ship], "ACE1")

ace2 = new_Campaign("ACE2", platform="ship", region="EU", CN=[ace2_cn_ship], SO4=[ace2_so4_ship])
accacia_ship = new_platform(label="ACCACIA_ship", platform="ship", region="Arctic", SO4=[accacia_so4_ship])
accacia_aircraft = new_platform(label="ACCACIA_air", platform="aircraft", region="Arctic", SO4=[accacia_so4])
accacia = new_Campaign_with_multiple_platforms([accacia_ship, accacia_aircraft], "ACCACIA")

aceasia_ship = new_platform(region="EA", platform="ship", CN=[aceasia_cn_ship], SO4=[aceasia_so4_ship])
aceasia_air = new_platform(region="EA", platform="aircraft", CN=[aceasia_cn_air], SO4=[aceasia_so4_air])
aceasia = new_Campaign_with_multiple_platforms([aceasia_air, aceasia_ship], "ACEASIA")

aegean_game = new_Campaign("AEGEAN-GAME", platform="aircraft", region="EU", SO4=[aegean_game_so4])
aforce = new_Campaign("A-FORCE", platform="aircraft", CN=[aforce_cn])
amaze = new_Campaign("AMAZE-08", CCN=amaze_ccn, platform="station", region="SA")
amma = new_Campaign("AMMA", platform="aircraft", region="AF", SO4=[amma_so4])
amf_cape_cod = new_platform(region="NA", platform="station",label="CapeCod")
amf_manacapuru = new_platform(region="SA", platform="station", label="Manacapuru")
amf_stations = new_Campaign_with_multiple_platforms([amf_cape_cod, amf_manacapuru], "AMF_stations")

aoe_1996 = new_Campaign("AOE1996", platform="ship", region="Arctic")
aoe_2001 = new_Campaign("AOE2001", platform="ship", region="Arctic")
appraise = new_Campaign("APPRAISE", CN=[appraise_cn], CCN=appraise_ccn)

arcpac = new_Campaign("ARCPAC2008", CCN=arcpac_ccn, SO4=[arcpac_so4], CN=[arcpac_cn])

arctas_pc3 = new_platform(platform="aircraft", region="NA", label="PC3", CN=[arctas_cn_pc3], CCN=arctas_ccn_pc3, SO4=[arctas_so4_pc3])
arctas_dc8 = new_platform(platform="aircraft", region="NA", label="DC8", CN=[arctas_cn_dc8], CCN=arctas_ccn_dc8, SO4=[arctas_so4_dc8])
arctas = new_Campaign_with_multiple_platforms([arctas_pc3, arctas_dc8], "ARCTAS")

bird_island = new_Campaign("BirdIsland", platform="station")
bortas = new_Campaign("BORTAS", platform="aircraft", SO4=[bortas_so4])

calnex_air = new_platform(region="NA", platform="aircraft", CN=[calnex_cn], CCN=calnex_ccn_air, SO4=[calnex_so4], label="CALNEX_air")
calnex_ship = new_platform(region="NA", platform="ship", CN=[calnex_cn_ship], CCN=calnex_ccn_ship, SO4=[calnex_so4_ship], label="CALNEX_ship")
calnex = new_Campaign_with_multiple_platforms([calnex_air, calnex_ship], "CALNEX")

# care_beijing = new_Campaign("CAREBeijing", platform="station", region="EA", CN=[care_beijing_cn], CCN=care_beijing_ccn)
care_beijing = new_Campaign("CAREBeijing", platform="station", region="EA", CCN=care_beijing_ccn)
caribic = new_Campaign("CARIBIC", platform="aircraft", region="AT", CN=[caribic_cn])
carriba = new_Campaign("CARRIBA", platform="station", CCN=carriba_ccn)
cast = new_Campaign("CAST", platform="aircraft")
clace = new_Campaign("CLACE6", CCN=clace_ccn, platform='station', region='EU')
cope = new_Campaign("COPE", platform="aircraft", SO4=[cope_so4])
cops = new_Campaign("COPS", platform="station")

dc3_dc8 = new_platform(label="DC8", platform="aircraft", region="NA", CN=[dc3_cn_dc8], CCN=dc3_ccn_dc8, SO4=[dc3_so4])
dc3_falcon = new_platform(label="Falcon", platform="aircraft", region="NA", CN=[dc3_cn_falcon])
dc3 = new_Campaign_with_multiple_platforms([dc3_dc8, dc3_falcon], "DC3")

discoveraq = new_Campaign("DISCOVERAQ", platform="aircraft", SO4=[discoveraq_so4])
em25 = new_Campaign("EM25", CCN=em25_ccn, platform="aircraft")
environment_canada = new_Campaign("Environment_Canada", platform="station", region="NA")
eucaari = new_Campaign("EUCAARI", CCN=eucaari_ccn, platform="aircraft", region="EU", SO4=[eucaari_so4])
goamazon = new_Campaign("GoAmazon", CN=[goamazon_cn], CCN=goamazon_ccn, platform="station", region="SA")
hippo = new_Campaign("HIPPO", platform="aircraft")
holme_moss = new_Campaign("HolmeMoss", platform="station")
icealot = new_Campaign("ICEALOT", CN=[icealot_cn], CCN=icealot_ccn, SO4=[icealot_so4], platform="ship", region="NA")
indoex = new_Campaign("INDOEX", platform="aircraft", region="NA", CN=[indoex_cn], CCN=indoex_ccn)
intexa = new_Campaign("INTEX-A", CN=[intexa_cn], SO4=[intexa_so4], platform="aircraft", region="NA")
intexb = new_Campaign("INTEX-B", CN=[intexb_cn], CCN=intexb_ccn, SO4=[intexb_so4], platform="aircraft", region="NA")
mamm = new_Campaign("MAMM", platform="aircraft")
mirage = new_Campaign("MIRAGE", CN=[mirage_cn], CCN=mirage_ccn, SO4=[mirage_so4], platform="aircraft", region="NA")
neaqs = new_Campaign("NEAQS2002", platform="ship")
op3 = new_Campaign("OP3", platform="station", SO4=[op3_so4])
pase = new_Campaign("PASE", CN=[pase_cn], CCN=pase_ccn, SO4=[pase_ams], platform="aircraft", region="NA")

pem_tropics_a_dc8 = new_platform(label="DC8", platform="aircraft", region="NA", SO4=[pem_tropics_a_so4], CN=[pem_tropics_a_cn])
pem_tropics_a_p3b = new_platform(label="P3B", platform="aircraft", region="NA", CN=[pem_tropics_a_cn_p3])
pem_tropics_a = new_Campaign_with_multiple_platforms([pem_tropics_a_dc8, pem_tropics_a_p3b], "PEMTropicsA")

pem_tropics_b_dc8 = new_platform(label="DC8", platform="aircraft", region="NA", CN=[pem_tropics_b_cn])
pem_tropics_b_p3b = new_platform(label="P3B", platform="aircraft", region="NA", CN=[pem_tropics_b_cn_p3])
pem_tropics_b = new_Campaign_with_multiple_platforms([pem_tropics_b_dc8, pem_tropics_b_p3b], "PEMTropicsB")

pem_west_a = new_Campaign("PEMWestA", CN=[pem_west_a_cn], SO4=[pem_west_a_so4], platform='aircraft', region="NP")
pem_west_b = new_Campaign("PEMWestB", SO4=[pem_west_b_so4], platform='aircraft', region="NP")


polarstern = new_Campaign("Polarstern", CCN=polarstern_ccn, platform="ship")
# pride = new_Campaign("PRIDE", CN=[pride_cn], CCN=pride_ccn, platform="station", region="EA")
pride = new_Campaign("PRIDE_PRD", CCN=pride_ccn, platform="station", region="EA")
rhamble = new_Campaign("RHaMBLe", platform="ship")
ronoco = new_Campaign("RONOCO", CN=[ronoco_cn], CCN=ronoco_ccn, SO4=[ronoco_so4], platform="aircraft", region="NA")

seac4rs = new_Campaign("SEAC4RS", CN=[seac4rs_cn], CCN=seac4rs_ccn, SO4=[seac4rs_so4], platform="aircraft", region="NA")

texaqs_ship = new_platform(region="NA", platform="ship", CN=[texaqs_cn_ship], CCN=texasqs_ccn_ship, SO4=[texaqs_so4_ship], label='TEXASQS_ship')
texaqs_air = new_platform(region="NA", platform="aircraft", CN=[texaqs_cn], CCN=texaqs_ccn_air, SO4=[texaqs_so4], label='TEXASQS_air')
texaqs = new_Campaign_with_multiple_platforms([texaqs_air, texaqs_ship], "TEXAQS2006")

trace_a = new_Campaign("TRACEA", CN=[trace_a_cn], platform="aircraft")
trace_p_dc8 = new_platform(region="EA", platform="aircraft", CN=[trace_p_cn_dc8], label='DC8')
trace_p_p3b = new_platform(region="EA", platform="aircraft", CN=[trace_p_cn, trace_p_ucn], label='P3B')
trace_p = new_Campaign_with_multiple_platforms([trace_p_dc8, trace_p_p3b], "TRACEP")

trompex = new_Campaign("TROMPEX", CCN=trompex_ccn, platform="aircraft")

vocals_c130 = new_platform(label="C-130", CN=[vocals_cn], CCN=vocals_ccn, SO4=[vocals_so4_c130], platform="aircraft", region="SA")
vocals_faam = new_platform(label="FAAM", CN=[vocals_cn_faam], CCN=vocals_faam_ccn, SO4=[vocals_so4_faam], platform="aircraft", region="SA")
vocals_ship = new_platform(label="ship", CN=[vocals_cn_ship], SO4=[vocals_so4_ship], platform="ship", region="SA")
vocals = new_Campaign_with_multiple_platforms([vocals_faam, vocals_c130, vocals_ship], "VOCALS")

weybourne = new_Campaign("Weybourne", platform="station")

campaigns = [ace1,
             ace2,
             accacia,
             aceasia,
             aegean_game,
             aforce,
             amaze,
             amma,
             amf_stations,
             aoe_1996,
             aoe_2001,
             appraise,
             arcpac,
             arctas_pc3,
             arctas_dc8,
             bird_island,
             bortas,
             calnex,
             care_beijing,
             carriba,
             caribic,
             cast,
             clace,
             cope,
             cops,
             dc3_dc8,
             dc3_falcon,
             discoveraq,
             em25,
             environment_canada,
             eucaari,
             goamazon,
             hippo,
             holme_moss,
             icealot,
             indoex,
             intexa,
             intexb,
             mamm,
             mirage,
             neaqs,
             op3,
             pase,
             pem_tropics_a,
             pem_tropics_b,
             pem_west_a,
             polarstern,
             pride,
             rhamble,
             ronoco,
             seac4rs,
             texaqs,
             trace_a,
             trace_p,
             trompex,
             vocals,
             weybourne,
             ]

# All NSD files and variables
nsd_campaigns = [
    NSDMeasurementDataset(campaign_platform=accacia.campaign_platforms[0], files=join(data_path, "ACCACIA", "DMPS*Ship*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=ace1_air, files=join(data_path, "ACE1", "*_NSD_*.nc"), variables="NUMDIST_DMA_OPC"),
    NSDMeasurementDataset(campaign_platform=aceasia_air, files=join(data_path, "ACEASIA", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=aegean_game.campaign_platforms[0], files=join(data_path, "AEGEAN-GAME", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amaze.campaign_platforms[0], files=join(data_path, "AMAZE-08", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amf_cape_cod, files=join(data_path, "AMF_stations", "CapeCod", "SMPS.*.nc"),
                        variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amf_manacapuru, files=join(data_path, "AMF_stations", "Manacapuru", "SMPS.*.nc"),
                        variables="NSD"),
    NSDMeasurementDataset(campaign_platform=aoe_1996.campaign_platforms[0], files=join(data_path, "AOE1996", "DMPS_AOE1996*.nc"), variables="NSD_DMPS"),
    NSDMeasurementDataset(campaign_platform=aoe_2001.campaign_platforms[0], files=join(data_path, "AOE2001", "DMPS_AOE2001*.nc"), variables="NSD_DMPS"),
    # TODO: There should be SMPS data from the DC8 too - but it's not in the folder, only the integrated data
    NSDMeasurementDataset(campaign_platform=arctas_pc3, files=join(data_path, "ARCTAS", "ARCTAS_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=bird_island.campaign_platforms[0], files=join(data_path, "BirdIsland",
                                                         "BirdIsland_2010_Schmale_submicronaerosolsizedistribution.txt.nc"),
                        variables="NSD_SMPS"),
    NSDMeasurementDataset(campaign_platform=bortas.campaign_platforms[0], files=join(data_path, "BORTAS", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=care_beijing.campaign_platforms[0], files=join(data_path, "CAREBeijing", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=clace.campaign_platforms[0], files=join(data_path, "CLACE6", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=cope.campaign_platforms[0], files=join(data_path, "COPE", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=cops.campaign_platforms[0], files=join(data_path, "COPS", "DMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=environment_canada.campaign_platforms[0], files=join(data_path, "Environment_Canada", "*SMPS*.nc"),
                        variables="SIZE_DISTRIBUTION"),
    NSDMeasurementDataset(campaign_platform=indoex.campaign_platforms[0], files=join(data_path, "INDOEX", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=intexa.campaign_platforms[0], files=join(data_path, "INTEX-A", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=mirage.campaign_platforms[0], files=join(data_path, "MIRAGE", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=op3.campaign_platforms[0], files=join(data_path, "OP3", "DMPS*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pase.campaign_platforms[0], files=join(data_path, "PASE", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pem_tropics_a_p3b, files=join(data_path, "PEMTropicsA", "*_NSD_*.nc"), variables="NSD"),
    # TODO: These files haven't been turned into a nice NSD yet, I suppose I could if I had the time or inclination...
    # NSDMeasurementDataset(campaign_platform=pem_tropics_b_dc8, files=join(data_path, "PEMTropicsB", "NSD_*.nc"), variables=???),
    # NSDMeasurementDataset(campaign_platform=pem_west_b.campaign_platforms[0], files=join(data_path, "PEMWestB", "AerComp_*.nc"), variables=???)
    NSDMeasurementDataset(campaign_platform=pem_tropics_b_p3b, files=join(data_path, "PEMTropicsB", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pride.campaign_platforms[0], files=join(data_path, "PRIDE_PRD", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=rhamble.campaign_platforms[0], files=join(data_path, "RHaMBLe", "DMPS*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=vocals_c130, files=join(data_path, "VOCALS", "*_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=vocals_faam, files=join(data_path, "VOCALS", "SMPS_VOCALS_*.nc"), variables="NSD")]

# PEMWestB - needs turning into a nice NSD

# All BC files and variables
bc_campaigns = [
    BCMeasurementDataset(campaign_platform=accacia_ship, files=join(data_path, "ACCACIA", "SP2*Ship*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=accacia_aircraft, files=join(data_path, "ACCACIA", "SP2*FAAM*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=aforce.campaign_platforms[0], files=join(data_path, "A-FORCE", "SP2*.nc"), variables="BCMCSTP"),
    BCMeasurementDataset(campaign_platform=arctas_dc8, files=join(data_path, "ARCTAS", "SP2*.nc"), variables="BC_MASS_1013HPA_273K"),
    BCMeasurementDataset(campaign_platform=arctas_pc3, files=join(data_path, "ARCTAS", "ARCTAS_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=arcpac.campaign_platforms[0], files=join(data_path, "ARCPAC2008", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=bortas.campaign_platforms[0], files=join(data_path, "BORTAS", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=calnex.campaign_platforms[0], files=join(data_path, "CALNEX", "SP2_mrg*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=cope.campaign_platforms[0], files=join(data_path, "COPE", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=cast.campaign_platforms[0], files=join(data_path, "CAST", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=clace.campaign_platforms[0], files=join(data_path, "CLACE6", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=dc3_falcon, files=join(data_path, "DC3", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=discoveraq.campaign_platforms[0], files=join(data_path, "DISCOVERAQ", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=eucaari.campaign_platforms[0], files=join(data_path, "EUCAARI", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=hippo.campaign_platforms[0], files=join(data_path, "HIPPO", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=holme_moss.campaign_platforms[0], files=join(data_path, "HolmeMoss", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=intexb.campaign_platforms[0], files=join(data_path, "INTEX-B", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=mamm.campaign_platforms[0], files=join(data_path, "MAMM", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=mirage.campaign_platforms[0], files=join(data_path, "MIRAGE", "MIRAGE_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=neaqs.campaign_platforms[0], files=join(data_path, "NEAQS2002", "NEAQS2002_carbon.nc"), variables="EC"),
    BCMeasurementDataset(campaign_platform=seac4rs.campaign_platforms[0], files=join(data_path, "SEAC4RS", "HDSP2_*.nc"), variables="BC"),
    BCMeasurementDataset(campaign_platform=texaqs.campaign_platforms[0], files=join(data_path, "TEXAQS2006", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=trace_p_dc8, files=join(data_path, "TRACEP", "BC_*.nc"), variables="BC"),
    BCMeasurementDataset(campaign_platform=vocals_c130, files=join(data_path, "VOCALS", "VOCALS_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=weybourne.campaign_platforms[0], files=join(data_path, "Weybourne", "SP2*.nc"), variables="BC_MASS")]


# Methods for actually reading the data
def load_gassp_data():
    from cis import read_data
    from .utils import cis_object_to_shp
    for md in MeasurementDataset.objects.all():
        d = read_data(md.files, str(md.measurementvariable_set.first()))
        shp = cis_object_to_shp(d)
        dt = d.coord('time')
        dt.convert_standard_time_to_datetime()
        t_start = dt.points.min()
        t_end = dt.points.max()
        md.measurementfile_set.add(wkt=shp.wkt)
