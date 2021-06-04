# -- coding: utf-8 --
from gtts import gTTS, lang
import ffmpeg
from io import BytesIO
import os
import youtube_dl
from mutagen.mp3 import MP3
import random, discord, asyncio, datetime, pytz, pickle, time
from discord.ext import commands
from discord.ext.commands import Bot
from time import sleep
from googletrans import Translator

command_name = ("키알봇 ", "kialbot ", "캴봇 ", "캴 ", "칼봇 ", "키알 ", "kial ")
client = commands.Bot(command_prefix=command_name)
game = discord.Game("키알과 키알")
bot = commands.Bot(command_prefix='키알봇 ', status=discord.Status.online, activity=game)

hi = '안녕', '안녕하세요', 'ㅎㅇ', 'hi', 'hello', '||...대답이 없다||'
dice6 = '아..아쉽게도 1이 나왔다..', '겨우 2..?', '그래도 중간인 3이 나왓다', '그래도 중간인 4가 나왓다!', '아쉽게 5가 나왔다!', '아닛! 6이 나오다니!\n 오늘은 운이 좋은걸!'
dice12 = '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'


def audio_len(path):
    global MP3
    audio = MP3(path)
    return(audio.info.length)


@client.command(name="tts")
async def tts(ctx, *, text):
    speech = gTTS(text=text, lang="ko", slow=False)
    speech.save()
    voicechannel = ctx.author.voice.channel
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio("tts.mp3"), after=lambda e: print("완료"))
    counter = 0
    cwd = os.getcwd()
    duration = audio_len(cwd + ("/tts.mp3"))
    while not counter >= duration:
        await asyncio.cleep(1)
        counter += 1
    await vc.disconnect()


@client.command(aliases=["통역", "trans"])
async def laik(ctx, *, text):
    translator = Translator()
    value = translator.translate(text, src='en', dest='ko')

    print(value)
    print(value.src)  # 변환할 언어
    print(value.dest)  # 변환될 언어
    await ctx.channel.send(value.text)  # 변환 결과


@client.command(name="역할", pass_context=True)
async def 역할(ctx, *, text):
    if text.split()[0:1] == "만들기":
        await client.create_role(a, reason=None)



@client.command()
async def 노래(ctx, url):
    channel = ctx.author.voice.channel
    if client.voice_clients == []:
    	await channel.connect()
    	await ctx.send(str(client.voice_clients[0].channel) + "채널에 입장하였습니다!")

    ydl_opts = {format: 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = client.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


@client.command(aliases=['안녕', '안녕하세요', 'ㅎㅇ', 'hi', '헬로'])
async def hello(ctx):
    await ctx.send(random.choice(hi))


@client.command(aliases=['kial', '키알'])
async def k(ctx):
    text = await ctx.send('키알을 없애고 내가 키알이 되겠다')
    sleep(1.5)
    await text.edit(content='...')
    sleep(2.5)
    await text.edit(content='키알?')


@client.command(aliases=['주사위', '기본주사위', '일반주사위', 'NormalDice', '6dice', '6주사위', 'nd'])
async def dice(ctx):
    await ctx.send(random.choice(dice6))


@client.command(aliases=['고오급주사위', '고급주사위', 'SpecialDice', '12dice', '12주사위', 'sd'])
async def special_dice(ctx):
    await ctx.send(random.choice(dice12))


@client.command(aliases=['청소', '지워'], pass_context=True)
async def clear(ctx, *, amount=5):
    i = (ctx.author.guild_permissions.manage_messages)
    if i is True or ctx.author.name == 'kial':
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f'<@!{ctx.author.id}>이 메세지 ``{amount}``개를 청소했습니다')
        sleep(1.2)
        amount = 0
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.channel.send("메세지를 청소할 권한이 없습니다")


@client.command(aliases=['따라하기', '따라해'], pass_context=True)
async def same(ctx, *, text):
    same = f'<@!{ctx.author.id}>, 따라하기 싫음', f'<@!{ctx.author.id}>, {text}'
    await ctx.channel.send(random.choice(same))


@client.command(name='아잉')
async def aing(ctx):
    await ctx.channel.send(f'<@!{ctx.author.id}>, 너 뭐해..?')


@client.command(aliases=['이름', '닉', '닉네임'])
async def name(ctx):
    await ctx.send(f"{ctx.author.name}")


@client.command(aliases=['임베드', '공지'], pass_context=True)
async def embad(ctx, *, text):
    amount = 0
    user = f'{ctx.author.name}'
    user_icon = f'{ctx.author.avatar_url}'
    title = text.split()[0]
    sub = text.split()[1]
    word_title = text.split()[2:3]
    word = text.split()[3:]
    embed = discord.Embed(title=title, description=sub, timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    embed.add_field(name=f"{word_title}", value=word, inline=False)
    embed.set_footer(text='requested by ' + user, icon_url=(user_icon))
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(embed=embed)


@client.command(name="부르기", pass_context=True)
async def hey(ctx, member: discord.Member=None):
    member = member or ctx.message.author
    await ctx.send(f"{ctx.author.name}이(가) {member}불렀음")


@client.command(name='프로필', pass_context=True)
async def proofile(ctx, user: discord.User):
    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(title=f"{user.name}님의 프로필", color=0x00cbff)
    embed.add_field(name="**유저 닉네임**", value=user.name, inline=False)
    embed.add_field(name="**서버 닉네임**", value=user.display_name, inline=True)

    embed.add_field(name="\n**유저 가입일**", value=date, inline=False)
    embed.add_field(name="\n**유저 아이디**", value=user.id, inline=True)

    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)


@client.command(aliases=['선택', '고르기', '골라', '선택해'], pass_context=True)
async def wich(ctx, *, text):
    a = text.split()[0]
    b = text.split()[1]
    c = [a, b]
    await ctx.send(f"흠..제 생각엔 {random.choice(c)}이(가) 좋을것 같아요!")


@client.command(name=('테스트'))
async def where(ctx):
    mp3_fp = BytesIO()
    tts = gTTS('hello', lang='en')
    tts.write_to_fp(mp3_fp)


@client.command(name=('채널'), pass_context=True)
async def channel(ctx, *, text):
    global channel
    channel = text
    await client.get_channel(int(channel)).send("테스트 성공")


@client.command(aliases=['배우기', '배워'], pass_context=True)
async def study(ctx, *, text):
    with open(text.split()[0], "wb") as fw:
        pickle.dump(text.split()[1:], fw)
        await ctx.send(f'{text.split()[0]}은(는) {text.split()[1:]}(이)라고요??')
        await ctx.send(f'가르쳐주셔서 감사해요! {ctx.author.name}님!')
        await ctx.send('**참고** 키알봇 배워 기능은 아직 beta - 0.01버전입니다.')


@client.command(name='잊어')
async def forget(ctx):
    await ctx.send('미완입니다.')


@client.command(aliases=['대화'], pass_context=True)
async def print(ctx, text):
    with open(text, "rb") as fr:
        data = pickle.load(fr)
        print_str = data.split()[0:]
        joined_str = ' '.join(print_str)
        await ctx.send(joined_str)
        await ctx.send('**참고** 키알봇 대화 기능은 아직 beta - 0.01버전입니다.')


@client.command(name='질문', pass_context=True)
async def w(ctx, text):
    with open(text, "wb") as fw:
        pickle.dump(text + f' {ctx.author.name}', fw)
        await ctx.send('질문을 보냈습니다!')


@client.command(name='테슷트', pass_context=True)
async def wtf(ctx, *, text):
    str = text
    splitted_str = str.split()[1:]
    joined_str = ' '.join(splitted_str)
    await ctx.send(joined_str)


@client.command(name="dm", pass_context=True)
async def dm(ctx, user: discord.User, *, text):
    channel = await user.create_dm()
    await channel.send(f"<@!{user.id}>! ``{ctx.author.name}``님이(가) 당신에게 dm을 보내셨습니다!")
    sleep(1)
    await channel.send(text)


@client.command(name="연결")
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send(f"<@!{ctx.author.id}>님! 음성채널에 접속한 후 사용해주세요!")


@client.command(name="끊기")
async def leave(ctx):
	await client.voice_clients[0].disconnect()


@client.command(aliases=['도움말', '도움', '명령어', '사용설명서', '사용법', '설명서'], pass_context=True)
async def abc(ctx, *, text):
    if text.split()[0] == '미니게임':
        embed = discord.Embed(title="키알봇 사용 설명서", description="미니게임 목록이에요!",
                        timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00cbff)
        embed.add_field(name="**키알봇 미니게임 명령어**",
                    value="키알봇 주사위\n``6, 12 주사위 중 하나를 굴려보세요!``", inline=True)
        embed.add_field(name="아직", value="\n미완이랍니다", inline=True)
        embed.add_field(name="**미니게임이..**", value="하나밖에 없어요!", inline=False)

        embed.set_footer(text="Bot Made by. kial#2460", icon_url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321157239832617/1618238751542.png?width=613&height=613"))
        embed.set_thumbnail(url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321119901614080/KakaoTalk_20200909_113509562.jpg?width=613&height=613"))
        await ctx.send(embed=embed)
    elif text.split()[0] == '서버':
        embed = discord.Embed(title="키알봇 사용 설명서", description="서버 목록이에요!",
                            timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00cbff)
        embed.add_field(name="**키알봇 서버 명령어**",
                        value="키알봇 청소\n``무려 키알이 청소를 해준대요!``", inline=True)
        embed.add_field(name="놀랍게도", value="\n밴과 경고는 제작 중이랍니다!", inline=True)
        embed.add_field(name="**ㅓ..**", value="그냥 기다리세요!", inline=False)

        embed.set_footer(text="Bot Made by. kial#2460", icon_url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321157239832617/1618238751542.png?width=613&height=613"))
        embed.set_thumbnail(url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321119901614080/KakaoTalk_20200909_113509562.jpg?width=613&height=613"))
        await ctx.send(embed=embed)
    elif text.split()[0] == '잡다한거':
        embed = discord.Embed(title="키알봇 사용 설명서", description="잡다한거 목록이에요!",
                        timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00cbff)
        embed.add_field(name="**키알봇 잡다한거 명령어**",
                        value="키알봇 (인사)\n``키알이 인사를 해줘요!``\n\n키알봇 따라하기 (하고 싶은 말)\n``헋..무려 키알이 따라해요..!``\n\n키알봇 부르기 (원하는 사람 맨션)\n``정말 쓸모 없지만 누가 불렀는지 알려줘요!``", inline=True)
        embed.add_field(name="키알", value="\n그냥 써보세요!", inline=True)
        embed.add_field(name="**ㅓ..**", value="내!", inline=False)

        embed.set_footer(text="Bot Made by. kial#2460", icon_url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321157239832617/1618238751542.png?width=613&height=613"))
        embed.set_thumbnail(url=(
            "https://media.discordapp.net/attachments/831067005582835715/831321119901614080/KakaoTalk_20200909_113509562.jpg?width=613&height=613"))
        await ctx.send(embed=embed)
    else:
        await ctx.send("**그딴거 업서 임마**")


access_token = os.environ['BOT_TOKEN']
client.run(access_token)
