from .classes.parser import *

class RouteParser(Parser):
    parser_type = 'route'
    match_keys = ['route', 'route_text_start', 'route_text_end', 'route_text', 'route_readable']
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
        route_readable = self.get_readable(route=route)
        return self.generate_match({'route': route, 'route_text_start': route_text_start, 'route_text_end': route_text_end, 'route_text': route_text, 'route_readable': route_readable})
    def get_readable(self, route=None):
        readable = route if route else ''
        return readable

class TopicalRouteParser(RouteParser):
    def normalize_pattern(self):
        topical_route_patterns = []
        for n, p in TOPICAL_ROUTES.items():
            # add the name of the pattern to the list of matched patterns
            p.append(n)
            # and join them with a | character
            # and add them to the route_patterns array
            topical_route_patterns.append(r'|'.join(p))
        pattern = re.compile(r'.*(?P<route>' + r'|'.join(topical_route_patterns) + r').*', flags = re.I)
        return pattern
    def normalize_match(self, match):
        route = get_normalized(TOPICAL_ROUTES, match.group('route'))
        route_text_start, route_text_end = match.span()
        route_text = match[0]
        route_readable = self.get_readable(route=route)
        return self.generate_match({'route': route, 'route_text_start': route_text_start, 'route_text_end': route_text_end, 'route_text': route_text, 'route_readable': route_readable})
    def get_readable(self, route=None):
        readable = route if route else ''
        return readable
        
class InferredOralRouteParser(RouteParser):
    pattern = r'\b(?P<route>(?!vaginal|sublingual)tab(?:let)?(?:s)?(?!.*(?:sublingual(?:ly)?|into|per|on the|between the|under|by sublingual route|by buccal route))|cap(?:sule)?(?:s)?|chew(?:able)?|\dpo|capful|pill)\b'
    def normalize_pattern(self):
        return re.compile(self.pattern, flags = re.I)
    def normalize_match(self, match):
        route = 'by mouth'
        route_text_start, route_text_end = match.span()
        route_text = match[0]
        route_readable = self.get_readable(route=route)
        return self.generate_match({'route': route, 'route_text_start': route_text_start, 'route_text_end': route_text_end, 'route_text': route_text, 'route_readable': route_readable})

parsers = [
    RouteParser(),
    TopicalRouteParser(),
    InferredOralRouteParser()
]

#print(RouteParser().parse('take one by mouth daily'))