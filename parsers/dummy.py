import re
sig = '             Take 1.5 tabs (**1,000 mg**) by "	mouth"     	     daily, then \'take\' .5 tabs 5. mg po Q.I.D. aft\nerwards.      '
# standardize to lower case
sig = sig.lower()
# remove:
# . if not bordered by a number (i.e. don't want to convert 2.5 to 25 or 0.5 to 05)
# , ; # * " ' ( ) \t
sig = re.sub(r'(?:(?<![0-9])\.(?![0-9])|,|;|#|\*|\"|\'|\(|\)|\t)', '', sig)
# remove duplicate spaces, and in doing so, also trim whitespaces from around sig
sig = ' '.join(sig.split())

print(sig)