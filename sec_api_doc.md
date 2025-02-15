
# EDGAR Application Programming Interfaces

https://www.sec.gov/search-filings/edgar-application-programming-interfaces

June 6, 2024

data.sec.gov" was created to host RESTful data Application Programming Inte=
rfaces (APIs) delivering JSON-formatted data to external customers and to w=
eb pages on SEC.gov. These APIs do not require any authentication or API ke=
ys to access.

Currently included in the APIs are the submissions history by filer and =
the XBRL data from financial statements (forms 10-Q, 10-K,8-K, 20-F, 40-F, =
6-K, and their variants).

The JSON structures are updated throughout the day, in real time, as sub=
missions are disseminated.

In addition, a bulk ZIP file is available to download all the JSON struc=
tures for an API. This ZIP file is updated and republished nightly at =
approximately 3:00 a.m. ET.

## data.sec.gov/submissions/

Each entity=E2=80=99s current filing history is available at the followi=
ng URL:

* https://data.sec.gov/submissions/CIK**######=
  ####**.json

Where the **##########** is the entity=E2=80=99s 10-digit Central Ind=
ex Key (CIK), including leading zeros.

This JSON data structure contains metadata such as current name, former =
name, and stock exchanges and ticker symbols of publicly-traded companies. =
The object=E2=80=99s property path contains at least one year=E2=80=99s of =
filing or to 1,000 (whichever is more) of the most recent filings in a comp=
act columnar data array. If the entity has additional filings, files will c=
ontain an array of additional JSON files and the date range for the filings=
each one contains.

## XBRL data APIs

Extensible Business Markup Language (XBRL) is an XML-based format for re=
porting financial statements used by the SEC and financial regulatory agenc=
ies across the world. XBRL, in a separate XML file or more recently embedde=
d in quarterly and annual HTML reports as inline XBRL, was first requi=
red by the SEC in 2009. XBRL facts must be associated for a standard US-GAA=
P or IFRS taxonomy. Companies can also extend standard taxonomies with thei=
r own custom taxonomies.

The following XBRL APIs aggregate facts from across submissions tha=
t

1. Use a non-custom taxonomy (e.g. us-gaap, ifrs-full, dei, or srt)
2. Apply to the entire filing entity

This ensures that facts have a consistent context and meaning across com=
panies and between filings and are comparable between companies and across =
time.

## data.sec.gov/api/xbrl/companyconcept/

The company-concept API returns all the XBRL disclosures from a single c=
ompany (CIK) and concept (a taxonomy and tag) into a single JSON file, with=
a separate array of facts for each units on measure that the company has c=
hosen to disclose (e.g. net profits reported in U.S. dollars and in Canadia=
n dollars).

* https://data.sec.gov/api/xbrl/companyconcept/=
  CIK##########/us-gaap/AccountsPayableCurrent.json

## data.sec.gov/api/xbrl/companyfacts/

This API returns all the company concepts data for a company into a sing=
le API call:

* https://data.sec.gov/api/xbrl/companyfacts/CI=
  K##########.json

## data.sec.gov/api/xbrl/frames/

The *xbrl/frames* API aggregates one fact for each reporting entity=
that is last filed that most closely fits the calendrical period requested=
. This API supports for annual, quarterly and instantaneous data:

* https://data.sec.gov/api/xbrl/frames/us-gaap/=
  AccountsPayableCurrent/USD/CY2019Q1I.json

Where the units of measure specified in the XBRL contains a numerator an=
d a denominator, these are separated by =E2=80=9C-per-=E2=80=9D such a=
s =E2=80=9CUSD-per-shares=E2=80=9D. Note that the default unit in XBRL is =
=E2=80=9Cpure=E2=80=9D.

The period format is CY#### for annual data (duration 365 days +/- 30 da=
ys), CY####Q# for quarterly data (duration 91 days +/- 30 days), and CY####=
Q#I for instantaneous data. Because company financial calendars can start a=
nd end on any month or day and even change in length from quarter to quarte=
r to according to the day of the week, the frame data is assembled by the d=
ates that best align with a calendar quarter or year. Data users should be =
mindful different reporting start and end dates for facts contained in a fr=
ame.

## CORS

data.sec.gov does not support Cross Origin Resource Scripting (CORS). Au=
tomated access must comply with [SEC.gov=E2=80=99s Privacy and Security Policy](3D%22https%3A//www.sec.gov/privacy.htm%22%3D), as described in the &nb=
sp; [Developer F=
AQ](3D%22https%3A//www.sec.gov/os/webmaster-faq#developers").

## Bulk data

The most efficient means to fetch large amounts of API data is the bulk =
archive ZIP files, which are recompiled nightly.

* The [companyfacts.zip file](3D%22http%3A//www.sec.gov/Archives/edgar/daily-index/xbrl/comp%3D) contains all the data from the XBRL=
  Frame API and the XBRL Company Facts API

[https://www.sec.gov/Archi=
ves/edgar/daily-index/xbrl/companyfacts.zip](3D%22https%3A//www.sec.gov/%3D)

* The [submission.zip file](3D%22https%3A//www.sec.gov/Archives/edgar/daily-index/bulkdata%3D) contains the public EDGAR filing =
  history for all filers from the Submissions API

[https://www.sec.gov/Ar=
chives/edgar/daily-index/bulkdata/submissions.zip](3D%22https%3A//www.sec.gov/%3D)

## Update Schedule

The APIs are updated in real-time as filings are disseminated. The *su=
bmissions* API is updated with a typical processing delay of less than a=
second; the *xbrl* APIs are updated with a typical processing delay o=
f under a minute. However these processing delays may be longer during peak=
filing times.

## Release notes

Check back as we make updates.

## We want to hear from you!

Send your recommendations regarding how we are implementing our APIs to&=
nbsp;webmaster@sec.gov.

Please note we cannot provide technical support for developing or debugg=
ing scripted downloading processes.

## Programmatic API Access

See the [Developer FAQ](3D%22https%3A//www.sec.gov/os/webmaster-faq#developers"=) on how to comply with the SEC's Web=
Site [Privacy and Security Policy](3D%22https%3A//www.sec.gov/privacy.htm#security").

=20
=20

Last Reviewed or Updated: June 17, 2024

