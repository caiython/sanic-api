from sanic import Sanic, json

app = Sanic("sanic-api")

@app.get('/')
async def hello_world(request):
    return json({'Hello': 'World!'}, status=200)