from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/chat/send/")
async def chat_send(reqeust: dict):
    data = reqeust
    print("--------------New Request-----------")
    print(data)
    message = "How can I find the key"
    try: 
        
        pass
    except:
        pass
    return JSONResponse(status_code=200, content={"success": True})

if __name__=="__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=5000, reload=True)