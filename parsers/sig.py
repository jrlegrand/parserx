from .classes.parser import *
from . import method, dose, strength, route, frequency, when, duration, indication
import csv

# TODO: need to move all this to the main app and re-purpose the sig.py parser

# a work in progress...
# read csv: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# general dataframe: https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# dataframe to csv: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
# csv to sql: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
class SigParser(Parser):
    parsers = {
        'method': method.parsers,
        'dose': dose.parsers,
        'strength': strength.parsers,
        'route': route.parsers,
        'frequency': frequency.parsers,
        'when': when.parsers,
        'duration': duration.parsers,
        'indication': indication.parsers,
    }
    # TODO: make this match_keys assignment more elegant
    #match_keys = ['original_sig_text'] + ['sig_text', 'sig_readable'] + method.parsers[0].match_keys + dose.parsers[0].match_keys + strength.parsers[0].match_keys + route.parsers[0].match_keys + frequency.parsers[0].match_keys + when.parsers[0].match_keys + duration.parsers[0].match_keys + indication.parsers[0].match_keys
    match_keys = ['sig_text', 'sig_readable'] + method.parsers[0].match_keys + dose.parsers[0].match_keys + strength.parsers[0].match_keys + route.parsers[0].match_keys + frequency.parsers[0].match_keys + when.parsers[0].match_keys + duration.parsers[0].match_keys + indication.parsers[0].match_keys
    parser_type = 'sig'

    def get_normalized_sig_text(self, sig_text):
        # standardize to lower case
        sig_text = sig_text.lower()
        # remove:
        # . if not bordered by a number (i.e. don't want to convert 2.5 to 25 or 0.5 to 05)
        # : if not bordered by a number (i.e. not 5:00 or 1:10000)
        # , ; # * " ' ( ) \t [ ] :
        sig_text = re.sub(r'(?:(?<![0-9])\.(?![0-9])|,|;|#|\*|\"|\'|\(|\)|\t|\[|\]|(?<![0-9]):(?![0-9]))', '', sig_text)
        # remove duplicate spaces, and in doing so, also trim whitespaces from around sig
        sig_text = ' '.join(sig_text.split())
        return sig_text

    def get_readable(self, method=None, dose=None, strength=None, route=None, frequency=None, when=None, duration=None, indication=None):
        method = method if method else ''
        dose = dose if dose else ''
        strength = strength if strength else ''
        route = route if route else ''
        frequency = frequency if frequency else ''
        when = when if when else ''
        duration = duration if duration else ''
        indication = indication if indication else ''

        if dose != '' and strength != '':
            strength = '(' + strength + ')'
        sig_elements = [method, dose, strength, route, frequency, when, duration, indication]
        # join sig elements with spaces
        readable = ' '.join(sig_elements)
        # remove duplicate spaces, and in doing so, also trim whitespaces from around sig
        # this accounts for empty sig elements
        readable = ' '.join(readable.split())
        return readable

    def parse(self, sig_text):
        match_dict = dict(self.match_dict)
        #match_dict['original_sig_text'] = sig_text
        sig_text = self.get_normalized_sig_text(sig_text)
        match_dict['sig_text'] = sig_text
        for parser_type, parsers in self.parsers.items():
            matches = []
            
            for parser in parsers:
                match = parser.parse(sig_text)
                if match:
                    matches += match
            
            if len(matches) > 1:
                # TODO: this is where we can put logic to determine the best dose / frequency / etc
                match = matches[0]
                for k, v in match.items():
                    match_dict[k] = v
            elif len(matches) == 1:
                match = matches[0]
                for k, v in match.items():
                    match_dict[k] = v
            #elif len(matches) == 0:
        match_dict['sig_readable'] = self.get_readable(
            method=match_dict['method_readable'],
            dose=match_dict['dose_readable'],
            strength=match_dict['strength_readable'],
            route=match_dict['route_readable'],
            frequency=match_dict['frequency_readable'],
            when=match_dict['when_readable'],
            duration=match_dict['duration_readable'],
            indication=match_dict['indication_readable']
        )
        # calculate admin instructions based on leftover pieces of sig
        # would need to calculate overlap in each of the match_dicts
        # in doing so, maybe also return a map of the parsed parts of the sig for use in frontend highlighting
        # i.e. 0,4|5,12|18,24
        return match_dict

    # infer method, dose_unit, and route from NDC or RXCUI
    def infer(self, ndc=None, rxcui=None):
        sig_elements = ['method', 'dose_unit', 'route']
        inferred = dict.fromkeys(sig_elements)
        for sig_element in sig_elements:
            inferred[sig_element] = infer_sig_element(sig_element, ndc, rxcui)
        return inferred

    # parse a csv
    def parse_sig_csv(self):
        file_path='parsers/csv/'
        file_name='drx_1000'
        csv_columns = self.match_keys
        # create an empty list to collect the data
        parsed_sigs = []
        # open the file and read through it line by line
        with open(file_path + file_name + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                # calculate total number of rows for progress bar
                row_total = sum(1 for row in csv_reader)
                row_count = 0
                # reset csv file to beginning
                csv_file.seek(0)
                for row in csv_reader:
                    row_count += 1
                    print_progress_bar(row_count, row_total)
                    sig = row[0]
                    parsed_sig = self.parse(sig)
                    parsed_sigs.append(parsed_sig.copy())

        output_file_path = 'parsers/csv/output/'
        try:
            file_suffix = '_parsed.csv'
            with open(output_file_path + file_name + file_suffix, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()
                for parsed_sig in parsed_sigs:
                    writer.writerow(parsed_sig)
        except IOError:
            print("I/O error")

        return parsed_sigs

    # parse and validate a csv
    def parse_validate_sig_csv(self):
        file_path='parsers/csv/'
        file_name='sig_prd_20200707'
        # create an empty list to collect the data
        parsed_sigs = []
        # open the file and read through it line by line
        with open(file_path + file_name + '.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                 # calculate total number of rows for progress bar
                row_total = sum(1 for row in csv_reader)
                row_count = 0
                # reset csv file to beginning
                csv_file.seek(0)
                # define fields that should all be equal to count as a match between two versions of sigs
                important_fields = ['method', 'dose', 'dose_max', 'dose_unit', 'strength', 'strength_max', 'strength_unit', 'route', 'frequency', 'frequency_max', 'period', 'period_max', 'period_unit', 'time_duration', 'time_duration_unit', 'day_of_week', 'time_of_day', 'when', 'offset', 'bounds', 'count', 'duration', 'duration_max', 'duration_unit', 'as_needed', 'indication']
                count_good = 0
                count_bad = 0
                count_neutral = 0
                # skip first row because it's just the headers from the database
                next(csv_reader)
                for row in csv_reader:
                    # initialize a dictionary to store differences
                    different_fields = dict.fromkeys(['different_' + field for field in important_fields])
                    row_count += 1
                    print_progress_bar(row_count, row_total)
                    sig = row['sig_text']
                    parsed_sig = self.parse(sig)
                    for field in important_fields:
                        # compare string versions of both fields because database CSV stores as string, but parser evaluates as integer for some items
                        # 'NULL' == None because database returns empty values as NULL, but parser returns blanks
                        different_fields['different_' + field] = 0 if str(parsed_sig[field]) == str(row[field]) or (parsed_sig[field] == None and row[field] == 'NULL') else 1
                        
                    # apply "new" prefix to keys in recently parsed sig
                    # this is so the output csv can differentiate between current, new, and different components
                    for key in list(parsed_sig.keys()):
                        parsed_sig['new_' + key] = parsed_sig.pop(key)
                    
                    if sum(different_fields.values()) == 0:
                        count_good += 1
                    else:
                        count_bad += 1
                    # https://www.geeksforgeeks.org/python-sum-list-of-dictionaries-with-same-key/
                    parsed_sigs.append({**row, **parsed_sig, **different_fields})

                print('Count good: {}, Count bad: {}'.format(count_good, count_bad))
        
        # use the combined dict's keys as csv columns
        csv_columns = parsed_sigs[0].keys()
        output_file_path = 'parsers/csv/output/'
        try:
            file_suffix = '_validated_parsed.csv'
            with open(output_file_path + file_name + file_suffix, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()
                for parsed_sig in parsed_sigs:
                    writer.writerow(parsed_sig)
        except IOError:
            print("I/O error")

        return parsed_sigs


def print_progress_bar (iteration, total, prefix = 'progress:', suffix = 'complete', decimals = 1, length = 50, fill = '█', print_end = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s (n = %s)' % (prefix, bar, percent, suffix, iteration), end = print_end)
    if iteration == total: 
        print()

#print(SigParser().infer(ndc='68788640709'))
parsed_sigs = SigParser().parse_sig_csv()
#parsed_sigs = SigParser().parse_validate_sig_csv()
#print(parsed_sigs)

# NOTE: if no dose found, check for numbers immediately following method (i.e. take 1-2 po qid)
# NOTE: if indication overlaps something else, then end indication just before the next thing starts
# NOTE: don't forget about the actual sig text and the sequence
# NOTE: split sig by "then" occurrences for sequence
# NOTE: Github has pieces that could make a FHIR converter