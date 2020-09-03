from .classes.parser import *

class DoseParser(Parser):
    parser_type = 'dose'
    match_keys = ['dose', 'dose_max', 'dose_unit', 'dose_text_start', 'dose_text_end', 'dose_text']
    def normalize_pattern(self):
        dose_patterns = []
        for n, p in DOSE_UNITS.items():
            # add the name of the pattern to the list of matched patterns
            p.append(n)
            # and join them with a | character
            # and add them to the dose_patterns array
            dose_patterns.append(r'|'.join(p))        
        pattern = re.compile(r'(?<!no more than)(?<!do not exceed)(?<!not to exceed)(?<!\bnmt)(?<!\bnte)\s*\(*\**(?P<dose>' + RE_RANGE + r')\**\)*(\s?\(.*\)\s?)?(?:\s*(?P<dose_unit>' + r'|'.join(dose_patterns) + r'))', flags = re.I)
        return pattern
    def normalize_match(self, match):
        dose_range = split_range(match.group('dose'))
        print(dose_range)
        dose, dose_max = dose_range
        dose_unit = get_normalized(DOSE_UNITS, match.group('dose_unit'))
        dose_text_start, dose_text_end = match.span()
        dose_text = match[0]
        return self.generate_match({'dose': dose, 'dose_max': dose_max, 'dose_unit': dose_unit, 'dose_text_start': dose_text_start, 'dose_text_end': dose_text_end, 'dose_text': dose_text})

parsers = [
    DoseParser()
]

#print(DoseParser().parse('take one capsule prn nausea for 5 days'))

# TODO: write this after route and frequency parsers are complete
def parse_lone_numeric_dose(sig):
    return 0
"""
// handle sigs like 1 qd or 1 po qd or one by mouth daily or one daily
// in these cases, we know the 'value' (i.e. 1 or one) but not the 'dose.unit' (i.e. tablet, mL, etc)
parseLoneNumericDose(sig: string): void {
    var regexRange = this.normalize.getRegexRange();
    var frequency = this.frequency.getFrequency();
    var route = this.route.getRoute();
    var index: number[] = [];
    
    frequency.map(f => index.push(f.match.index));
    route.map(r => index.push(r.match.index));
    
    // this pattern is similar to others, but doesn't list a 'unit' in the standardize function
    var p: any = {
        pattern: new RegExp('(?<!(?:no more than|do not exceed|not to exceed|\\bnmt|\\bnte)\\s*)\\**(' + regexRange + ')\\**\\s*', 'ig'),
        standardize: (match: any[]) => {
            var value = match[1].replace(/(?:to|or)/ig, '-').replace(/\s/g, '').split('-');
            var dose = value.length > 1 ? { doseRange: { low: { value: value[0] }, high: { value: value[1] } } } : { doseQuantity: { value: value[0] } }; 
            return dose;
        }
    };

    var match: any;
    while (match = p.pattern.exec(sig)) {
        // if the last character of the match is just before the start of a route or frequency
        // then add it to the list of doses
        if (index.indexOf(match.index + match[0].length) > -1) {
            this.dose.push({
                match: match,
                standardized: p.standardize(match)
            });
        }
    }
}
"""






"""
'(?:extended release|delayed release|buccal|sustained release buccal|chewable|disintegrating|enteric coated|extended release enteric coated|sublingual|vaginal)?\s*(?:oral)?\s*tablet': [],
'spray': [],
'actuation': [],
'puff': [],
'drop': [],
'bar': [],
'capsule': [],
'pad\b': [],
'patch': [],
'tape': [],
'gum': [],
'gel': [],
'lozenge': [],
'strip': [],
'film': [],
'tab(?:s)?\b': [],
'cap\b': [],
'stick'
"""