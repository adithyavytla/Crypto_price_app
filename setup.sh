mkdir -p ~/.streamlit/

echo "
[server]
port = $PORT
enableCORS = false
headless = true
[theme]
base='dark'
primaryColor='#ed0af1'
" >> ~/.streamlit/config.toml
