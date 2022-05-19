import pandas as pd
import re
from datetime import datetime


def LoadDictionary():

    df2 = pd.read_excel(r'C:\Users\ashsingh42\Downloads\book2.xlsx') #PUBLICIS CATEGORIES LIST

    data_dict = df2.to_dict("list")

    for k, d in data_dict.items():              #REMOVING NULL VALUES FROM LIST
        L2 = [x for x in d if pd.isnull(x) == False]
        data_dict[k] = L2

    performics_values = []
    for k, d in data_dict.items():              #MERGING ALL COLUMS TO SINGLE LIST
        performics_values.extend(d)

    list1 = [words for segment in performics_values for words in segment.split()]      #SPLITTING WORDS CONTAINING SPACE

    list2 = [x.lower() for x in list1]         #LOWERCASE ITEMS
    final = []
    [final.append(x) for x in list2 if x not in final]    #REMOVING DUPLICATE GENERATED DUE TO SPLIT
    return final

def UncategorisedKeywords():

    df = pd.read_excel (r'C:\Users\ashsingh42\Downloads\Categorised_Data.xlsx')
    df.drop(df.columns[3:20], axis=1, inplace=True)
    values = df['Keyword Idea'].tolist()        #JOINING ALL KEYWORDS TO SINGLE STRING
    str_values = ' '.join(values)
    values_list = list(str_values.split(" "))


    # out = [x for x in values_list if x not in final]        #REMOVING KEYWORDS ALREADY IN OUR DICTIONARY
    # out1 = []
    # [out1.append(x) for x in out if x not in out1]          #REMOVING DUPLICATES

    final_list = LoadDictionary()
    #REMOVING KEYWORDS USING REGEX FOR SPECIALCASE VOWELS
    performics_valuesReg = "|".join(final_list)
    performics_valuesReg = re.sub('a|á', "[aá]", performics_valuesReg)
    performics_valuesReg = re.sub('e|é', "[eé]", performics_valuesReg)
    performics_valuesReg = re.sub('i|í', "[ií]", performics_valuesReg)
    performics_valuesReg = re.sub('o|ó|ö|ő', "[oóöő]", performics_valuesReg)
    performics_valuesReg = re.sub('u|ú|ü|ű', "[uúüű]", performics_valuesReg)


    #KEEPING KEYWORDS THAT ARE NOT IN OUT LIST
    CopyL = []
    for x in values_list:
        z = re.match('('+ performics_valuesReg+')',x)
        y = re.match("(^(\d+|[a-z])$)",x)  #KEYWORDS THAT ARE JUST NUMBERS OR SINGLE ALPHABETS
        if not (z or y):
            CopyL.append(x)

    out1 = []
    [out1.append(x) for x in CopyL if x not in out1]

    #AGGREGATING MONTHLY SEARCH FOR NEW WORDS
    Searches_sum = []
    for word in out1:
        df1 =  df[df['Keyword Idea'].str.contains(word)]
        add = df1['Monthly Searches'].sum()
        Searches_sum.append(add)

    #print(len(Searches_sum))

    return out1, Searches_sum

if __name__ == "__main__":

    UC_List, Searches = UncategorisedKeywords()

    df = pd.DataFrame(list(zip(UC_List, Searches)), columns=['Uncategorised_Keywords', 'Aggregated_Monthly_Seach'])

    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts1=str(ts)
    df.to_excel(r'C:\Users\ashsingh42\Downloads\UC-List'+ts1+'.xlsx', index = False, header=True)

