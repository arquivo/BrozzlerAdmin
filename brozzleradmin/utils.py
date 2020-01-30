from urllib.parse import urlparse


def get_url_base(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)


def generate_unique_site_seeds(seeds):
    sites_basename = set()
    for seed in seeds:
        parsing_result = get_url_base(seed)
        sites_basename.add(parsing_result)
    return sites_basename
