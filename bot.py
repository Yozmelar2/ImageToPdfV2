import os
import time
import datetime
import asyncio
import string
import random
import shutil
from PyPDF2 import PdfReader
from PIL import Image
import requests
import weasyprint
import urllib.request
from translation import Translation 
from bs4 import BeautifulSoup
from pyrogram import Client,filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


TOKEN = os.environ.get("TOKEN", "")

UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))

API_ID = int(os.environ.get("API_ID", 12345))

API_HASH = os.environ.get("API_HASH", "")
app = Client(
        "pdf",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )


LIST = {}

#os.environ['TZ'] = "Kolkata"

currentTime = datetime.datetime.now()

if currentTime.hour < 12:
	wish = "Good morning"
elif 12 <= currentTime.hour < 18:
	wish = 'Good afternoon.'
else:
	wish = 'Good evening.'


@app.on_message(filters.command(['start', 'help']))
async def start(client, message):
 #await client.send_message(LOG_CHANNEL, f"**New User Joined:** \n\nUser [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started Bot!!")
 await message.reply_text(text=f"""{wish}
Hello [{message.from_user.first_name }](tg://user?id={message.from_user.id})

i can convert images & Web Page to pdf \nAlso count Total Pages from PDF""", reply_to_message_id = message.message_id, reply_markup=InlineKeyboardMarkup(
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
 if UPDATE_CHANNEL:
  try:
   user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
   if user.status == "kicked":
    await message.reply_text(" Sorry, You are **B A N N E D**")
    return
  except UserNotParticipant:
   # await message.reply_text(f"Join @{UPDATE_CHANNEL} To Use Me")
   await message.reply_text(
    text="**Please Join My Update Channel Before Using Me..**",
    reply_markup=InlineKeyboardMarkup([
    [ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/{UPDATE_CHANNEL}")]
    ])
   )
   return
  else:
   ms = await message.reply_text("Converting to PDF ......")
 file = await client.download_media(file_id)
 p = await message.forward(LOG_CHANNEL)
 trace_msg = None
 trace_msg = await p.reply_text(f'User Name: {message.from_user.mention(style="md")}\n\nUser Id: `{message.from_user.id}`')
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} image   Successful created PDF if you want add more image Send me One by one\n\n **if done click here 👉 /convert** ")
 

@app.on_message(filters.private & filters.document)
async def pdf(client,message):
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.document.file_id)

 if UPDATE_CHANNEL:
  try:
   user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
   if user.status == "kicked":
    await message.reply_text(" Sorry, You are **B A N N E D**")
    return
  except UserNotParticipant:
   # await message.reply_text(f"Join @{UPDATE_CHANNEL} To Use Me")
   await message.reply_text(
    text="**Please Join My Update Channel Before Using Me..**",
    reply_markup=InlineKeyboardMarkup([
    [ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/{UPDATE_CHANNEL}")]
    ])
   )
   return
  else:
   isPdfOrImg = message.document.file_name
  fileSize = message.document.file_size
  fileNm, fileExt = os.path.splitext(isPdfOrImg)
  suprtedFile = ['.jpg','.jpeg','.png']
  if fileExt not in suprtedFile and fileSize <= 10000000:
   await ms.edit("Dont abuse me, only send Photos upto 10MB.")
   return
  if fileExt in suprtedFile and fileSize <= 10000000:
   ms = await message.reply_text("Converting to PDF ......")
   file = await client.download_media(file_id)
 o = await message.forward(LOG_CHANNEL)
 trace_mssg = None
 trace_mssg = await o.reply_text(f'User Name: {message.from_user.mention(style="md")}\n\nUser Id: `{message.from_user.id}`')
 
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
 mt = message.text
 if (" " in message.text):
  cmd, file_name = message.text.split(" ", 1)
 #if file_name.endswith(".pdf"):
  #filename = file_name.split(".")[0]
 #else:
  #filename = file_name

 if isinstance(images, list):
  pgnmbr = len(LIST[message.from_user.id])
 if not images:
  await message.reply_text( "No image !!")
  return
 thumb_path = os.path.join(os.getcwd(), "img")
 if not os.path.isdir(thumb_path):
  os.makedirs(thumb_path)
  urllib.request.urlretrieve(Translation.THUMB_URL, os.path.join(thumb_path, "thumbnail.png"))
 else:
  pass
    #
 thumbnail = os.path.join(os.getcwd(), "img", "thumbnail.png")
 path0 = f"{message.from_user.id}" + ".pdf"
 
 if file_name in mt:
  path = f"{filename}" + ".pdf"
 else:
  path = path0

 #path = f"{message.from_user.id}" + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 
 msg = await client.send_document(message.from_user.id, open(path, "rb"), caption = "Here your pdf !!\n\nTotal Pages:{}".format(pgnmbr), thumb = thumbnail)
 os.remove(path)
 await abcd.delete()
 await msg.forward(LOG_CHANNEL)
 
 
@app.on_message(filters.command(['pages']))
async def total_pages(client, message):
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
  await a.edit_text(f"The total number of pages in the given PDF file = {pdf_page_count}")
  q = await file_s.forward(LOG_CHANNEL)
  trace_mssg = None
  trace_mssg = await q.reply_text(f'User Name: {message.from_user.mention(style="md")}\n\nUser Id: `{message.from_user.id}`\n\nTotal Pages: {pdf_page_count}')
  
  os.remove(file)


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
    if message.text.startswith("http"):
        f = await message.forward(LOG_CHANNEL)
        trace_msg = None
        trace_msg = await f.reply_text(f'User Name: {message.from_user.mention(style="md")}\n\nUser Id: `{message.from_user.id}`')
    file_name = str()
    #
    thumb_path = os.path.join(os.getcwd(), "img")
    if not os.path.isdir(thumb_path):
        os.makedirs(thumb_path)
        urllib.request.urlretrieve(Translation.THUMB_URL, os.path.join(thumb_path, "thumbnail.png"))
    else:
        pass
    #
    thumbnail = os.path.join(os.getcwd(), "img", "thumbnail.png")
    #
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
        caption=Translation.CAPTION_TXT.format(file_name),
        thumb=thumbnail
    )
    await msgg.forward(LOG_CHANNEL)
    print(
        '@' + message.from_user.username if message.from_user.username else message.from_user.first_name,
        "has downloaded the file",
        file_name
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
