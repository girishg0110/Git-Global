import requests
from bs4 import BeautifulSoup

class GithubClient:

    def get_user_repo_summaries(username : str, user_type : str, page_limit : int = float("inf"), link_limit : int = float("inf")):
        repo_links = GithubClient.get_user_repo_links(username, user_type, link_limit = link_limit, page_limit = page_limit)
        user_repo_summaries = []
        for link in repo_links:
            repo_summary = GithubClient.get_repo_summary(link)
            if repo_summary:
                user_repo_summaries.append(repo_summary)
        return user_repo_summaries

    def get_user_repo_links(username : str, user_type : str, page_limit : int = float("inf"), link_limit : int = float("inf")):
        # returns links
        base_link = f"https://github.com/orgs/{username}/repositories?page=" if user_type == "org" \
            else f"https://github.com/{username}?tab=repositories&page="
        repo_links = []

        page_number = 1
        while True:
            resp = requests.get(base_link + str(page_number))
            soup = BeautifulSoup(resp.content, features="html.parser")

            if user_type == "org":
                repos = soup.find_all(attrs = {"class" : "Box-row"})
            else:
                user_repositories_list = soup.find(id="user-repositories-list")
                repos = user_repositories_list.find_all("li")
            if not repos:
                break

            repo_links.extend([row.find('a')["href"] for row in repos])
            if page_number == page_limit:
                break
            page_number += 1
        
        link_count_bound = min(link_limit, len(repo_links))
        return repo_links[:link_count_bound]

    def get_repo_summary(rel_link : str):
        base_link = "https://github.com" + rel_link
        resp = requests.get(base_link)
        soup = BeautifulSoup(resp.content, features="html.parser")

        title = soup.find("title").string
        readme = soup.find(id="readme")
        if not readme:
            return {}
        readme_html = str(readme)
        readme_text = list(filter(lambda x: x.strip(), readme.find_all(text=True)))

        return {
            "title" : title, 
            "readme_text" : readme_text, 
            "readme_html" : readme_html
        }
