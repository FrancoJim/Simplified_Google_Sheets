#!/usr/bin/env python3

import datetime
import logging as l

import gspread
from oauth2client.service_account import ServiceAccountCredentials

GGLJSONAUTH = ''


def dict_to_spreadsheet_format(data, include_header=False):
    '''
    Converts a list of nested dictionaries into spreadsheet format.
    Retains order of first listed dictionary.

    :param data: List of nested dictionaries.
    :param include_header: bool: If True, adds column headers to first line using dictionary keys.
    :return: Lists nested in list. i.e. [["Header 1", "Header 2", ...], ["Column 1", "Column 1", ...]]
    '''
    if isinstance(data, (list,)):
        try:
            headers = [k.__str__() for k in data[0].keys()]

            X = [headers] if include_header else []

            for i in data:
                X.append([i[h].__str__() for h in headers])

        except:
            # todo: Need logging and action.
            pass

        return X
    else:
        w = 'Input must be in a list of nested dictionaries.'
        l.warning(w)
        return [[w]]


def datetime_to_string(dt_obj):
    '''
    Reformats datetime obj to string format.

    :param dt_obj: datetime object with date value.
    :return: Defined datetime in string format.
    '''

    if isinstance(dt_obj, datetime.datetime):
        try:
            dt_obj = datetime.datetime.strftime(dt_obj, "%Y-%m-%d %H:%M:%S %z")
        except Exception as e:
            l.error(str(e))

    return dt_obj


def import_to_gsheets(workbook, spreadsheet, data, ggluser=None):
    """
    Create Google Sheets workbook > new/open spreadsheet > Clear old data, if exists > enter data.

    :param workbook: String of Google Sheets' Workbook name and location. i.e. "Workbook_name"
    :param spreadsheet: String of Spreadsheet name to enter data.
    :param data: Nested lists within list (data for Spreadsheet). i.e. [ [ 'Cell A1', 'Cell A2', ... ], [ 'Cell B1', 'Cell B2', ... ] ]
    :return: 0: successful; 1: successful.
    Data is also entered into defined Google Sheet.

    """
    l.info("Starting Google Sheet Importing process.")
    l.info("Authorizing Google User")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GGLJSONAUTH, scope)
    g = gspread.authorize(creds)
    l.info("Opening Workbook {0}".format(workbook))
    try:
        sh = g.open(workbook)
        l.info("Workbook opened.")
    except gspread.exceptions.SpreadsheetNotFound:
        sh = g.create(workbook)

    if ggluser != None:
        l.info("Sharing document to {0}".format(ggluser))
        sh.share(ggluser, perm_type='user', role='owner')

    if data.__len__() > 0:
        try:
            l.info("Opening Spreadsheet {0}".format(spreadsheet))
            sp_sheet = sh.worksheet(spreadsheet)
            sp_sheet.clear()
            sp_sheet.resize(data.__len__(), cols=max(data[0], key=len).__len__())

        except Exception as e:
            l.error(str(e))
            l.info("{0} does not exist. Creating Spreadsheet {0}".format(spreadsheet))
            sh.add_worksheet(spreadsheet, rows=data.__len__(), cols=max(data[0], key=len).__len__())
            sp_sheet = sh.worksheet(spreadsheet)

        try:
            data = balance_rows(data)
            l.info("Add lines to Google Sheets")
            outpt = sp_sheet.range(1, 1, data.__len__(), max(data[0], key=len).__len__())
            x = -1
            for i in data:
                for d in i:
                    x += 1
                    outpt[x].value = d
            return outpt

            sp_sheet.update_cells(cell_list=outpt)
            return 0
        except Exception as e:
            l.error(str(e))
            return 1


def balance_rows(data):
    '''
    Adds empty str variables to nested lists so nested lists have same number of iterations.
    :param data:
    :return:
    '''
    payload = []

    if isinstance(data, (list,)):
        l.info(type(data))

        for i in data:
            t = i
            x = []

            if i.__len__() < max(data, key=len).__len__():
                l.info("Balance rows")
                x = [""] * (max(data, key=len).__len__() - i.__len__())
            payload.append(t + x)
    else:
        l.warning("Item is not a list. Please check data and try again.")

    return payload
