import pandas as pd
import re as re
import numpy as np


def Export_Cleanup():
    df2 = pd.read_excel(r'C:\Users\ashsingh42\Downloads\export_dataframe.xlsx')
    df2.drop_duplicates(keep='first', inplace=True)
    df2.drop(df2[(df2['Monthly Searches'] == 0) & (df2['Competition'] == 'UNSPECIFIED')].index, inplace=True)


    #Creating column without special character to extract data
    clean_keyword = df2['Keyword Idea'].copy()
    clean_keyword = clean_keyword.str.replace('á','a', regex= False)
    clean_keyword = clean_keyword.str.replace(r'(é|è)', 'e', regex=True)
    clean_keyword = clean_keyword.str.replace('í', 'i', regex=False)
    clean_keyword = clean_keyword.str.replace(r'(ó|ö|ő)', 'o', regex=True)
    clean_keyword = clean_keyword.str.replace(r'(ú|ü|ű)', 'u', regex=True)

    df2['Keyword_idea_cleaned'] = clean_keyword

    return df2

def Keyword_Extract():

    df2 = pd.read_excel(r'C:\Users\ashsingh42\Downloads\Book2.xlsx')
    data_dict = df2.to_dict("list")

    for k, d in data_dict.items():              #REMOVING NULL VALUES FROM LIST
        L2 = [x for x in d if pd.isnull(x) == False]
        data_dict[k] = L2

    df = Export_Cleanup()

    for k,d in data_dict.items():
        performics_valuesReg = "|".join(d)
        performics_valuesReg = performics_valuesReg.lower()
        performics_valuesReg = re.sub('a|á', "[aá]", performics_valuesReg)
        performics_valuesReg = re.sub('e|é', "[eé]", performics_valuesReg)
        performics_valuesReg = re.sub('i|í', "[ií]", performics_valuesReg)
        performics_valuesReg = re.sub('o|ó|ö|ő', "[oóöő]", performics_valuesReg)
        performics_valuesReg = re.sub('u|ú|ü|ű', "[uúüű]", performics_valuesReg)
        performics_valuesReg = re.sub(r"[a-z]\s[a-z0-9]", "[- ]?", performics_valuesReg)  #replacing spaces with optional character

        df[k] = df['Keyword_idea_cleaned'].str.extract('('+performics_valuesReg+')')
        df[k] = df['Keyword Idea'].str.extract('('+performics_valuesReg+')')

    df.drop(['Category','Subcategory', 'Keyword_idea_cleaned'], axis = 1, inplace=True)
    #df.to_excel(r'C:\Users\ashsingh42\Downloads\Categorised_Data.xlsx', index=False, header=True)
    return df

def Keyword_Mapping():
    map_df = pd.read_excel(r'C:\Users\ashsingh42\Downloads\KeywordMapping.xlsx')
    raw_df = Keyword_Extract()

    #CREATING DICTIONARY FOR MAPPING
    map_dict = dict(zip(map_df['Search Term'].str.lower(), map_df['Mapping'].str.lower()))

    #REPLACING TERM FROM EXTRACTED DATAFRAME FOR ALLIGNMENT
    for i in range(0,raw_df.shape[0]):
        for j in range(3,raw_df.shape[1]):
            if raw_df.iat[i,j] in map_dict.keys():
                raw_df.iat[i, j] = map_dict[raw_df.iat[i,j]]

    #REPLACE NOT WORKING WITH MAPPING AS DICTIONARY
    # raw_df = raw_df.iloc[:,9:].copy()
    # raw_df.replace(map_dict, value=None, inplace=True)

    raw_df.to_excel(r'C:\Users\ashsingh42\Downloads\Categorised_Data.xlsx', index=False, header=True)

if __name__ == "__main__":
    Keyword_Mapping()