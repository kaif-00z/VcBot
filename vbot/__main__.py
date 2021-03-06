#    This file is part of the Vc distribution.
#    Copyright (c) 2021 kaif-00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/kaif-00z/VcBot/blob/main/License> .


from . import *

LOGS.info("Starting...")

try:
    user.start()
except Exception as erc:
    LOGS.info(erc)

group_call_factory = GroupCallFactory(
    user, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
)
VC = {}

_ = 'youtube-dl -g -f "best[height<=?720][width<=?1280]" {}'

@user.on(events.NewMessage(outgoing=True, pattern="\\.ping"))
async def ping(event):
    t = time.time()
    x = await event.edit("Pɪɴɢ!!!")
    tt = time.time() - t
    p = float(str(tt)) * 1000
    await x.edit(f"Pɪɴɢ: {int(p)}ms")


@user.on(events.NewMessage(outgoing=True, pattern="\\.help"))
async def help(event):
    await event.edit(
        """
        **Available Commands**:\n
        • `.play <youtube link / reply>` - This command play Audio in Vc.\n
        • `.videoplay <youtube link>` - This command play Video in Vc.\n
        • `.stopvc` - This command stop Vc.\n
        • `.pausevc` - This command pause Vc.\n
        • `.resumevc` - This command resume Vc.\n
        • `.mutevc` - This command mute Vc.\n
        • `.unmutevc` - This command unmute Vc.
       """
    )


@user.on(events.NewMessage(outgoing=True, pattern="\\.play"))
async def play(event):
    c_id = event.chat_id
    if event.reply_to:
        x = await event.edit("`converting...`")
        reply = await event.get_reply_message()
        down = await user.download_media(reply)
        group_call = group_call_factory.get_group_call()
        await group_call.join(event.chat_id)
        await group_call.start_audio(f"{down}")
        VC[c_id] = group_call
        await x.edit(f"`✓Joined Vc Sucessfully in {event.chat_id}.`")
        return
    link = event.text.split()[1]
    x = await event.edit("`Downloading & Converting...`")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.mp3",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"{link}"])
        info_dict = ydl.extract_info(link, download=False)
        audio_id = info_dict.get("id") + ".mp3"
    group_call = group_call_factory.get_group_call()
    try:
        await group_call.join(event.chat_id)
        await group_call.start_audio(f"{audio_id}")
        VC[c_id] = group_call
        await x.edit(f"`✓Joined Vc Sucessfully in {event.chat_id}.`")
    except Exception as ERROR:
        await x.edit(f"`✘Error while Joining Vc in {event.chat_id}.`")
        LOGS.info(str(ERROR))


@user.on(events.NewMessage(outgoing=True, pattern="\\.videoplay"))
async def videoplay(event):
    c_id = event.chat_id
    xx = await event.edit("`Converting...`")
    link = event.text.split()[1]
    sh = _.format(link)
    process = await asyncio.create_subprocess_shell(
        sh, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    dlink = stdout.decode()
    error = stderr.decode()
    try:
        if error:
            await event.edit("Something Went Wrong")
            return LOGS.info(str(error))
    except BaseException:
        pass
    group_call = group_call_factory.get_group_call()
    try:
        await group_call.join(event.chat_id)
        await group_call.start_video(f"{dlink}")
        VC[c_id] = group_call
        await xx.edit(f"`✓Joined Vc Sucessfully in {event.chat_id}.`")
    except Exception as no:
        await xx.edit(f"`✘Error while Joining Vc in {event.chat_id}.`")
        LOGS.info(str(no))


@user.on(events.NewMessage(outgoing=True, pattern="\\.stopvc"))
async def stopvc(event):
    try:
        await VC[event.chat_id].stop()
        await event.edit(f"`✓Successfully Left the Vc in {event.chat_id}.`")
    except Exception as err:
        await event.edit(f"`✘Error while Lefting the Vc in {event.chat_id}.`")
        LOGS.info(str(err))


@user.on(events.NewMessage(outgoing=True, pattern="\\.pausevc"))
async def pause(event):
    try:
        await VC[event.chat_id].set_pause(True)
        await event.edit(f"`✓Sucessfully pause the Vc in {event.chat_id}`.")
    except Exception as eror:
        await event.edit(f"`✘Error while pausing the Vc in {event.chat_id}.`")
        LOGS.info(str(eror))


@user.on(events.NewMessage(outgoing=True, pattern="\\.resumevc"))
async def resume(event):
    try:
        await VC[event.chat_id].set_pause(False)
        await event.edit(f"`✓Sucessfully resume the Vc in {event.chat_id}.`")
    except Exception as er:
        await event.edit(f"`✘Error while resuming the Vc in {event.chat_id}.`")
        LOGS.info(str(er))


@user.on(events.NewMessage(outgoing=True, pattern="\\.mutevc"))
async def mute(event):
    try:
        await VC[event.chat_id].set_is_mute(True)
        await event.edit(f"`✓Sucessfully mute the Vc in {event.chat_id}.`")
    except Exception as ere:
        await event.edit(f"`✘Error while muting the Vc in {event.chat_id}.`")
        LOGS.info(str(ere))


@user.on(events.NewMessage(outgoing=True, pattern="\\.unmutevc"))
async def unmute(event):
    try:
        await VC[event.chat_id].set_is_mute(False)
        await event.edit(f"`✓Sucessfully unmute the Vc in {event.chat_id}.`")
    except Exception as ok:
        await event.edit(f"`✘Error while unmuting the Vc in {event.chat_id}.`")
        LOGS.info(str(ok))


LOGS.info("Bot has started...")
user.run_until_disconnected()
