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

Output (Balance Sheet):

|    | xbrl_tag                                                              | label                                                                                                                                                   |   value_in_millions |
|---:|:----------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|
|  0 | us-gaap_CashAndCashEquivalentsAtCarryingValue                         | Cash and cash equivalents                                                                                                                               |                 960 |
|  1 | us-gaap_HeldToMaturitySecuritiesCurrent                               | Short-term investments (Note 13)                                                                                                                        |                  46 |
|  2 | us-gaap_AccountsReceivableNetCurrent                                  | Accounts receivable, net (Note 10)                                                                                                                      |                1722 |
|  3 | us-gaap_MaterialsSuppliesAndOther                                     | Materials and supplies                                                                                                                                  |                 621 |
|  4 | us-gaap_OtherAssetsCurrent                                            | Other current assets                                                                                                                                    |                 202 |
|  5 | us-gaap_AssetsCurrent                                                 | Total current assets                                                                                                                                    |                3551 |
|  6 | us-gaap_InvestmentsInAffiliatesSubsidiariesAssociatesAndJointVentures | Investments                                                                                                                                             |                2241 |
|  7 | us-gaap_PropertyPlantAndEquipmentNet                                  | Properties, net (Note 11)                                                                                                                               |               54871 |
|  8 | us-gaap_OperatingLeaseRightOfUseAsset                                 | Operating lease assets (Note 16)                                                                                                                        |                1787 |
|  9 | us-gaap_OtherAssetsNoncurrent                                         | Other assets                                                                                                                                            |                1075 |
| 10 | us-gaap_Assets                                                        | Total assets                                                                                                                                            |               63525 |
| 11 | us-gaap_AccountsPayableAndAccruedLiabilitiesCurrent                   | Accounts payable and other current liabilities (Note 12)                                                                                                |                3578 |
| 12 | us-gaap_LongTermDebtAndCapitalLeaseObligationsCurrent                 | Debt due within one year (Note 14)                                                                                                                      |                2166 |
| 13 | us-gaap_LiabilitiesCurrent                                            | Total current liabilities                                                                                                                               |                5744 |
| 14 | us-gaap_LongTermDebtAndCapitalLeaseObligations                        | Debt due after one year (Note 14)                                                                                                                       |               27563 |
| 15 | us-gaap_OperatingLeaseLiabilityNoncurrent                             | Operating lease liabilities (Note 16)                                                                                                                   |                1429 |
| 16 | us-gaap_DeferredIncomeTaxLiabilitiesNet                               | Deferred income taxes (Note 7)                                                                                                                          |               12675 |
| 17 | us-gaap_OtherLiabilitiesNoncurrent                                    | Other long-term liabilities                                                                                                                             |                1953 |
| 18 | us-gaap_Liabilities                                                   | Total liabilities                                                                                                                                       |               49364 |
| 19 | us-gaap_CommonStockValue                                              | Common shares, $2.50 par value, 1,400,000,000 authorized; 1,112,440,400 and 1,112,227,784 issued; 638,841,656 and 671,351,360 outstanding, respectively |                2781 |
| 20 | us-gaap_AdditionalPaidInCapital                                       | Paid-in-surplus                                                                                                                                         |                4979 |
| 21 | us-gaap_RetainedEarningsAccumulatedDeficit                            | Retained earnings                                                                                                                                       |               55049 |
| 22 | us-gaap_TreasuryStockValue                                            | Treasury stock                                                                                                                                          |              -47734 |
| 23 | us-gaap_AccumulatedOtherComprehensiveIncomeLossNetOfTax               | Accumulated other comprehensive loss (Note 9)                                                                                                           |                -914 |
| 24 | us-gaap_StockholdersEquity                                            | Total common shareholders' equity                                                                                                                       |               14161 |
| 25 | us-gaap_LiabilitiesAndStockholdersEquity                              | Total liabilities and common shareholders' equity                                                                                                       |               63525 |
|  0 | us-gaap_CashAndCashEquivalentsAtCarryingValue                         | Cash and cash equivalents                                                                                                                               |                1799 |
|  1 | us-gaap_HeldToMaturitySecuritiesCurrent                               | Short-term investments (Note 13)                                                                                                                        |                  60 |
|  2 | us-gaap_AccountsReceivableNetCurrent                                  | Accounts receivable, net (Note 10)                                                                                                                      |                1505 |
|  3 | us-gaap_MaterialsSuppliesAndOther                                     | Materials and supplies                                                                                                                                  |                 638 |
|  4 | us-gaap_OtherAssetsCurrent                                            | Other current assets                                                                                                                                    |                 212 |
|  5 | us-gaap_AssetsCurrent                                                 | Total current assets                                                                                                                                    |                4214 |
|  6 | us-gaap_InvestmentsInAffiliatesSubsidiariesAssociatesAndJointVentures | Investments                                                                                                                                             |                2164 |
|  7 | us-gaap_PropertyPlantAndEquipmentNet                                  | Properties, net (Note 11)                                                                                                                               |               54161 |
|  8 | us-gaap_OperatingLeaseRightOfUseAsset                                 | Operating lease assets (Note 16)                                                                                                                        |                1610 |
|  9 | us-gaap_OtherAssetsNoncurrent                                         | Other assets                                                                                                                                            |                 249 |
| 10 | us-gaap_Assets                                                        | Total assets                                                                                                                                            |               62398 |
| 11 | us-gaap_AccountsPayableAndAccruedLiabilitiesCurrent                   | Accounts payable and other current liabilities (Note 12)                                                                                                |                3104 |
| 12 | us-gaap_LongTermDebtAndCapitalLeaseObligationsCurrent                 | Debt due within one year (Note 14)                                                                                                                      |                1069 |
| 13 | us-gaap_LiabilitiesCurrent                                            | Total current liabilities                                                                                                                               |                4173 |
| 14 | us-gaap_LongTermDebtAndCapitalLeaseObligations                        | Debt due after one year (Note 14)                                                                                                                       |               25660 |
| 15 | us-gaap_OperatingLeaseLiabilityNoncurrent                             | Operating lease liabilities (Note 16)                                                                                                                   |                1283 |
| 16 | us-gaap_DeferredIncomeTaxLiabilitiesNet                               | Deferred income taxes (Note 7)                                                                                                                          |               12247 |
| 17 | us-gaap_OtherLiabilitiesNoncurrent                                    | Other long-term liabilities                                                                                                                             |                2077 |
| 18 | us-gaap_Liabilities                                                   | Total liabilities                                                                                                                                       |               45440 |
| 19 | us-gaap_CommonStockValue                                              | Common shares, $2.50 par value, 1,400,000,000 authorized; 1,112,440,400 and 1,112,227,784 issued; 638,841,656 and 671,351,360 outstanding, respectively |                2781 |
| 20 | us-gaap_AdditionalPaidInCapital                                       | Paid-in-surplus                                                                                                                                         |                4864 |
| 21 | us-gaap_RetainedEarningsAccumulatedDeficit                            | Retained earnings                                                                                                                                       |               51326 |
| 22 | us-gaap_TreasuryStockValue                                            | Treasury stock                                                                                                                                          |              -40420 |
| 23 | us-gaap_AccumulatedOtherComprehensiveIncomeLossNetOfTax               | Accumulated other comprehensive loss (Note 9)                                                                                                           |               -1593 |
| 24 | us-gaap_StockholdersEquity                                            | Total common shareholders' equity                                                                                                                       |               16958 |
| 25 | us-gaap_LiabilitiesAndStockholdersEquity                              | Total liabilities and common shareholders' equity                                                                                                       |               62398 |
