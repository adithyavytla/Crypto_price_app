mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor='#ed0af1'\n\
backgroundColor='#0E1117'\n\
secondaryBackgroundColor='#262730'\n\
textColor='#FAFAFA'\n\
font = 'sans serif'\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" >> ~/.streamlit/config.toml
