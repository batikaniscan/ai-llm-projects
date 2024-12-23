"""
Project #1 : Company Brochure

Enter a website name and main website URL to generate a company brochure.
Generate a relevant image to add to the brochure.
Week 1 Community contributions company brochure, Week 2 day 2, Week 2 day 5
"""

from utils.load_openai_client import create_openai_client
from projects.website import Website
import json

openai = create_openai_client()

question = """
You are provided with the following prompt that asks an AI model to extract pertinent links from a list of links. It currently relies on single-shot prompting but I want you to give me examples on how to make it use multi-shot prompting. Give me several examples to test out.
The prompt in question: You are provided with a list of links found on a webpage. You are able to decide which of the links would be most relevant to include in a brochure about the company, such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

link_system_prompt = """
    You are provided with a list of links found on a webpage. You are able to decide which of the links would be most
    relevant to include in a brochure about the company, such as links to an About page, or a Company page, or Careers/Jobs pages. You should
    respond in JSON as in this example:"
    {
            "links":[
                {"type": "about page", "url": "https://full.url/goes/here/about"},
                {"type": "careers page": "url": "https://another.full.url/careers"}
            ]
        }
    """

brochure_generation_system_prompt = """
    You are an assistant that analyzes the contents of several relevant pages from a company website and creates a short brochure about the
    company for prospective customers, investors and recruits. Respond in markdown. Include details of company culture, customers and careers/jobs
    if you have the information.
"""

def get_relevant_links_user_prompt(website: Website):
    link_user_prompt = f"""
        Here is the list of links on the website of {website.url} - please decide which of these are relevant web links
        for a brochure about the company, respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, email links.
        Links (some might be relative links):
    """
    link_user_prompt += "\n".join(website.links)
    return link_user_prompt

def get_brochure_user_prompt(website: Website):
    user_prompt = f"""
        You are looking at a company called: {website.name}
        Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.
    """
    user_prompt += get_company_details(website)
    user_prompt = user_prompt[:20_000] # Truncate if more than 20,000 characters
    return user_prompt

def get_website_links(website: Website):
    relevant_links_response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_relevant_links_user_prompt(website)}
        ],
        response_format={"type":"json_object"}
    )
    return json.loads(relevant_links_response.choices[0].message.content)

def get_company_details(website: Website):
    result = "Landing page:\n"
    result += Website(website.url).get_contents()
    links = get_website_links(website)
    
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    
    return result

def generate_company_brochure(company_name, company_url):
    website = Website(company_url, company_name)

    stream = openai.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {"role": "system", "content": brochure_generation_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(website)}
          ],
        stream = True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

if __name__ == "__main__":
    print("testing")
    web = Website("https://huggingface.co")