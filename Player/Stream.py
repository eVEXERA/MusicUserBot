"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


import os
from Player import Config
from Player import Gana
from pyrogram import Client
from yt_dlp import YoutubeDL
from pytgcalls import PyTgCalls
from Player import generate_cover
from Player import get_group, set_title
from pytgcalls.types.stream import MediaStream
from pyrogram.raw.types import InputPeerChannel
from pytgcalls.types import AudioQuality, VideoQuality
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall


abhi = {}
ydl_opts = {
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}
app = Client(
    "MusicPlayerUB",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION,
    in_memory=True,
)
ytdl = YoutubeDL(ydl_opts)
pytgcalls = PyTgCalls(app)


async def start_stream(song: Gana, lang):
    chat = song.request_msg.chat
    if abhi.get(chat.id) is not None:
        try:
            await abhi[chat.id].delete()
        except BaseException:
            pass
    infomsg = await song.request_msg.reply_text(lang["downloading"])
    try:
        await pytgcalls.play(
            chat.id,
            get_quality(song),
        )
    except (NoActiveGroupCall, GroupCallNotFound):
        peer = await app.resolve_peer(chat.id)
        await app.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=app.rnd_id() // 9000000000,
            )
        )
        return await start_stream(song, lang)
    await set_title(chat.id, song.title, client=app)
    thumb = await generate_cover(
        song.title,
        chat.title,
        chat.id,
        song.thumb,
    )
    abhi[chat.id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"]
        % (
            song.title,
            song.source,
            song.duration,
            song.request_msg.chat.id,
            (
                song.requested_by.mention
                if song.requested_by
                else song.request_msg.sender_chat.title
            ),
        ),
        quote=False,
    )
    await infomsg.delete()
    if os.path.exists(thumb):
        os.remove(thumb)


def get_quality(song: Gana) -> MediaStream:
    group = get_group(song.request_msg.chat.id)
    if group["stream_mode"] == "video":
        if Config.QUALITY.lower() == "high":
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                VideoQuality.FHD_1080p,
                headers=song.headers,
            )
        elif Config.QUALITY.lower() == "medium":
            return MediaStream(
                song.remote,
                AudioQuality.MEDIUM,
                VideoQuality.HD_720p,
                headers=song.headers,
            )
        elif Config.QUALITY.lower() == "low":
            return MediaStream(
                song.remote,
                AudioQuality.LOW,
                VideoQuality.SD_480p,
                headers=song.headers,
            )
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                VideoQuality.FHD_1080p,
                headers=song.headers,
            )
    else:
        if Config.QUALITY.lower() == "high":
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        elif Config.QUALITY.lower() == "medium":
            return MediaStream(
                song.remote,
                AudioQuality.MEDIUM,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        elif Config.QUALITY.lower() == "low":
            return MediaStream(
                song.remote,
                AudioQuality.LOW,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
