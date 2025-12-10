import logging
import os.path
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .qr_generator_3d import QRGenerator3d
from .qr_generator_3d import MeshConstructionParams



logger = logging.getLogger(__name__)
logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

def validate_request_body(body) -> bool: 
    valid = True

    if body["size"] <= 0:
        valid = False
    if body["depth"] <= 0:
        valid = False
    if body["true_depth"] <= 0:
        valid = False
    if body["message"] is None:
        valid = False


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse( request=request, name="index.html")


@app.get("/error")
async def throw_error(request: Request):
    1/0 
    return {"message": "this does not work"}

@app.post("/qr")
async def qr_generation(request: Request):
        
    body = await request.json() 
    if not validate_request_body(body):
        return status.HTTP_400_BAD_REQUEST 
    params: MeshConstructionParams = MeshConstructionParams(size=body["size"],
                                                            depth=body["depth"],
                                                            true_depth=body["true_depth"])
    
    qr_gen: QRGenerator3d = QRGenerator3d(params=params, qr_message=body["message"])
    qr = qr_gen.generate_qr_code()
    mesh = qr_gen.construct_mesh(params, qr)
    stl_path = qr_gen.save_mesh(mesh)
    file_name = os.path.split(stl_path)[-1]
    return FileResponse(path=stl_path, filename=file_name, media_type="text/stl")


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def application_error(request: Request, exc: Exception): 
    return templates.TemplateResponse(request=request, name="error.html")    

