from .classes.parser import *

# as needed for heartburn | prn for heartburn | p.r.n. heartburn | prn heartburn
# asNeededBoolean = true
# TODO: replace wildcard indication search with INDICATIONS list from normalize.py
class IndicationParser(Parser):
    parser_type = 'indication'
    pattern = r'(?P<as_needed>as needed for|as needed|p\.r\.n\. for|prn for|p\.r\.n\.|prn)(?:\s+(?P<indication>.*))?'
    match_keys = ['as_needed', 'indication', 'indication_text_start', 'indication_text_end', 'indication_text']
    def normalize_match(self, match):
        as_needed = 1
        indication_text = match.group('indication')
        indication = (get_indication(indication_text) if indication_text != None else indication_text)
        indication_text_start, indication_text_end = match.span()
        indication_text = match.group(0)
        return self.generate_match({'as_needed': as_needed, 'indication': indication, 'indication_text_start': indication_text_start, 'indication_text_end': indication_text_end, 'indication_text': indication_text})

"""
# NOTE: Dosage does not capture indication unless it is a PRN indication
NOTE: this should be "reasonCode"
{	
// for nausea and vomiting (exclude prn before 'for', and exclude numbers immediately after 'for')
// asNeededBoolean = false
pattern: new RegExp('(?<!(?:as needed|p.r.n.|prn)\s*)(?:for\s+(?!(?:' + regexRange + '))((?:\w|\s)+))', 'ig'),
standardize: (match: any[]) => {
    var reasons = match[1] ? match[1].split(' ') : null;
    // TODO: match each word against a database of diagnoses (ICD-10 / UMLS?)
    // https://documentation.uts.nlm.nih.gov/rest/search/
    if (reasons) { 
        var indicationWords: string[] = [];
        var indicationSearch: string = '';
        reasons.forEach(r => {
            indicationWords.push(r);
            indicationSearch = indicationWords.join(' ');
            console.log(indicationSearch);
            // TODO do a UMLS search with the indicationSearch keyword, each time
            // adding it to an array of search results, afterwards selecting the
            // best match. Maybe limit to 5 words?
        });
    }
    return {
        reasonCode: reasons
    }
}

"""

parsers = [
    IndicationParser()
]