import os
import time
import datetime
from datetime import datetime
import asyncio
import string
import random
import shutil
import pytz
from PyPDF2 import PdfReader, PdfFileReader, PdfWriter
from PIL import Image
import requests
import weasyprint
import urllib.request
from translation import Translation 
from bs4 import BeautifulSoup
from pyrogram import Client,filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


TOKEN = os.environ.get("TOKEN", "5752725687:AAH-IgljX7Jtqfb7pl6CyooMhjVD14ib0BQ")

API_ID = int(os.environ.get("API_ID", "534493"))

API_HASH = os.environ.get("API_HASH", "ac922823455e814e44020a9f3ee17914")

app = Client(
        "pdf",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )


LIST = {}

tz = pytz.timezone("Asia/Kolkata")

#currentTime = datetime.datetime.now()
currentTime = datetime.now(tz)

if currentTime.hour < 12:
	wish = "Good morning..."
elif 12 <= currentTime.hour < 16:
	wish = 'Good afternoon...'
else:
	wish = 'Good evening...'


@app.on_message(filters.command(['start', 'help']))
async def start(client, message):
 await message.reply_text(text=f"""{wish}
Hello [{message.from_user.first_name }](tg://user?id={message.from_user.id})

i can convert images to pdf and more…""", reply_to_message_id = message.message_id, reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support Group", url="https://t.me/NewBotzSupport"),
                    InlineKeyboardButton("Update Channel", url="https://t.me/NewBotz") ]       ]        ) )


@app.on_message(filters.command(['id']))
async def id(client, message):
 await client.send_chat_action(message.chat.id, "typing")
 await message.reply_text(text=f'Your ID - `{message.chat.id}`', reply_to_message_id=message.message_id)


@app.on_message(filters.private & filters.photo)
async def pdf(client,message):
 
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.photo.file_id)
 
 ms = await message.reply_text("Converting to PDF ......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} image   Successful created PDF if you want add more image Send me One by one\n\n **if done click here 👉 /convert** ")
 

@app.on_message(filters.private & filters.document)
async def pdf(client,message):
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.document.file_id)

 isPdfOrImg = message.document.file_name
 fileSize = message.document.file_size
 fileNm, fileExt = os.path.splitext(isPdfOrImg)
 suprtedFile = ['.jpg','.jpeg','.png']
 if fileExt in suprtedFile and fileSize <= 10000000:
  ms = await message.reply_text("Converting to PDF ......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} image   Successful created PDF if you want add more image Send me One by one\n\n **if done click here 👉 /convert** ")
 

@app.on_message(filters.command(['cancel']))
async def cancel(client, message):
 images = LIST.get(message.from_user.id)
 if not images:          
   await client.send_message(message.chat.id, f"Nothing to Cancel", reply_to_message_id=message.message_id)
   return
 await client.send_message(
   chat_id=message.chat.id,
   text=f"Cancelled your process",
   reply_to_message_id=message.message_id
 )
 del LIST[message.from_user.id]
 shutil.rmtree(f"{message.chat.id}")


@app.on_message(filters.command(['convert']))
async def done(client,message):
 images = LIST.get(message.from_user.id)
 abcd = await message.reply_text( "Uploading your PDF")
 
 if isinstance(images, list):
  pgnmbr = len(LIST[message.from_user.id])
 if not images:
  await abcd.edit( "No image !!")
  return
 #removed thumbnail support if u want u can add
 #thumb_path = os.path.join(os.getcwd(), "img")
 #if not os.path.isdir(thumb_path):
  #os.makedirs(thumb_path)
  #urllib.request.urlretrieve(Translation.THUMB_URL, os.path.join(thumb_path, "thumbnail.png"))
 #else:
  #pass
    
 #thumbnail = os.path.join(os.getcwd(), "img", "thumbnail.png")
 path = f"{message.from_user.id}" + ".pdf"

 images[0].save(path, save_all = True, append_images = images[1:])
 
 msg = await client.send_document(message.from_user.id, open(path, "rb"), caption = "Here your pdf !!\n\nTotal Pages:{}".format(pgnmbr)) #, thumb = thumbnail)
 os.remove(path)
 await abcd.delete()
 

@app.on_message(filters.command(['compress']))
async def compress_pdf(client, message):
 if message.chat.id not in LIST:          
  await client.send_message(message.chat.id, f"Send me a pdf first 😅", reply_to_message_id=message.message_id)
  return

 if message.reply_to_message is not None:
  file_s = message.reply_to_message
  a = await client.send_message(
   chat_id=message.chat.id,
   text=f"Processing…",
   reply_to_message_id=message.message_id
  )
  c_time = time.time()
  file = await client.download_media(file_s, progress_args=(f"Processing…", a, c_time))
  
  reader = PdfReader(file)
  writer = PdfWriter()

  for page in reader.pages:
   page.compress_content_streams()  # This is CPU intensive!
   writer.add_page(page)

  path = f"{message.from_user.id}" + ".pdf"

  with open("path", "wb") as f:
   writer.write(f)

  msg = await client.send_document(message.from_user.id, path) #open(path, "rb"), caption = "Here your pdf !!\n\nTotal Pages:{}".format(pgnmbr)) #, thumb = thumbnail)
  await abcd.delete()
  os.remove(file)


@app.on_message(filters.command(['info']))
async def pdf_info(client, message):
 if message.chat.id not in LIST:          
  await client.send_message(message.chat.id, f"Send me a pdf first 😅", reply_to_message_id=message.message_id)
  return

 if message.reply_to_message is not None:
  file_s = message.reply_to_message
  a = await client.send_message(
   chat_id=message.chat.id,
   text=f"Processing…",
   reply_to_message_id=message.message_id
  )
  c_time = time.time()
  file = await client.download_media(file_s, progress_args=(f"Processing…", a, c_time))
  reader = PdfReader(file)
  pdf_page_count = len(reader.pages)
  meta = reader.metadata
  await a.edit_text(f"The informations on the given PDF file\n\n**Pages** = {pdf_page_count}\n**Author:** {(meta.author)}\n**Creator:** {(meta.creator)}\n**Producer:** {(meta.producer)}\n**Subject:** {(meta.subject)}\n**Title:** {(meta.title)}")
   
  os.remove(file)


@app.on_message(filters.command(['pdf2text']))
async def pdftotext(client, message):
 if message.chat.id not in LIST:          
  await client.send_message(message.chat.id, f"Send me a pdf first 😅", reply_to_message_id=message.message_id)
  return

 if message.reply_to_message is not None:
  file_s = message.reply_to_message
  a = await client.send_message(
   chat_id=message.chat.id,
   text=f"Processing…",
   reply_to_message_id=message.message_id
  )
  c_time = time.time()
  file = await client.download_media(file_s, progress_args=(f"Processing…", a, c_time))

  read_pdf = PdfFileReader(file)
  page = read_pdf.getPage(0)
  page_content = page.extractText()
  await message.reply_text(f"{page_content}",  parse_mode="html", disable_web_page_preview=True, reply_to_message_id = message.message_id)
  await a.delete()
  await os.remove(file)


@app.on_message(filters.private & filters.text)
async def link_extract(client, message):
    if not message.text.startswith("http"):
        await message.reply_text(
            Translation.INVALID_LINK_TXT,
            reply_to_message_id=message.message_id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_btn")]]
            )
        )
        return
    file_name = str()
    
    #thumb_path = os.path.join(os.getcwd(), "img")
    #if not os.path.isdir(thumb_path):
        #os.makedirs(thumb_path)
        #urllib.request.urlretrieve(Translation.THUMB_URL, os.path.join(thumb_path, "thumbnail.png"))
    #else:
        #pass
    
    #thumbnail = os.path.join(os.getcwd(), "img", "thumbnail.png")
    
    await client.send_chat_action(message.chat.id, "typing")
    msg = await message.reply_text(Translation.PROCESS_TXT, reply_to_message_id=message.message_id)
    try:
        req = requests.get(message.text)
        # using the BeautifulSoup module
        soup = BeautifulSoup(req.text, 'html.parser')
        # extracting the title frm the link
        for title in soup.find_all('title'):
            file_name = str(title.get_text()) + '.pdf'
        # Creating the pdf file
        weasyprint.HTML(message.text).write_pdf(file_name)
    except Exception:
        await msg.edit_text(
            Translation.ERROR_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_btn")]]
            )
        )
        return
    try:
        await msg.edit(Translation.UPLOAD_TXT)
    except Exception:
        pass
    await client.send_chat_action(message.chat.id, "upload_document")
    msgg = await message.reply_document(
        document=file_name,
        caption=Translation.CAPTION_TXT.format(file_name)
        #thumb=thumbnail
    )
    try:
        os.remove(file_name)
    except Exception:
        pass
    await msg.delete()


# --------------------------------- Close Button Call Back --------------------------------- #
@app.on_callback_query(filters.regex(r'^close_btn$'))
async def close_button(self, cb: CallbackQuery):
    await self.delete_messages(
        cb.message.chat.id,
        [cb.message.reply_to_message.message_id, cb.message.message_id]
    )

 
app.run()
