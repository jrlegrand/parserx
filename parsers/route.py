from .classes.parser import *

class RouteParser(Parser):
    parser_type = 'route'
    match_keys = ['route', 'route_text_start', 'route_text_end', 'route_text']
    def normalize_pattern(self):
        route_patterns = []
        for n, p in ROUTES.items():
            # add the name of the pattern to the list of matched patterns
            p.append(n)
            # and join them with a | character
            # and add them to the route_patterns array
            route_patterns.append(r'|'.join(p))
        pattern = re.compile(r'\b(?P<route>' + r'|'.join(route_patterns) + r')\b', flags = re.I)
        return pattern
    def normalize_match(self, match):
        route = get_normalized(ROUTES, match.group('route'))
        route_text_start, route_text_end = match.span()
        route_text = match[0]
        return self.generate_match({'route': route, 'route_text_start': route_text_start, 'route_text_end': route_text_end, 'route_text': route_text})

parsers = [
    RouteParser()
]

#print(RouteParser().parse('take one by mouth daily'))