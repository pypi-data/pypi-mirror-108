import datetime as dt
import pandas as pd
from googlewrapper.connect import Connection
from numpy import nan


class GoogleSearchConsole:
    def __init__(self, auth = Connection().gsc()):
        self.auth = auth
        self._filter = None
        self._dims = ["page", "date"]
        self._site_list = None
        self._branded_dict = None
        self._s_date = dt.date.today() - dt.timedelta(days=7)
        self._e_date = dt.date.today()

        self._current_site = None

    def set_sites(self, site_list):
        """
        site_list: list of sites we want to pull from GSC API
            type: list

        if not called, self._site_list = None from __init__
        """
        self._site_list = site_list

    def set_dimensions(self, dimensions):
        """
        d: what we want to break it down by
            type: list
            options: ['page','date','query', 'device','country']
        """
        self._dims = dimensions

    def set_filters(self, filter_object):
        """
        filters_list: list of filters formated as GSC requires
        example_filter = {
                        "dimension": string,
                        "operator": string,
                        "expression": string
                        }
        """
        self._filter = filter_object

    def set_date(self,date):
        """
        date: calls the start and end date as the same day
        """
        self._s_date = date
        self._e_date = date

    def set_start_date(self, start_date):
        """
        start_date: the starting point (inclusive) 
                        for the API pull
            type: dt.datetime or dt.date

        declared by __init__ to be 7 days ago
        """
        self._s_date = start_date

    def set_end_date(self, end_date):
        """
        end_date: the ending point (inclusive) 
                    for the API pull
            type: dt.datetime or dt.date

        declared by __init__ to be today
        """
        self._e_date = end_date

    def set_branded(self, branded_dictionary):
        """
        pass in a dictionary object

        keys are GSC url properties
        values are a list of branded strings
        """
        self._branded_dict = branded_dictionary

    def all_sites(self, site_filters=None):
        """
        return a list of all verfied sites that you have in GSC.
        
        It will give you all by default, but if you pass in
        a list of words it will only return
        those properties that contain your set of words
        """
        site_list = self.auth.sites().list().execute()
        clean_list = [
            s["siteUrl"]
            for s in site_list["siteEntry"]
            if s["permissionLevel"] != "siteUnverifiedUser"
            and s["siteUrl"][:4] == "http"
        ]
        if site_filters is None:
            return clean_list
        elif isinstance(site_filters, list):
            return [s for s in clean_list if any(xs in s for xs in site_filters)]


    def build_request(self, agg_type="auto", limit=25000, start_row=0, pull=True):
        """
        https://developers.google.com/webmaster-tools/
        search-console-api-original/v3/searchanalytics/query

        agg_type: auto is fine can be byPage or byProperty
            defaults "auto"
        limit: number of rows to return
            defaults 25000
        start_row: where to start, if need more than 25,000
            defaults 0
        pull: if we want to call the api and pull data
            defaults True
        """

        request_data = {
            "startDate": self._s_date.strftime("%Y-%m-%d"),
            "endDate": self._e_date.strftime("%Y-%m-%d"),
            "dimensions": self._dims,
            "aggregationType": agg_type,
            "rowLimit": limit,
            "startRow": start_row,
            "dimensionFilterGroups": [{"filters": self._filter}],
        }
        if pull:
            return self.execute_request(request_data)
        else:
            return request_data

    def execute_request(self, request):
        """
        Executes a searchAnalytics.query request.

        property_uri: The site or app URI to request data for.
        request: The request to be executed.

        Returns an array of response rows.
        """
        return (
            self.auth.searchanalytics()
            .query(siteUrl=self._current_site, body=request)
            .execute()
        )

    def clean_resp(self, data):
        """
        Takes raw response, and cleans the data into a pd.Dataframe
        """
        df = pd.DataFrame(data["rows"])
        df.index.name = "idx"
        keys = df["keys"].apply(pd.Series)
        keys.columns = self._dims
        df = df.merge(keys, how="left", on="idx")
        df.drop(columns="keys", inplace=True)
        df.columns = df.columns.str.capitalize()

        # branded check
        if isinstance(self._branded_dict, dict) and "Query" in df.columns:
            df["Branded"] = self.check_branded(df["Query"])

        # convert to datetime
        if 'Date' in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])

        df[["Clicks", "Impressions"]] = df[["Clicks", "Impressions"]].astype(int)

        return df

    def check_branded(self, query_list):
        """
        Takes in a list of queries.

        Returns as pd.Series of Bool if the query is branded
        """
        branded_list = self._branded_dict[self._current_site]
        if branded_list in [nan,[],['']]:
            return False
        return pd.Series(query_list).str.contains(
            "|".join(branded_list), na=False
        )

    def get_data(self):
        """
        will loop through the site list,
        grab the data from the api,
        clean it,
        and add it to a dictionary with the site as the key
        after completion
        returns the created dictionary of pd.DataFrame objects
        """
        data = {}
        for x in self._site_list:
            self._current_site = x
            start = 0
            row_limit = 25000
            temp_df = pd.DataFrame()
            while True:
                try:
                    temp_df = temp_df.append(
                        self.clean_resp(
                            self.build_request(limit=row_limit, start_row=start)
                        )
                    )
                except:
                    break
                start += row_limit

            data[x] = temp_df

        return data
