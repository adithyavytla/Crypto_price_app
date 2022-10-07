mkdir -p ~/.streamlit/

echo "\
primaryColor='#020202'\n\
backgroundColor='#c4c3c3'\n\
secondaryBackgroundColor='#ebd316'\n\
font = 'sans serif'\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" >> ~/.streamlit/config.toml
