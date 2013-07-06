
import re
from urlparse import urlparse 

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.utils.url import canonicalize_url, url_is_from_any_domain, url_has_any_extension

_is_valid_url = lambda url: url.split('://', 1)[0] in set(['http', 'https', 'file'])

def qualified_range_match(url, regexs, ranges):
    #print "qualified_range_match: url=%s, ranges=%s" % (url, ranges)
    if not ranges:
        return any((r.search(url) for r in regexs))


    if len(regexs) != len(ranges):
        raise ValueError("Qualified Range count must match regex count!")

    for i in range(0, len(regexs)):
        r = regexs[i]
        rng = ranges[i]

        matches = r.search(url)
        if matches:
            matches = matches.groups()
            
            # We support only a single capture
            if len(matches) != 1:
                raise ValueError("Qualified Range regex must contain a single capture!")

            match = int(matches[0])

            if len(rng) != 2:
                raise ValueError("Qualified Range must be a pair!")
            
            if rng[0] != None and match < rng[0]:
                #print "Rejecting: %s < %s" % (match, rng[0])
                continue
            if rng[1] != None and match >= rng[1]:
                #print "Rejecting: %s >= %s" % (match, rng[1])
                continue
            #print "ACCEPTING: %s <= %s < %s" % (rng[0], match, rng[1])
            return True

    return False



class QualifiedRangeSgmlLinkExtractor(SgmlLinkExtractor):
    def __init__(self, *args, **kwargs):
        self.allow_range = kwargs.pop('allow_range', None)
        self.deny_range = kwargs.pop('deny_range', None)

        SgmlLinkExtractor.__init__(self, *args, **kwargs)

    def _link_allowed(self, link):
        parsed_url = urlparse(link.url)
        allowed = _is_valid_url(link.url)
        if self.allow_res:
            allowed &= qualified_range_match(link.url, self.allow_res, self.allow_range)
        if self.deny_res:
            allowed &= not qualified_range_match(link.url, self.deny_res, self.deny_range)
        if self.allow_domains:
            allowed &= url_is_from_any_domain(parsed_url, self.allow_domains)
        if self.deny_domains:
            allowed &= not url_is_from_any_domain(parsed_url, self.deny_domains)
        if self.deny_extensions:
            allowed &= not url_has_any_extension(parsed_url, self.deny_extensions)
        if allowed and self.canonicalize:
            link.url = canonicalize_url(parsed_url)
        return allowed


    def matches(self, url):
        if self.allow_domains and not url_is_from_any_domain(url, self.allow_domains):
            return False
        if self.deny_domains and url_is_from_any_domain(url, self.deny_domains):
            return False

        if self.allow_res:
            allowed = qualified_range_match(url, self.allow_res, self.allow_range) 
        else:
            allowed = True
        
        if self.deny_res:
            denied = qualified_range_match(link.url, self.deny_res, self.deny_range)
        else:
            denied = False

        print "matches(%s) allowed=%s, denied=%s" % (url, allowed, denied)
        return allowed and not denied
