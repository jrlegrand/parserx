import collections
import re
from fractions import Fraction

RE_WRITTEN_NUMBERS = r'one(?:\s|-)?(?:quarter|half)|quarter|half|one point (?:one|two|three|four|five|six|seven|eight|nine)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty(?:\s|-)?(?:one|two|three|four|five|six|seven|eight|nine)|twenty|thirty(?:\s|-)?five|thirty'
#one (?:and |& )one(?:-|\s)half| 

# NOTE: keep the x-y at the beginning and x at the end so that it finds the x-y first without stopping
# (
#   (
#     (WRITTEN_NUMBER OR 1.5 OR 1/2)
#     TO
#     (WRITTEN_NUMBER OR 1.5 OR 1/2) 
#   )
#   OR (1.5 OR 1/2)
#   OR WRITTEN_NUMBER
# )
RE_RANGE = r'(?:(?:' + RE_WRITTEN_NUMBERS + r'|(?:\d*(?:\.|/))?\d+)(?:\s*(?:to|-|or|/|&|and)\s*)(?:' + RE_WRITTEN_NUMBERS + r'|(?:\d*(?:\.|/))?\d+)|(?:\d*(?:\.|/))?\d+|(?:' + RE_WRITTEN_NUMBERS + r'))'

RE_DAYS_OF_WEEK = r'monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon\b|tue\b|tues\b|wed\b|thu\b|thur\b|thurs\b|fri\b|sat\b|sun\b|m\b|tu\b|w\b|th\b|t\b|f\b|sa\b|su\b|s\b|mwf'
 
"""
  TODO: make all of the ac / pc / hs / etc
	https://www.hl7.org/fhir/valueset-event-timing.html
	Code	System	Display	Definition
	MORN	http://hl7.org/fhir/event-timing	Morning	event occurs during the morning
	AFT	http://hl7.org/fhir/event-timing	Afternoon	event occurs during the afternoon
	EVE	http://hl7.org/fhir/event-timing	Evening	event occurs during the evening
	NIGHT	http://hl7.org/fhir/event-timing	Night	event occurs during the night
	
	PHS	http://hl7.org/fhir/event-timing	After Sleep	event occurs [offset] after subject goes to sleep
	HS	http://hl7.org/fhir/v3/TimingEvent	HS	Description: Prior to beginning a regular period of extended sleep (this would exclude naps). Note that this might occur at different times of day depending on a person's regular sleep schedule.
	WAKE	http://hl7.org/fhir/v3/TimingEvent	WAKE	Description: Upon waking up from a regular period of sleep, in order to start regular activities (this would exclude waking up from a nap or temporarily waking up during a period of sleep) Usage Notes: e.g. Take pulse rate on waking in management of thyrotoxicosis. Take BP on waking in management of hypertension Take basal body temperature on waking in establishing date of ovulation
	
	C	http://hl7.org/fhir/v3/TimingEvent	C	Description: meal (from lat. ante cibus)
	CM	http://hl7.org/fhir/v3/TimingEvent	CM	Description: breakfast (from lat. cibus matutinus)
	CD	http://hl7.org/fhir/v3/TimingEvent	CD	Description: lunch (from lat. cibus diurnus)
	CV	http://hl7.org/fhir/v3/TimingEvent	CV	Description: dinner (from lat. cibus vespertinus)
	
	AC	http://hl7.org/fhir/v3/TimingEvent	AC	before meal (from lat. ante cibus)
	ACM	http://hl7.org/fhir/v3/TimingEvent	ACM	before breakfast (from lat. ante cibus matutinus)
	ACD	http://hl7.org/fhir/v3/TimingEvent	ACD	before lunch (from lat. ante cibus diurnus)
	ACV	http://hl7.org/fhir/v3/TimingEvent	ACV	before dinner (from lat. ante cibus vespertinus)
	
	PC	http://hl7.org/fhir/v3/TimingEvent	PC	after meal (from lat. post cibus)
	PCM	http://hl7.org/fhir/v3/TimingEvent	PCM	after breakfast (from lat. post cibus matutinus)
	PCD	http://hl7.org/fhir/v3/TimingEvent	PCD	after lunch (from lat. post cibus diurnus)
	PCV	http://hl7.org/fhir/v3/TimingEvent	PCV	after dinner (from lat. post cibus vespertinus)
"""
"""
	TODO: associate these common codings with each structured frequency
	https://www.hl7.org/fhir/valueset-timing-abbreviation.html
	Code	Display	Definition
	BID	BID	Two times a day at institution specified time
	TID	TID	Three times a day at institution specified time
	QID	QID	Four times a day at institution specified time
	AM	AM	Every morning at institution specified times
	PM	PM	Every afternoon at institution specified times
	QD	QD	Every Day at institution specified times
	QOD	QOD	Every Other Day at institution specified times
	Q4H	Q4H	Every 4 hours at institution specified times
	Q6H	Q6H	Every 6 Hours at institution specified times
"""
# pattern: new RegExp('(with|before|after)\s*(breakfast|lunch|dinner|meals|each meal)', 'ig'),	

# NOTE: periodUnit 'day' should include pretty much all of 'when' array
# for FHIR conversion: https://www.hl7.org/fhir/valueset-units-of-time.html
PERIOD_UNIT = {
  'day': [ 'daily', 'dialy', 'nightly', 'days', 'day', r'\bd\b', 'morning', 'morn', 'am', 'afternoon', 'aft', 'pm', 'evening at bedtime', 'bedtime', 'evening', 'eve', 'night', 'hs' ],
  'week': [ 'weekly', 'weeks', 'week', 'wks', 'wk', r'\bw\b' ],
  'month': [ 'monthly', 'months', 'month', 'mon', 'mo' ],
  'hour': [ 'hourly', 'hours', 'hour', 'hrs', 'hr', r'\bh\b' ],
  'minute': [ 'minutes', 'minute', 'mins', 'min', r'\bm\b' ],
  'second': [ 'seconds', 'second', 'secs', 'sec', r'\bs\b' ],
  'year': [ 'yearly', 'years', 'year', 'yrs', 'yr', r'\by\b' ],
}

# for FHIR conversion: https://www.hl7.org/fhir/valueset-days-of-week.html
DAY_OF_WEEK = {
  'monday': [ 'monday', 'mon', 'mo', 'm' ],
  'tuesday': [ 'tuesday', 'tues', 'tue', 'tu' ],
  'wednesday': [ 'wednesday', 'weds', 'wed', 'wd', 'w' ],
  'thursday': [ 'thursday', 'thurs', 'thu', 'th' ],
  'friday': [ 'friday', 'fri', 'fr', 'f' ],
  'saturday': [ 'saturday', 'sat', 'sa' ],
  'sunday': [ 'sunday', 'sun', 'su' ],
}
 
#(?:with|\bc\.|before|\ba|\ba\.|after|\bp|\bp\.|in the|at|every)
WHEN = {
  'in the morning': [ r'(?:in the|every|each)\s?(?:morn(?:ing)?|a\.m\.|am)', 'a.m.', r'\bam\b', r'\bqam\b' ],
  'in the afternoon': [ r'(?:in the|every|each)\s?(?:aft(?:ernoon)?|p\.m\.|pm)', r'\bqpm\b' ],
  'in the evening at bedtime': [r'(?:in the|every)\s?evening at bedtime'],
  'in the evening': [ r'(?:in the|every|each)\s?eve(?:ning)?' ],
  'at night': [ r'(?:in the|at|every|each)\s?night', 'nightly' ],
  'at bedtime': [ r'(?:in the|at|every|each)\s?bedtime', r'\bqhs\b', r'q\.h\.s\.', 'bedtime', r'\bhs\b' ],
  'with meal': [ r'(?:with|each|every|at)?\s?meal(?:s)?', r'c\.c\.', r'\bcc\b' ],
  'with breakfast': [ r'(?:with|each|every|at)? breakfast' ],
  'with lunch': [ r'(?:with|each|every|at)?\s?lunch', r'\bcd\b', r'c\.d\.' ],
  'with dinner': [ r'(?:with|each|every|at)?\s?dinner', r'\bcv\b', r'c\.v\.' ],		
  'before meal': [ r'before meal(?:s)?', r'\bac\b', r'a\.c\.' ],
  'before breakfast': [ 'before breakfast', r'\bacm\b', r'a\.c\.m\.' ],
  'before lunch': [ 'before lunch', r'\bacd\b', r'a\.c\.d\.' ],
  'before dinner': [ 'before dinner', r'\bacv\b', r'a\.c\.v\.' ],
  'after meal': [ r'after meal(?:s)?', r'\bpc\b', r'p\.c\.' ],
  'after breakfast': [ 'after breakfast', r'\bpcm\b', r'p\.c\.m\.' ],
  'after lunch': [ 'after lunch', r'\bpcd\b', r'p\.c\.d\.' ],
  'after dinner': [ 'after dinner', r'\bpcv\b', r'p\.c\.v\.' ],
}

METHODS = {
  'swish and swallow': [],
  'dilute': [],
  'inject': [],
  'wash': [],
  'sprinkle': [],
  'apply': [],
  'administer': [],
  'dissolve': [],
  'shampoo': [],
  'inhale': [],
  'insert': [],
  'use': [],
  'push': [],
  'give': [],
  'take': [r'\btk\b'],
  'swallow': [],
  'instill': [],
  'chew': [],
  'swish': [],
  'suck': [],
  'sniff': [],
  'place': [],
  'spray': [],
  'implant': [],
}
"""
# other "methods" from FHIR
'subtract - dosing instruction fragment': [],
'as': [],
'or': [],
'finish': [],
'until gone': [],
'upon': [],
'per': [],
'sparingly': [],
'call': [],
'when': [],
'to': [],
'then': [],
'multiply': [],
'discontinue': [],
'with': [],
'then discontinue': [],
'until': [],
'every': [],
'before': [],
'now': [],
'follow directions': [],
'if': [],
'and': [],
'twice': [],
'follow': [],
'until finished': [],
'during': [],
'at': [],
'dosing instruction imperative': [],
'only': [],
'hold': [],
'constant': [],
'divide': [],
'add': [],
'once': [],
'then stop': [],
"""

# TODO: laterality for ophthalmic, otic, nasal routes - likely as a get_laterality method or something
ROUTES = {
	'by mouth': ['oral', r'on (?:the )?tongue', r'orally(?! disintegrating)', r'po\b', r'p\.o\.', r'oral\b', r'\b(?!vaginal|sublingual)tab(?:let)?(?:s)?\b', r'\bcap(?:sule)?(?:s)?\b', r'\bchew\b', r'\dpo\b'],
  'in left ear': [r'(?:in to |into |in |to |per )?(?:the )?left ear', r'\ba\.s\.\b'],
  'in right ear': [r'(?:in to |into |in |to |per )?(?:the )?right ear', r'\ba\.d\.\b'],
  'in both ears': [r'(?:in to |into |in |to |per )?(?:both ears|each ear|ears)', r'\ba\.u\.\b', r'\bau\b'],
  'in ear(s)': ['by ear', 'otically', 'otic', r'(?:in to |into |in |to |per )?(?:the )?(?:affected )?ear\b'],
  'in left nostril': [r'(?:in to |into |in |to |per )?(?:the )?left (?:nose|nostril|nare)'],
  'in right nostril': [r'(?:in to |into |in |to |per )?(?:the )?right (?:nose|nostril|nare)'],
  'in each nostril': [r'(?:in to |into |in |to |per )?(?:both nostrils|each nostril|nostrils|each nare)'],
  'in nostril(s)': ['by nose', 'nasally', 'nasal',  r'(?:in to |into |in |to |per )?(?:the )?(?:affected)?(?:nose|nostril|nare)\b'],
  'in left eye': [r'(?:in to |into |in |to |per )?(?:the )?left eye', r'\bo\.s\.\b', r'\bos\b'],
  'in right eye': [r'(?:in to |into |in |to |per )?(?:the )?right eye', r'\bo\.d\.\b', r'\bod\b'],
  'in both eyes': [r'(?:in to |into |in |to |per )?(?:both eyes|each eye|eyes)', r'\bo\.u\.\b', r'\bou\b'],
  'in eye(s)': ['by eye', 'ophthalmically', 'ophthalmic', r'(?:in to |into |in |to |per )?(?:the )?(?:affected )?eye\b'],
  'vaginally': ['vaginal', r'(?:in to|into|in|to|per)(?: the)? vagina', r'p\.v\.', r'pv\b'],
  'sublingually': ['sublingual', r'under (?:the )?tongue', r'sub(?: |-)?lingual(?:ly)?', r'\bs\.l\.\b', r'\bsl\b'],
  'subcutaneously': ['subcutaneous', r'(?:in|under) the skin', r'sub(?: |-)*cutaneous(?:ly)?', r'subq\b', r'sub\.q\.', r'sc\b', r'subcu\b', r's\.c\.', r'sq\b', r's\.q\.'],
  'rectally': ['rectal', r'p\.r\.\b', r'pr\b', r'in(?:to)* the (?:butt|anus|rectum)'],
  'intramuscularly': [r'i\.m\.\b', r'\bim\b', 'intramuscular', r'in(?:to)* the muscle' ],
  'intravenously': [r'i\.v\.', r'\biv\b', 'intravenous'],
  'cutaneously': [r'\bcutaneous'],
  'transdermally': ['transdermal', 'patch', 'patches'],
  'topically': [r'(?:to|on)(?: the)? skin', r'(?:cleaned|clean|dry) skin', 'topical', r'(?:to|on) affected (?:area|site)(?:s|\(s\))', 'application', 'scalp', r'face\b', 'apply', 'patch'],
  'enterally': ['enteral'],
  'via g-tube': [r'(?:via|per) g(?:-| )?tube', 'gastrostomy'],
  'via j-tube': [r'(?:via|per) j(?:-| )?tube', 'jejunostomy'],
  'via ng-tube': [r'(?:via|per) (?:ng|n\.g\.)(?:-| )?tube', 'nasogastrically', 'nasogastricly', 'nasogastric'],
  'to the teeth': ['dentally', 'dental', r'to(?: the)? teeth'],
  'intra-articularly': [r'(?:in to|into|in|to|per) (?:the|one|both|two|all) joint', 'intra-articular'],
  'via nebulization': [r'(?:via |per|using a |from the |by )?nebuliz(?:ation|ed|er|e)'],
  'via inhalation': ['respiratory tract', r'(?:via |per |using a |from the )?inhal(?:ation|ed|er|e)', r'puff(?:s)?', r'inh\b', r'inhalation(?:s)?'],
  'in urethra': [r'(?:into|via|within the|within) urethra', 'urethrally', 'urethral','intrauterine'],
  'translingually': ['translingual', 'on the tongue'],
  'buccally': [r'between (?:the )?cheek and (?:the )?gums', 'buccal'],
  'to mucous membrane': [r'(?:to|on) (?:the )?mucous membrane(?:s)?', r'mucous membrane(?:s)?'],
  'via injection': [r'(?:via |per )injection', r'injection(?:s)?'],
  'swish and spit': [],
  'swish and swallow': [],
  'miscellaneous': ['misc'],
}

"""
NOTE: other "routes" from FHIR
  'endocervical': [],
  'endosinusial': [],
  'endotracheopulmonary': [],
  'extra-amniotic': [],
  'gastroenteral': [],
  'gingival': [],
  'intraamniotic': [],
  'intrabursal': [],
  'intracardiac': [],
  'intracavernous': [],
  'intracoronary': [],
  'intradermal': [],
  'intradiscal': [],
  'intralesional': [],
  'intralymphatic': [],
  'intraocular': [],
  'intrapleural': [],
  'intrasternal': [],
  'intravesical': [],
  'oromucosal': [],
  'periarticular': [],
  'perineural': [],
  'subconjunctival': [],
  'intraluminal': [],
  'intraperitoneal': [],
  'transmucosal': [],
  'intrabiliary': [],
  'epidural': [],
  'suborbital': [],
  'caudal': [],
  'intraosseous': [],
  'intrathoracic': [],
  'intraductal': [],
  'intratympanic': [],
  'intravenous central': [],
  'intramyometrial': [],
  'gastro-intestinal stoma': [],
  'colostomy': [],
  'periurethral': [],
  'intracoronal': [],
  'retrobulbar': [],
  'intracartilaginous': [],
  'intravitreal': [],
  'intraspinal': [],
  'orogastric': [],
  'transurethral': [],
  'intratendinous': [],
  'intracorneal': [],
  'oropharyngeal': [],
  'peribulbar': [],
  'nasojejunal': [],
  'fistula': [],
  'surgical drain': [],
  'intracameral': [],
  'paracervical': [],
  'intrasynovial': [],
  'intraduodenal': [],
  'intracisternal': [],
  'intratesticular': [],
  'intracranial': [],
  'tumor cavity': [],
  'paravertebral': [],
  'intrasinal': [],
  'transcervical': [],
  'subtendinous': [],
  'intraabdominal': [],
  'subgingival': [],
  'intraovarian': [],
  'ureteral': [],
  'peritendinous': [],
  'intrabronchial': [],
  'intraprostatic': [],
  'submucosal': [],
  'surgical cavity': [],
  'ileostomy': [],
  'intravenous peripheral': [],
  'periosteal': [],
  'esophagostomy': [],
  'urostomy': [],
  'laryngeal': [],
  'intrapulmonary': [],
  'mucous fistula': [],
  'nasoduodenal': [],
  'body cavity': [],
  'intraventricular route - cardiac': [],
  'intracerebroventricular': [],
  'percutaneous': [],
  'interstitial': [],
  'arteriovenous graft': [],
  'intraesophageal': [],
  'intragingival': [],
  'intravascular': [],
  'intradural': [],
  'intrameningeal': [],
  'intragastric': [],
  'intracorpus cavernosum': [],
  'intrapericardial': [],
  'intralingual': [],
  'intrahepatic': [],
  'conjunctival': [],
  'intraepicardial': [],
  'transendocardial': [],
  'transplacental': [],
  'intracerebral': [],
  'intraileal': [],
  'periodontal': [],
  'peridural': [],
  'lower respiratory tract': [],
  'intramammary': [],
  'intratumor': [],
  'transtympanic': [],
  'transtracheal': [],
  'digestive tract': [],
  'intraepidermal': [],
  'intrajejunal': [],
  'intracolonic': [],
  'intra-arterial': [],
  'intramedullary': [],
  'intrauterine': [],
  'arteriovenous fistula': [],
  'intrathecal': [],
"""

# TODO: add a lot more here (mL, mcg, g, etc)
STRENGTH_UNITS = {
  'mg': [r'(?:milligram(?:s)?|mgs)\b'],
  'mcg': [r'(?:microgram(?:s)?|mcgs)\b'],
  'g': [r'(?:gm|gms|gram(?:s)?)\b'],
  'international units': [r'i\.u\.\b', r'iu\b', 'international unit', r'int\'l unit',  'intl unit'],
  'units': [r'unit'],
  'mEq': [r'milliequivalent(?:s)?'],
  'teaspoon': [r'\btsp\b'],
  'tablespoon': [r'\btbsp\b'],
}

DOSE_UNITS = {
  # to match ahead of one-letter dose form (L)
  'lozenge': [r'\bloz\b'],
  'liniment': [],
  'lotion': [],
  'liquid dose form': [],
  # volume
  'mL': [r'(?:milliliter)', r'mls\b'],
  'L': [r'(?:\bliter)'],
  'oz': ['ounce'],
  'cm': ['centimeter', r'cm\b', r'cms\b'],
  # tablet
  # TODO: add all synonyms to exclusion for tablet
  # ERROR: make sure "tablespoon" does not match on "tab" -- use a negative lookahead
  'tablet': [r'(?<!film-coated)(?<!effervescentgastro-resistant)(?<!orodispersible)(?<!prolonged-release)(?<!vaginal)(?<!effervescent vaginal)(?<!modified-release)(?<!chewable)(?<!sublingual)(?<!buccalmuco-adhesive buccal)(?<!soluble)(?<!dispersible)(?<!delayed-release particles)(?<!oral)(?<!inhalation vapor)(?<!implantation)(?<!extended-release film coated)(?<!ultramicronized)(?<!extended-release)(?<!extended-release enteric coated)(?<!delayed-release)(?<!coated particles)(?<!sustained-release buccal)(?<!multilayer)\s*tab(?:let)?(?:s)?', r'\bt\b'],
  'film-coated tablet': [r'(?:film-coated|film coated) tab(?:let)?(?:s)?'],
  'effervescent tablet': [r'effervescent tab(?:let)?(?:s)?'],
  'gastro-resistant tablet': [r'(?:gastro-resistant|gastro resistant) tab(?:let)?(?:s)?'],
  'orodispersible tablet': [r'(?:orodispersible|oral disintegrating|orally disintegrating) tab(?:let)?(?:s)?', r'\bodt\b', r'o.d.t.'],
  'prolonged-release tablet': [r'(?:prolonged-release|prolonged release) tab(?:let)?(?:s)?'],
  'vaginal tablet': [r'vaginal tab(?:let)?(?:s)?'],
  'effervescent vaginal tablet': [r'effervescent vaginal tab(?:let)?(?:s)?'],
  'modified-release tablet': [r'(?:modified-release|modified release) tab(?:let)?(?:s)?'],
  'chewable tablet': [r'chewable tab(?:let)?(?:s)?', r'chewable'],
  'sublingual tablet': [r'(?:sublingual|s.l.|sl) tab(?:let)?(?:s)?'],
  'buccal tablet': [r'buccal tab(?:let)?(?:s)?'],
  'muco-adhesive buccal tablet': [r'(?:muco-adhesive|muco adhesive) buccal tab(?:let)?(?:s)?'],
  'soluble tablet': [r'soluble tab(?:let)?(?:s)?'],
  'dispersible tablet': [r'dispersible tab(?:let)?(?:s)?'],
  'delayed-release particles tablet': [r'(?:delayed-release|delayed release|d.r.|dr) particles tab(?:let)?(?:s)?'],
  'oral tablet': [r'oral tab(?:let)?(?:s)?'],
  'inhalation vapor tablet': [r'inhalation vapor tab(?:let)?(?:s)?'],
  'implantation tablet': [r'implantation tab(?:let)?(?:s)?'],
  'extended-release film coated tablet': [r'(?:extended-release|extended release|e.r.|er) (?:film coated|film-coated) tab(?:let)?(?:s)?'],
  'ultramicronized tablet': [r'(?:ultramicronized|ultra-micronized) tab(?:let)?(?:s)?'],
  'extended-release tablet': [r'(?:extended release|er|e.r.) tablet'],
  'extended-release enteric coated tablet': [r'(?:extended release|extended release|er|e.r.) (?:enteric coated|enteric-coated|e.c.|ec) tablet'],
  'delayed-release tablet': [r'(?:delayed release|d.r.|dr) tablet'],
  'coated particles tablet': [r'coated particles tab(?:let)?(?:s)?'],
  'sustained-release buccal tablet': [r'(?:sustained-release|sustained release|s.r.|sr) buccal tab(?:let)?(?:s)?'],
  'multilayer tablet': [r'(?:multilayer|multi-layer) tab(?:let)?(?:s)?'],		
  # capsule
  'capsule': [r'cap(?:sule)?(?:s)?\b'],
  'hard capsule': [r'hard cap(?:sule)?(?:s)?\b'],
  'soft capsule': [r'soft cap(?:sule)?(?:s)?\b'],
  'vaginal capsule': [r'vaginal cap(?:sule)?(?:s)?\b'],
  'hard capsule inhalation powder': [r'hard cap(?:sule)?(?:s)?\b inhalation powder'],
  'hard vaginal capsule': [r'hard vaginal cap(?:sule)?(?:s)?\b'],
  'soft vaginal capsule': [r'soft vaginal cap(?:sule)?(?:s)?\b'],
  'rectal capsule': [r'rectal cap(?:sule)?(?:s)?\b'],
  'inhalation vapor capsule': [r'inhalation vapor cap(?:sule)?(?:s)?\b'],
  'gastro-resistant capsule': [r'(?:gastro-resistant|gastro resistant) cap(?:sule)?(?:s)?\b'],
  'prolonged-release capsule': [r'(?:prolonged-release|prolonged release) cap(?:sule)?(?:s)?\b'],
  'coated pellets capsule': [r'coated pellets cap(?:sule)?(?:s)?\b'],
  'delayed-release capsule': [r'(?:delayed-release|delayed release|d.r.|dr) cap(?:sule)?(?:s)?\b'],
  'oral capsule': [r'oral cap(?:sule)?(?:s)?\b'],
  'extended-release film coated capsule': [r'(?:extended-release|extended release|e.r.|er) (?:film coated|film-coated) cap(?:sule)?(?:s)?\b'],
  'extended-release coated capsule': [r'(?:extended-release|extended release|e.r.|er) coated cap(?:sule)?(?:s)?\b'],
  'extended-release capsule': [r'(?:extended-release|extended release|e.r.|er) cap(?:sule)?(?:s)?\b'],
  'coated capsule': [r'coated cap(?:sule)?(?:s)?\b'],
  'extended-release enteric coated capsule': [r'(?:extended-release|extended release|e.r.|er) (?:enteric coated|enteric-coated|e.c.|ec) cap(?:sule)?(?:s)?\b'],
  'delayed-release pellets capsule': [r'(?:delayed-release|delayed release|d.r.|dr) pellets cap(?:sule)?(?:s)?\b'],
  'modified-release capsule': [r'(?:modified-release|modified release) cap(?:sule)?(?:s)?\b'],
  'oromucosal capsule': [r'oromucosal cap(?:sule)?(?:s)?\b'],
  # patch
  'drug patch': [r'(?<!transdermal ) patch'],
  'transdermal patch': [r'patch'],
  # drops
  'drops': [r'drop', r'gtt'],
  'oral drops': [r'oral drop'],
  'eye/ear drops': [r'eye/ear drop'],
  'eye drops': [r'eye drop', r'ophthalmic drop'],
  'prolonged-release eye drops': [r'(?:prolonged-release|prolonged release) eye drop'],
  'nasal drops': [r'nasal drop', r'nose drop'],
  'eye/ear/nose drops': [r'eye/ear/nose drop'],
  'ear drops': [r'ear drop', r'otic drop'],
  'modified release drops': [r'modified release drop', r'modified-release drop'],
  # spray
  'spray': [],
  'oromucosal spray': [],
  'sublingual spray': [],
  'cutaneous spray': [],
  'cutaneous powder spray': [],
  'aerosol spray': [],
  'powder spray': [],
  'ear spray': [r'otic spray'],
  'vaginal spray': [],
  'rectal spray': [],
  'metered spray': [],
  'pressurized spray': [],
  'nasal spray': [],
  'cutaneous suspension spray': [],
  'cutaneous solution spray': [],
  # inhalation
  'puff': [r'inhalation', r'puff', r'\bpuf\b', r'pressurized inhalation(?:s)?'],
  'pressurised inhalation solution': [],
  'pressurised inhalation suspension': [],
  'pressurised inhalation emulsion': [],
  'inhalation powder': [],
  'inhalation vapor': [],
  'inhalation vapor powder': [],
  'inhalation vapor solution': [],
  'inhalation vapor ointment': [],
  'inhalation vapor liquid': [],
  'inhalation gas': [],
  # aerosol
  'aerosol generator': [],
  'metered dose aerosol inhaler': [],
  'nasal aerosol': [r'nasal spray'],
  'aerosol powder': [],
  'cutaneous aerosol': [],
  'metered dose aerosol': [],
  # gum
  'gum': [],
  'oral gum': [],
  'medicated chewing-gum': [r'medicated chewing gum'],
  # film
  'film': [],
  'extended-release film': [r'(?:extended-release|extended release|e.r.|er) film'],
  # cone
  'cone': [],
  'dental cone': [],
  # sponge
  'sponge': [],
  'vaginal sponge': [],
  'cutaneous sponge': [],
  # pellet
  'implantable pellet': [],
  'pellet': [],
  # inhaler
  'inhaler': [],
  'metered dose powder inhaler': [],
  'metered dose inhaler': [r'MDI', r'M.D.I.'],
  'breath activated powder inhaler': [],
  'breath activated inhaler': [],
  # stick
  'ear stick': [],
  'nasal stick': [],
  'drug stick': [],
  'dental stick': [],
  'cutaneous stick': [],
  'urethral stick': [],
  'wound stick': [],
  # tampon
  'tampon dose form': [r'tampon'],
  'ear tampon': [],
  'medicated vaginal tampon': [],
  'rectal tampon': [],
  # paste
  'oral paste': [],
  'drug paste': [r'(?<!oral )paste'],
  'oromucosal paste': [],
  'gingival paste': [],
  # pill
  'pill': [],
  'pillule': [],
  'caplet': [],
  'drug aerosol': [],
  'drug aerosol foam': [r'foam'],
  'cachet': [],
  'drug pledget': [],
  'oral lyophilisate': [],
  'oromucosal gel': [],
  'gingival gel': [],
  'dental gel': [],
  'dental insert': [],
  'dental powder': [],
  'shampoo': [],
  'collodion': [],
  'medicated nail laquer': [],
  'poultice': [],
  'ophthalmic insert': [],
  'ear powder': [],
  'nasal powder': [],
  'eye/ear/nose ointment': [],
  'pessary': [],
  'enema': [],
  'suppository': [],
  'implantation chain': [],
  'implant dosage form': [],
  'extended-release insert': [],
  'vaginal insert': [],
  'urethral suppository': [],
  'metered powder': [],
  'rectal suppository': [],
  'extended-release suppository': [],
  'pastille': [],
  'gaseous dose form': [],
  'vaginal suppository': [],
  'extended-release bead implant': [],
  'solid dose form': [],
  'eye/ear ointment': [],
  'transdermal drug delivery system': [],
  'medicated toothpaste': [],
  'tincture': [],
  'spirit': [],
  'modified-release pessary': [],
  'bar': [],
  'buccal film': [],
  'orodispersible film': [],
  'pen': [],
  'applicatorful': ['applicatorsful'],
  'application': [],
  'capful': [],
  'injection': [],
  'packet': [],
  'strip': [],
  'syringe': [],
  'vial': [],
  'kit': [],
}

PAIN_SEVERITIES = {
  'acute': [],
  'chronic': [],
  'any level of': [],
  'breakthrough': [],
  'mild to moderate': [r'mild-moderate'],
  'moderate to severe': [r'moderate-severe'],
  'mild to severe': [r'mild-severe'],
  'mild': [],
  'moderate': [],
  'severe': [],
  'intense': [],
  'intolerable': [],
}

PAIN_LOCATIONS = {
  'abdominal': [],
  'arthritis': [],
  'ear': [],
  'eye': [],
  'muscle/joint': [],
  'muscle': [],
  'joint': [],
  'throat': [],
  'back': [],
  'knee': [],
  'leg': [],
  'stent': [],
  'lower back': [],
  'upper back': [],
  'back': [],
  'post-operative': [r'post(?:-|\s)?op(?:erative)?'],
}

PAIN_TRIGGERS = {
  'unrelieved by PO medications': [],
  'with swallowing': ['w/ swallowing', 'on swallowing'],
  'with urination': ['w/ urination', 'on urination'],
}

RE_BASIC_PAIN = re.compile(r'\bpain', flags = re.I)
RE_PAIN_SEVERITY = []
RE_PAIN_LOCATION = []
RE_PAIN_TRIGGER = []
for n, p in PAIN_SEVERITIES.items():
  p.append(n)
  RE_PAIN_SEVERITY.append(r'|'.join(p))
for n, p in PAIN_LOCATIONS.items():
  p.append(n)
  RE_PAIN_LOCATION.append(r'|'.join(p))
for n, p in PAIN_TRIGGERS.items():
  p.append(n)
  RE_PAIN_TRIGGER.append(r'|'.join(p))
PAIN_PATTERN = re.compile(r'(?P<pain_severity>' + r'|'.join(RE_PAIN_SEVERITY) + r')?\s*(?P<pain_location>' + r'|'.join(RE_PAIN_LOCATION) + r')?\s*\bpain\s*(?P<pain_trigger>' + r'|'.join(RE_PAIN_TRIGGER) + r')?\s*(?:score|scale|rated)?\s*(?:(?:(?P<pain_logical_expression>greater than or equal to|>=|greater than|>|\bgte\b|\bg\.t\.e\.\b|\bgt\b|\bg\.t\.\b)\s*)?(?P<pain_score>' + RE_RANGE + r'))?', flags = re.I)

# NOTE: pain is intentionally missing from here because it has its own PainIndicationParser
INDICATIONS = {
  'acne': [],
  'acute migraine': [],
  'agitation': [],
  'allergic reaction': [],
  'allergies': [],
  'allergy': [],
  'anaphylaxis': [],
  'anxiety': [],
  'arthritis': [],
  'asthma': [],
  'bedwetting': [],
  'bee sting': [],
  'bladder irritation': [],
  'bladder spasm': [],
  'bleeding': [],
  'blood sugar less than': [],
  'bradycardia': [],
  'burning with urination': [],
  'chest pain': [],
  'cold sore': ['cold sores'],
  'cold': [],
  'congestion': [],
  'constipation': [],
  'cough': [],
  'cramping': [],
  'cravings': [],
  'dandruff': [],
  'delirium': [],
  'demand feeding': [],
  'depression': [],
  'diarrhea': [],
  'difficulty breathing': [],
  'discomfort': [],
  'dizziness': [],
  'drainage': [],
  'dressing change': [],
  'dry eyes': [],
  'dry mouth': [],
  'dry skin': [],
  'dysmenorrhea': [],
  'dyspnea': [],
  'dysuria': [],
  'ear drainage': [],
  'ear fullness': [],
  'eczema': [],
  'edema': [],
  'erectile dysfunction': [r'e\.d\.', r'\bed\b'],
  'fever': [],
  'fever blisters': [],
  'fever greater than or equal to': [],
  'flares': [],
  'food allergy': [],
  'flatulence': [],
  'gas': [],
  'glaucoma': [],
  'gout': [],
  'hallucination': [],
  'headache': [],
  'heartburn': [],
  'hiccups': [],
  'hemorrhoids': [],
  'high blood pressure': [],
  'high blood sugar': [],
  'hives': [],
  'hypoglycemia': [],
  'incontinence': [],
  'indigestion': [],
  'inflammation': [],
  'insomnia': [],
  'intercourse': [],
  'irritation': [],
  'itchiness': [],
  'itching': [],
  'line care': [],
  'low blood sugar': [],
  'low heart rate': [],
  'migraine': [],
  'mucositis': [],
  'movement disorder': [],
  'muscle spasm': [],
  'nasal congestion': [],
  'nasal dryness': [],
  'nausea': [],
  'numbness': [],
  'opioid reversal': [],
  'outbreak': [],
  'palpitations': [],
  'perianal irritation': [],
  'pharyngitis': [],
  'rash': [],
  'reflux': [],
  'respiratory distress': [],
  'respiratory depression': [],
  'rhinitis': [],
  'rigors': [],
  'seasonal allergies': [],
  'sedation': [],
  'seizure clusters': [],
  'seizures lasting longer than': [],
  'seizures lasting more than': [],
  'severe allergic reaction': [],
  'severe food allergies': [],
  'severe headache': [],
  'severe hypoglycemia': [],
  'severe low blood sugar': [],
  'sexual activity': [],
  'sex': [],
  'shivering': [],
  'shortness of breath': [r'\bsob\b', r's\.o\.b\.'],
  'sinus pressure': [],
  'sleep': [],
  'smoking cessation': [],
  'social situations': [],
  'sore throat': [],
  'soreness': [],
  'spasm': [],
  'stomatitis': [],
  'swelling': [],
  'teething': [],
  'thrush': [],
  'tremor': ['tremors'],
  'unable to take po': [],
  'urge to smoke': [],
  'urinary burning': [],
  'urinary tract irritation': [],
  'urinary tract symptoms': [],
  'vertigo': [],
  'vomiting': [],
  'weight gain': [],
  'withdrawal': ['withdrawl'],
  'wheeze': [],
  'wheezing': [],
  'wound care': [],
  'yeast infection': [],
  # less specific
  'blood pressure': [],
}

RE_INDICATION = []
for n, p in INDICATIONS.items():
  p.append(n)
  RE_INDICATION.append(r'|'.join(p))        
INDICATION_PATTERN = re.compile(r'(?P<indication>' + r'|'.join(RE_INDICATION) + r')', flags = re.I)

LOGICAL_EXPRESSIONS = {
  'greater than or equal to': [r'\bgte\b', r'>=', r'g\.t\.e\.', r'> ='],
  'less than or equal to': [r'\blte\b', r'<=', r'l\.t\.e\.', r'< ='],
  'greater than': [r'>'],
  'less than': [r'<'],
}

# splits '1 to 2' or '1-2' or '1 or 2' into [1,2] and returns '1' as [1,None] because FHIR doesn't capture frequencyMax when frequency is q8h
def split_range(text):
  split = text.lower()
  split = re.sub(r'  ', ' ', split)
  split = re.sub(r'(?:,|mg)', '', split)
  split = re.sub(r'(?:to|or)', '-', split, flags = re.I)
  split = re.sub(r'(?<!(?:\d|\s))-(?!(?:\d|\s))', '', split) # don't split one-half, but do split on 1/2-1 and 1/2 - 1 --> convert one-half to onehalf
  split = split.split('-') 
  split = [number_text_to_int(s) for s in split]
  return [split[0], split[1]] if len(split) > 1 else [split[0], None]

# similar to split_range, but specific to frequencies
# once -> [1,None], 3-4 times -> [3,4]
def split_frequency_range(text):
  split = text
  split = re.sub(r'(?:times|time|(?<=\d|\s)x|nights|days)', '', split, flags = re.I)
  split = re.sub(r'once|a|per', '1', split, flags = re.I)
  split = re.sub(r'twice', '2', split, flags = re.I)
  split = split_range(split)
  return split

# once IndicationParser returns a string of text following "as needed for", this tries to parse a specific indication
# it first tries to find a pain-related indication, and then looks for more general indications
# TODO: expand the pain-type search to blood glucose levels (i.e. prn BG > 120) and other specific types of indications
def get_indication(indication_text):
  indication = []
  if re.search(RE_BASIC_PAIN, indication_text) != None:
    for match in re.finditer(PAIN_PATTERN, indication_text):
      pain_severity = match.group('pain_severity')
      pain_location = match.group('pain_location')
      pain_trigger = match.group('pain_trigger')
      pain_logical_expression = match.group('pain_logical_expression')
      pain_score = match.group('pain_score')
      indication.append((get_normalized(PAIN_SEVERITIES, pain_severity) + ' ' if pain_severity else '') + (get_normalized(PAIN_LOCATIONS, pain_location) + ' ' if pain_location else '') + 'pain' + (' ' + get_normalized(PAIN_TRIGGERS, pain_trigger) if pain_trigger else '') + (' score' if pain_score else '') + (' ' + get_normalized(LOGICAL_EXPRESSIONS, pain_logical_expression) if pain_logical_expression else '') + (' ' + pain_score if pain_score else ''))
  
  for match in re.finditer(INDICATION_PATTERN, indication_text):
    indication.append(get_normalized(INDICATIONS, match.group('indication')))
  
  indication = ','.join(indication)
  indication = None if indication == '' else indication
  return indication

def get_frequency_readable(frequency=None,frequency_max=None,period=None,period_max=None,period_unit=None,time_duration=None,time_duration_unit=None,day_of_week=None,count=None):
  frequency_readable = ''
  frequency_range = str(frequency) + ('-' + str(frequency_max) if frequency_max else '') if frequency != None else ''
  # period - don't show period if period = 1 (i.e. don't show every 1 day, just show every day -- or better yet, daily)
  period_range = ('' if period == 1 and period_max == None else str(period) + ('-' + str(period_max) if period_max else '')) if period != None else ''

  frequency_readable += 'once' if count == 1 else ''

  if frequency != None and period_unit != None and frequency > 1:
    if frequency_range == '2' and period_unit == 'day':
      frequency_readable += 'twice daily'
    else:
      frequency_readable += frequency_range + ' times per ' + str(period_unit)
  elif frequency != None and period_unit != None and frequency == 1:
    if period_range == '' and period_unit == 'day':
      frequency_readable += 'daily'
    else:
      frequency_readable += 'every ' + period_range + (' ' if period_range != '' else '') + period_unit + ('s' if period_range != '' else '')

  frequency_readable += '' if time_duration == None and time_duration_unit == None else ' for ' + str(time_duration) + ' ' + time_duration_unit

  frequency_readable += ' on ' + ', '.join(day_of_week.split('|')) if day_of_week != None else ''
  
  return frequency_readable

# converts one to 1, thirty to 30, etc
def number_text_to_int(textnum):
  # convert 1 and 1/2 to 1 1/2
  # convert one and one half to one one half
  textnum = re.sub(r'(?:&\s|\band\s)', '', textnum)
  try:
    # try integer (i.e. 1)
    return int(textnum)
  except:
    try:
      # try float (i.e. 1.5)
      return float(textnum)
    except:
      try:
        # try fraction (i.e. 1 1/2 -> 1.5)
        return float(sum(Fraction(s) for s in textnum.split()))
      except:
        try:
          # not sure what would match here...
          return eval(textnum)
        except:
          try:
            # otherwise, we have text-based numbers and need to figure it out
            # TODO: make this better - re-write the core numwords function to make more sense for sigs
            #       we are never going to see the word trillion in a sig, but could definitey see "one quarter tablet"
            #       and this algorithm doesn't account for that, which is why the below is hard coded
            # NOTE: we remove & and from textnum
            # NOTE: we also convert one-half to onehalf in split_range method
            numwords = []
            fractions = [ 'half', 'third', 'quarter', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth' ]
            decimals = [ 'point one', 'point two', 'point three', 'point four', 'point five', 'point six', 'point seven', 'point eight', 'point nine' ]
            units = [ 'zero', 'one', 'two', 'three', r'four(?!teen)', 'five', r'six(?!teen|ty)', r'seven(?!teen|ty)', r'eight(?!een|y)', r'nine(?!teen|ty)', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', ]
            tens = [ 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety' ]
            
            for idx, pattern in enumerate(fractions):   numwords.append((re.compile(r'(P<multiplier>' + r'|'.join(units) + r')?' + pattern, re.I), 1 / (idx + 2)))
            for idx, pattern in enumerate(decimals):    numwords.append((re.compile(pattern, re.I), (idx + 1) / 10))
            for idx, pattern in enumerate(units):       numwords.append((re.compile('(?<!point )' + pattern + r'(?!\s*(?:' + r'|'.join(fractions) + r'))', re.I), idx))
            for idx, pattern in enumerate(tens):        numwords.append((re.compile(pattern, re.I), (idx + 2) * 10))

            number = 0
            for pattern, increment in numwords:
              if re.search(pattern, textnum):
                number += increment
            return number
          except:
            return None

# normalizes text using constant pattern groups
# pattern groups are tuples with the following format:
# (name, [pattern,...])
def get_normalized(patterns, text):
  # trim whitespace from beginning and end of string
  normalized = text.strip()
  for n, p in patterns.items():
    # normalized = re.sub(r'(?:\b' + r'|'.join(p) + r'\b)', n, text, flags=re.I)
    normalized = re.sub(r'^(?:' + r'|'.join(p) + r')$', n, text, flags=re.I)
    if normalized != text:
        break
  return normalized


#print(split_range('2.5-fifty'))
#print(get_frequency_readable(frequency=1,frequency_max=2,period=3,period_unit='day'))
#print(get_indication_(frequency=1,frequency_max=2,period=3,period_unit='day'))