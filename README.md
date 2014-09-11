SPSS_formula_runner
===================

SPSS formula runner


SPSS regression doesn't support cross validation or running against with testing data (at least for version 17.0), in other words, it can only train models, but no way to test them. 
So here is a Python script which generates the regression results by fitting test data with the SPSS training model (the formula). Currently, only supports logistic regression.
