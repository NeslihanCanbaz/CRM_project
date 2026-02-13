import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from backend.auth import auth


def download_file(real_file_id):
  """Downloads a file
  Args:
      real_file_id: ID of the file to download
  Returns : IO object with location.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = auth()



  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_id = real_file_id

    file_metadata = service.files().get(fileId = file_id).execute()
    name = file_metadata.get("name")

  

    # pylint: disable=maybe-no-member
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}.")

    with open(f"{name}", "wb") as f:
      f.write(file.getvalue())

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

# #dosya yok diye hata veriyr onun icin ekledim
#     if file is None or file.getbuffer().nbytes == 0:
#         print("File could not be downloaded or is empty")
#         return None

  return file.getvalue()


if __name__ == "__main__":
  download_file(real_file_id="1pKafh72kSlNyl4N2wrd8D3oeduRrlP34")