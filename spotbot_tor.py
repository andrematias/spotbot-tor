import os
from time import sleep
from multiprocessing import Process

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()


class SpotBot:

  PROXY = "socks5://127.0.0.1:9050"
  URL = "https://accounts.spotify.com/pt-BR/login?continue=https://open.spotify.com/"
  DRIVE_PATH = "./bin/chromedriver"

  def __init__(self):
    print("SpotBot Iniciando...", end="\n")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={self.PROXY}")
    chrome_options.add_argument("--headless")
    self._drive = webdriver.Chrome(executable_path=self.DRIVE_PATH, options=chrome_options)
    
  def check_ip(self):
    self._drive.get('http://icanhazip.com')
    ip = self._drive.find_element_by_tag_name('pre')
    print("O Ip utilizado: ", ip.text, end="\n")

  def login(self, username, password):
    print("Logando com o usuário:", username, end="\n")
    self._drive.get(self.URL)
    usernameInput = self._drive.find_element_by_xpath("//input[@id='login-username']")
    passwordInput = self._drive.find_element_by_xpath("//input[@id='login-password']")
    button = self._drive.find_element_by_xpath("//button[@id='login-button']")
    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    button.click()

  def search(self, query):
    self._drive.get(f"https://open.spotify.com/search/")
  
    try:
      search_input = WebDriverWait(self._drive, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="search-input"]'))
      )

      search_input.send_keys(query)
      search_input.send_keys(Keys.ENTER)
    except Exception as ex:
      print(ex)

  def playArtist(self, hash):
    print("Executando a playlist:", hash, end="\n")
    self._drive.get(f"https://open.spotify.com/artist/{hash}")
    sleep(20)
    play_script = "document.querySelector('button[aria-label=\"Play\"]').click()"
    self._drive.execute_script(play_script)
    print("Musica executando")

  def close(self):
    self._drive.close()

  def screenshot(self, name="last_shot.png", wait_for=0):
    sleep(wait_for)
    self._drive.save_screenshot(f'./screenshots/{name}')

def main():
    spotBot = SpotBot()
    spotBot.check_ip()
    spotBot.login(os.getenv('SPOTIFY_USERNAME'), os.getenv('SPOTIFY_PASSWORD'))
    spotBot.screenshot("login.png")
    # spotBot.search("2Pac")
    spotBot.playArtist('1ZwdS5xdxEREPySFridCfh')
    spotBot.screenshot("playing.png", 15)
    # spotBot.close() 

if __name__ == '__main__':
  for i in range(1):
    p = Process(target=main).start()