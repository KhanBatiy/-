from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_wikipedia_earth_oxygen():
    """
    Тест для проверки содержания кислорода в атмосфере Земли на странице Википедии.
    """
    # Инициализация драйвера с автоматической установкой ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Шаг 1: Переход на главную страницу Википедии
        driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        print("Открыта главная страница Википедии")
        
        # Шаг 2: Поиск поля ввода поиска
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        print("Найдено поле поиска")
        
        # Шаг 3: Ввод слова "Земля" и нажатие Enter
        search_input.clear()
        search_input.send_keys("Земля")
        search_input.send_keys(Keys.RETURN)
        print("Выполнен поиск по запросу 'Земля'")
        
        # Шаг 4: Ожидание появления страницы с результатами поиска и клик по ссылке "Земля"
        # Ищем ссылку с title="Земля" и href="/wiki/%D0%97%D0%B5%D0%BC%D0%BB%D1%8F"
        earth_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//a[@title='Земля' and @href='/wiki/%D0%97%D0%B5%D0%BC%D0%BB%D1%8F']"))
        )
        print("Найдена ссылка на статью 'Земля' в результатах поиска")
        
        # Кликаем по ссылке
        earth_link.click()
        print("Выполнен переход на страницу статьи 'Земля'")
        
        # Шаг 5: Ожидание загрузки страницы о Земле
        WebDriverWait(driver, 10).until(
            lambda d: "Земля" in d.title or "ru.wikipedia.org/wiki/Земля" in d.current_url
        )
        print("Страница о Земле загружена")
        
        # Шаг 6: Поиск элемента с информацией о составе атмосферы
        # Ищем div с style="margin-left:1em", который содержит информацию о составе атмосферы
        # Сначала пробуем найти div с точным стилем или содержащим margin-left:1em
        atmosphere_divs = driver.find_elements(By.XPATH, 
            "//div[contains(@style, 'margin-left:1em') or @style='margin-left:1em']")
        
        oxygen_element = None
        for div in atmosphere_divs:
            div_text = div.text
            if "20,95" in div_text and "кислород" in div_text.lower():
                oxygen_element = div
                break
        
        # Если не нашли через стиль, ищем любой элемент, содержащий и процент, и слово кислород
        if not oxygen_element:
            try:
                oxygen_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//div[contains(., '20,95') and contains(., 'кислород')] | "
                        "//*[contains(text(), '20,95') and contains(text(), 'кислород')]"))
                )
            except:
                # Последняя попытка: ищем любой элемент с текстом "20,95"
                all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '20,95')]")
                for elem in all_elements:
                    parent_text = elem.find_element(By.XPATH, "./..").text
                    if "кислород" in parent_text.lower():
                        oxygen_element = elem.find_element(By.XPATH, "./..")
                        break
        
        # Проверка наличия элемента
        assert oxygen_element is not None, "Элемент с информацией о кислороде не найден"
        
        # Получаем текст элемента
        element_text = oxygen_element.text
        
        # Проверка: содержит ли текст информацию о 20,95% кислорода
        assert "20,95" in element_text, f"Текст не содержит '20,95'. Найденный текст: {element_text[:200]}"
        assert "кислород" in element_text.lower(), f"Текст не содержит 'кислород'. Найденный текст: {element_text[:200]}"
        
        print(f"✓ Тест пройден успешно! Найдена информация о содержании кислорода: 20,95%")
        print(f"  Фрагмент текста: {element_text[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Тест не пройден. Ошибка: {str(e)}")
        raise
        
    finally:
        # Закрытие браузера
        driver.quit()
        print("Браузер закрыт")


def test_wikipedia_search_nonexistent_article():
    """
    Негативный тест: проверка поиска несуществующей статьи в Википедии.
    Ожидается, что будет показано сообщение об отсутствии результатов или предложение создать статью.
    """
    # Инициализация драйвера с автоматической установкой ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Шаг 1: Переход на главную страницу Википедии
        driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        print("Открыта главная страница Википедии")
        
        # Шаг 2: Поиск поля ввода поиска
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        print("Найдено поле поиска")
        
        # Шаг 3: Ввод несуществующего запроса (случайная комбинация букв)
        nonexistent_query = "Абвгд12345НесуществующаяСтатья"
        search_input.clear()
        search_input.send_keys(nonexistent_query)
        search_input.send_keys(Keys.RETURN)
        print(f"Выполнен поиск по запросу '{nonexistent_query}'")
        
        # Шаг 4: Ожидание загрузки страницы результатов
        time.sleep(2)
        
        # Шаг 5: Проверка, что мы попали на страницу с результатами поиска или сообщением об отсутствии результатов
        # Ищем индикаторы того, что статья не найдена:
        # - Текст "Создать страницу" или "Создать статью"
        # - Текст "ничего не найдено" или "не найдено"
        # - Или URL содержит "search" (страница поиска)
        
        page_text = driver.page_source.lower()
        current_url = driver.current_url
        
        # Проверяем, что мы не на странице существующей статьи
        assert "ru.wikipedia.org/wiki/" + nonexistent_query.lower().replace(" ", "_") not in current_url.lower(), \
            f"Неожиданно найдена статья по запросу '{nonexistent_query}'"
        
        # Проверяем наличие индикаторов отсутствия результатов
        has_no_results = (
            "создать" in page_text and ("страницу" in page_text or "статью" in page_text) or
            "не найдено" in page_text or
            "ничего не найдено" in page_text or
            "search" in current_url.lower()
        )
        
        assert has_no_results, \
            f"Не найдены индикаторы отсутствия результатов для запроса '{nonexistent_query}'. URL: {current_url}"
        
        print(f"✓ Негативный тест пройден успешно! Статья '{nonexistent_query}' не найдена, как и ожидалось.")
        print(f"  Текущий URL: {current_url}")
        
        return True
        
    except AssertionError as e:
        print(f"✗ Негативный тест не пройден. Ошибка: {str(e)}")
        raise
    except Exception as e:
        print(f"✗ Негативный тест не пройден. Неожиданная ошибка: {str(e)}")
        raise
        
    finally:
        # Закрытие браузера
        driver.quit()
        print("Браузер закрыт")


if __name__ == "__main__":
    print("=" * 60)
    print("Запуск позитивного теста: проверка содержания кислорода")
    print("=" * 60)
    test_wikipedia_earth_oxygen()
    
    print("\n" + "=" * 60)
    print("Запуск негативного теста: поиск несуществующей статьи")
    print("=" * 60)
    test_wikipedia_search_nonexistent_article()
    
    print("\n" + "=" * 60)
    print("Все тесты выполнены!")
    print("=" * 60)


