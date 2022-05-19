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
        performics_valuesReg = re.sub(r"\b\s\b", "[- ]?", performics_valuesReg)  #replacing spaces with optional character

        df[k] = df['Keyword Idea'].str.extract('(' + performics_valuesReg + ')')
        df[k] = df['Keyword_idea_cleaned'].str.extract('('+performics_valuesReg+')')


    df.drop(['Category','Subcategory', 'Keyword_idea_cleaned'], axis = 1, inplace=True)
    #df.to_excel(r'C:\Users\ashsingh42\Downloads\Categorised_Data.xlsx', index=False, header=True)
    return df,data_dict


def CreateMapping(dictionary):
    Term = []
    Mapping = []

    for k, d in dictionary.items():
        for x in d:
            temp = re.sub(r'\s', '', x)  # Term without space
            Term.append(temp)
            Mapping.append(x)

            temp1 = re.sub('a|á', "a", x)
            temp1 = re.sub('e|é', "e", temp1)
            temp1 = re.sub('i|í', "i", temp1)
            temp1 = re.sub('o|ó|ö|ő', "o", temp1)
            temp1 = re.sub('u|ú|ü|ű', "u", temp1)
            Term.append(temp1)  # Term without special characters
            Mapping.append(x)

            temp2 = re.sub(r'\s', '', temp1)
            Term.append(temp2)  # Term without special charcter and space
            Mapping.append(x)

    df2 = pd.DataFrame(list(zip(Term, Mapping)), columns=['Search Term', 'Mapping'])
    df2.to_excel(r'C:\Users\ashsingh42\Downloads\Keyword_Mapping_New.xlsx', index=False, header=True)

    return df2


def Keyword_Mapping():

    raw_df, raw_mapping_dict = Keyword_Extract()
    map_df = CreateMapping(raw_mapping_dict)

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

    raw_df.to_excel(r'C:\Users\ashsingh42\Downloads\Categorised_Data1.xlsx', index=False, header=True)

if __name__ == "__main__":
    Keyword_Mapping()











