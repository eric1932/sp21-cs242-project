if [[ -f ./venv/bin/activate ]]; then
  source ./venv/bin/activate
fi
uvicorn main:app --reload
