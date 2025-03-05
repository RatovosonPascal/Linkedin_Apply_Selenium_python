import random
import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

driver = webdriver.Chrome()


def disable_scroll():
    """Désactive le scroll global sur la page."""
    driver.execute_script("document.body.style.overflow = 'hidden';")


def enable_scroll():
    """Réactive le scroll global sur la page."""
    driver.execute_script("document.body.style.overflow = 'auto';")


def is_popup_open():
    """Vérifie si le pop-up est ouvert."""
    try:
        popup = driver.find_element(By.CLASS_NAME, 'artdeco-modal__content')
        return popup.is_displayed()
    except NoSuchElementException:
        return False


try:
    driver.get("https://www.linkedin.com/")
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    driver.maximize_window()
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes



    # Essayer de fermer l'alerte si elle existe
    try:
        alert_button = driver.find_element(By.XPATH,
                                           "//*[@id='artdeco-global-alert-container']/div/section/div/div[2]/button[2]")
        alert_button.click()
        print("Alerte fermée.")
    except:
        print("Pas d'alerte à fermer.")
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    # Connexion
    print("Attente du bouton S'identifier...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "S’identifier"))).click()
    print("Connexion...")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating").click()

    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes
    # Attente pour vérifier la connexion
    print(driver.current_url)
    print(driver.page_source[:500])  # Affiche les 500 premiers caractères du HTML

    print("Recherche d'un poste...")
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Recherche']")))
    search_box.click()
    search_box.send_keys("Développeur Java")
    search_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes


    print("Clic sur Emplois...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Emplois']"))).click()

    print("Activation du filtre Candidature simplifiée...")
    candidature_simple_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchFilter_applyWithLinkedin"))
    )
    candidature_simple_button.click()
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    # Saisie de la ville
    print("Saisie de la ville...")
    location_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Ville, département ou code postal']"))
    )
    location_input.click()
    location_input.send_keys(Keys.CONTROL + "a")
    location_input.send_keys(Keys.BACKSPACE)
    location_input.send_keys("Lille")
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    # Clic sur Recherche
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-search-box__submit-button"))
    )
    search_button.click()

    # Attendre le rechargement des résultats
    time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

    offres = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-container"))
    )

    print(f"Nombre d'offres trouvées : {len(offres)}")

    for index, offre in enumerate(offres):

        # ✅ Vérifie si un pop-up est ouvert avant de commencer l'offre suivante
        if is_popup_open():
            print(f"⏳ Pop-up détecté avant l'offre {index + 1}, attente de fermeture...")
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content'))
            )
            print("✅ Pop-up fermé, reprise du traitement.")

        try:
            print(f"\n🔹 Ouverture de l'offre {index + 1}...")

            # On désactive le scroll pendant le traitement de la pop-up
            if is_popup_open():
                disable_scroll()

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", offre)
            time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

            offre.click()
            time.sleep(random.randint(4, 6))  # Pause entre 5 et 10 secondes

            try:
                candidature_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Candidature simplifiée']/ancestor::button"))
                )
                candidature_button.click()

                wait = WebDriverWait(driver, 5)
                try:
                    popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content')))

                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
                    time.sleep(1)

                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Suivant"]')
                        if next_button.is_displayed():
                            next_button.click()
                            print("✅ Bouton 'Suivant' cliqué")
                            time.sleep(1)
                    except NoSuchElementException:
                        print("ℹ️ Pas de bouton 'Suivant' trouvé")

                    try:
                        submit_button = driver.find_element(By.CSS_SELECTOR,
                                                            'button[aria-label="Envoyer la candidature"]')
                        if submit_button.is_displayed():
                            submit_button.click()
                            print("✅ Bouton 'Envoyer la candidature' cliqué")
                            time.sleep(2)
                    except NoSuchElementException:
                        print("ℹ️ Pas de bouton 'Envoyer la candidature' trouvé")

                except TimeoutException:
                    print("❌ Le pop-up n'est pas apparu")

                # Fermer le pop-up
                try:
                    fermer_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Fermer']"))
                    )
                    fermer_button.click()
                    time.sleep(2)
                    print("🔒 Pop-up fermé.")
                except TimeoutException:
                    print("❌ Impossible de fermer le pop-up.")

                # On réactive le scroll de la page
                enable_scroll()

                # Attendre que le pop-up disparaisse
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content'))
                )
                print("✅ Pop-up disparu, on passe à l'offre suivante.")

            except Exception:
                print(f"⚠️ Pas de bouton 'Candidature simplifiée' pour l'offre {index + 1}. Skipping...")

        except Exception as e:
            print(f"❌ Erreur avec l'offre {index + 1} :", e)

except Exception as e:
    print("Erreur globale :", e)

finally:
    print("Fermeture du navigateur.")
    driver.quit()
