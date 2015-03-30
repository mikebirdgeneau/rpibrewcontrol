#!flask/bin/python
from app import app

#app.initialize()

app.run(debug=True,host='0.0.0.0', port=5000, use_reloader=False)
