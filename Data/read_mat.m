data_GMO = load("GMO.mat")
save -mat7-binary GMO_oct.mat date_GMO

data_Transgenic = load("Transgenic.mat")
save -mat7-binary Transgenic_oct.mat data_Transgenic


data_Genetically_Modified_Organism = load("Genetically_Modified_Organism.mat")
save -mat7-binary Geneticall_Modified_Organism_oct.mat data_Genetically_Modified_Organism

data_Vaccine = load("Vaccine.mat")
save -mat7-binary Vaccine_oct.mat data_Vaccine


time_stamps = load("file_name_versus_date.mat")
save -mat7-binary file_name_versus_time_stamps.mat time_stamps
