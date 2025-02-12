from sec_xbrl.stock import Stock
import pandas as pd
import traceback

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
    #ticker="ORCL"; year=2022
    #ticker = "ACN"; year=2023; get_annual_statement(ticker, year)
    stock = Stock(ticker)
    filing = stock.get_filing(period='annual', year=year); #self = filing
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

if __name__ == "__main__":
    #import importlib ; import sec_xbrl.get_statement; importlib.reload(sec_xbrl.get_statement)
    from sec_xbrl.get_statement import get_annual_statement
    import pandas as pd
    errors = []
    #ABT likely has xbrl error ; 
    #MMM likely too
    for ticker in ["MSFT", "AAPL", "MMM", "WMT", "ACN",  "AMZN", "NFLX", "ORCL", "QCOM"]:
        for year in range(2019, 2023):
            try:
                    df_all = get_annual_statement(ticker=ticker, year=year)
                #print(df_all.head())
            except Exception as e:
                this_error = f"Error for {ticker} in {year}: {e}"
                this_error_dict = {"ticker": ticker, "year": year, "error": this_error}
                errors.append(this_error_dict)
                print(this_error)
                traceback.print_exc(limit = 10)

    errors

    df_errors = pd.DataFrame.from_records(errors, index=["ticker", "year"]).reset_index()
    df_errors
