Spss Formula Runner
===================

Spss Formula Runner:  generates regression results by fitting test data with the SPSS training model. 


SPSS regression doesn't support cross-validation or running against with testing data (at least for version 17.0), in other words, it can only train models, but no way to test them. 
So here is a Python script which generates the regression results by fitting test data with the SPSS training model (the formula). Currently, only supports logistic regression.

USAGE
-------

```
python SPSS_formula_runner.py [label column number] [formula file name] [test data file name]
```
e.g: 
```
python SPSS_formula_runner.py 3 pfa_formula.csv pfa_test_data.csv
```



LICENSE
--------
No license, do whatever you want, I couldn't possibly comment.  

