import random

timeSleep = 5
i = 1
catalog_final = []
catalog_spec_final =[] 
def parsurl(url):
    reg = requests.get(url)
    if reg.ok:
        print(reg)
        print('Начали искать ссылки!')
        soup = BeautifulSoup(reg.text)
        try:
            soup.find(class_ = 'n-snippet-card2__title')
            print('Нашли!')
            links = soup.findAll(class_ = 'n-snippet-card2__title')
            for link in links:
                print(len(links))
                url = 'https://market.yandex.ru'+str(link.find('a').attrs['href'])
                #url = 'https://market.yandex.ru'+str(links[n].find('a').attrs['href'])
                print(url)
                gettrack(url)
                print('Переход на следующую ссылку')
                
        except:
            time.sleep(random.randint(5, 20))
            print('Restat function parsul!')
            parsurl(url)
    
    
def gettrack(url):
    time.sleep(timeSleep)
    reg = requests.get(url)
    if reg.ok:
        print(reg)
        soup = BeautifulSoup(reg.text)
        try:
            link = 'https://market.yandex.ru'+ str(soup.find(class_= "n-product-tabs__item n-product-tabs__item_name_spec").find('a').attrs['href'])
            print(link)
            tableSpec(link)
        except:
            time.sleep(random.randint(5, 20))
            print('Опять на ссылках на спецификацию JS!')
            gettrack(url)
def tableSpec(url):
    global i
    time.sleep(timeSleep)
    reg = requests.get(url)
    catalog_spec = ['ID', 'Название', 'Цена']
    catalog_val =['i']
    soup = BeautifulSoup(reg.text)
    try:
        soup.find('a')
        elements = soup.findAll(class_ = 'n-product-spec')
        print(len(soup.findAll(class_ = 'n-product-spec')))
        for el in elements:
            try:
                answer = str(el.find(class_ ='n-product-spec__name-inner').text)
                try:
                    catalog_spec.append(str(answer.split('?')[0]))
                except:
                    catalog_spec.append(str(answer))
                    
            except:
                print('This is none')
        try:
            name = soup.find(class_ = 'n-title__text').find('h1').text
        except:
            name = soup.find(class_ = 'n-title__text').find('h1').find('a').text
        pattern = r'Телевизор '
        name = re.sub(pattern, '', name)
        catalog_val.append(name)
        try:
            price = soup.find(class_='price').text
            price = price[:-1]
            pattern = r'\s'
            price = re.sub(pattern, '', price)
            pattern = r'От'
            price = re.sub(pattern, '', price)
        except:
            price = 'NAN'
        
        catalog_val.append(price)      
        elements =  soup.findAll(class_ = 'n-product-spec__value')
        for el in elements:
            catalog_val.append(el.text)
            
        catalog_dict = []
        if len(catalog_spec) == len(catalog_val):
            for n in range(0, len(catalog_spec)):
                catalog = [catalog_spec[n], catalog_val[n]]
                catalog_dict.append(catalog)
        
            catalog_dict = dict(catalog_dict)
          
        elif len(catalog_spec) != len(catalog_val):
            catalog_dict = 'Nan'
        for cat in catalog_spec:
            catalog_spec_final.append(cat)
            
        #sqlAddData(row, lst)
        catalog_dict['ID'] = i 
        print(len(catalog_spec), ' ', len(catalog_val))
        print('Парсинг конечного товара закончен ', i)
        i+=1
        print('final')
        catalog_final.append(catalog_dict)
        
    except:
        time.sleep(timeSleep)
        print('Restart function tableSpec')
        tableSpec(random.randint(5, 20))
    
    
    

#url = 'https://market.yandex.ru/catalog--televizory/59601/list?hid=90639&track=pieces&onstock=1&local-offers-first=0'
#url = 'https://market.yandex.ru/product--televizor-samsung-ue49nu7100u/38452261/spec?track=tabs'
#parsurl(url)
#tableSpec(url)
for char in range(1, 3):
    url = 'https://market.yandex.ru/catalog--televizory/59601/list?hid=90639&track=pieces&onstock=1&local-offers-first=0&page='+str(char)
    print(url)
    parsurl(url)
print(catalog_final)
print('\n')
print(set(catalog_spec_final))
cat_min = catalog_final
cat_spec = set(catalog_spec_final)
finalNumber = int(cat_min[-1]['ID'])
print(finalNumber)

a1 = ''

for name in cat_spec:
    if name == 'ID':
        a1+= '['+name+'] int ,'
    if name != 'ID':
        a1+= '['+name+'] text ,'

sql = sqlite3.connect('test.db')
c = sql.cursor()
request = 'create table tvs ('+a1[:-2]+')'
print(request, '\n')
c.execute(request)
sql.commit()
c.close()
sql.close()

for name in cat_min:
    request_lst = "insert into[tvs] values ("
    for a1 in cat_spec:
        try:
            request_lst += "'"+str(name[a1])[:-1] +"',"
        except:
            request_lst += "'NAN',"
    request_lst = request_lst[:-3] + "')"
    print(request_lst)
    sql = sqlite3.connect('test.db')
    c = sql.cursor()
    c.execute(request_lst)
    sql.commit()
    c.close()
    sql.close()
    print('\n\n')