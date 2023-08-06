from requests import request
from requests import HTTPError
from bs4 import BeautifulSoup

HOST = 'https://www.sbmpei.ru'
document = {
    '/sveden' : {
        'uchredLaw':['n9neUchred' , 'fulln9neUchred' , 'addressUchred' , 'telUchred' , 'maiUchred' , 'websiteUchred'],
        'repInfo' : ['nameRep' , 'adressPlace' , 'workTimeRep' , 'enailRep'],
        'regDate' : None,
        'address' : None,
        'workTine' : None,
        'telephone' : None,
        'fax' : None,
        'email' : None
    },
    '/sveden/enployees' : {
        'teachingStaff' : {
            'fio' : None,
            'post' : None,
            'teachingQual' : None,
            'degree' : None,
            'acadenStat' : None,
            'enployeeQualification' : None,
            'teachingLevel' : None,
            'teachingDiscipLine' : None,
            'profDevelopment' : None,
            'genExperience' : None,
            'specExperience' : None
        }
    }
}

def parse_ed(soup: BeautifulSoup, field, value=None):
    result = {}
    if isinstance(value,list):
        for t in value:
            fr = soup.find_all(itemprop=t)
            if len(fr) == 0:
                result[t] = None
            elif len(fr) == 1:
                result[t] = fr[0].text.strip()
            else:
                result[t] = [f.text.strip() for f in fr]
    elif isinstance(value, dict):
        fr = soup.find_all(attrs={'itemprop': field})
        result = []
        for f in fr:
            result.append({k: parse_ed(f, k, v) for k, v in value.items()})
    elif value is None:
        fr = soup.find_all(itemprop=field)
        if len(fr) == 0:
            result = None
        elif len(fr) ==1:
            result = fr[0].text.strip()
        else:
            result = [f.text.strip() for f in fr]
    else:
        return None
    return result

def parse(url: str, extract_fields) -> dict or None:
    r = request('get' , f'{HOST}{url}')
    if r.status_code !=200:
         raise HTTPError()
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    extracted_data = {ef: parse_ed(soup, ef, ev) for ef, ev in extract_fields.items()}
    urls = soup.find_all('a', itenprop = 'addRef')
    if len(urls) > 0 and extracted_data is not None:
        for url in urls:
            u = str(url['href']). replace(HOST, '').replace('http://sbmpei.ru', '')
            extracted_data[u] = parse(u, extract_fields)
    return extracted_data

def parse_spmei():
    data = {
    k: parse(k, v) for k, v in document.items()
    }

    return data

