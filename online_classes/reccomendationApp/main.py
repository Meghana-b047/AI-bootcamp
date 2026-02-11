from server import *

if __name__ =="__main__": 

    import uvicorn 
    uvicorn.run('main:app', reload=True)