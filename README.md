Forked from `https://github.com/farhadab/sec-edgar-financials`

Testing running the code only

# To installl
`git clone "https://github.com/reeyarn/sec_xbrl"`


# Example:



```
import pandas as pd
from sec_xbrl.get_statement import  get_annual_statement
from sec_xbrl.filing import Filing

# Customize cache settings
from pathlib import Path
Filing.CACHE_DIR = Path('sec_reports')  # Change cache directory
Filing.CACHE_VALIDITY_DAYS = 7  # Change cache expiration to 7 days


df_all = get_annual_statement(ticker="UNP", year=2022)

df_balance = df_all[df_all["statement"]=="BalanceSheet"]
df_balance[["xbrl_tag",	"label",	"value_in_millions"]].head(60)

df_balance.to_csv("UNP_BalanceSheet_2022.csv", index=False)

df_spf = df_all[df_all["statement"]=="IncomeStatement"]
df_spf[["xbrl_tag",	"label",	"value_in_millions"]].head(60)
df_spf.to_csv("UNP_IncomeStatement_2022.csv", index=False)

```

