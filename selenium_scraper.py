import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('selenium-scraper')
logger.setLevel(logging.DEBUG)

class SeleniumScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Ativa o modo headless
        chrome_options.add_argument('--no-sandbox') 
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        chrome_options.add_argument(f'user-agent={chrome_user_agent}')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        # Aplicando selenium-stealth
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=False,
                )

        self.wait = WebDriverWait(self.driver, 10)
        
        logger.info('WebDriver iniciado com User-Agent do Chrome em modo headless.')

    def get_clan_data(self, url, card_selector, name_selector, points_selector):
        logger.info(f'Acessando URL: {url}')
        self.driver.get(url)
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, card_selector)))
            clan_data = []
            clans = self.driver.find_elements(By.CSS_SELECTOR, card_selector)
            for clan in clans:
                name = clan.find_element(By.CSS_SELECTOR, name_selector).text
                points = clan.find_element(By.CSS_SELECTOR, points_selector).text
                clan_data.append({'name': name, 'points': points})
            logger.info(f'Dados capturados: {clan_data}')
            return clan_data
        except Exception as e:
            logger.error(f'Erro ao capturar dados: {e}')
            return []

    def get_featured_clans(self, url):
        return self.get_clan_data(url, ".home-featured-card", ".clan-name", ".clan-points-total")

    def get_recent_matches(self, url):
        logger.info(f'Acessando URL: {url}')
        self.driver.get(url)
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".home-matches-card")))
            recent_matches = []
            matches = self.driver.find_elements(By.CSS_SELECTOR, ".home-matches-card")
            for match in matches:
                date = match.find_element(By.CLASS_NAME, "match-date").text
                clan1_name = match.find_elements(By.CLASS_NAME, "match-clan-name")[0].text.strip()
                clan2_name = match.find_elements(By.CLASS_NAME, "match-clan-name")[1].text.strip()
                clan1_score = match.find_elements(By.CLASS_NAME, "match-results-score")[0].text
                clan2_score = match.find_elements(By.CLASS_NAME, "match-results-score")[1].text
                recent_matches.append({
                    'date': date,
                    'clan1': {'name': clan1_name, 'score': clan1_score},
                    'clan2': {'name': clan2_name, 'score': clan2_score}
                })
            logger.info(f'Partidas recentes capturadas: {recent_matches}')
            return recent_matches
        except Exception as e:
            logger.error(f'Erro ao capturar partidas recentes: {e}')
            return []

    def get_top_clans(self, url):
        return self.get_clan_data(url, ".home-topthree-card", ".clan-name", ".clan-points-total")

    def get_ranking_from_leaderboard(self, url):
        logger.info(f'Acessando URL: {url}')
        self.driver.get(url)
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ranks-table.table-body .table-row")))
            ranking = []
            rows = self.driver.find_elements(By.CSS_SELECTOR, ".ranks-table.table-body .table-row")
            for row in rows:
                position = row.find_element(By.CSS_SELECTOR, ".col-1 .clan-rank").text
                name = row.find_element(By.CSS_SELECTOR, ".col-4 a").text.strip()
                leader = row.find_element(By.CSS_SELECTOR, ".col-5 a").text.strip()
                points = row.find_element(By.CSS_SELECTOR, ".col-6").text.strip()
                profile_url = row.find_element(By.CSS_SELECTOR, ".col-4 a").get_attribute('href')
                emblem_url = row.find_element(By.CSS_SELECTOR, ".col-3 img").get_attribute('src')

                ranking.append({
                    'position': position,
                    'name': name,
                    'leader': leader,
                    'points': points,
                    'profile_url': profile_url,
                    'emblem_url': emblem_url
                })
            logger.info(f'Ranking capturado da leaderboard: {ranking}')
            return ranking
        except Exception as e:
            logger.error(f'Erro ao capturar dados: {e}')
            return []

    def search_clan_by_name(self, clan_name):
        logger.info(f'Pesquisando clã pelo nome: {clan_name}')
        search_url = "https://br.crossfire.z8games.com/clan/leaderboard"
        self.driver.get(search_url)
        try:
            search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input-text.member-search-input")))
            search_box.send_keys(clan_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(4)
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".table-row")))
            clans = self.driver.find_elements(By.CSS_SELECTOR, ".table-row")
            clan_results = []
            for clan in clans:
                name_element = clan.find_element(By.CSS_SELECTOR, "div.col-4 h4 a")
                profile_url = name_element.get_attribute('href')
                name = name_element.text.strip()
                clan_results.append({'name': name, 'profile_url': profile_url})
            logger.info(f'Clãs encontrados: {clan_results}')
            return clan_results
        except Exception as e:
            logger.error(f'Erro ao pesquisar clã: {e}')
            return []

    def get_clan_details(self, clan_profile_url):
        logger.info(f'Acessando URL do perfil do clã: {clan_profile_url}')
        self.driver.get(clan_profile_url)
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".clan-name")))
            clan_name = self.driver.find_element(By.CSS_SELECTOR, ".clan-name").text.strip()
            leader_name = self.driver.find_element(By.CSS_SELECTOR, ".clan-leader a").text.strip()
            creation_date = self.driver.find_element(By.CSS_SELECTOR, ".clan-creation-date").text.strip()
            points = self.driver.find_element(By.CSS_SELECTOR, ".clan-season-date").text.strip()
            rank = self.driver.find_element(By.CSS_SELECTOR, ".clan-season-pts").text.strip()
            emblem_url = self.driver.find_element(By.CSS_SELECTOR, ".clan-logo img").get_attribute('src')
            description = self.driver.find_element(By.CSS_SELECTOR, ".pfl-desc").text.strip()
            win_rate = self.driver.find_element(By.CSS_SELECTOR, ".win-rate-percent-info span").text.strip()
            win_count = self.driver.find_element(By.CSS_SELECTOR, ".stat-item.win .stat-number").text.strip()
            loss_count = self.driver.find_element(By.CSS_SELECTOR, ".stat-item.loss .stat-number").text.strip()
            draw_count = self.driver.find_element(By.CSS_SELECTOR, ".stat-item.draw .stat-number").text.strip()
            recent_matches = []
            matches_elements = self.driver.find_elements(By.CSS_SELECTOR, ".match-history-table .table-row")
            for match in matches_elements:
                date = match.find_element(By.CSS_SELECTOR, ".col-1 .small-column-text").text.strip()
                result = match.find_element(By.CSS_SELECTOR, ".col-2 .match-result").text.strip()
                opponent_clan = match.find_element(By.CSS_SELECTOR, ".col-3 .match-clan-name a").text.strip()
                score = match.find_element(By.CSS_SELECTOR, ".col-4 .match-score").text.strip()
                map_name = match.find_element(By.CSS_SELECTOR, ".col-5 h4").text.strip()
                recent_matches.append({
                    'date': date,
                    'result': result,
                    'opponent_clan': opponent_clan,
                    'score': score,
                    'map_name': map_name
                })
            clan_details = {
                'name': clan_name,
                'leader': leader_name,
                'creation_date': creation_date,
                'points': points,
                'rank': rank,
                'emblem_url': emblem_url,
                'description': description,
                'profile_url': clan_profile_url,
                'win_rate': win_rate,
                'win_count': win_count,
                'loss_count': loss_count,
                'draw_count': draw_count,
                'recent_matches': recent_matches
            }
            logger.info(f'Detalhes do clã capturados: {clan_details}')
            return clan_details
        except Exception as e:
            logger.error(f'Erro ao capturar detalhes do clã: {e}')
            return None

    def close(self):
        self.driver.quit()
        logger.info('WebDriver fechado.')

if __name__ == "__main__":
    url = "https://br.crossfire.z8games.com/clan/leaderboard"
    scraper = SeleniumScraper()
    try:
        ranking = scraper.get_ranking_from_leaderboard(url)
        for clan in ranking:
            print(f"Posição: {clan['position']}, Nome: {clan['name']}, Líder: {clan['leader']}, Pontos: {clan['points']}")
    finally:
        scraper.close()