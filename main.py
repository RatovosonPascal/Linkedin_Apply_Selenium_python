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
from gpt4free import generer_reponses

load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
ville = os.getenv("ADRESSE")
poste= os.getenv("POSTE")
with open("cv.txt", "r", encoding="utf-8") as file:
    cv = file.read()
promptGpt = "je vais vous demander de me donner la reponse exact juste avec un chiffre, pas de phrase, les questions entre accolade suivant en tennant compte du CV après"


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
    time.sleep(random.randint(2, 4))

    driver.maximize_window()
    time.sleep(random.randint(2, 4))



    # Essayer de fermer l'alerte si elle existe
    try:
        alert_button = driver.find_element(By.XPATH,
                                           "//*[@id='artdeco-global-alert-container']/div/section/div/div[2]/button[2]")
        alert_button.click()
        print("Alerte fermée.")
    except:
        print("Pas d'alerte à fermer.")
    time.sleep(random.randint(2, 4))

    # Connexion
    print("Attente du bouton S'identifier...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "S’identifier"))).click()
    print("Connexion...")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    time.sleep(random.randint(2, 4))

    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating").click()

    time.sleep(random.randint(2, 4))
    # Attente pour vérifier la connexion
    print(driver.current_url)
    print(driver.page_source[:500])  # Affiche les 500 premiers caractères du HTML

    print("Recherche d'un poste...")
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Recherche']")))
    search_box.click()
    search_box.send_keys(poste)
    search_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(4, 6))


    print("Clic sur Emplois...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Emplois']"))).click()

    print("Activation du filtre Candidature simplifiée...")
    candidature_simple_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchFilter_applyWithLinkedin"))
    )
    candidature_simple_button.click()
    time.sleep(random.randint(4, 6))

    # Saisie de la ville
    print("Saisie de la ville...")
    location_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Ville, département ou code postal']"))
    )
    location_input.click()
    location_input.send_keys(Keys.CONTROL + "a")
    location_input.send_keys(Keys.BACKSPACE)
    location_input.send_keys(ville)
    time.sleep(random.randint(4, 6))

    # Clic sur Recherche
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-search-box__submit-button"))
    )
    search_button.click()

    # Attendre le rechargement des résultats
    time.sleep(random.randint(4, 6))

    offres = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-container"))
    )

    print(f"Nombre d'offres trouvées : {len(offres)}")

    for index, offre in enumerate(offres):

        #  Vérifie si un pop-up est ouvert avant de commencer l'offre suivante
        if is_popup_open():
            print(f" Pop-up détecté avant l'offre {index + 1}, attente de fermeture...")
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content'))
            )
            print(" Pop-up fermé, reprise du traitement.")

        try:
            print(f"\n Ouverture de l'offre {index + 1}...")

            # On désactive le scroll pendant le traitement de la pop-up
            if is_popup_open():
                disable_scroll()

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", offre)
            time.sleep(random.randint(1, 2))

            offre.click()
            time.sleep(random.randint(1, 2))

            try:
                candidature_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Candidature simplifiée']/ancestor::button"))
                )
                candidature_button.click()

                wait = WebDriverWait(driver, 5)
                try:
                    popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content')))
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
                    time.sleep(1)

                    while True:
                        try:
                            next_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Suivant']/ancestor::button"))
                            )
                            print("Bouton 'Suivant' trouvé et cliquable")
                            next_button.click()
                            print("Bouton 'Suivant' cliqué")
                            time.sleep(2)

                        except (NoSuchElementException, TimeoutException):
                            print("Plus de bouton 'Suivant', on continue")
                            break

                        except Exception as e:
                            print(f"Exception inattendue dans la boucle 'Suivant' : {e}")
                            break

                    questions = [] # Liste pour stocker les réponses
                    reponses = []  # Liste pour stocker les réponses générées pour chaque question

                    try:
                        # Attendre que les labels contenant des questions apparaissent
                        WebDriverWait(driver, 50).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, "//label[contains(@class, 'artdeco-text-input--label')]"))
                        )

                        # Trouver tous les éléments label qui contiennent des questions
                        elements = driver.find_elements(By.XPATH,
                                                        "//label[contains(@class, 'artdeco-text-input--label')]")

                        # Extraire le texte des questions et stocker dans la liste questions
                        for elem in elements:
                            question_text = elem.text.strip()
                            if question_text:
                                questions.append(question_text)

                        if questions:
                            print("-----------gQuestions trouvées :")
                            for idx, q in enumerate(questions, 1):
                                print(f"{idx}. {q}")

                            # Générer les réponses GPT pour chaque question
                            for idx, question in enumerate(questions):
                                # Appel de la fonction pour générer la réponse GPT pour chaque question
                                response = generer_reponses(cv,
                                                            promptGpt,question)  # Assurez-vous que cette fonction génère une réponse pour chaque question
                                reponses.append(response)  # Stocker la réponse générée

                                print(f"Réponse générée pour la question {idx} : {response}")

                            # Remplir les zones de texte avec les réponses générées
                            for idx, response in enumerate(reponses):
                                WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      f"//label[contains(text(), '{questions[idx]}')]/ancestor::div[1]//input[contains(@class, ' artdeco-text-input--input')]"))
                                )
                                # Trouver la zone de texte correspondante à la question
                                input_field = driver.find_elements(By.XPATH,
                                                                   f"//label[contains(text(), '{questions[idx]}')]/ancestor::div[1]//input[@class=' artdeco-text-input--input']")
                                if input_field:
                                    input_field[idx].click()
                                    input_field[idx].send_keys(Keys.BACKSPACE)
                                    input_field[idx].send_keys(Keys.CONTROL + "a")
                                    input_field[idx].send_keys(response)  # Remplir la zone de texte avec la réponse générée
                                    print(f"Réponse insérée pour la question {idx + 1}: {questions[idx]}")
                                else:
                                    print(f"Zone de texte non trouvée pour la question {idx + 1}: {questions[idx]}")
                        else:
                            print("Aucune question détectée.")

                    except TimeoutException:
                        print("Les questions ne se sont pas chargées à temps.")

                    time.sleep(50)

                    try:
                        verify_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[text()='Vérifier']/ancestor::button"))
                        )
                        verify_button.click()
                        print("Bouton 'Verifier' cliqué")
                        time.sleep(1)
                    except TimeoutException:
                        print("Bouton 'Verifier' introuvable ou pas cliquable")

                    try:
                        submit_button = driver.find_element(By.CSS_SELECTOR,
                                                            'button[aria-label="Envoyer la candidature"]')
                        if submit_button.is_displayed():
                            submit_button.click()
                            print("Bouton 'Envoyer la candidature' cliqué")
                            time.sleep(2)
                    except NoSuchElementException:
                        print("Pas de bouton 'Envoyer la candidature' trouvé")

                except TimeoutException:
                    print("Le pop-up n'est pas apparu")
                time.sleep(2)
                # Fermer le pop-up
                try:
                    fermer_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Fermer']"))
                    )
                    fermer_button.click()
                    time.sleep(2)
                    print("Pop-up fermé.")
                except TimeoutException:
                    print("Impossible de fermer le pop-up.")

                # On réactive le scroll de la page
                enable_scroll()

                # Attendre que le pop-up disparaisse
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'artdeco-modal__content'))
                )
                print(" Pop-up disparu, on passe à l'offre suivante.")

            except Exception:
                print(f" Pas de bouton 'Candidature simplifiée' pour l'offre {index + 1}. Skipping...")

        except Exception as e:
            print(f" Erreur avec l'offre {index + 1} :", e)

except Exception as e:
    print("Erreur globale :", e)

finally:
    print("Goodbye")

