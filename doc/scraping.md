# Scraping Github

## The GithubClient Class
The GithubClient class has three static methods. 
1. get_user_repo_summaries(username : str, user_type : str)
Taking a Github username and user_type ("user" or "org") as input, this method returns a list of repo summary dictionaries (fields listed and explained in get_repo_summary). This method coordinates the pipeline of get_user_repo_links (which fetches all repositories listed across a user's "Repositories" tab pages) and get_repo_summary (which fetches the README information for a single repo).

2. get_user_repo_links(username : str, user_type : str)
Taking a Github username and user_type ("user" or "org") as input, this method makes HTTP requests iteratively over the "Repositories" tab pages of the user. The parsing logic for organizations differs from that for developer accounts. Within each page, all repository links are scraped. Currently, the iteration over pages ends when there are no repositories on a page, meaning it queries one page that does not exist.

3. get_repo_summary(rel_link : str)
Taking a relative link to a Github repository as input, this method makes an HTTP request to the Github repository pointed to by that link. Then, the README.md display element is isolated and its content parsed. The information contained therein is returned in a dict suitable for the remaining functionality of Git-Global (see the comments in get_repo_summary for more information on the fields returned).

## Judicious Use
When scraping websites it is important to be judicious about the load we place onto the target websites. There are a number of steps that we can take to mitigate any adverse impacts in this regards.

The most effective is to place an intentional limit on the number of READMEs that are fetched when a search query is executed. 
1. We can limit the number of "Repositories" tab pages scraped. Each page has up to 30 repositories during the scraping process.
2. We can limit the number of repos opened and scraped directly. 

Both of these functionalities are implemented in the Streamlit deployment of this project and in the scrape.py methods. Feel free to use those parameters as well as to experiment with alternative ways of fetching the relevant data while reducing the cumulative server load (i.e. looking at Github's developer APIs). 