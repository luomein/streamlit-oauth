# streamlit-oauth
import streamlit as st
import os

import requests

GITHUB_CLIENT_ID = st.secrets["github_clientid"]
GITHUB_CLIENT_SECRET =  st.secrets['github_clientsecret']
GITHUB_REDIRECT_URI = st.secrets['github_redirect_uri']

#st.write("DB username:", st.secrets["github_clientid"])
#st.write('GITHUB_CLIENT_ID' ,GITHUB_CLIENT_ID )

def main():
    st.title("GitHub OAuth Login with Streamlit")

    # Step 1: Provide the GitHub login link
    if 'access_token' not in st.session_state:
        #st.write('GITHUB_CLIENT_ID' ,GITHUB_CLIENT_ID )
        login_url = f"https://github.com/login/oauth/authorize?scope=user:email&client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}"
        st.markdown(f"[Login with GitHub]({login_url})")

    # Step 2: Handle the OAuth callback
    st.write(st.query_params)
    code = st.query_params.get('code')
    if code and 'access_token' not in st.session_state:
        #code = code[0]
        st.write(code)
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        }
        token_headers = {
            "Accept": "application/json"
        }
        response = requests.post(token_url, data=token_data, headers=token_headers)
        st.write(response , response.json())
        response_json = response.json()
        access_token = response_json.get('access_token')

        if access_token:
            st.session_state['access_token'] = access_token

    # Step 3: Fetch and display user information
    if 'access_token' in st.session_state:
        access_token = st.session_state['access_token']
        user_url = "https://api.github.com/user"
        user_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_response = requests.get(user_url, headers=user_headers)
        user_data = user_response.json()

        st.write(f"Hello, {user_data['login']}!")
        st.image(user_data['avatar_url'])

if __name__ == "__main__":
    main()

