

from fastapi import APIRouter, Request, Depends , File,  UploadFile

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from fastapi import Body

from app.services.archivo_service import (
    Archivo_service
)

import base64
import json

router = APIRouter(
    prefix="/tecnicoi/spo/sad/archivo/Archivo.svc/Archivo",
    tags=["Archivo"]
)

@router.post("/ObtenerTipoDocumentoPorAtencion")
async def obtener_tipo_doc_atencion(
    request:Request,
    db:AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    
    return await Archivo_service.obtener_tipo_doc_atencion(
        db,
        payload=payload,
        headers=dict(request.headers)
    )


@router.post("/AgregarDocumento")
async def agregar_documento(
    request:Request,
    db:AsyncSession = Depends(get_db)
):

    headers = dict(request.headers)
    datos = str(headers.get("datos"))
    payload = json.loads(
        base64.b64decode(datos)
    )

    print("headers: ",headers)
    print("payload: ",payload)
    #print("datos: ",datos)

    #return await Archivo_service.agregar_doc(
    #    db,
    #    payload=payload,
    #    headers=dict(request.headers)
    #)
