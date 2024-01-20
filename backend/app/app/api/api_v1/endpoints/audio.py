from fastapi import APIRouter, Depends
from ....crud import crud_audio
from ....schemas import audio
from ... import deps
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from gtts import gTTS
from io import BytesIO
from ....crud import crud_audio



router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)

# works
@router.post("/", response_model=audio.Audio)
def create_Audio(Audio: audio.AudioCreate, db: Session = Depends(deps.get_db)):
    return crud_audio.Audio.create_Audio(db=db, obj_in=Audio)


# # works
# @router.get("/", response_model=List[audio.Audio])
# # def read_Audios(book_id: int, page_number: int, db: Session = Depends(deps.get_db)): 
# #     pass 

# def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):

#     # Convert text to audio
#     audio_data = crud_audio.Audio.get_audio_stream(book_id=book_id, db=db)

#     # Provide audio as a download using StreamingResponse
#     return StreamingResponse(
#         BytesIO(audio_data), media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'}
#     )


# @router.get("/text_to_audio/{book_id}")
# def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):
#     # Get audio streams
#     audio_streams = crud_audio.Audio.get_audio_stream(book_id=book_id, db=db)

#     print(audio_streams)

    # Return a list of StreamingResponse objects
    # return StreamingResponse(
    #     audio_streams[0], media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'}
    # )

@router.get("/text_to_audio/{book_id}")
def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):
    # Get audio streams
    audio_streams = crud_audio.Audio.get_audio_stream(book_id=book_id, db=db)

    # Convert async generators to regular generators
    audio_streams = [audio_stream for audio_stream in audio_streams]

    print(audio_streams)

    return StreamingResponse(
                    audio_streams[0][0], media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'},
                    )
        # i =  0
        # length = len(audio_streams)
        # while i<length:
        #     audio = StreamingResponse(
        #             audio_streams[i], media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'},
        #             )
        #     i += 1

    # Return a list of StreamingResponse objects
    # return List[audio]


# import io
# import zipfile
# from fastapi import HTTPException

# @router.get("/text_to_audio/{book_id}")
# def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):
#     # Get audio streams
#     audio_streams = crud_audio.Audio.get_audio_stream(book_id=book_id, db=db)

#     # Convert async generators to regular generators
#     audio_streams = [audio_stream for audio_stream in audio_streams]

#     # If there are no audio streams, raise an HTTP exception
#     if not audio_streams:
#         raise HTTPException(status_code=404, detail="No audio streams found")

#     # Create a zip file containing audio streams
#     with io.BytesIO() as zip_buffer:
#         with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
#             for i, audio_stream in enumerate(audio_streams, start=1):
#                 # Write each audio stream to the zip file with a unique name
#                 zip_file.writestr(f'audio_{i}.mp3', audio_stream.read())

#         # Seek to the beginning of the zip buffer
#         zip_buffer.seek(0)

#         # Return the zip file as a StreamingResponse
#         return StreamingResponse(
#             zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=audio.zip"}
#         )




# from zipfile import ZipFile
# from io import BytesIO

# def create_zip_v1():
#     """
#     returns: zip archive
#     """
#     archive = BytesIO()

#     with ZipFile(archive, 'w') as zip_archive:
#         # Create three files on zip archive
#         with zip_archive.open('docker/docker-compose.yaml', 'w') as file1:
#             file1.write(b'compose-file-content...')
        
#         with zip_archive.open('app/app-config.json', 'w') as file2:
#             file2.write(b'app-config-content...')

#         with zip_archive.open('root-config.json', 'w') as file3:
#             file3.write(b'root-config-content...')


#     return archive

# archive = create_zip_v1()

# # Flush archive stream to a file on disk
# with open('config.zip', 'wb') as f:
#     f.write(archive.getbuffer())

# archive.close()