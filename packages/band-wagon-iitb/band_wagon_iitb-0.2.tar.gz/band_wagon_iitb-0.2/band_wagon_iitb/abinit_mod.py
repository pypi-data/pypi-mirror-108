# Importing the libraries

import os
import time
import fileinput
import sys
import shutil
import glob
import pandas as pd
import subprocess
import re

#*************************************************************************************************
#****************************************> replace_expression <***********************************
# replace_expression : Function to search and replace an expression in a document
# Variables: 
# 1. file_name : The path of the document (str)
# 2. search_expression : The expression to be replaced (str)
# 3. replace_expression : The new expression (str)

def replace_expression(file_name, replace_expression, search_expression):
    for l in fileinput.input(file_name,inplace = 1):
        if search_expression in l: l = l.replace(search_expression,replace_expression)
        sys.stdout.write(l)

#**************************************************************************************************
#***************************************> replace_nth_line <***************************************
#**************************************************************************************************

# replace_nth_line : Function to replace the original text at n'th line in the document with new exp.
# Variables:
# 1. file_name : The path of the document (str)
# 2. line_number : The number of the line the document
# 3. replace_expression : The new expression (str)

def replace_nth_line(file_name, replace_expression, line_number):
        f = open(file_name,"r")
        lines = f.readlines()
        lines[line_number-1]  = replace_expression + "\n"
        f = open(file_name,"w")
        f.writelines(lines)
        f.close()

#*************************************************************************************************
#**************************************> create_folders <*****************************************
#*************************************************************************************************

# create_folders : Function to create different folders with pseudopotential files, input files with different 'k point' and 'ecut' values
# Variables:
# 1. ecut_list : List of ecut values (list of int) (example: [45, 50, 55, 60] or [55,65] )
# 2. grid_lsit : List of 'k point' grid values (list of str) (example: ['9x9x5', '11x11x7'])
# 3. valence_bands : Number of valence bands (int)
# 4. first_pseudo_path : Path of the first pseudopotential file (str)
# 5. second_pseudo_path : Path of the second pseudopotential file (str)
# 6. input_path : Path of the input file (str)
# 7. files_path : Path of the xfiles file (str)


def create_folders(ecut_list , grid_list, valence_bands, first_pseudo, second_pseudo, input_path, files_path ):
    
    # ecut_list is the list of ecut values
    
    for i in range(len(grid_list)):
        name_grid_folder = grid_list[i]
        os.system("mkdir " + name_grid_folder)
        os.system("cd " + name_grid_folder + "/")

        for ecut_value in ecut_list:
            os.system("mkdir " + name_grid_folder +  "/ecut_" + str(ecut_value))
            os.system("cd " + name_grid_folder +  "/ecut_" + str(ecut_value))
            os.system("cp " + first_pseudo + " " + curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/")
            os.system("cp " + second_pseudo + " " + curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/")
            os.system("cp " + input_path + " " + curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/")
            os.system("cp " + files_path + " " + curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/")
            replace_nth_line(curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/" + "telast_1.in", "ecut  " + str(ecut_value) + ".0", 70)
            replace_nth_line(curr_dir + "/" + name_grid_folder + "/" + "ecut_" + str(ecut_value) + "/" + "telast_1.in", "ngkpt  " + ngkpt_grid_list[i], 76)
            os.system("cd ..")
        os.system("cd ..")
        

#****************************************************************************************************
# calc_lattice_parameters : Function to calculate lattice parameters for a given ecut list and kpt list values.

# Variables:
# 1. ecut_list : List of ecut values (list of int) (example: [45, 50, 55, 60] or [55,65] )
# 2. grid_lsit : List of 'k point' grid values (list of str) (example: ['9x9x5', '11x11x7'])
# 3. output_path : The path where you want to store the output analysis files (str)
        
def calc_lattice_parameters(ecut_list, kpt_grid, output_path ) :
    curr_dir = os.getcwd()

    # List of the subdirectories
    list_folders = grid_list

    # Data file
    new_data = output_path + "/Final_Data_Lattice_Parameter.csv"

    ideal_ecut = ""

    column_names = []
    for i in ecut_list:
        column_names += ["ecut_"+str(i)]
        
    for i in list_folders :
        newFob = open(new_data,'a')
        newFob.write("kpt grid : "+ str(i))
        newFob.write("  ")
        newFob.close()
        data_frame = pd.DataFrame(index = range(1, 3), columns = column_names)
        for j in ecut_list:
            file_name_tbase3_out = curr_dir + "/" + i + "/" + "ecut_" + str(j) + "/"
            os.chdir(file_name_tbase3_out)
            fob = open("telast_1.out", 'r')
            objectLines = fob.readlines()
            startFound = False
            running_index = 1
            for line in objectLines:
                if startFound and "etotal2 " in line:
                    value = line.split(" ")[-1]
                    data_frame["ecut_"+str(j)][running_index] = float(value)
                    startFound = False
                    running_index += 1
            if startFound:
                value = line.split(" ")[-1]
                data_frame["ecut_"+str(j)][running_index] = float(value) 
                running_index += 1
            if "etotal1 " in line:
                value = line.split(" ")[-1]
                data_frame["ecut_"+str(j)][running_index] = float(value)
                startFound = True
                running_index += 1
        os.chdir(curr_dir)
    data_frame.loc['Minimum_Values'] = data_frame.min(axis=0)
    difference = [0]
    for l in range(1,len(column_names)): 
        difference.append((data_frame.iloc[-1][column_names[l-1]]-data_frame.iloc[-1][column_names[l]])*27211.4)

    for l in range(1,len(column_names)): 
        if difference[l] < 1: 
            ideal_ecut = column_names[l-1]
            break

    data_frame.loc['Difference'] = difference
    data_frame.to_csv(output_path + "/Final_Data_Lattice_Parameter.csv",mode='a')
    print("The ecut should be: " + ideal_ecut.split("_")[1])


#***************************************************************************************************
# give_jobs : Function to give abinit jobs for pseudopotential files, input files with different 'k point' and 'ecut' values
# Variables:
# 1. ecut_list : List of ecut values (list of int) (example: [45, 50, 55, 60] or [55,65] )
# 2. grid_lsit : List of 'k point' grid values (list of str) (example: ['9x9x5', '11x11x7'])
# 3. abinit_path : Path of the abinit package in bin (str)


def give_jobs(abinit_path,ecut_list, grid_list):
    
    # Current directory
    curr_dir = os.getcwd()

    # List of the subdirectories
    list_folders = [str(i) for i in grid_list]

    for i in list_folders :
        for j in ecut_list:
            file_name_tbase3_x = curr_dir + "/" + i + "/" + "ecut_" + str(j) + "/"
            os.chdir(file_name_tbase3_x)
            os.system(abinit_path + " <telast_1.files > telast_1.stdout")

    def length_doc(file_name):
        lines_in_file = open(file_name, 'r').readlines()
        return len(lines_in_file)
    
    def found_expression(file_name,expression):
        with open(file_name) as f:
                if expression in f.read():
                    return True
        return False

    time.sleep(30)    
    for i in list_folders :
        for j in ecut_list:
            file_name_tbase3_x = curr_dir + "/" + i + "/" + "ecut_" + str(j) + "/"
            os.chdir(file_name_tbase3_x)
            while not found_expression("telast_1.out", " Calculation completed.") : time.sleep(60)
            print("Calculation completed for " + i + " ecut value: " + str(j))


#**************************************************************************************************
#******************************> bandgap_calc <****************************************************
#**************************************************************************************************

# bandgap_calc : Function to calculate bandgap values for a certain pair ecut and kpt grid values.
# Variables:
# 1. abinit_path : Path of the abinit package in bin (str)
# 2. abinit_structure_maker_path : Path of the structure maker file (str)
# 3. kpt_grid_desired : The grid value for which bandgap is to be calculated (str)
# 4. ecut_desired : The ecut value for which bandgap is to be calculated (int)
# 5. output_path : The path of the output data folder

def bandgap_calc(abinit_path, abinit_structure_maker_path, kpt_grid_desired, ecut_desired, valence_bands, output_path):
    vbm = valence_bands
    curr_dir = os.getcwd()
    ecut_desired = str(ecut_desired)
    
    # Find the line number for a certain phrase
    def find_kpt_line_numbers(file_name,phrase,kpt_number_array):
        with open(file_name) as file_blob:
            for index,line in enumerate(file_blob,1):
                if phrase in line : kpt_number_array.append(index)

    os.system("mkdir " + curr_dir + "/"+ kpt_grid_desired + "/" + ecut_desired + "/" + "Band_Structure")

    os.system("cp " + curr_dir + "/tbase3_5.files" + " " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure")
    os.system("cp " + curr_dir + "/tbase3_5.in" + " " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure")
    os.system("cp " + curr_dir + "/" + first_pseudo + " " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure")
    os.system("cp " + curr_dir + "/" + second_pseudo + " " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure")
    os.system("cp " + abinit_structure_maker_path + " " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure")
    os.chdir(curr_dir + "/"+ kpt_grid_desired + "/" + ecut_desired + "/" + "Band_Structure")
    os.system(abinit_path + " <tbase3_5.files > tbase3_5.stdout")
    os.system("python " + abinit_structure_maker_path+ " tbase3_5.out")
    os.system("python " + abinit_structure_maker_path+ " tbase3_5.out.dbs")
    os.system("xmgrace tbase3_5.out.agr")

    os.system("cp " + curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/"+ "Band_Structure" +"/" + "tbase3_5.out.agr" + " " + curr_dir + "/" + "Output_Data/")
    file_name_tbase3_stdout = curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/Band_Structure/" + "tbase3_5.out.dbs"
    fob = open(file_name_tbase3_stdout, 'r')
    objectLines = fob.readlines()

    kpt_array = []
    find_kpt_line_numbers(file_name_tbase3_stdout,"kpt", kpt_array)
    last = 0
    kpt_array = [i+1 for i in kpt_array]

    for i in range(1,2):
        master_string_array_2 = objectLines[kpt_array[i]].split(" ")
        master_string_array_2 = [(i) for i in master_string_array_2 if i][:-1]
        column_l = len(master_string_array_2)


    columns_names = ["band_" + str(i+1) for i in range(column_l)]
    data_frame = pd.DataFrame(columns = columns_names)

    kpt_array.append(kpt_array[1]-kpt_array[0]+kpt_array[-1])
    for p in range(len(kpt_array)-1):

        master_string_array_2 = objectLines[kpt_array[p]].split(" ")
        master_string_array_2 = [(i) for i in master_string_array_2 if i][:-1]
        master_string_array_2 = [float(i) for i in master_string_array_2]
        data_frame.loc['kpt# '+str(p+1)] = master_string_array_2
        last = i



    data_frame = data_frame.iloc[:,vbm-1:vbm+1]
    data_frame['Direct_Bandgap'] = data_frame.apply(lambda x:x['band_'+str(vbm+1)] - x['band_' + str(vbm)], axis = 1)
    data_frame_direct = data_frame.sort_values(by =['Direct_Bandgap'],ascending= True)
    direct_band_gap = data_frame_direct['Direct_Bandgap'][0]
    print("Direct Bandgap of : " + str(direct_band_gap) + " at kpt: " + str(data_frame_direct.idxmin()[-1]))

    kpt_vbm = data_frame_direct.idxmax()[0]
    kpt_cbm = data_frame_direct.idxmin()[1]
    indirect_band_gap = data_frame['band_'+str(vbm+1)].min() -  data_frame['band_'+str(vbm)].max() 
    print("Indirect Bandgap of : "+ str(indirect_band_gap) + " VBM kpt = " + str(kpt_vbm) + " and CBM kpt = " + str(kpt_cbm))

    data_frame.to_csv(output_path+"/Band_Gap.csv")

    newFob = open(output_path+"/Band_Gap.csv",'a')
    newFob.write(("Direct Bandgap of : " +  str(direct_band_gap) +  " at kpt: " + str(data_frame_direct.idxmin()[-1])))
    newFob.write("  ")
    newFob.close()

    newFob = open(output_path+"/Band_Gap.csv",'a')
    newFob.write(("Indirect Bandgap of : " +  str(indirect_band_gap) + " VBM kpt = " +  str(kpt_vbm) + " CBM kpt = " + str(kpt_cbm)))
    newFob.write("  ")
    newFob.close()


#*************************************************************************************************
#******************************************> band_energy_calc <***********************************
#*************************************************************************************************
# bandgap_calc : Function to calculate bandgap values for a certain pair ecut and kpt grid values.
# Variables:
# 1. kpt_grid_desired : The grid value
# 2. ecut_desired : The ecut value
# 3. valence_bands : Number of valence bands
# 4. output_path : The ouput folder path


def band_energy_calc(kpt_grid_desired, ecut_desired, valence_bands):
    vbm = valence_bands
    # Find the line number for a certain phrase
    def find_kpt_line_numbers(file_name,phrase,kpt_number_array):
        with open(file_name) as file_blob:
            for index,line in enumerate(file_blob,1):
                if phrase in line : kpt_number_array.append(index)

    curr_dir = os.getcwd()

    file_name_tbase3_stdout = curr_dir+"/"+ kpt_grid_desired + "/" + ecut_desired + "/" + "telast_1.stdout"
    fob = open(file_name_tbase3_stdout, 'r')
    objectLines = fob.readlines()

    kpt_array = []
    wtk_array = []
    find_kpt_line_numbers(file_name_tbase3_stdout,"kpt#", kpt_array)
    last = 0
    kpt_array = kpt_array[(len(kpt_array) - len(kpt_array)/2 ): ]
    for i in range(1,2):

        master_string = ""

        for j in range(last,i): 
            master_string += objectLines[kpt_array[j]]
        master_string_array_1 = [float(x) for x in re.findall("-?\d+.?\d*(?:[Ee]-\d+)?", master_string)]
        column_l = len(master_string_array_1)

    columns_names = ["band_" + str(i+1) for i in range(column_l)]
    data_frame = pd.DataFrame(columns = columns_names)

    kpt_array.append(kpt_array[1]-kpt_array[0]+kpt_array[-1])
    for i in range(1,len(kpt_array)):

        master_string = ""

        for j in range(last,i): 
            master_string += objectLines[kpt_array[j]]
        
        master_string_array_1 = [float(x) for x in re.findall("-?\d+.?\d*(?:[Ee]-\d+)?", master_string)]
        data_frame.loc['kpt# '+str(i)] = master_string_array_1
        last = i

    for i in range(len(kpt_array)-1):
        wtk_array.append(float(objectLines[kpt_array[i]-1].split("wtk=  ")[1].split(",")[0]))

    data_frame = data_frame.iloc[:,:vbm]
    data_frame['Summation'] = data_frame.sum(axis=1)
    data_frame['wtk'] = wtk_array
    data_frame['Sum*wtk'] =  data_frame.apply(lambda x:x['Summation']*x['wtk'],axis=1)
    data_frame.to_csv(curr_dir+"/Output_Data/Band_Energy.csv")
    newFob = open(curr_dir+"/Output_Data/Band_Energy.csv",'a')
    newFob.write("Total Energy : " + str(sum(data_frame['Sum*wtk'])))
    newFob.write("  ")
    newFob.close()

#************************************************************************************************



    
    
    
    
