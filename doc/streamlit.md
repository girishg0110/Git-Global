# Building on Streamlit 🚧

## Google's Cloud Translation API 🌐
1. def get_translation(texts : list, from_lang : str = "en", to_lang : str = "en"): 
To query the Cloud Translation API, it is necessary to provide a list of texts that are to be translated and a language to translate them into. It is not necessary to specify the source language since Google can infer that from the given sentence with more-than-reasonable accuracy. The HTTP request is formatted as appropriate, the request is posted, the response is received, and the response is parsed for the list of text translations.

## State Transitions ➡️
1. def show_readmes():
All READMEs retrieved by the search functionality are stored in a list and accessible by st.session_state["repos"]. The indices of the visible READMEs at any point in time are stored in a list and accessible by st.session_state["visible_repos"]. show_readmes iterates through the visible repos and shows them in the main search results section.

2. def show_translated_readmes():
The selected READMEs for translation (indicated by the checkbox associated with each repo) are translated by a call to get_translation. The visible repos are updated and show_readmes is called to update the view.

3. def show_finetuned_repos(): 
First the keyword upon which to filter results is translated into English from the indicated native language of the user. Then, a lexical search is performed iteratively over all the visible repos for this keyword. The set of visible repos is updated with only those where the lexical search is successful and show_readmes is called to update the view.

4. def show_searched_repos(): 
Using get_user_repo_summaries from the scraping.py file, the "repos" session state variable is updated. Then, the visible repos are update to include all of the retrieved repos. The view is updated by a call to show_readmes.

## Sidebar Forms 📋
1. def show_search_form(): 
The search form has three fields and a button: the handle to be searched for on Github, the identification of user type (either "user" or "organization), an optional limit to the number of repositories retrieved, and a submit button.

2. def show_keyword_form(): 
The keyword form has two fields and a button: the user's native language, a keyword or phrase in their native language, and a submit button.  The native language of the user is stored in state and used later when translating Github READMEs.

3. def reset_views(): 
The reset button is linked to this function. The visible repos state variable is realigned with the full list of repos that have been retrieved ("repos" state variable). This is useful for redoing a finetuning that has filtered out too many results. 