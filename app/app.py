import logging
import os.path
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .qr_generator_3d import QRGenerator3d
from .qr_generator_3d import MeshConstructionParams



logger = logging.getLogger(__name__)
logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO, filemode="w")
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
    return valid

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse( request=request, name="index.html")


@app.post("/qr")
async def qr_generation(request: Request, response: Response):
    """
    constructs a qr code as a 3d object, by creating a depth for when a module is false, 
    and another depth for when a module is considered true

    :request request: a request object containing a json body
    :returns FileResponse: a blob containing an stl
    
    """
    body = await request.json() 
    logging.info(body) 
    if not validate_request_body(body):
        logging.info("Bad user request")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 
    params: MeshConstructionParams = MeshConstructionParams(size=body["size"],
                                                            depth=body["depth"],
                                                            true_depth=body["true_depth"])
    
    qr_gen: QRGenerator3d = QRGenerator3d(params=params, qr_message=body["message"])
    qr = qr_gen.generate_qr_code()
    mesh = qr_gen.construct_mesh(params, qr)
    stl_path = qr_gen.save_mesh(mesh)
    file_name = os.path.split(stl_path)[-1]
    logging.info("Post qr generation")
    return FileResponse(path=stl_path, filename=file_name, media_type="text/stl")


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def application_error(request: Request, exc: Exception): 
    return templates.TemplateResponse(request=request, name="error.html")    

