from sec_xbrl.stock import Stock
import pandas as pd

def statement_to_df(statements):
    dfs = []
    for report in statements.reports :
        df_this_report = pd.DataFrame.from_dict(report.map, orient='index')
        df_this_report["label"] = df_this_report[0].apply(lambda x: x.label)
        df_this_report["value_in_millions"] = df_this_report[0].apply(lambda x: x.value/1000000)
        df_this_report["date"] = report.date
        df_this_report["months"] = report.months
        df_this_report.drop(columns=[0], inplace=True)
        df_this_report = df_this_report.reset_index()
        df_this_report.rename(columns={"index": "xbrl_tag"}, inplace=True)
        dfs.append(df_this_report)
    df = pd.concat(dfs)
    return df


def get_annual_statement(ticker="UNP", year=2022):
    #ticker="UNP"; year=2022
    stock = Stock(ticker)
    filing = stock.get_filing(period='annual', year=year)
    income_statements = filing.get_income_statements()
    cash_flows = filing.get_cash_flows()
    balance_sheets = filing.get_balance_sheets()
    #retained_earnings = filing.get_retained_earnings()

    df_income = statement_to_df(income_statements)
    df_income['statement'] = 'IncomeStatement'

    df_cash = statement_to_df(cash_flows)
    df_cash["statement"] = "CashFlowStatement"

    df_balance = statement_to_df(balance_sheets)
    df_balance["statement"]="BalanceSheet"

    #df_retained_earnings = statement_to_df(retained_earnings)
    #df_retained_earnings["statement"]="RetainedEarnings"
    #self = filing
    df_all = pd.concat([df_income, df_cash, df_balance])
    return df_all
