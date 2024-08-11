import csv
import PyPDF2
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

a = PyPDF2.PdfReader('testroll.pdf')

extracted_text = []

for i in range(len(a.pages)):
    text = a.pages[i].extract_text()
    extracted_text.append(text)
    
    
csv_file = 'extracted_text.csv'

def join(lst):
    string=""
    for i in lst:
        string+=i+" "
    return string.strip()
    

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for text in extracted_text:
        lines=text.split('\n')
        for line in lines:
            words=line.split()
            
            try:
                if words[0][0].isdigit() and len(words)!=0:
                    writer.writerow([words[2],join(words[3:-1])])
            except:
                pass


with open(csv_file, 'r', encoding='utf-8') as file:
    reader=csv.reader(file)
    for i in reader:
        print(i)

    
os.environ['PATH'] += r"C:\Users\Home\AppData"

letters = "SRATPJMDCBKLEGNHIFUVWYOZQX"



def func():
    flag=0
    with open('extracted_text.csv', mode='r') as file:
        reader = csv.reader(file)
        for i in reader:
            name=i [1]
            rollno= i[0]
            try:
                realroll = rollno
            except:
                print("Student not found!")
                flag=1

            if flag==0:
                rollno = str(rollno)
                rollno = rollno[5:7]

                admit = name[0] + '_' + rollno + "2794"

                i = 0

                driver = webdriver.Chrome()
                driver.get("https://cbseresults.nic.in/class_xii_2023/ClassTwelfth_c_2023.htm")
                driver.implicitly_wait(2)

                while True:
                    roll = driver.find_element(By.NAME, 'regno')
                    roll.send_keys(realroll)

                    school = driver.find_element(By.NAME, 'sch')
                    school.send_keys(27130)


                    admid = driver.find_element(By.NAME, 'admid')
                    new_admit = admit[:1] + letters[i] + admit[2:]
                    admid.clear()
                    admid.send_keys(new_admit)

                    submit = WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.CLASS_NAME,'btn'))
                        )

                    submit.click()

                    check=driver.find_elements(By.XPATH, "//*[contains(text(), 'Result Not Found')]")
                    if check:
                        pass
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, '*')

                        desired_width = 36
                        desired_height = 15
                        matching_elements = []
                        
                        for element in elements:
                            width = element.size['width']
                            height = element.size['height']
                            if width == desired_width and height == desired_height:
                                matching_elements.append(element.text)

                        sum=0
                        for i in matching_elements:
                            i=int(i)
                            sum+=i
                            
                        sum=(sum/500)*100
                        print(sum)
                        
                        file=open("results.csv",'a',newline="")
                        obj=csv.writer(file)
                        lst=[name,sum]
                        obj.writerow(lst)
                        print("record added!")
                        driver.quit()
                        break
                    
                    back = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Check Another Result')]"))
                    )
                    back.click()

                    i += 1


while True:
    func()

megalist=[]

file=open("results.csv",'r')
reader=csv.reader(file)
for i in reader:
    megalist.append(i)
file.close()

print(sorted(megalist))


with open("results.csv",'w',newline='') as file:
    writer=csv.writer(file)
    writer.writerows(megalist)

print("thank you :)")
