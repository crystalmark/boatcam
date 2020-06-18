import requests


class Tide:
    leith_url = 'http://environment.data.gov.uk/flood-monitoring/id/measures/E70824-level-tidal_level-Mean-15_min-m'

    @staticmethod
    def current_height():
        r = requests.get(Tide.leith_url)
        station = r.json()
        return station["items"]["latestReading"]["value"]
