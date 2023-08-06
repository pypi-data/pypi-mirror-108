# ClipperData python API

import requests
import json
import pandas as pd
from colorama import Fore, Back, Style, init
init(strip = False)
import pprint
import datetime as dt
from typing import List, Dict
pp = pprint.PrettyPrinter(indent=4)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", dest = "host", type = str,
        default = "https://api.clipperdata.com/")
args, unknown = parser.parse_known_args()

class Jencoder(json.JSONEncoder):
    """ manages json enconding of date, datetime objects """

    def default(self, obj):
        if isinstance(obj, (dt.datetime, dt.date)):
            return "'" + obj.strftime("%Y-%m-%d") + "'"

class Clipper():
    """ container class for all functionality related to python access to the
    ClipperData API """

    def __init__(self, username, password, url = args.host):
        print((f"{Back.CYAN}{Fore.BLACK}{Style.BRIGHT}ClipperData LLC Python API v 07.26. "
               f"Please visit www.clipperdata.com for more information{Style.RESET_ALL}"))
        print()
        self.username = username
        self.password = password
        self.url = url
        self.session = requests.Session()
        self.token = ""
        self.jencoder = Jencoder()
        if not self._check_server_accessible(url):
            raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Cannot access url '{url}'{Style.RESET_ALL}")
        hlp = self.help()
        if "error" in hlp:
            self._error_print(hlp.get("detail"))
            raise Exception((f"{Fore.YELLOW}{Style.BRIGHT}Query could not get help data structure"
                    f"{Style.RESET_ALL}"))
        else:
            print("credentials validated")

    def _check_server_accessible(self, url):
        try:
            requests.head(url)
            success = True
        except:
            success = False
        return success

    def help(self):
        content = self._req("V1/help")
        if "error" in content:
            return {"error": "error getting help",
                    "detail": content}
        return content

    def auth(self):
        payload = {"username": self.username, "password": self.password}
        try:
            ss = self.session.post(self.url + "token", data = payload)
            cred = json.loads(ss.content)
            self.token = cred.get("access_token", "")
        except:
            raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Could not connect to server{Style.RESET_ALL}")

    def _get_and_parse(self, url):
        headers = {"Authorization": "Bearer " + str(self.token)}
        try:
            data = self.session.get(self.url + url, headers = headers)
        except Exception as e:
            return {"error": "error getting data",
                    "detail": {"url": url},
                    "exception": e}
        try:
            content = json.loads(data.content)
        except:
            return {"error": "error parsing data",
                    "detail": {"url": url, "data": data}}
        return content

    def _error_print(self, err):
        print(f"{Fore.RED}{Style.NORMAL}{err['error']}{Back.RED}{Fore.WHITE}")
        pp.pprint(err.get("detail", err))
        print(Fore.RED + Style.RESET_ALL)

    def _req(self, url):
        content = self._get_and_parse(url)
        if content.get("detail", "") == "Could not validate credentials":
            self.auth()
            content = self._get_and_parse(url)
            if content.get("detail", "") == "Could not validate credentials":
                content = {"error": "Could not validate credentials",
                           "detail": "Two attempts made"}
        return content

    def _type_translator(self, pgtype):
        pgtype = pgtype.upper()
        if pgtype in ["TEXT", "STR", "CHARACTER"]:
            return str
        if pgtype in ["INTEGER", "BIGINT"]:
            return int
        if pgtype in ["FLOAT", "DOUBLE PRECISION", "NUMERIC"]:
            return float
        if pgtype in ["DATE", "TIMESTAMP WITHOUT TIME ZONE", "TIMESTAMP"]:
            return dt.datetime
        if pgtype in ["BOOLEAN"]:
            return bool
        return None


    def _validate_groupby(self, glist, field_types):
        glist_error = {"error": ("The groupby clause must be a list of strings of the form"
                              " [field_name, operator, aggregation_field], "
                              " where the operator is one of"
                              " 'SUM', 'AVG', 'MIN', 'MAX', 'COUNT'"),
                       "detail": glist}
        if not isinstance(glist, list):
            return glist_error
        if len(glist) != 3:
            return glist_error
        if not tuple((isinstance(x, str) for x in glist)) == (True, True, True):
            print(tuple((isinstance(x, str) for x in glist)))
            return glist_error
        if (not glist[0] in field_types) or (not glist[2] in field_types):
            return {"error": (f"Specified field '{glist[0]}' is not in table. "
                               "Please consult the fields() method for more information"),
                    "detail": glist}
        if not glist[1] in ["SUM", "AVG", "MIN", "MAX", "COUNT"]:
            return glist_error
        target_type = self._type_translator(field_types[glist[0]])
        if not isinstance(glist[2], target_type):
            return {"error": (f"comparator type {glist[2]} "
                        f"must be the same as target field type {target_type}"),
                    "detail": glist}
        return {}

    def _validate_where(self, wdict, field_types):
        condict = {"eq": "=", "ne": "<>", "gt": ">", "lt": "<",
                   "gte": ">=", "lte": "<=", "like": "like"}
        if not isinstance(wdict, dict):
            return {"error": "at least one where clause is not a dict", "detail": wdict}
        if len(wdict) != 2:
            return {"error": ("where clause must have two entries, first is field name, "
                "second is conjunction '', 'AND', or 'OR'"),
                "detail": wdict}
        if not ("conjunction" in wdict):
            return {"error": "Missing AND or OR conjunction", "detail": wdict}
        if not wdict["conjunction"] in ["", "AND", "OR"]:
            return {"error": "conjunction can only be '', 'AND', or 'OR'", "detail": wdict}
        target_field_l = list(wdict.keys())
        target_field_l.remove("conjunction")
        target_field = target_field_l[0]
        if not (target_field in field_types):
            return {"error": (f"Specified field '{target_field}' is not in table. "
                               "Please consult the fields() method for field information"),
                    "detail": wdict}
        comparator_dict = wdict[target_field]
        if not isinstance(comparator_dict, dict):
            return {"error": "comparands must be a dict", "detail": wdict}
        if not len(comparator_dict) == 1:
            return {"error": "comparand dict must have only one entry", "detail": wdict}
        if not list(comparator_dict.keys())[0] in condict:
            return {"error": "comparator must be one of " + " ,".join(condict.keys),
                    "detail": wdict}
        target_type = self._type_translator(field_types[target_field])
        if not isinstance(list(comparator_dict.values())[0], target_type):
            return {"error": (f"comparator type {list(comparator_dict.values())[0].__class__} "
                        f"must be the same as target field type {target_type}"),
                    "detail": wdict}
        return {}

    def fields(self):
        hlp = self.help()
        if "error" in hlp:
            self._error_print(hlp)
            raise Exception((f"{Fore.YELLOW}{Style.BRIGHT}Query could not get help data structure"
                    f"{Style.RESET_ALL}"))
        result = {t: [(f["name"], self._type_translator(f["type"]), f["help"]) \
                for f in hlp["tables"][t]["table_fields"]] \
                for t in hlp["tables"]}
        return result

    def query(self,
              table: str,
              fields: List[str] = [],
              where: List[dict] = [],
              orderby: dict = None,
              batch_size: int = 150000,
              offset: int = 0,
              max_update_date: str = None,
              silent: bool = False,
              debug: bool = False,
              active_records: bool = True):

        hlp = self.help()
        if "error" in hlp:
            self._error_print(hlp)
            raise Exception((f"{Fore.YELLOW}{Style.BRIGHT}Query could not get help data structure"
                    f"{Style.RESET_ALL}"))
        qs = "V1/query/"


        # validate table
        if not isinstance(table, str):
            self._error_print({"error": "Table name must be a string",
                               "detail": table})
            raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Bad table name{Style.RESET_ALL}")
        if table in hlp["tables"]:
            actual_table_name = hlp["tables"][table]["table_name"]
            report_id = str(hlp["tables"][table]["report_id"])
            qs = qs + f"{table}/?actual_table_name={actual_table_name}&report_id={report_id}"
        else:
            raise Exception((f"{Fore.YELLOW}{Style.BRIGHT}table {table} is not in the help['tables'] "
                    f"dictionary{Style.RESET_ALL}"))
        # fields
        if not isinstance(fields, list):
            self._error_print({"error": "Fields must be contained in list",
                               "detail": fields})
            raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Bad fields{Style.RESET_ALL}")
        if not all([isinstance(x, str) for x in fields]):
            self._error_print({"error": "All field entries must be strings",
                               "detail": fields})
            raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Bad fields{Style.RESET_ALL}")

        all_table_fields = [x["name"] for x in hlp["tables"][table]["table_fields"]]
        all_table_fields_admin = [x["name"]  for x in hlp["tables"][table]["table_fields"] \
                if x["category"] == "Administrative"]
        all_table_types = [x["type"] for x in hlp["tables"][table]["table_fields"]]
        all_table_allowed_vals = [x["allowed_values"] for x in hlp["tables"][table]["table_fields"]]
        field_types = dict(zip(all_table_fields, all_table_types))
        good_fields = list(filter(lambda x: x in all_table_fields, fields))
        if len(good_fields) < len(fields):
            bad_fields = set(fields) - set(good_fields)
            print((f"{Fore.MAGENTA}These fields are not in the table and were ignored: "
                  f"{' '.join(bad_fields)}{Style.RESET_ALL}"))
        if len(fields) == 0:
            good_fields = all_table_fields # if no fields passed, assume all fields
        good_fields = [x for x in good_fields if x not in all_table_fields_admin] # remove admin fields
        good_fields = good_fields + all_table_fields_admin # force them back in at the end
        qs = qs + "&fields=" + "&fields=".join(good_fields)

        # where
        if not isinstance(where, list):
            raise Exception((f"{Fore.YELLOW}{Style.BRIGHT}Where clauses must be contained in a list"
                        f"{Style.RESET_ALL}"))
        for w in where:
            try:
                val_res = self._validate_where(w, field_types)
            except:
                val_res = {"error": "Could not validate where clause",
                           "detail": w}
            if not "error" in val_res:
                qs = qs + "&where=" + self.jencoder.encode(w)
            else:
                self._error_print(val_res)
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}where field clause error{Style.RESET_ALL}")
        if len(where) > 0:
            if not [w["conjunction"] for w in where][0] == "":
                self._error_print({"error": "first conjunction must be empty string ''", "detail": where})
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}where field clause error{Style.RESET_ALL}")

        # orderby
        if orderby is not None:
            orderby_error = {"error": ("orderby must be a dict in the form "
                                       "{field: 'ASC'} or {field: 'DESC'}"),
                             "detail": orderby}
            if not isinstance(orderby, dict):
                self._error_print(orderby_error)
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}order by clause error{Style.RESET_ALL}")
            if len(orderby) != 1:
                self._error_print(orderby_error)
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}order by clause error{Style.RESET_ALL}")
            if not list(orderby.keys())[0] in field_types:
                self._error_print({"error": (f"orderby field '{list(orderby.keys())[0]}' not found "
                                              "in field list. "
                                              "Use the fields() method for field information"),
                                   "detail": orderby})
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}order by clause error{Style.RESET_ALL}")
            if not list(orderby.values())[0] in ["ASC", "DESC"]:
                self._error_print(orderby_error)
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}order by clause error{Style.RESET_ALL}")
            qs = qs + "&orderby=" + self.jencoder.encode(orderby)

        # update
        if max_update_date:
            if not isinstance(max_update_date, str):
                self._error_print({"error": "max_update_date must be a string",
                                  "detail": max_update_date})
                raise Exception("max_update_date error")
            qs = qs + f"&max_update_date={max_update_date}"

        # this is Python
        qs = qs + "&endpoint=Python"

        # is debug mode on
        if debug:
            qs = qs + "&debug=1"

        # is active_records mode on
        if active_records:
            qs = qs + "&active_records=1"

        # run the query
        do_offset = offset
        limit = batch_size
        results = []
        query_time = dt.datetime.utcnow()
        batch_time = dt.datetime.utcnow()
        max_update_date = ""
        while True:
            qs_send = qs + f"&offset={do_offset}&limit={limit}"
            if not silent:
                print(f"{Fore.GREEN}{qs_send}{Style.RESET_ALL}")
            content = self._req(qs_send)
            if len(content.get("data", [])) == 0:
                break
            if "error" in content:
                self._error_print(content)
                raise Exception(f"{Fore.YELLOW}{Style.BRIGHT}Error retreiving data{Style.RESET_ALL}")
            results = results + content["data"]
            if content["max_update_date"] > max_update_date:
                max_update_date = content["max_update_date"]
            if not silent:
                print((f"{Fore.BLUE}Received {len(results)} rows, "
                       f" {len(content.get('data', []))}-row batch time: {dt.datetime.utcnow() - batch_time}, "
                       f" {len(results)}-row total time: {dt.datetime.utcnow() - query_time}"
                       f" {Style.RESET_ALL}"))
            batch_time = dt.datetime.utcnow()
            do_offset = do_offset + batch_size
        if len(results) > 0:
            pd_results = pd.DataFrame(results, columns = content["fields"]).infer_objects()
        else:
            pd_results = pd.DataFrame([])
        return {"data": pd_results, "last_update": max_update_date}

query_examples = [
    # This pulls the IMO & Load Date fields for all crude records where Load Date is in the current
    # month (greater than or equal to first of current month)
    {"table": "Crude",
     "fields": ["IMO", "Load Date"],
     "where": [{ "Load Date": {"gte": dt.datetime((dt.datetime.today()).year,
         (dt.datetime.today()).month, 1)}, "conjunction": "" }]},

    # This pulls all fields for all active crude records with a Load Date greater than 2020-1-1,
    # and then orders the result by Load Date ascending
    {"table": "Crude", "fields": [],
    "where": [{"Load Date": {"gt": dt.datetime(2020, 1, 1)}, "conjunction": ""}],
    "active_records": {True},
    "orderby": {"Load Date": "ASC"}},

    # US Crude Exports in Sep 2020
    {"table": "Crude",
    "where": [
        {"Load Country": {"eq": "UNITED STATES"}, "conjunction": ""},
        {"Offtake Country": {"ne": "UNITED STATES"}, "conjunction": "AND"},
        {"Load Date": {"gte": dt.datetime(2020, 9, 1)}, "conjunction": "AND"},
        {"Load Date": {"lt": dt.datetime(2020, 10, 1)}, "conjunction": "AND"}]},

    # US crude imports in wk ending 2020-9-18
    {"table": "Crude",
    "where": [
        {"Grade Country": {"ne": "UNITED STATES"}, "conjunction": ""},
        {"Vessel Flag": {"ne": "UNITED STATES"}, "conjunction": "AND"},
        {"Offtake Country": {"eq": "UNITED STATES"}, "conjunction": "AND"},
        {"Offtake Date": {"gte": dt.datetime(2020, 9, 12)}, "conjunction": "AND"},
        {"Offtake Date": {"lt": dt.datetime(2020, 9, 19)}, "conjunction": "AND"}]},

    # Arab Gulf crude loadings since Sep 2020
    {"table": "Crude",
    "fields": [],
    "where": [
        {"Load Region": {"eq": "ARAB GULF"}, "conjunction": ""},
        {"Load Date": {"gte": dt.datetime(2020, 9, 1)}, "conjunction": "AND"}]},

    # US east coast gasoline imports in Aug 2020
    {"table": "Clean Products",
    "where": [
        {"Load Country": {"ne": "UNITED STATES"}, "conjunction": ""},
        {"Commodity": {"eq": "GASOLINE"}, "conjunction": "AND"},
        {"Offtake Area": {"eq": "US Atlantic Coast"}, "conjunction": "AND"},
        {"Offtake Date": {"gte": dt.datetime(2020, 8, 1)}, "conjunction": "AND"},
        {"Offtake Date": {"lt": dt.datetime(2020, 9, 1)}, "conjunction": "AND"}]},

    # US distillate exports in wk 38 2020
    {"table": "Clean Products",
    "where": [
        {"Load Country": {"eq": "UNITED STATES"}, "conjunction": ""},
        {"Grade Type": {"eq": "Diesel"}, "conjunction": "AND"},
        {"Offtake Country": {"ne": "UNITED STATES"}, "conjunction": "AND"},
        {"Load Trading Year": {"eq": 2020}, "conjunction": "AND"},
        {"Load Trading Week": {"eq": 38}, "conjunction": "AND"}]},
]


def sample(username, password):
    clipper = Clipper(username, password)
    #print(cl.query("Crude", fields = ["IMO", "Barrels", "AIS Timestamp"]))
    hlp = clipper.help()
    # note usage of optional batch_size variable here
    data0 = clipper.query(**query_examples[0], batch_size = 1000)
    print(data0["data"])
    input("Press Enter to run next query")

    data1 = clipper.query(**query_examples[1])
    print(data1["data"])
    input("Press Enter to run next query")

    data2 = clipper.query(**query_examples[2])
    print(data2["data"])
    input("Press Enter to run next query")

    data3 = clipper.query(**query_examples[3])
    print(data3["data"])
    input("Press Enter to run next query")

    data4 = clipper.query(**query_examples[4])
    print(data4["data"])
    input("Press Enter to run next query")

    data5 = clipper.query(**query_examples[5])
    print(data5["data"])
    input("Press Enter to run next query")

    data6 = clipper.query(**query_examples[6])
    print(data6["data"])
    print("last update:", data6["last_update"])

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    sample(username, password)
