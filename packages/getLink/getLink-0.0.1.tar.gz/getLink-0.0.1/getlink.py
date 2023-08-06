class GetLink():
    def __init__(self, cik, company):
        self._cik = cik
        self._company = company
        self.url = f"https://www.sec.gov/edgar/search/?r=el#/q=485bpos&page=1&ciks={self._cik}&entityName={self._company.upper()}"
        print(f"You will find cik {self._cik} for Company {self._company} in url {self.url}")



GetLink(cik="0001021882", company="VANGuARd")
    
