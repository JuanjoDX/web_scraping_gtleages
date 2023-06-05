from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime

# Se define la funcion obtener_data la cual se encarga de traer los equipos que juegan, los jugadores, el horario, resultado y el estado del encuentro, los organiza
# y devuelve un df 

def obtener_data():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Equipos 

    eq = soup.find_all("div", class_ = "flex flex-column flex-center")
    equipos = list()
    for i in eq:
        equipos.append(i.text)

    # Jugadores

    jug = soup.find_all("strong")
    jugadores = list()
    for i in jug:
        jugadores.append(i.text)

    # Horario 

    hora = soup.find_all("td", class_ = "MuiTableCell-root MuiTableCell-body MuiTableCell-alignLeft")
    horarios = list()
    for i in hora:
        horarios.append(i.text)

    # Resultado

    res = soup.find_all('input', {'value': True})
    resultados = [elemento['value'] for elemento in res][:-1]

    # Estado

    est = soup.find_all("span", class_ = "MuiChip-label")
    estado = list()
    for i in est:
        estado.append(i.text)

    localeq = equipos[::2]
    visitaeq = equipos[1::2]

    localjug = jugadores[::2]
    visitajug = jugadores[1::2]

    horarios = horarios[3::10]

    localres = resultados[::2]
    visitares = resultados[1::2]

    return(pd.DataFrame({'Fecha': horarios, 'Equipo Local': localeq, 'Jugador Local': localjug,
                          'Equipo Vista': visitaeq, 'Jugador Visita': visitajug,
                          'Resultado Local': localres,"Resultado Visita": visitares, "Estado": estado}))


# la funcion data_dia se encarga de ir por cada uno de los dias de juego de partidos y recolectar la información llamando la funcion obtener_data 

def data_dia(dia):
    # esperar a que cargue la página
    time.sleep(15)
    
    try:
        botondia = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="flex justify-center p-4 my-4 bg-white"]//div[text()="{0}"]'.format(dia))))
        botondia.click()
        
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", botondia)
   
    # esperar a que cargue la página
    time.sleep(15)

    # Localiza el elemento que representa el menú desplegable.
    select_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='MuiSelect-root MuiSelect-select MuiTablePagination-select MuiSelect-selectMenu MuiInputBase-input']")))
    select_element.click()

    option_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//li[@role='option' and @data-value='100']")))
    option_element.click()

    datos = pd.DataFrame(columns=['Fecha', 'Equipo Local', 'Jugador Local', 'Equipo Vista',
                                  'Jugador Visita', 'Resultado Local', 'Resultado Visita', 'Estado'])

    con = 1
    while True:
        time.sleep(5)
        try:
            print(con)
            df = obtener_data()
            datos = pd.concat([datos,df])

            time.sleep(3)

            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Next Page"]/button')))
            next_button.click()
            con +=1

        except TimeoutException:
            print("No hay más páginas")
            break
            
    return(datos)

### Finalmente se abre la pagina y se obtiene la informacion para el dia actual

# abrir la página web con Selenium
driver = webdriver.Chrome()
driver.get("https://www.gtleagues.com/past-results")
driver.minimize_window()

fecha_actual = datetime.datetime.now()
dias = [fecha_actual.strftime("%d %b")] ### en caso de querer un dia en especifico debe ser menor a 5 dias atras

for i in dias:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    time.sleep(5)
    data_dia(i).to_csv("../Datos/" + i.replace(" ","_") + ".csv",index = False,encoding = "utf-8-sig")
    time.sleep(5)
    
driver.quit()

