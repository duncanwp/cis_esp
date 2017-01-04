from .models import Dataset, MeasurementFile, Measurement, MeasurementVariable, \
    CCNMeasurementVariable, Campaign
import itertools
from os.path import join
from os.path import expanduser

home = expanduser("~")
local_data = join(home, "Local data")

old_data_path = join(local_data, 'gassp_data', 'Level_2')
data_path = join(local_data, 'gassp_data', 'Level_2_1')


def new_platform(region, platform, campaign=None, name=None, **kwargs):
    # Flatten the various measurement campaigns
    measurements = [m for k, ml in kwargs.items() for m in ml if ml is not None]
    cp, _ = Dataset.objects.get_or_create(region=region, platform_type=platform, name=name, campaign=campaign,
                                          is_gridded=False)
    cp.measurement_set.add(*measurements)
    # cp.measurement_campaigns = measurements
    return cp


# Campaign constructor
def new_Campaign(name, region=None, platform=None, **kwargs):
    campaign, _ = Campaign.objects.get_or_create(name=name)
    cp = new_platform(region, platform, campaign=campaign, **kwargs)
    campaign.dataset_set.add(cp)
    return campaign


def add_variables_and_create_if_needed(measurement_type, inst_vars):
    for v in inst_vars:
        if v in MeasurementVariable.objects.all():
            measurement_type.measurementvariable_set.add(v)
        else:
            measurement_type.measurementvariable_set.add(v, bulk=False)


def CNMeasurementDataset(files, variables):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.CN)
    v = [MeasurementVariable(variable_name=var, measurement_type=mt) for var in variables.split(",")]
    add_variables_and_create_if_needed(mt, v)
    return mt


def SO4MeasurementDataset(files, variables):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.SO4)
    v = [MeasurementVariable(variable_name=var) for var in variables.split(",")]
    add_variables_and_create_if_needed(mt, v)
    return mt


def BCMeasurementDataset(files, variables, campaign_platform):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.BC,
                                              dataset=campaign_platform)
    v = [MeasurementVariable(variable_name=var) for var in variables.split(",")]
    add_variables_and_create_if_needed(mt, v)
    return mt


def NSDMeasurementDataset(files, variables, campaign_platform):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.NSD,
                                              dataset=campaign_platform)
    v = [MeasurementVariable(variable_name=var) for var in variables.split(",")]
    add_variables_and_create_if_needed(mt, v)
    return mt


def CCNMeasurementDataset(files, variables, fixed_ss=None, ss_variable=None):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.CCN)
    if ss_variable is not None:
        v = [CCNMeasurementVariable(variable_name=var, fixed_ss=fixed_ss, ss_variable=ss_var) for var, ss_var in
             zip(variables.split(","), ss_variable.split(","))]
    else:
        v = [CCNMeasurementVariable(variable_name=var, fixed_ss=fixed_ss) for var in variables.split(",")]
    add_variables_and_create_if_needed(mt, v)
    return mt


def CCN_with_multiple_variables(files, variables):
    mt, _ = Measurement.objects.get_or_create(files=files, measurement_type=Measurement.CCN)
    add_variables_and_create_if_needed(mt, variables)
    return mt


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
                               variables=[CCNMeasurementVariable(variable_name="CCN0_02", fixed_ss=0.02),
                                          CCNMeasurementVariable(variable_name="CCN0_08", fixed_ss=0.08),
                                          CCNMeasurementVariable(variable_name="CCN0_2", fixed_ss=0.2),
                                          CCNMeasurementVariable(variable_name="CCN0_6", fixed_ss=0.6)])]

amaze_ccn = [CCNMeasurementDataset(files=join(data_path, "AMAZE-08", "CCN*.nc"), variables="TOTAL_CCN",
                                    ss_variable="S")]

appraise_ccn = [CCNMeasurementDataset(files=join(data_path, "APPRAISE", "faam-ccnrack*.nc"),
                                       variables="CCN_COLA,CCN_COLB", ss_variable="SS_COLA,SS_COLB")]

arcpac_ccn = [CCNMeasurementDataset(files=join(data_path, "ARCPAC2008", "CCN*.nc"),
                                     variables="NUMBER_CONCENTRATION", ss_variable="SUPERSATURATION")]

arctas_ccn_pc3 = [
    CCN_with_multiple_variables(files=join(data_path, "ARCTAS", "ARCTAS_CCN*.nc"),
                                variables=[CCNMeasurementVariable(variable_name="CCN_LT0_08", fixed_ss=0.04),
                                           CCNMeasurementVariable(variable_name="CCN0_08TO0_23", fixed_ss=0.155),
                                           CCNMeasurementVariable(variable_name="CCN0_23TO0_43", fixed_ss=0.33),
                                           CCNMeasurementVariable(variable_name="CCN0_43TO0_65", fixed_ss=0.54)])]

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
                                variables=[CCNMeasurementVariable(variable_name="CCN0_02_MEASURED", fixed_ss=0.02),
                                           CCNMeasurementVariable(variable_name="CCN0_08_MEASURED", fixed_ss=0.08),
                                           CCNMeasurementVariable(variable_name="CCN0_2_MEASURED", fixed_ss=0.2),
                                           CCNMeasurementVariable(variable_name="CCN0_6_MEASURED", fixed_ss=0.6)])]

mirage_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "MIRAGE", "MIRAGE_CCN*.nc"),
                                variables=[CCNMeasurementVariable(variable_name="CCN0_08TO0_13", ss_variable="SSC_PERCENT"),
                                           CCNMeasurementVariable(variable_name="CCN0_13TO0_18", ss_variable="SSC_PERCENT"),
                                           CCNMeasurementVariable(variable_name="CCN0_18TO0_23", ss_variable="SSC_PERCENT")])]

icealot_ccn = [CCNMeasurementDataset(files=join(data_path, "ICEALOT", "CCNpmel*.nc"), variables="CCN_N",
                                      ss_variable="CCNSS")]

pase_ccn = [
    CCN_with_multiple_variables(files=join(data_path, "PASE", "PASE_CCN*.nc"),
                                variables=[CCNMeasurementVariable(variable_name="CCN0_2", fixed_ss=0.2),
                                           CCNMeasurementVariable(variable_name="CCN0_04", fixed_ss=0.04)])]

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
                                variables=[CCNMeasurementVariable(variable_name="CCNLT0_3", fixed_ss=0.15),
                                           CCNMeasurementVariable(variable_name="CCNGT0_8", fixed_ss=1.0)])]

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


ace1, _ = Campaign.objects.get_or_create(name="ACE1")
ace1_ship = new_platform(region="NA", platform=Dataset.SHIP, CN=[ace1_cn_ship], SO4=[ace1_so4_ship], name="ACE1 Ship",
                         campaign=ace1)
ace1_air = new_platform(region="NA", platform=Dataset.AIRCRAFT, CN=[ace1_cn], CCN=ace1_ccn, name="ACE1 C-130",
                        campaign=ace1)

ace2 = new_Campaign("ACE2", platform=Dataset.SHIP, region="EU", CN=[ace2_cn_ship], SO4=[ace2_so4_ship])

accacia, _ = Campaign.objects.get_or_create(name="ACCACIA")
accacia_ship = new_platform(name="ACCACIA_ship", platform=Dataset.SHIP, region="Arctic", SO4=[accacia_so4_ship],
                            campaign=accacia)
accacia_aircraft = new_platform(name="ACCACIA_air", platform=Dataset.AIRCRAFT, region="Arctic", SO4=[accacia_so4],
                                campaign=accacia)

aceasia, _ = Campaign.objects.get_or_create(name="ACEASIA")
aceasia_ship = new_platform(region="EA", platform=Dataset.SHIP, CN=[aceasia_cn_ship], SO4=[aceasia_so4_ship],
                            campaign=aceasia)
aceasia_air = new_platform(region="EA", platform=Dataset.AIRCRAFT, CN=[aceasia_cn_air], SO4=[aceasia_so4_air],
                           campaign=aceasia)

aegean_game = new_Campaign("AEGEAN-GAME", platform=Dataset.AIRCRAFT, region="EU", SO4=[aegean_game_so4])
aforce = new_Campaign("A-FORCE", platform=Dataset.AIRCRAFT, CN=[aforce_cn])
amaze = new_Campaign("AMAZE-08", CCN=amaze_ccn, platform=Dataset.GROUND_STATION, region="SA")
amma = new_Campaign("AMMA", platform=Dataset.AIRCRAFT, region="AF", SO4=[amma_so4])

amf_stations, _ = Campaign.objects.get_or_create(name="AMF_stations")
amf_cape_cod = new_platform(region="NA", platform=Dataset.GROUND_STATION, name="CapeCod",
                            campaign=amf_stations)
amf_manacapuru = new_platform(region="SA", platform=Dataset.GROUND_STATION, name="Manacapuru",
                              campaign=amf_stations)


aoe_1996 = new_Campaign("AOE1996", platform=Dataset.SHIP, region="Arctic")
aoe_2001 = new_Campaign("AOE2001", platform=Dataset.SHIP, region="Arctic")

appraise = new_Campaign("APPRAISE", CN=[appraise_cn], CCN=appraise_ccn, platform=Dataset.AIRCRAFT)

arcpac = new_Campaign("ARCPAC2008", CCN=arcpac_ccn, SO4=[arcpac_so4], CN=[arcpac_cn], platform=Dataset.AIRCRAFT)

arctas, _ = Campaign.objects.get_or_create(name="ARCTAS")
arctas_pc3 = new_platform(platform=Dataset.AIRCRAFT, region="NA", name="PC3", CN=[arctas_cn_pc3], CCN=arctas_ccn_pc3, SO4=[arctas_so4_pc3],
                          campaign=arctas)
arctas_dc8 = new_platform(platform=Dataset.AIRCRAFT, region="NA", name="DC8", CN=[arctas_cn_dc8], CCN=arctas_ccn_dc8, SO4=[arctas_so4_dc8],
                          campaign=arctas)

bird_island = new_Campaign("BirdIsland", platform=Dataset.GROUND_STATION)
bortas = new_Campaign("BORTAS", platform=Dataset.AIRCRAFT, SO4=[bortas_so4])

calnex, _ = Campaign.objects.get_or_create(name="CALNEX")
calnex_air = new_platform(region="NA", platform=Dataset.AIRCRAFT, CN=[calnex_cn], CCN=calnex_ccn_air, SO4=[calnex_so4], name="CALNEX_air",
                          campaign=calnex)
calnex_ship = new_platform(region="NA", platform=Dataset.SHIP, CN=[calnex_cn_ship], CCN=calnex_ccn_ship, SO4=[calnex_so4_ship], name="CALNEX_ship",
                           campaign=calnex)

# care_beijing = new_Campaign("CAREBeijing", platform=Dataset.GROUND_STATION, region="EA", CN=[care_beijing_cn], CCN=care_beijing_ccn)
care_beijing = new_Campaign("CAREBeijing", platform=Dataset.GROUND_STATION, region="EA", CCN=care_beijing_ccn)
caribic = new_Campaign("CARIBIC", platform=Dataset.AIRCRAFT, region="AT", CN=[caribic_cn])
carriba = new_Campaign("CARRIBA", platform=Dataset.GROUND_STATION, CCN=carriba_ccn)
cast = new_Campaign("CAST", platform=Dataset.AIRCRAFT)
clace = new_Campaign("CLACE6", CCN=clace_ccn, platform=Dataset.GROUND_STATION, region='EU')
cope = new_Campaign("COPE", platform=Dataset.AIRCRAFT, SO4=[cope_so4])
cops = new_Campaign("COPS", platform=Dataset.GROUND_STATION)

dc3, _ = Campaign.objects.get_or_create(name="DC3")
dc3_dc8 = new_platform(name="DC8", platform=Dataset.AIRCRAFT, region="NA", CN=[dc3_cn_dc8], CCN=dc3_ccn_dc8, SO4=[dc3_so4],
                       campaign=dc3)
dc3_falcon = new_platform(name="Falcon", platform=Dataset.AIRCRAFT, region="NA", CN=[dc3_cn_falcon],
                          campaign=dc3)

discoveraq = new_Campaign("DISCOVERAQ", platform=Dataset.AIRCRAFT, SO4=[discoveraq_so4])
em25 = new_Campaign("EM25", CCN=em25_ccn, platform=Dataset.AIRCRAFT)
environment_canada = new_Campaign("Environment_Canada", platform=Dataset.GROUND_STATION, region="NA")
eucaari = new_Campaign("EUCAARI", CCN=eucaari_ccn, platform=Dataset.AIRCRAFT, region="EU", SO4=[eucaari_so4])
goamazon = new_Campaign("GoAmazon", CN=[goamazon_cn], CCN=goamazon_ccn, platform=Dataset.GROUND_STATION, region="SA")
hippo = new_Campaign("HIPPO", platform=Dataset.AIRCRAFT)
holme_moss = new_Campaign("HolmeMoss", platform=Dataset.GROUND_STATION)
icealot = new_Campaign("ICEALOT", CN=[icealot_cn], CCN=icealot_ccn, SO4=[icealot_so4], platform=Dataset.SHIP, region="NA")
indoex = new_Campaign("INDOEX", platform=Dataset.AIRCRAFT, region="NA", CN=[indoex_cn], CCN=indoex_ccn)
intexa = new_Campaign("INTEX-A", CN=[intexa_cn], SO4=[intexa_so4], platform=Dataset.AIRCRAFT, region="NA")
intexb = new_Campaign("INTEX-B", CN=[intexb_cn], CCN=intexb_ccn, SO4=[intexb_so4], platform=Dataset.AIRCRAFT, region="NA")
mamm = new_Campaign("MAMM", platform=Dataset.AIRCRAFT)
mirage = new_Campaign("MIRAGE", CN=[mirage_cn], CCN=mirage_ccn, SO4=[mirage_so4], platform=Dataset.AIRCRAFT, region="NA")
neaqs = new_Campaign("NEAQS2002", platform=Dataset.SHIP)
op3 = new_Campaign("OP3", platform=Dataset.GROUND_STATION, SO4=[op3_so4])
pase = new_Campaign("PASE", CN=[pase_cn], CCN=pase_ccn, SO4=[pase_ams], platform=Dataset.AIRCRAFT, region="NA")

pem_tropics_a, _ = Campaign.objects.get_or_create(name="PEMTropicsA")
pem_tropics_a_dc8 = new_platform(name="DC8", platform=Dataset.AIRCRAFT, region="NA", SO4=[pem_tropics_a_so4], CN=[pem_tropics_a_cn],
                                 campaign=pem_tropics_a)
pem_tropics_a_p3b = new_platform(name="P3B", platform=Dataset.AIRCRAFT, region="NA", CN=[pem_tropics_a_cn_p3],
                                 campaign=pem_tropics_a)

pem_tropics_b, _ = Campaign.objects.get_or_create(name="PEMTropicsB")
pem_tropics_b_dc8 = new_platform(name="DC8", platform=Dataset.AIRCRAFT, region="NA", CN=[pem_tropics_b_cn],
                                 campaign=pem_tropics_b)
pem_tropics_b_p3b = new_platform(name="P3B", platform=Dataset.AIRCRAFT, region="NA", CN=[pem_tropics_b_cn_p3],
                                 campaign=pem_tropics_b)

pem_west_a = new_Campaign("PEMWestA", CN=[pem_west_a_cn], SO4=[pem_west_a_so4], platform=Dataset.AIRCRAFT, region="NP")
pem_west_b = new_Campaign("PEMWestB", SO4=[pem_west_b_so4], platform=Dataset.AIRCRAFT, region="NP")


polarstern = new_Campaign("Polarstern", CCN=polarstern_ccn, platform=Dataset.SHIP)
# pride = new_Campaign("PRIDE", CN=[pride_cn], CCN=pride_ccn, platform=Dataset.GROUND_STATION, region="EA")
pride = new_Campaign("PRIDE_PRD", CCN=pride_ccn, platform=Dataset.GROUND_STATION, region="EA")
rhamble = new_Campaign("RHaMBLe", platform=Dataset.SHIP)
ronoco = new_Campaign("RONOCO", CN=[ronoco_cn], CCN=ronoco_ccn, SO4=[ronoco_so4], platform=Dataset.AIRCRAFT, region="NA")

seac4rs = new_Campaign("SEAC4RS", CN=[seac4rs_cn], CCN=seac4rs_ccn, SO4=[seac4rs_so4], platform=Dataset.AIRCRAFT, region="NA")

texaqs, _ = Campaign.objects.get_or_create(name="TEXAQS2006")
texaqs_ship = new_platform(region="NA", platform=Dataset.SHIP, CN=[texaqs_cn_ship], CCN=texasqs_ccn_ship, SO4=[texaqs_so4_ship], name='TEXASQS_ship',
                           campaign=texaqs)
texaqs_air = new_platform(region="NA", platform=Dataset.AIRCRAFT, CN=[texaqs_cn], CCN=texaqs_ccn_air, SO4=[texaqs_so4], name='TEXASQS_air',
                          campaign=texaqs)

trace_a = new_Campaign("TRACEA", CN=[trace_a_cn], platform=Dataset.AIRCRAFT)

trace_p, _ = Campaign.objects.get_or_create(name="TRACEP")
trace_p_dc8 = new_platform(region="EA", platform=Dataset.AIRCRAFT, CN=[trace_p_cn_dc8], name='DC8',
                           campaign=trace_p)
trace_p_p3b = new_platform(region="EA", platform=Dataset.AIRCRAFT, CN=[trace_p_cn, trace_p_ucn], name='P3B',
                           campaign=trace_p)

trompex = new_Campaign("TROMPEX", CCN=trompex_ccn, platform=Dataset.AIRCRAFT)

vocals, _ = Campaign.objects.get_or_create(name="VOCALS")
vocals_c130 = new_platform(name="C-130", CN=[vocals_cn], CCN=vocals_ccn, SO4=[vocals_so4_c130], platform=Dataset.AIRCRAFT, region="SA",
                           campaign=vocals)
vocals_faam = new_platform(name="FAAM", CN=[vocals_cn_faam], CCN=vocals_faam_ccn, SO4=[vocals_so4_faam], platform=Dataset.AIRCRAFT, region="SA",
                           campaign=vocals)
vocals_ship = new_platform(name="ship", CN=[vocals_cn_ship], SO4=[vocals_so4_ship], platform=Dataset.SHIP, region="SA",
                           campaign=vocals)

weybourne = new_Campaign("Weybourne", platform=Dataset.GROUND_STATION)

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
    NSDMeasurementDataset(campaign_platform=accacia.dataset_set.all()[0], files=join(data_path, "ACCACIA", "DMPS*Ship*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=ace1_air, files=join(data_path, "ACE1", "ACE1_NSD_*.nc"), variables="NUMDIST_DMA_OPC"),
    NSDMeasurementDataset(campaign_platform=aceasia_air, files=join(data_path, "ACEASIA", "ACEASIA_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=aegean_game.dataset_set.all()[0], files=join(data_path, "AEGEAN-GAME", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amaze.dataset_set.all()[0], files=join(data_path, "AMAZE-08", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amf_cape_cod, files=join(data_path, "AMF_stations", "CapeCod", "SMPS.*.nc"),
                        variables="NSD"),
    NSDMeasurementDataset(campaign_platform=amf_manacapuru, files=join(data_path, "AMF_stations", "Manacapuru", "SMPS.*.nc"),
                        variables="NSD"),
    NSDMeasurementDataset(campaign_platform=aoe_1996.dataset_set.all()[0], files=join(data_path, "AOE1996", "DMPS_AOE1996*.nc"), variables="NSD_DMPS"),
    NSDMeasurementDataset(campaign_platform=aoe_2001.dataset_set.all()[0], files=join(data_path, "AOE2001", "DMPS_AOE2001*.nc"), variables="NSD_DMPS"),
    # TODO: There should be SMPS data from the DC8 too - but it's not in the folder, only the integrated data
    NSDMeasurementDataset(campaign_platform=arctas_pc3, files=join(data_path, "ARCTAS", "ARCTAS_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=bird_island.dataset_set.all()[0], files=join(data_path, "BirdIsland",
                                                         "BirdIsland_2010_Schmale_submicronaerosolsizedistribution.txt.nc"),
                        variables="NSD_SMPS"),
    NSDMeasurementDataset(campaign_platform=bortas.dataset_set.all()[0], files=join(data_path, "BORTAS", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=care_beijing.dataset_set.all()[0], files=join(data_path, "CAREBeijing", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=clace.dataset_set.all()[0], files=join(data_path, "CLACE6", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=cope.dataset_set.all()[0], files=join(data_path, "COPE", "SMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=cops.dataset_set.all()[0], files=join(data_path, "COPS", "DMPS_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=environment_canada.dataset_set.all()[0], files=join(data_path, "Environment_Canada", "*SMPS*.nc"),
                        variables="SIZE_DISTRIBUTION"),
    NSDMeasurementDataset(campaign_platform=indoex.dataset_set.all()[0], files=join(data_path, "INDOEX", "INDOEX_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=intexa.dataset_set.all()[0], files=join(data_path, "INTEX-A", "INTEX-A_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=mirage.dataset_set.all()[0], files=join(data_path, "MIRAGE", "MIRAGE_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=op3.dataset_set.all()[0], files=join(data_path, "OP3", "DMPS*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pase.dataset_set.all()[0], files=join(data_path, "PASE", "PASE_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pem_tropics_a_p3b, files=join(data_path, "PEMTropicsA", "PEMTropicsA_NSD_*.nc"), variables="NSD"),
    # TODO: These files haven't been turned into a nice NSD yet, I suppose I could if I had the time or inclination...
    # NSDMeasurementDataset(campaign_platform=pem_tropics_b_dc8, files=join(data_path, "PEMTropicsB", "NSD_*.nc"), variables=???),
    # NSDMeasurementDataset(campaign_platform=pem_west_b.dataset_set.all()[0], files=join(data_path, "PEMWestB", "AerComp_*.nc"), variables=???)
    NSDMeasurementDataset(campaign_platform=pem_tropics_b_p3b, files=join(data_path, "PEMTropicsB", "PEMTropicsB_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=pride.dataset_set.all()[0], files=join(data_path, "PRIDE_PRD", "NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=rhamble.dataset_set.all()[0], files=join(data_path, "RHaMBLe", "DMPS*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=vocals_c130, files=join(data_path, "VOCALS", "VOCALS_NSD_*.nc"), variables="NSD"),
    NSDMeasurementDataset(campaign_platform=vocals_faam, files=join(data_path, "VOCALS", "SMPS_VOCALS_*.nc"), variables="NSD")]

# PEMWestB - needs turning into a nice NSD

# All BC files and variables
bc_campaigns = [
    BCMeasurementDataset(campaign_platform=accacia_ship, files=join(data_path, "ACCACIA", "SP2*Ship*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=accacia_aircraft, files=join(data_path, "ACCACIA", "SP2*FAAM*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=aforce.dataset_set.all()[0], files=join(data_path, "A-FORCE", "SP2*.nc"), variables="BCMCSTP"),
    BCMeasurementDataset(campaign_platform=arctas_dc8, files=join(data_path, "ARCTAS", "SP2*.nc"), variables="BC_MASS_1013HPA_273K"),
    BCMeasurementDataset(campaign_platform=arctas_pc3, files=join(data_path, "ARCTAS", "ARCTAS_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=arcpac.dataset_set.all()[0], files=join(data_path, "ARCPAC2008", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=bortas.dataset_set.all()[0], files=join(data_path, "BORTAS", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=calnex.dataset_set.all()[0], files=join(data_path, "CALNEX", "SP2_mrg*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=cope.dataset_set.all()[0], files=join(data_path, "COPE", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=cast.dataset_set.all()[0], files=join(data_path, "CAST", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=clace.dataset_set.all()[0], files=join(data_path, "CLACE6", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=dc3_falcon, files=join(data_path, "DC3", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=discoveraq.dataset_set.all()[0], files=join(data_path, "DISCOVERAQ", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=eucaari.dataset_set.all()[0], files=join(data_path, "EUCAARI", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=hippo.dataset_set.all()[0], files=join(data_path, "HIPPO", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=holme_moss.dataset_set.all()[0], files=join(data_path, "HolmeMoss", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=intexb.dataset_set.all()[0], files=join(data_path, "INTEX-B", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=mamm.dataset_set.all()[0], files=join(data_path, "MAMM", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=mirage.dataset_set.all()[0], files=join(data_path, "MIRAGE", "MIRAGE_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=neaqs.dataset_set.all()[0], files=join(data_path, "NEAQS2002", "NEAQS2002_carbon.nc"), variables="EC"),
    BCMeasurementDataset(campaign_platform=seac4rs.dataset_set.all()[0], files=join(data_path, "SEAC4RS", "HDSP2_*.nc"), variables="BC"),
    BCMeasurementDataset(campaign_platform=texaqs.dataset_set.all()[0], files=join(data_path, "TEXAQS2006", "SP2*.nc"), variables="BC_MASS"),
    BCMeasurementDataset(campaign_platform=trace_p_dc8, files=join(data_path, "TRACEP", "BC_*.nc"), variables="BC"),
    BCMeasurementDataset(campaign_platform=vocals_c130, files=join(data_path, "VOCALS", "VOCALS_SP2*.nc"), variables="INCMASS"),
    BCMeasurementDataset(campaign_platform=weybourne.dataset_set.all()[0], files=join(data_path, "Weybourne", "SP2*.nc"), variables="BC_MASS")]


# These files have no measurement data...
broken_files = ['ARCTAS_AMS_RF02_20080327_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF11_20080622_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF12_20080624_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF13_20080626_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF14_20080626_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF15_20080628_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF16_20080629_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF17_20080630_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF18_20080702_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF19_20080703_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF20_20080706_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF21_20080707_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF22_20080709_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF23_20080710_r2ict_apr2012.nc',
                'ARCTAS_AMS_RF24_20080712_r2ict_apr2012.nc',
                'ARCTAS_SP2_RF11_20080622_r2ict_apr2012.nc',
                'MIRAGE_AMS_20060322.154100_224100.PNI_plus.nc',
                'VOCALS_AMS_20081025.062900_152500.PNI.nc',
                'VOCALS_AMS_20081028.061800_151200.PNI.nc',
                'MIRAGE_SP2_20060312.172600_013501.PNI_plus.nc',
                'ACE1_NSD_RF11_11171995224801_11181995073133.nc',
                'ACE1_NSD_RF12_11181995222509_11191995072145.nc',
                'ACEASIA_PILS_20010401.234300_081330.PNI_plus.nc',
                'ACEASIA_PILS_20010403.235800_085659.PNI_plus.nc',
                'PASE_AMS_20070804.202300_021358.PNI_plus.nc',
                # These have missing CNHot (N13 vol) measurements which breaks everything...
                'INDOEX_CPC_RF01_0216_plus.nc',
                'INDOEX_CPC_RF02_0218_plus.nc',
                # Transit flight with no data
                'PEMTropicsA_CPC_RF04_p3b_19960815_plus.nc',
                'PEMTropicsA_CPC_RF07_p3b_19960824_plus.nc',
                'PEMTropicsB_CPC_RF01_p3b_19990304_r0.nc',
                'ACE1_NSD_RF33_12221995171406_12231995030924.nc',
                'PEMTropicsA_NSD_RF04_p3b_19960815_plus.nc',
                'PEMTropicsA_NSD_RF05_p3b_19960818_plus.nc',
                'PEMTropicsA_NSD_RF06_p3b_19960821_plus.nc',
                'PEMTropicsA_NSD_RF20_p3b_19960925_plus.nc',
                'PEMTropicsA_NSD_RF21_p3b_19960926_plus.nc',
                # No valid points...
                'AerDen_pwa15090.m.nc',
                'N_ACE1_NSD_RF01_10311995160522_11011995012858.nc']


# Methods for actually reading the data
def load_gassp_data(test_set=False):
    from cis.data_io.data_reader import DataReader
    from django.contrib.gis.geos import GEOSGeometry
    from glob import glob
    from django.utils import timezone
    from .utils import cis_object_to_shp
    from os.path import basename
    from itertools import islice

    # Create a datareader so that we can read coordinates rather than datasets
    dr = DataReader()
    limit = 2 if test_set else None

    for md in Measurement.objects.all():
        for f in islice(glob(md.files), 0, limit):
            # Skip broken or already processed files
            if basename(f) in broken_files or len(MeasurementFile.objects.filter(filename=f).all()) > 0:
                # Don't process this one
                print("Skipping: {}".format(f))
                continue
            print("Processing: {}".format(f))
            d = dr.read_coordinates(f)
            if d.count() == 0:
                print("Empty file.")
                continue

            # Get the spatial extent
            try:
                geom = GEOSGeometry(cis_object_to_shp(d, platform_type=md.dataset.get_platform_type_display()).wkt)
            except ValueError:
                print("Unable to determine spatial extent of file.")
                geom = None

            # Sort the time extent
            dt = d.coord('time')
            dt.convert_standard_time_to_datetime()
            t_start = dt.points.min()
            t_end = dt.points.max()
            # Add UTC timezone stamp
            t_start = timezone.make_aware(t_start, timezone.UTC())
            t_end = timezone.make_aware(t_end, timezone.UTC())
            md.measurementfile_set.create(spatial_extent=geom, time_start=t_start, time_end=t_end, filename=f)


def clean_GASSP_datasets(buffer_width=2.0):
    """
    Add a dataset name and region to each Dataset if they aren't present
    """
    from django.contrib.gis.geos import GeometryCollection
    for d in Dataset.objects.all():
        if d.name is None:
            d.name = d.campaign.name + " " + d.get_platform_type_display()

        if d.spatial_extent is None:
            lines = GeometryCollection(*(mf.spatial_extent for ms in d.measurement_set.all()
                                            for mf in ms.measurementfile_set.all()))
            d.spatial_extent = GeometryCollection(lines.buffer(buffer_width).unary_union.simplify(0.2))
