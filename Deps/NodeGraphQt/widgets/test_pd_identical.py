import pandas as pd



def are_identical(dataframe_1:pd.DataFrame, dataframe_2:pd.DataFrame):
    is_empty_1 = dataframe_1.empty
    is_empty_2 = dataframe_2.empty

    if is_empty_1 and is_empty_2:
        return True
    elif is_empty_2 != is_empty_1:
        return False
    else:
        try:
            return dataframe_1.equals(dataframe_2)
        except:
            return False
    






pd1 = pd.DataFrame()
pd2 = pd.DataFrame()

pd3 = pd.DataFrame([1,2,3])
pd5 = pd.DataFrame([1,2,3])
pd4 = pd.DataFrame({"chose": [1,2,3,5,6]})

print(pd1, pd2, pd3, pd4)
print(are_identical(pd1, pd2))
print(are_identical(pd3, pd2))
print(are_identical(pd4, pd2))
print(are_identical(pd4, pd3))
print(are_identical(pd5, pd3))