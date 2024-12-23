from bs4 import BeautifulSoup
import requests

class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url, name = ""):
        self.name = name
        self.url = url
        self.parse_website()

    def parse_website(self):
        response = requests.get(self.url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    
    def set_relevant_links(self, relevant_links):
        self.relevant_links = relevant_links