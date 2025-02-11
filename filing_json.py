'''
Logic related to the handling of filings and documents
'''
from sec_xbrl.requests_wrapper import GetRequest
from sec_xbrl.document import Document
from sec_xbrl.sgml import Sgml
from sec_xbrl.dtd import DTD
from sec_xbrl.financials import get_financial_report
from datetime import datetime

from thefuzz import fuzz

FILING_SUMMARY_FILE = 'FilingSummary.xml'




class Statements:
    # used in parsing financial data; these are the statements we'll be parsing
    # To resolve "could not find anything for ShortName..." error, likely need
    # to add the appropriate ShortName from the FilingSummary.xml here.
    # TODO: perhaps add guessing/best match functionality to limit this list
    income_statements = ['consolidated statements of income',
                    'consolidated statements of operations',
                    'consolidated statement of earnings',
                    'condensed consolidated statements of income (unaudited)',
                    'condensed consolidated statements of income',
                    'condensed consolidated statements of operations (unaudited)',
                    'condensed consolidated statements of operations',
                    'condensed consolidated statement of earnings (unaudited)',
                    'condensed consolidated statement of earnings',
                    'condensed statements of income',
                    'condensed statements of operations',
                    'condensed statements of operations and comprehensive loss'
                    ]
    balance_sheets = ['consolidated balance sheets',
                    'consolidated statement of financial position',
                    'condensed consolidated statement of financial position (current period unaudited)',
                    'condensed consolidated statement of financial position (unaudited)',
                    'condensed consolidated statement of financial position',
                    'condensed consolidated balance sheets (current period unaudited)',
                    'condensed consolidated balance sheets (unaudited)',
                    'condensed consolidated balance sheets',
                    'condensed balance sheets'
                    ]
    cash_flows = ['consolidated statements of cash flows',
                    'condensed consolidated statements of cash flows (unaudited)',
                    'condensed consolidated statements of cash flows',
                    'condensed statements of cash flows'
                    ]
    retained_earnings = ['consolidated retained earnings',
                    'consolidated statement of retained earnings',
                    'condensed consolidated statement of retained earnings',
                    'condensed statement of retained earnings'
                    'condensed consolidated statement of retained earnings (unaudited)',
                    "statement of changes in common shareholders' equity",
                    "consolidated statement of changes in common shareholders' equity",
                    ]

    all_statements = income_statements + balance_sheets + cash_flows + retained_earnings


from datetime import datetime
from pathlib import Path
import json
import os



class Filing:
    STATEMENTS = Statements()
    CACHE_DIR = Path('edgar_cache/filings')
    CACHE_VALIDITY_DAYS = 30  # Cache files for 30 days by default
    sgml = None

    def __init__(self, url, company=None):
        self.url = url
        self.company = company
        self.documents = {}
        
        # Create cache directory if it doesn't exist
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Load from cache or fetch and cache
        self._load_or_fetch_filing()

    def _get_cache_filename(self):
        """Generate a safe filename for caching based on the URL"""
        # Convert URL to a safe filename by replacing unsafe characters
        safe_filename = self.url.replace('/', '_').replace(':', '_').replace('.', '_')
        return self.CACHE_DIR / f"{safe_filename}.json"

    def _is_cache_valid(self, cache_path):
        """Check if cache file exists and is not too old"""
        if not cache_path.exists():
            return False
        
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age = datetime.now() - file_time
        return age.days < self.CACHE_VALIDITY_DAYS

    def _save_to_cache(self, cache_data):
        """Save filing data to cache"""
        cache_path = self._get_cache_filename()

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, default=str) # Use default=str to handle non-serializable objects
        except TypeError as e:
            print(f"Error saving to cache: {e}") # Log the error and potentially remove the incomplete cache file
            try:
                os.remove(cache_path)
            except OSError:
                pass # Ignore if file doesn't exist
        print(f'Saved filing to cache: {cache_path}')

    def _extract_document_text(self, document, document_raw):
        """Extract or generate the text content of a document."""
        # Implement your logic here to extract the text content from document_raw
        # This will depend on the structure of your Document objects and the raw data
        # Example:
        try:
            return document_raw.text # If document_raw has a text attribute
        except AttributeError:
            # Implement other extraction methods based on document_raw structure
            # For instance, if it's a list of strings:
            try:
                return "".join(document_raw)
            except TypeError:
                return "" # Or handle other cases as needed. Return an empty string if extraction fails.


    def _load_from_cache(self, cache_path):
        """Load filing data from cache"""
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            
        self.text = cache_data['text']
        self.date_filed = datetime.strptime(cache_data['date_filed'], '%Y-%m-%d')
        
        # Reconstruct documents from cached data
        for doc_filename, doc_data in cache_data['documents'].items():
            document = Document(None)  # Create empty document
            document.__dict__.update(doc_data)  # Update with cached data
            self.documents[doc_filename] = document

        print(f'Loaded filing from cache: {cache_path}')

    def _fetch_and_process_filing(self):
        """Fetch filing from URL and process it"""
        print(f'Fetching filing from {self.url}')
        response = GetRequest(self.url).response
        self.text = response.text

        print('Processing SGML at ' + self.url)
        dtd = DTD()
        sgml = Sgml(self.text, dtd)
        self.sgml = sgml

        # Process documents
        for document_raw in sgml.map.get(dtd.sec_document.tag, {}).get(dtd.document.tag, []):  # Handle potential missing tags
            try:
                document = Document(document_raw)
                # Ensure document.text is extracted or set appropriately
                if not hasattr(document, 'text'):
                    document.text = self._extract_document_text(document, document_raw) # New method to handle text extraction
                self.documents[document.filename] = document
            except Exception as e:
                print(f"Error processing document: {e}") # Log the error and continue

        # Process filing date
        acceptance_datetime_element = sgml.map[dtd.sec_document.tag][dtd.sec_header.tag][dtd.acceptance_datetime.tag]
        acceptance_datetime_text = acceptance_datetime_element[:8]
        self.date_filed = datetime.strptime(acceptance_datetime_text, '%Y%m%d')

        # Cache the results
        cache_data = {
            'text': self.text,
            'date_filed': self.date_filed.strftime('%Y-%m-%d'),
            'documents': {
                filename: {
                    'filename': doc.filename,
                    'type': doc.type,
                    'description': doc.description,
                    'text': doc.text
                }
                for filename, doc in self.documents.items()
            }
        }
        self._save_to_cache(cache_data)

    def _load_or_fetch_filing(self):
        """Load filing from cache if available, otherwise fetch and cache it"""
        cache_path = self._get_cache_filename()
        
        if self._is_cache_valid(cache_path):
            try:
                self._load_from_cache(cache_path)
                return
            except Exception as e:
                print(f'Error loading from cache: {e}. Fetching fresh data...')
        
        self._fetch_and_process_filing()

    def get_statements(self):
        """Get financial statements from the filing"""
        return self.STATEMENTS.process(self)







    def get_financial_data(self):
        '''
        This is mostly just for easy QA to return all financial statements
        in a given file, but the intended workflow is for he user to pick
        the specific statement they want (income, balance, cash flows)
        '''
        return self._get_financial_data(self.STATEMENTS.all_statements, True)



    def _get_financial_data(self, statement_short_names, get_all):
        '''
        Returns financial data used for processing 10-Q and 10-K documents
        '''
        financial_data = []

        for names in self._get_statement(statement_short_names):
            short_name = names[0]
            filename = names[1]
            #print('Getting financial data for {0} (filename: {1})'.format(short_name, filename))
            financial_html_text = self.documents[filename].doc_text.data

            financial_report = get_financial_report(self.company, self.date_filed, financial_html_text)

            if get_all:
                financial_data.append(financial_report)
            else:
                return financial_report

        return financial_data



    def _get_statement(self, statement_short_names):
        '''
        Return a list of tuples of (short_names, filenames) for
        statement_short_names in filing_summary_xml
        '''
        statement_names = []

        if FILING_SUMMARY_FILE in self.documents:
            filing_summary_doc = self.documents[FILING_SUMMARY_FILE]
            filing_summary_xml = filing_summary_doc.doc_text.xml

            for short_name in statement_short_names:
                filename = self.get_html_file_name(filing_summary_xml, short_name)
                if filename is not None:
                    statement_names += [(short_name, filename)]
        # else:
        #     print('No financial documents in this filing')

        if len(statement_names) == 0:
            print('No financial documents could be found. Likely need to \
            update constants in edgar.filing.Statements.')
            
        return statement_names



    @staticmethod
    def get_html_file_name(filing_summary_xml, report_short_name):
        '''
        Return the HtmlFileName (FILENAME) of the Report in FilingSummary.xml
        (filing_summary_xml) with ShortName in lowercase matching report_short_name
        e.g.
             report_short_name of consolidated statements of income matches
             CONSOLIDATED STATEMENTS OF INCOME
        #report_short_name = balance_sheets[1]
        '''
        reports = filing_summary_xml.find_all('report')
        best_match = {
            'ratio': 75,
            'filename': None
        }        
        for report in reports:
            short_name = report.find('shortname')
            #print(short_name)
            if short_name is None:
                #print('The following report has no ShortName element')
                #print(report)
                continue
            # otherwise, get the text and keep procesing
            short_name = short_name.get_text().lower()

            # we want to make sure it matches, up until the end of the text
            this_ratio = fuzz.ratio(short_name, report_short_name.lower())
            if this_ratio > best_match['ratio']:
                best_match['ratio'] = this_ratio
                best_match['filename'] = report.find('htmlfilename').get_text()

        if best_match['ratio'] > 80: # this condition need to fuzzy 
            filename = best_match['filename']
            return filename
        else:
            #print(f'could not find anything for ShortName {report_short_name.lower()}')
            return None



    def get_income_statements(self):
        return self._get_financial_data(self.STATEMENTS.income_statements, False)

    def get_balance_sheets(self):
        return self._get_financial_data(self.STATEMENTS.balance_sheets, False)

    def get_cash_flows(self):
        return self._get_financial_data(self.STATEMENTS.cash_flows, False)
    def get_retained_earnings(self):
        return self._get_financial_data(self.STATEMENTS.retained_earnings, False)
