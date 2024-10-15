import os
import socket
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Return hostname by JSON
@app.get("/hostname", status_code=200)
def hostname():
    if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount') or os.getenv('KUBERNETES_SERVICE_HOST') is not None:
        hostname = os.environ.get("HOSTNAME")
        return {
                "hostname": {hostname}
            }
    else:
        hostname = socket.gethostname()
    
# Return hostname, request headers by HTML
@app.get("/", status_code=200)
def welcome(request: Request):

    if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount') or os.getenv('KUBERNETES_SERVICE_HOST') is not None:
        hostname = os.environ.get("HOSTNAME")
    else:
        hostname = socket.gethostname()
    
    header_list = ""
    for item in request.headers.items():
        header_list += f"<li>{item[0]}: {item[1]}</li>"
    
    html_content = f"""
                <html>
                    <head>
                        <title> Welcome Page </title>
                    </head>
                    <body>
                        <h1> Welcome to my sample FastAPI Server </h1>
                        <ul>
                            <li> <strong>Server Hostname:</strong> {hostname}</li> 
                            <li> <strong>Client Information:</strong> </li> 
                            <li> <strong>request_header:</strong> </li>
                                <ul>
                                    {header_list}
                                </ul> 
                            <li> <strong>request_method:</strong> {request.method}</li> 
                            <li> <strong>request_address:</strong> {request.client}</li> 
                            <li> <strong>request_path_params:</strong> {request.path_params}</li> 
                            <li> <strong>request_query_params:</strong> {request.query_params}</li> 
                            <li> <strong>request_url:</strong> {request.url} </li>
                        </ul>
                    </body>
                </html>
            """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run("app:app", 
                host="0.0.0.0", 
                port=8000, 
                log_level="debug", 
                reload=True, 
                access_log=True)