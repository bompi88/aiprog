""" Helper method for changing part of a domain"""


def domaincopy(domains):
    """ Creates a new dict instance with the same references as values """
    new_domains = {}

    for (key, domain) in domains.items():
        new_domains[key] = domain

    return new_domains
