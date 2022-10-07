mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
[theme]\n\
base='#000000'\n\
primaryColor='#ed0af1'\n\
" >> ~/.streamlit/config.toml
