mkdir -p ~/.streamlit/

echo "[theme]
base="dark"
primaryColor="#ed0af1"
[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml
