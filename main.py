from VerifyInputs import *
from CreateOutputs import *
from AnalysisFunctions import *
from Exploracy import *
from Normalisation import *
from SeparatingPheno import*
import logging


logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(filename="test.log", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    input_path = "/Users/alexandreunger/desktop/datas/input_folders"
    output_path = "/Users/alexandreunger/desktop/datas/output_folders"

    if verify(input_path):
        logger.info("All inputs files and directory are ok ...")
    else:
        exit(1)

    if create_all_outputs(output_path):
        logger.info("All outputs files and directory were successfully created ...")
    else:
        exit(1)

    change_dir(input_path)
    for is_epileptic_case in [True, False]:
        if is_epileptic_case is True:
            directory_in = epilepsy_case_folder
            directory_out = epileptic_patient_folder
        else:
            directory_in = epilepsy_1KGP_folder
            directory_out = KGP_patient_folder

        counter = 0
        pt_checked_list = []
        for patient_file in os.listdir(directory_in): # == varcopp_results_folder
            code_patient = extrade_BEP(patient_file, is_epileptic_case)
            if is_epileptic_case:
                CodeWithoutBep = code_patient[3:]
                pt_checked_list.append(CodeWithoutBep)
            else:
                pt_checked_list.append(code_patient) # save in the final file only those who were analyzed
            gene_pairs_epi_global = analyse_varcopp_data(code_patient, patient_file, output_path, is_epileptic_case)
            filtering_by_panel(code_patient, gene_pairs_epi_global, input_path, output_path, is_epileptic_case)
            counter += 1
            logger_info("avancement " + str(counter / len(os.listdir(directory_in))))
        exploracy(directory_out, input_path, output_path, pt_checked_list, is_epileptic_case) # analyse exploratrice des datas ici

        exploracy_epi_path = os.path.join(output_path, exploracy_epi_file)
        output_normalized_exploracy = os.path.join(output_path, os.path.join(exploracy_folder, "normalized_exploracy_epi.csv"))

        if is_epileptic_case:
            normalisation(exploracy_epi_path, output_normalized_exploracy)
            separate_pheno(output_normalized_exploracy) # creating subfile to do the pheno comparaison in R





