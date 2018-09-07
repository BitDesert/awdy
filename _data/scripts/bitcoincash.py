from coinscrapper import CoinScrapper
from api_methods import CryptoidAPI

class BitcoinCash(CoinScrapper,CryptoidAPI):

    def __init__ (self, driver):
        self.name = 'bitcoin cash'
        self.driver = driver

    def get_public_nodes(self):
        self.get_page("https://cash.coin.dance/nodes");
        node_count_container = self.attempt_find_element( lambda: self.driver.find_element_by_css_selector("[title].nodeTitle > strong"))
        public_nodes_source = node_count_container.text
        return int(public_nodes_source)
        
    def get_wealth_distribution(self):
        return self.bitinfo_wealth_dist()


    def get_client_codebases(self):
        self.get_page("https://cash.coin.dance/nodes");
        count_containers = self.attempt_find_element( lambda: self.driver.find_elements_by_css_selector(".nodeCountBlock > h3 > .nodeTitle > strong"))
        all_counts = [int(container.text) for container in count_containers]
        client_codebases = self.get_cumulative_grouping_count(all_counts, .9)
        return client_codebases

    def get_consensus_distribution(self):
        self.get_page('https://cash.coin.dance/blocks/today')
        tspan_objects =  self.attempt_find_element( lambda: self.driver.find_element_by_id('chartobject-1').find_elements_by_css_selector('tspan'))
        a = []
        for span in tspan_objects:
            text = span.text
            if ',' in text:
                s = text.split(',')[1].replace('%', '').strip()
                a.append(float(s))
        consensus_distribution = self.get_cumulative_grouping_count(a, .5)
        return consensus_distribution

