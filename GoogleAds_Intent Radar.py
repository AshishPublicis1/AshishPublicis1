#!/usr/bin/env python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example generates keyword ideas from a list of seed keywords."""

import argparse
import sys
import datetime
import pandas as pd
from openpyxl import load_workbook
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Location IDs are listed here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
# and they can also be retrieved using the GeoTargetConstantService as shown
# here: https://developers.google.com/google-ads/api/docs/targeting/location-targeting
_DEFAULT_LOCATION_IDS = ["2348"]  # location ID for New York, NY
# A language criterion ID. For example, specify 1000 for English. For more
# information on determining this value, see the below link:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
_DEFAULT_LANGUAGE_ID = "1024"  # language ID for English


# [START generate_keyword_ideas]
def main(
    client, customer_id, location_ids, language_id, keyword_texts, page_url
):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = (
        client.enums.KeywordPlanCompetitionLevelEnum
    )
    keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    )
    location_rns = _map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(
        language_id
    )

    # Either keywords or a page_url are required to generate keyword ideas
    # so this raises an error if neither are provided.
    if not (keyword_texts or page_url):
        raise ValueError(
            "At least one of keywords or page URL is required, "
            "but neither was specified."
        )

    # Only one of the fields "url_seed", "keyword_seed", or
    # "keyword_and_url_seed" can be set on the request, depending on whether
    # keywords, a page_url or both were passed to this function.
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network

    # To generate keyword ideas with only a page_url and no keywords we need
    # to initialize a UrlSeed object with the page_url as the "url" field.
    if not keyword_texts and page_url:
        request.url_seed.url = page_url

    # To generate keyword ideas with only a list of keywords and no page_url
    # we need to initialize a KeywordSeed object and set the "keywords" field
    # to be a list of StringValue objects.
    if keyword_texts and not page_url:
        request.keyword_seed.keywords.extend(keyword_texts)

    # To generate keyword ideas using both a list of keywords and a page_url we
    # need to initialize a KeywordAndUrlSeed object, setting both the "url" and
    # "keywords" fields.
    if keyword_texts and page_url:
        request.keyword_and_url_seed.url = page_url
        request.keyword_and_url_seed.keywords.extend(keyword_texts)

    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )
    allkeywords=[]
    monthlysearch=[]
    competition=[]
    for idea in keyword_ideas:
        competition_value = idea.keyword_idea_metrics.competition.name
        #appending results
        allkeywords.append(idea.text)
        monthlysearch.append(idea.keyword_idea_metrics.avg_monthly_searches)
        competition.append(competition_value)

    df= pd.DataFrame(data=zip(allkeywords, monthlysearch, competition), columns=['Keyword Idea', 'Monthly Searches', 'Competition'])

    return df


    # [END generate_keyword_ideas]


def map_keywords_to_string_values(client, keyword_texts):
    keyword_protos = []
    for keyword in keyword_texts:
        string_val = client.get_type("StringValue")
        string_val.value = keyword
        keyword_protos.append(string_val)
    return keyword_protos


def _map_locations_ids_to_resource_names(client, location_ids):
    """Converts a list of location IDs to resource names.
    Args:
        client: an initialized GoogleAdsClient instance.
        location_ids: a list of location ID strings.
    Returns:
        a list of resource name strings using the given location IDs.
    """
    build_resource_name = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path
    return [build_resource_name(location_id) for location_id in location_ids]


def Seed_Combination():
    df2 = pd.read_excel(r'C:\Users\ashsingh42\Downloads\book2.xlsx')
    df = pd.read_excel(r'C:\Users\ashsingh42\Downloads\book3.xlsx', header=None)
    data_dict = df2.to_dict("list")

    for k, d in data_dict.items():
        L2 = [x for x in d if pd.isnull(x) == False]
        data_dict[k] = L2

    KSeed = []
    for index, row in df.iterrows():
        Combo = row[0].split(' + ')
        L1 = data_dict[Combo[0]]
        L2 = data_dict[Combo[1]]
        for i in L1:
            for j in L2:
                temp = i + " " + j;
                KSeed.append(temp)
    return KSeed



if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.

    credentials = {
        "developer_token": "LgFhvleyZL83VBhvMbBo1w",
        "refresh_token": "1//0gQ7Ns87CNpBGCgYIARAAGBASNwF-L9IrEsQ4TembVHuX1yAzOjx16wlyTaerS-GxyqOcFGi8sYEzwZEmZ-BJZa-th3-2U9VaXgQ",
        "client_id": "66023082163-p2nuu87in3il0kd5d6uc3o272lhuseb5.apps.googleusercontent.com",
        "client_secret": "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",
        "use_proto_plus": "True"
    }

    googleads_client = GoogleAdsClient.load_from_dict(credentials)

    customer_id = "2225872227"
    developer_token = "LgFhvleyZL83VBhvMbBo1w"
    refresh_token = "1//0gQ7Ns87CNpBGCgYIARAAGBASNwF-L9IrEsQ4TembVHuX1yAzOjx16wlyTaerS-GxyqOcFGi8sYEzwZEmZ-BJZa-th3-2U9VaXgQ",
    client_id = "66023082163-p2nuu87in3il0kd5d6uc3o272lhuseb5.apps.googleusercontent.com"
    client_secret = "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"
    language_id = "1024"
    location_ids = ["2348"]

    i=0
    DF=pd.DataFrame()
    Keywords = Seed_Combination()
    for kwords in Keywords:
        i=i+1
        print("Working for -" + kwords)
        keyword_texts = [kwords]
        result=main (googleads_client, customer_id, location_ids, language_id,keyword_texts,None)
        DF = pd.concat([DF, result], ignore_index=True)
        if i%2==0:
            time.sleep(3)



    DF.to_excel (r'C:\Users\ashsingh42\Downloads\export_dataframe1.xlsx', index = False, header=True)








