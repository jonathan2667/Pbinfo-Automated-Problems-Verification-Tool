import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

UrlPbinfo = "https://www.pbinfo.ro/"
Mesaj1 = "Salut, ma poti ajuta te rog cu rezolvarea la problema "
Mesaj2 = " . Nu reusesc sa obtin decat un punctaj partial si nu stiu din ce cauza gresesc. Multumesc mult!"

def LogIn(driver, username, pasword) :
    driver.find_element_by_id("user").send_keys(username)
    driver.find_element_by_id("parola").send_keys(pasword)
    driver.find_element_by_xpath("//*[@id=\"form-login\"]/div/div[2]/div[4]/button").click()
    time.sleep(3)

def isproblem(driver) :
    if driver.title == "https://www.pbinfo.ro/" :
        return 0
    else :
        return 1


driverFirefox = webdriver.Firefox(executable_path=r"C:\Users\jmogo\AppData\Local\Temp\Temp1_geckodriver-v0.28.0-win64.zip\geckodriver.exe")
driverFirefox.get(UrlPbinfo)
LogIn(driverFirefox, "***", "123")
time.sleep(2)

driverChrome = webdriver.Firefox(executable_path=r"C:\Users\jmogo\AppData\Local\Temp\Temp1_geckodriver-v0.28.0-win64.zip\geckodriver.exe")
driverChrome.get(UrlPbinfo)
LogIn(driverChrome, "***", "123")
time.sleep(2)


for NrOfProblem in range (3700, 4501) :
    time.sleep(1)
    NewUrl = "https://www.pbinfo.ro/probleme/" + str(NrOfProblem)
    UrlSolOF = "https://www.pbinfo.ro/?pagina=solutie-oficiala&id=" + str(NrOfProblem)
    driverFirefox.get(NewUrl) #intru pe site la pb

    if isproblem(driverFirefox) == 1 and NrOfProblem != 3308 : #verific daca este pb
        driverFirefox.get(UrlSolOF) #intru pe site sol of
        if "numai de utilizatorii" in driverFirefox.page_source : #daca nu am pb in 500IQ
            NrOfProblemAsked = 0

            f = open("out1.txt", "a")
            NrOfProblemInString = str(NrOfProblem) + "\n"
            f.write(NrOfProblemInString)
            f.close()

            driverChrome.get(NewUrl)
            time.sleep(1.5)
            driverChrome.find_element_by_css_selector("ul.nav:nth-child(15) > li:nth-child(2) > a:nth-child(1)").click()
            driverChrome.find_element_by_css_selector(".open > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)").click()  # sunt pe pag cu sol

            UrlSolutii = driverChrome.current_url #caut pe prima pagina
            if "inexistent" in driverChrome.page_source:
                driverChrome.title
            else:
                for i in range(1, 51) :
                    if NrOfProblemAsked > 2 :
                        break
                    XpathString = "//*[@id=\"zona-mijloc\"]/div/div[6]/table/tbody/tr[" + str(i) + "]/td[7]" #Xpath punctaj
                    CssProfile = ".table > tbody:nth-child(2) > tr:nth-child(" + str(i) + ") > td:nth-child(3) > span:nth-child(1) > a:nth-child(1)" #css proofil
                    cssValue = driverChrome.find_element_by_xpath(XpathString).value_of_css_property("background-color")
                    if cssValue == "rgb(189, 255, 124)" : #255
                        driverChrome.find_element_by_css_selector(CssProfile).click()
                        time.sleep(3.5)
                        #SendMessage(driverChrome, NrOfProblem) #trimit mesaj pe daniel_radu
                        if "acestui utilizator" in driverChrome.page_source :
                            driverChrome.title
                        else:  # daca este accesebila pagina
                            if "Conversații mai vechi" in driverChrome.page_source:
                                driverChrome.title
                            else:  # daca nu am mai vbit cu el
                                driverChrome.find_element_by_xpath("//*[@id=\"zona-mijloc\"]/div/div[3]/div[2]/div[1]/div[3]/a").click()
                                time.sleep(2)
                                if "să fie contactat" in driverChrome.page_source:
                                    driverChrome.title
                                else :
                                    if driverChrome.current_url != "https://www.pbinfo.ro/profil/Prekzursil" :
                                        NrOfProblemAsked += 1
                                        driverChrome.find_element_by_css_selector("#mesaj").click()
                                        driverChrome.find_element_by_css_selector("#mesaj").send_keys(Mesaj1 + str(NrOfProblem) + Mesaj2)
                                        driverChrome.find_element_by_css_selector("input.btn").click()
                                        time.sleep(1)
                                        driverChrome.find_element_by_css_selector("div.row:nth-child(6) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > span:nth-child(2) > a:nth-child(1)").click()
                                        driverChrome.find_element_by_css_selector("li.inline:nth-child(4) > a:nth-child(1)").click()
                                        driverChrome.find_element_by_css_selector("li.inline:nth-child(4) > a:nth-child(1)").click()
                                        time.sleep(5)
                        driverChrome.get(UrlSolutii)
                if NrOfProblemAsked <= 2 :
                    for x in range(0,2) :
                        if NrOfProblemAsked > 2 :
                            break
                        if NrOfProblemAsked <= 2 :
                            if x == 0 :
                                UrlSolutii = UrlSolutii + "?start=50" #caut pe a 2a pag
                            else :
                                UrlSolutii = UrlSolutii[:-9]
                                UrlSolutii = UrlSolutii + "?start=100"  # caut pe a 2a pag
                            driverChrome.get(UrlSolutii)
                            if "inexistent" in driverChrome.page_source :
                                driverChrome.title
                            else :
                                for i in range(1, 51):
                                    if NrOfProblemAsked > 2:
                                        break
                                    XpathString = "//*[@id=\"zona-mijloc\"]/div/div[6]/table/tbody/tr[" + str(i) + "]/td[7]"
                                    CssProfile = ".table > tbody:nth-child(2) > tr:nth-child(" + str(i) + ") > td:nth-child(3) > span:nth-child(1) > a:nth-child(1)"
                                    cssValue = driverChrome.find_element_by_xpath(XpathString).value_of_css_property("background-color")
                                    if cssValue == "rgb(189, 255, 124)":
                                        driverChrome.find_element_by_css_selector(CssProfile).click()
                                        time.sleep(3.5)
                                        #SendMessage(driverChrome, NrOfProblem)  # trimit mesaj pe daniel_radu
                                        if "acestui utilizator" in driverChrome.page_source :
                                            driverChrome.title
                                        else:  # daca este accesebila pagina
                                            if "Conversații mai vechi" in driverChrome.page_source:
                                                driverChrome.title
                                            else:  # daca nu am mai vbit cu el
                                                driverChrome.find_element_by_xpath("//*[@id=\"zona-mijloc\"]/div/div[3]/div[2]/div[1]/div[3]/a").click()
                                                time.sleep(2)
                                                if "să fie contactat" in driverChrome.page_source:
                                                    driverChrome.title
                                                else:
                                                    if driverChrome.current_url != "https://www.pbinfo.ro/profil/Prekzursil":
                                                        NrOfProblemAsked += 1
                                                        driverChrome.find_element_by_css_selector("#mesaj").click()
                                                        driverChrome.find_element_by_css_selector("#mesaj").send_keys(Mesaj1 + str(NrOfProblem) + Mesaj2)
                                                        driverChrome.find_element_by_css_selector("input.btn").click()
                                                        time.sleep(1)
                                                        driverChrome.find_element_by_css_selector("div.row:nth-child(6) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > span:nth-child(2) > a:nth-child(1)").click()
                                                        driverChrome.find_element_by_css_selector("li.inline:nth-child(4) > a:nth-child(1)").click()
                                                        driverChrome.find_element_by_css_selector("li.inline:nth-child(4) > a:nth-child(1)").click()
                                                        time.sleep(5)
                                        driverChrome.get(UrlSolutii)


