#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This function runs SPSS logistic regression formula with a test data file.
The formula must be contained in a CSV file and only have features and the associated beta values.
The test data file is also a CSV file and has same layout as the training file that you used in SPSS.

Xiaolu Xiong
xxiong@wpi.edu
"""

from csv import reader, writer


E = 2.718281828

def SPSS_formula_runner (target_col_num,
                         formula_file_name,
                         testing_data_file_name,
                         output_file_name=None):

    zeop_value_tags = ["0c", "0b"]
    intercept_tag = "Intercept"

    target_col_num = int(target_col_num)

    # Open formula and testing data file
    formula_file = open(formula_file_name, 'rU')
    test_data_file = open(testing_data_file_name, 'rb')

    # Open output file
    if output_file_name is None:
        output_file_name = testing_data_file_name.split('.')[0]+'_fit_result.csv'
    output_file = open(output_file_name, 'wb')
        
    # Init data dicts 
    factor_dict = {}
    covariance_dict = {}
    parameter_dict = {}
    intercept = 0

    formula_csv_reader = reader(formula_file)
    test_data_csv_reader = reader(test_data_file)
    output_cst_writer = writer(output_file)

    for row in formula_csv_reader:
        item = row[0]
        beta = row[1]
        
        if (beta in zeop_value_tags):
            beta = 0
            
        if item == intercept_tag:
            intercept = -1*float(beta)
        elif ('[' in item) and ("]" in item):
            item = item[1:-1]
            key = item.split('=')[0]
            value = item.split('=')[1]
            if factor_dict.has_key(key):
                factor_dict[key][value] = -1*float(beta)
            else:
                factor_dict[key] = {}
                factor_dict[key][value] = -1*float(beta)
        else:
            covariance_dict[item] = -1*float(beta)
    formula_file.close()

    print ("Found factors %s in the formula file." % factor_dict.keys())
    print ("Found covariances %s in the formula file." % covariance_dict.keys())

    for key in factor_dict.keys():
        avg = sum(factor_dict[key].values())/float(len(factor_dict[key].values()))
        factor_dict[key+'_avg'] = avg

    # Get pass the title row
    row = test_data_csv_reader.next()
    for n, item in enumerate(row):
        if (item in factor_dict.keys()) or (item in covariance_dict.keys()):
            parameter_dict[item] = n
        else:
            print("Didn't find %s in formula, make sure this is what you are excepting." % item)

    for row in test_data_csv_reader:
        result = 0
        result += intercept
        target = row[target_col_num]
        
        for parameter_name in parameter_dict.keys():
            parameter_pos = parameter_dict[parameter_name]
            if parameter_name in covariance_dict:
                value = float(row[parameter_pos])
                beta = covariance_dict[parameter_name]
                result += beta * value
            elif parameter_name in factor_dict:
                value = row[parameter_pos]
                if factor_dict[parameter_name].has_key(value):
                    result += factor_dict[parameter_name][value]
                else:
                    result += factor_dict[parameter_name+'_avg']
            else:
                raise Exception("parameter_name error!")
        final_result = E ** result/(1 + E ** result)
        output_cst_writer.writerow([target, final_result])
        
    test_data_file.close()
    output_file.close()

    print ("Done, output file is %s" % output_file_name)

if __name__ == '__main__':

    target_col_num = 3
    formula_file_name = "pfa_formula.csv"
    testing_data_file_name = "pfa_test_data.csv"
    
    SPSS_formula_runner(target_col_num,
                         formula_file_name,
                         testing_data_file_name,
                         output_file_name=None)
