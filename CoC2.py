from pyrogram import Client, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Filters, Emoji, ContinuePropagation, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.errors import MessageNotModified, FloodWait, MessageTooLong, RPCError, MessageIdInvalid
from myModule import *
import coc
import asyncio
import time
import json
import datetime
import schedule
import re
import threading
import logging
from uuid import uuid4
from validate_email import validate_email
from babel.numbers import format_decimal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import locale
import csv
import copy


locale.setlocale(locale.LC_TIME, "it_IT.utf8")

f = open("nomeBot.txt", "r")
nomeBot = f.readline()

traduzioni = {
    "lightning spell": "Incantesimo Fulmine",
    "healing spell": "Incantesimo Cura 👨‍⚕",
    "rage spell": "Incantesimo Furia 🤬",
    "jump spell": "Incantesimo  Salto 🐰",
    "freeze spell": "Incantesimo Congelamento ❄️",
    "poison spell": "Incantesimo Veleno 👨‍🔬",
    "earthquake spell": "Incantesimo Terremoto 🕳",
    "haste spell": "Incantesimo Velocità 💨",
    "clone spell": "Incantesimo Clonazione 👭",
    "skeleton spell": "Incantesimo Scheletri 💀",
    "bat spell": "Incantesimo Pipistrello 🦇",
    "barbarian": "Barbaro",
    "archer": "Arciere",
    "giant": "Gigante",
    "goblin": "Goblin",
    "wall breaker": "Spaccamuro",
    "balloon": "Mongolfiera",
    "healer": "Guaritore",
    "dragon": "Drago",
    "p.e.k.k.a": "P.E.K.K.A",
    "baby dragon": "Cucciolo di Drago",
    "miner": "Minatore",
    "electro dragon": "Drago Elettrico",
    "wizard": "Stregone",
    "minion": "Sgherro",
    "hog rider": "Domatore di Cinghiali",
    "valkyrie": "Valchiria",
    "golem": "Golem",
    "witch": "Strega",
    "bowler": "Bocciatore",
    "ice golem": "Golem di Ghiaccio",
    "lava hound": "Mastino",
    "wall wrecker": "Sgretolamuri",
    "battle blimp": "Dirigibile",
    "stone slammer": "Sganciapietre",
    "raged barbarian": "Barbaro Furioso",
    "sneaky archer": "Arciere Furtivo",
    "beta minion": "Sgherro Mutante",
    "boxer giant": "Gigante Pugile",
    "bomber": "Bombarolo",
    "super pekka": "Super Pekka",
    "cannon cart": "Cannone a Rotelle",
    "night witch": "Strega Notturna",
    "drop ship": "Mongolfiere Cimiteriale",
    "barbarian king": "🤴 Re Barbaro",
    "archer queen": "👸 Regina degli Arcieri",
    "grand warden": "⚜️ Gran Sorvegliante",
    "battle machine": "🤖 Macchina da Guerra"
}

f = open("token.txt")
token = f.readline()

app = Client(
    "CoC2",
    bot_token = token,
)


"""
Funzioni
"""
async def resetSeason():
    for giocatore in risorsePers:
        if datetime.datetime.now().day == 1:
            player = get_some_player(giocatore)

            achivments = player.achievements_dict
            elixir = achivments["Elixir Escapade"].value
            gold = achivments["Gold Grab"].value    
            dark = achivments["Heroic Heist"].value

            risorsePers[giocatore]["startElixirSeason"] = elixir
            risorsePers[giocatore]["startGoldSeason"] = gold
            risorsePers[giocatore]["startDarkSeason"] = dark
            risorsePers[giocatore]["startWarStarsSeason"] = player.war_stars
            risorsePers[giocatore]["startDonationsSeason"] = achivments["Friend in Need"].value

    await app.send_message("thefamilycommunity","**__La stagione è finita!__**\nLe risorse stagionali sono state **resettate** con successo")
    with open("risorsePers.json", 'w') as fp:
        json.dump(risorsePers, fp,sort_keys=True, indent=4)

scheduler = AsyncIOScheduler()
scheduler.add_job(resetSeason, 'cron', day='1',hour = "00", minute = "00")
scheduler.start()

def aggiornaGiorno(giocatore):
    risorsePers[giocatore]["giorni"] += 1
    SaveJson("risorsePers.json",risorsePers)

def aggiornaGiornoDistr(giocatore):
    distruzioni[giocatore]["giorni"] += 1
    SaveJson("distruzioni.json",distruzioni)

def AggStr(lvl,punti,nome,tipoClassifica):
    if lvl == 4:
        municipi[tipoClassifica]["messaggioTh4"] += f"**{municipi[tipoClassifica]['pos4']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]['pos4'] += 1
    if lvl == 5:
        municipi[tipoClassifica]["messaggioTh5"] += f"**{municipi[tipoClassifica]['pos5']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos5"] += 1
    if lvl == 6:
        municipi[tipoClassifica]["messaggioTh6"] += f"**{municipi[tipoClassifica]['pos6']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos6"] += 1
    if lvl == 7:
        municipi[tipoClassifica]["messaggioTh7"] += f"**{municipi[tipoClassifica]['pos7']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos7"] += 1
    if lvl == 8:
        municipi[tipoClassifica]["messaggioTh8"] += f"**{municipi[tipoClassifica]['pos8']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos8"] += 1
    if lvl == 9:
        municipi[tipoClassifica]["messaggioTh9"] += f"**{municipi[tipoClassifica]['pos9']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos9"] += 1
    if lvl == 10:
        municipi[tipoClassifica]["messaggioTh10"] += f"**{municipi[tipoClassifica]['pos10']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos10"] += 1
    if lvl == 11:
        municipi[tipoClassifica]["messaggioTh11"] += f"**{municipi[tipoClassifica]['pos11']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos11"] += 1
    if lvl == 12:
        municipi[tipoClassifica]["messaggioTh12"] += f"**{municipi[tipoClassifica]['pos12']}.** {nome} - {punti}\n"
        municipi[tipoClassifica]["pos12"] += 1

running = True
def startJob():
    while running==True:
        schedule.run_pending()
        time.sleep(1)

t1 = threading.Thread(target=startJob)
t1.start()


"""
Inizializzazione dizionari e schedules
"""
with open('giocatori.json', 'r') as fp:
    giocatori = json.load(fp)

with open('flag.json', 'r') as fp:
    f = json.load(fp)

with open('item.json', 'r') as fp:
    items = json.load(fp)

with open('risorsePers.json', 'r') as fp:
    risorsePers = json.load(fp)

with open('distruzioni.json', 'r') as fp:
    distruzioni = json.load(fp)

with open('risorse.json', 'r') as fp:
    risorse = json.load(fp)

with open('municipi.json', 'r') as fp:
    municipi = json.load(fp)

with open('registrazioni.json', 'r') as fp:
    registrazioni = json.load(fp)

with open('giaReg.json', 'r') as fp:
    giàRegistrati = json.load(fp)

for giocatore in risorsePers:
    data = risorsePers[giocatore]["dataSchedule"]
    schedule.every().day.at(data).do(aggiornaGiorno, giocatore).tag(f"Evento {giocatore}")

for giocatore in distruzioni:
    data = distruzioni[giocatore]["dataSchedule"]
    schedule.every().day.at(data).do(aggiornaGiornoDistr, giocatore).tag(f"distr {giocatore}")

"""
Comandi
"""
@app.on_message(Filters.command(["stats",f"stats{nomeBot}"],['/','.']))
async def statsComando(app,message):
    global giocatori
    try:
        utente = str(message.from_user.id)
        flag = False
        codice = codiceFunc()
        f[f"{utente}{codice}"] = dict()

        try:
            giocatore = message.command[1]
            f[f"{utente}{codice}"]["flag"] = ""
        except IndexError:
            f[f"{utente}{codice}"]["flag"] = None
            giocatore = ""

        f[f"{utente}{codice}"]["SoloLettura"] = False
        if f[f"{utente}{codice}"]["flag"] != None:
            if utente in giocatori:
                flag = True
                giocatore = message.command[1]
            try:
                if giocatore not in giocatori[utente]["tag"]:
                    f[f"{utente}{codice}"]["SoloLettura"] = True
            except KeyError:
                pass

        if f[f"{utente}{codice}"]["flag"] == None:
            if utente in giocatori:
                giocatore = giocatori[utente]["tag"][0]
                flag = "abacab"

            else:
                await message.reply("Il tuo account telegram non è ancora associato a nessun tag! Inserisci il tag del tuo account Clash of Clans dopo questo comando per poterti registrare\nEsempio: `/stats #C9CUYPVP`")
                return

        SaveJson("flag.json",f)


        if flag == "abacab":
            markup = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
            start = 0
            for item in giocatori[utente]["tag"]:

                nome = await get_some_player(item)
                convertitore = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:13,13:14,14:0}
                start = convertitore[start]
                markup[start].append(InlineKeyboardButton(nome, f"item|{item}|{codice}"))
                
                items[item] = dict()
                items[item]["nome"] = nome.name
                items[item]["utente"] = message.from_user.id

            SaveJson("item.json",items)
            await message.reply("Scegli l'account che vuoi utilizzare 🧐",reply_markup=InlineKeyboardMarkup(markup), quote = False)

        player = await get_some_player(giocatore)


        if flag == False:
            await message.reply(
                "Cosa vuoi visualizzare {}?".format(player),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Clan 🏰",
                                callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Profilo 📊",
                                callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Truppe 👮‍♂",
                                callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Eroi 👑",
                                callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Incantesimi 👨‍🔬",
                                callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Risorse 🏝",
                                callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Distruzione 🌋",
                                callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Associa TAG",
                                callback_data="asssocia|{}|{}|{}".format(giocatore,utente,codice)
                                )                      
                        ]                  
                    ]
                ),
                quote = False
            )
        elif flag == True:
            await message.reply(
                "Cosa vuoi visualizzare {}?".format(player),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Clan 🏰",
                                callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Profilo 📊",
                                callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Truppe 👮‍♂",
                                callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Eroi 👑",
                                callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                )

                        ],
                        [
                            InlineKeyboardButton(
                                "Incantesimi 👨‍🔬",
                                callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Risorse 🏝",
                                callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Distruzione 🌋",
                                callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                          InlineKeyboardButton(
                                "Aggiungi TAG",
                                callback_data="aggiungiTag|{}|{}".format(giocatore,utente)
                                )  
                        ]      
                    ]
                ),
                quote = False
            )


    except coc.errors.NotFound:
        await message.reply("Questo giocatore non esiste")

@app.on_message(Filters.command(["classifica",f"classifica{nomeBot}"],['/','.']))
async def classifica(_,message):
    utente = message.from_user.id
    await app.send_message(
        message.chat.id,
        "Scegli il tipo di classifica che vuoi visualizzare!",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Elisir Nero ⚫️",
                                callback_data="classifica|elisir nero|{}".format(utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Municipi 🏛",
                                callback_data="classifica|municipi|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Mura 🧱",
                                callback_data="classifica|mura|{}".format(utente)
                                ),
                        ],
                        [
                            InlineKeyboardButton(
                                "Mortai 🚀",
                                callback_data="classifica|mortai|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Archi X 🏹",
                                callback_data="classifica|archi x|{}".format(utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Torri Inferno 🗼",
                                callback_data="classifica|torri inferno|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Artiglieria Aquila 🦅",
                                callback_data="classifica|artiglierie aquila|{}".format(utente)
                                )
                        ],
                    ]
            ) 
        )  

@app.on_message(Filters.command(["lista",f"lista{nomeBot}"],['/','.']) & Filters.user(["Anatras02","Jokerino00",807419215,"redthemaster"]))
async def lista(_,message):
    lista = ""
    await app.send_chat_action(message.chat.id,"typing")
    for utenteFor in giocatori:
        nomi = giocatori[utenteFor]["tag"]
        try:
            nomeTelegram = (await app.get_users(int(utenteFor))).username
            if nomeTelegram == None:
                nomeTelegram = (await app.get_users(int(utenteFor))).first_name 
        except KeyError:
            continue
        except RPCError as e:
            print(e,utenteFor)
            continue
        lista += f"**__{nomeTelegram}:__**\n"
        for nome in nomi:
            player = await get_some_player(nome)
            lista += f"> {player} - `{player.tag}`\n"
    await message.reply(lista,quote = False)
    await app.send_chat_action(message.chat.id,"cancel")

@app.on_message(Filters.command(["rimuovi",f"rimuovi{nomeBot}"],['/','.']) & Filters.user(["Anatras02","Jokerino00",807419215,"redthemaster"]))
async def rimuovi(_,message):
    giocatore = message.command[1]

    flag = False
    for utenteFor in giocatori:
        if giocatore in giocatori[utenteFor]["tag"]:
            giocatori[utenteFor]["tag"].remove(giocatore)
            profilo = (await app.get_users(utenteFor)).username
            if profilo == None:
                profilo = (await app.get_users(utenteFor)).first_name
            flag = True
            break

    if flag:
        await message.reply(f"Ho rimosso {giocatore} dal profilo di {profilo}")
        if giocatori[utenteFor]["tag"] == []:
            del giocatori[utenteFor]
    else:
        await message.reply(f"{giocatore} non è associato a nessun account telegram")
    SaveJson("giocatori.json",giocatori)

@app.on_message(Filters.command(["gestisciEventi",f"gestisciEventi{nomeBot}"],['/','.']) & Filters.user(["Anatras02","simon70","EmyMey71","Jokerino00","fleed73","Paolaconte76","redthemaster"]))
async def gestisci(_,message):
    if "#" in message.text:
        giocatore = message.command[1]
        try:
            player = await get_some_player(giocatore)
            await app.send_message(
                message.chat.id,
                "Seleziona una scelta!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Inizio Evento",
                                callback_data="Evento|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Fine Evento",
                                callback_data="Fine|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],

                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Risorse",
                                callback_data="Risorse|{}".format(giocatore) # Note how callback_data must be bytes
                                ),
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni",
                                callback_data="Distruzioni|{}".format(giocatore) # Note how callback_data must be bytes
                                )

                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Chiudi",
                                callback_data="Chiudi" # Note how callback_data must be bytes
                                )
                        ],

                    ]
                )
            )
        except coc.errors.NotFound:
            await message.reply("Questo giocatore non esiste")
    else:
        await message.reply("TAG invalido")    

@app.on_message(Filters.command(["start",f"start{nomeBot}"],['/','.']))
async def start(_,message):
    messaggio = ("Benvenuti nel nostro bot! Noi siamo la [The Family Community](https://t.me/thefamilycommunity)! Questo Bot vi permetterà di tenere traccia delle vostre statistiche giocatore e clan! ❤️⚔️\n\n"
    "🔰 Per eventuali problemi scrivete a @redthemaster 🔰")
    await app.send_message(message.chat.id,messaggio,disable_web_page_preview = True)

@app.on_message(Filters.command(["help",f"help{nomeBot}"],['/','.']))
async def help(_,message):
    messaggio = (
        "**Lista comandi:**\n"
        "/stats - vedi stats di un giocatore\n"
        "/risorse - gestisci le risorse acquisite\n"
        "/distruzione - gestisci le distruzione fatte\n"
        "/incantesimi - mostra livelli incantesimi di un giocatore\n"
        "/truppe - mostra livell truppe di un giocatore\n"
        "/eroi - mostra livelli eroi di un giocatore\n"
        "/clan  mostra informazioni di un clan\n"
        "classifica - mostra classifica evento"
        )
    await app.send_message(message.chat.id,messaggio)

@app.on_message(Filters.command(["listaEvento",f"listaEvento{nomeBot}"],['/','.']))
async def listaEvento(_,message):
    try:
        tag = message.command[1]
    except IndexError:
        tag = ""

    if tag == "":
        messaggio = ""
        for user in registrazioni:
            if registrazioni[user]["inRegistrazione"] != -1:
                continue

            firstName = (await app.get_users(int(user))).first_name
            nome = f"[{firstName}](tg://user?id={user})"
            tag = registrazioni[user]["tag"]
            messaggio += f"{nome} - `{tag}`\n"

        try:
            await message.reply(messaggio,quote = False)
        except MessageTooLong:
            n = 4096
            messaggiSplit = [messaggio[i:i+n] for i in range(0, len(messaggio), n)]

            for messaggio in messaggiSplit:
                await message.reply(messaggio,quote = False)


    else:
        flag = False
        for user in registrazioni:
            if registrazioni[user]["inRegistrazione"] != -1:
                continue

            if registrazioni[user]["tag"] == tag:
                firstName = (await app.get_users(int(user))).first_name
                nome = f"[{firstName}](tg://user?id={user})"
                messaggioSearch = (
                    f"**__Queste sono le info di__** {nome}\n"
                    f"**Contatto Preferito**: {registrazioni[user]['accountPreferito']}\n"
                    f'**Account:** {registrazioni[user]["account"]}\n'
                    f'**TAG:** {registrazioni[user]["tag"]}\n'
                    f'**Codice tessera GEC:** {registrazioni[user]["GEC"]}\n'
                    )
                flag = True
                break

        if flag:
            await message.reply(messaggioSearch)
        else:
            await message.reply("Questo giocatore non si è ancora registrato")

@app.on_message(Filters.command(["resetEvento",f"resetEvento{nomeBot}"],['/','.']) & Filters.user(["Anatras02","Jokerino00",807419215,"redthemaster"]))
async def resetEvento(_,message):
    giàRegistrati.clear()
    await message.reply("Fatto, adesso chiunque può iscriversi all'evento")
    SaveJson("giaReg.json",giàRegistrati)


@app.on_message(Filters.command(["registrami",f"registrami{nomeBot}"],['/','.']))
async def registrazione(_,message):
    if message.chat.type != "private":
        privato = "__[qui](tg://user?id=747455144)__"
        await message.reply("Ti invito ad avviarmi in chat privata per proseguire!\n▶️ Clicca {} e digita /registrami".format(privato))
        return


    utente = str(message.from_user.id)
    registrazioni[utente] = dict()
    registrazioni[utente]["inRegistrazione"] = 0

    nome = message.from_user.username
    if nome == None:
        nome = message.from_user.first_name

    await message.reply(f"Benvenuto nel percorso di iscrizione guidata **{nome}**!\n\nCome prima cosa inviami dimmi dove preferisci essere contattato fra `Email`, `Discord` e `Telegram`!",quote=False)

    SaveJson("registrazioni.json",registrazioni)

def dictToCsv(dic):
    header = set(i for b in map(dict.keys, dic.values()) for i in b)
    with open('evento.csv', 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['Giocatori', *header])
        for a, b in dic.items():
            write.writerow([a]+[b.get(i, '') for i in header])

@app.on_message(Filters.private & Filters.text & ~Filters.command(["help","start","classifica","stats","gestisciEventi","lista","rimuovi"]), group = -1)
async def messaggi(_,message):
    utente = str(message.from_user.id)

    if message.text == "/registrami":
        registrazioni[utente] = dict()
        registrazioni[utente]["inRegistrazione"] = 0
        return

    try:
        registrazioni[utente]
    except KeyError:
        return

    if registrazioni[utente]["inRegistrazione"] <= 3:
        if registrazioni[utente]["inRegistrazione"] == 0:
            account = message.text
            if account.lower() == "discord":
                await message.reply(f"Bene!\nInviami il tuo username Discord adesso",quote=False)
                registrazioni[utente]["accountPreferito"] = "Discord"
                registrazioni[utente]["inRegistrazione"] += 1
            elif account.lower() == "telegram":
                await message.reply(f"Perfetto, questo account Telegram verrà usato come principale contatto!\nOra inviami il **TAG** del tuo villaggio 😃",quote=False)
                registrazioni[utente]["accountPreferito"] = "Telegram"
                registrazioni[utente]["account"] = message.from_user.id
                registrazioni[utente]["inRegistrazione"] += 2
            elif account.lower() == "email":
                await message.reply(f"Bene!\nInviami la tua email adesso",quote=False)
                registrazioni[utente]["accountPreferito"] = "Email"
                registrazioni[utente]["inRegistrazione"] += 1
            else:
                await message.reply(f"Eh no, devi scegliere una via di contatto valido!",quote=False)

        elif registrazioni[utente]["inRegistrazione"] == 1:
            if registrazioni[utente]["accountPreferito"] == "Email":
                if validate_email(message.text):
                    registrazioni[utente]["account"] = message.text
                    registrazioni[utente]["inRegistrazione"] += 1
                    await message.reply("Perfetto, ora inviami il **TAG** del tuo villaggio 😃")
                else:
                    await message.reply(f"L'email da te inserita ({message.text}) non è in un formato giusto, inviala nuovamente!",quote=False)

            elif registrazioni[utente]["accountPreferito"] == "Discord":
                registrazioni[utente]["accountPreferito"] = message.text
                registrazioni[utente]["inRegistrazione"] += 1
                await message.reply("Perfetto, ora inviami il **TAG** del tuo villaggio 😃")


        elif registrazioni[utente]["inRegistrazione"] == 2:
            try:
                player = await get_some_player(message.text)
                registrazioni[utente]["tag"] = message.text
                registrazioni[utente]["inRegistrazione"] += 1
                await message.reply(f"Piacere di conoscerti {player}!\nOra mi servirebbe sapere il **codice della tua tessera GEC** (se vuoi partecipare ad **eventi a premi**) altrimenti inserisci `None` (per partecipare solo ad **eventi senza premi**)")
            except coc.errors.NotFound:
                await message.reply(f"Questo TAG ({message.text}) non è associato a nessun account Clash Of Clans, inseriscilo nuovamente!",quote=False)

        elif registrazioni[utente]["inRegistrazione"] == 3:
            try: 
                int(message.text)
                flag = True
            except ValueError:
                flag = False

            if flag:
                registrazioni[utente]["GEC"] = int(message.text)
            elif message.text == "None":
                registrazioni[utente]["GEC"] = message.text
            else:
                await message.reply(f"Hey, il codice da te inserito ({message.text}) non puoi esistere..\nInseriscilo nuovamente correttamente!")
                return

            await message.reply(f"Complimenti! Hai finito la tua registrazione")
            registrazioni[utente]["inRegistrazione"] = -1
            messaggio = (
                f"**Contatto Preferito**: {registrazioni[utente]['accountPreferito']}\n"
                f'**Account:** {registrazioni[utente]["account"]}\n'
                f'**TAG:** {registrazioni[utente]["tag"]}\n'
                f'**Codice tessera GEC:** {registrazioni[utente]["GEC"]}\n'
                )
            await message.reply("Ti sei iscritto con successo!\n\n**Revisione Dati:**\n"+messaggio)

            player = await get_some_player(registrazioni[utente]["tag"])
            heroes = player.heroes
            EroeStr = f"**Lista Eroi {player.name}:**\n"
            counter = 0
            for eroe in heroes:
                counter += 1
                nomeEroe = traduzioni[eroe.name.lower()]
                livello = eroe.level
                registrazioni[utente][f"Livello "+nomeEroe] = livello
                EroeStr += f"**{nomeEroe}** __Livello {livello}__\n"
            if counter == 0:
                EroeStr = f"{player.name} non ha nessun eroe"

            nome = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            livelloMunicipio = player.town_hall
            registrazioni[utente]["Livello Municipio"] = livelloMunicipio
            messaggioPvt = (
                f'**{nome} ha richiesto di iscriversi all\'evento!**\n\n'
                f'**Contatto Preferito**: {registrazioni[utente]["accountPreferito"]}\n'
                f'**Account:** {registrazioni[utente]["account"]}\n'
                f'**TAG:** {registrazioni[utente]["tag"]}\n'
                f'**Livello Municipio:** {livelloMunicipio}\n'
                f'**Codice tessera GEC:** {registrazioni[utente]["GEC"]}\n\n'
                f"{EroeStr}\n"
                f'Se hai deciso di aggiungerlo all\'evento usa il comando `/gestisciEventi {registrazioni[utente]["tag"]}`'
            )

            dictToCsv(registrazioni)

            sendTo = ["Anatras02",807419215,"Jokerino00","redthemaster"]
            for user in sendTo:
                try:
                    await app.send_document(user,"evento.csv")
                    await app.send_message(user,messaggioPvt)
                except RPCError as e:
                    print(e)
                    continue
        SaveJson("registrazioni.json",registrazioni)

            
"""
Inline Query
"""
@app.on_inline_query()
async def inlineStats(_,inline_query):
    utente = str(inline_query.from_user.id)
    codice = codiceFunc()
    f[f"{utente}{codice}"] = dict()
    f[f"{utente}{codice}"]["flag"] = None
    f[f"{utente}{codice}"]["SoloLettura"] = True
    if utente in giocatori:
        markup = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        start = 0
        for item in giocatori[utente]["tag"]:
            nome = await get_some_player(item)
            convertitore = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:13,13:14,14:0}
            start = convertitore[start]
            markup[start].append(InlineKeyboardButton(nome, f"item|{item}|{codice}"))
            
            items[item] = dict()
            items[item]["nome"] = nome.name
            items[item]["utente"] = inline_query.from_user.id

        SaveJson("item.json",items)
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Scegli l'account da utilizzare",
                    input_message_content=InputTextMessageContent("Scegli l'account che vuoi utilizzare 🧐"),
                    reply_markup=InlineKeyboardMarkup(markup)
                )
            ],
            cache_time=1
        )


"""
Inserimento Utenti
"""
@app.on_callback_query()
async def asssociaTag(_,callback_query):
    if "asssocia" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = str(callback_query.data.split("|")[2])
        codice = callback_query.data.split("|")[3]

        if callback_query.from_user.id == int(utente):
            for utenteFor in giocatori:
                if giocatore in giocatori[utenteFor]["tag"]:
                    nome = await app.get_users(int(utenteFor))
                    try:
                        if nome != None:
                            nome = nome.username
                        else:
                            nome = nome.first_name
                    except KeyError:
                        continue
                    except RPCError as e:
                        print(e,utenteFor)
                        continue
                    await callback_query.answer("Questo account è gia registrato da {}".format(nome))
                    await callback_query.message.delete()
                    return        
            giocatori[utente] = dict()
            giocatori[utente]["tag"] = [giocatore]
            nome = (await app.get_users(utente)).username
            await callback_query.answer(f"{nome} è ora associato con il tag {giocatore}")
            player = await get_some_player(giocatore)
            await callback_query.edit_message_text(
                "Cosa vuoi visualizzare {}?\n\nPiù account? Usa nuovamente il comando con un tag e salvalo!".format(player),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Clan 🏰",
                                callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Stats 📊",
                                callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Truppe 👮‍♂",
                                callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Eroi 👑",
                                callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Incantesimi 👨‍🔬",
                                callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Risorse 🏝",
                                callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                ),
                            InlineKeyboardButton(
                                "Distruzione 🌋",
                                callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
         
                    ]
                )
            )

            SaveJson("giocatori.json",giocatori)
        else:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
    
    else:
        raise ContinuePropagation        

@app.on_callback_query()
async def AltroAccount(_,callback_query):
    if "aggiungiTag" in callback_query.data:

        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]

        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        for utenteFor in giocatori:
            if giocatore in giocatori[utenteFor]["tag"]:
                try:
                    nome = await app.get_users(int(utenteFor))
                    if nome != None:
                        nome = nome.username
                    else:
                        nome = nome.first_name
                except KeyError:
                    continue
                except RPCError as e:
                    print(e,utenteFor)
                    continue

                await callback_query.answer("Questo account è gia registrato da {}".format(nome))
                await callback_query.message.delete()
                return

        player = await get_some_player(giocatore)

        await callback_query.edit_message_text(
            "Confermi di voler aggiungere l'account secondario {}?".format(player),
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Sì",
                                callback_data="Sip|{}|{}".format(giocatore,utente)
                                ),
                            InlineKeyboardButton(
                                "No",
                                callback_data = "Nop|{}".format(utente)
                                )
                        ]
                    ]
                )
        )

    elif "Sip" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]

        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        for utenteFor in giocatori:
            if giocatore in giocatori[utenteFor]["tag"]:
                nome = (await app.get_users(utenteFor)).first_name
                await callback_query.answer("Questo account è gia registrato da {}!".format(nome))
                await callback_query.message.delete()
                return

        giocatori[utente]["tag"].append(giocatore)
        listaAccount = ""
        for account in giocatori[utente]["tag"]:
            player = await get_some_player(account)
            time.sleep(0.007)
            listaAccount += f"- {player}\n"
        await callback_query.edit_message_text("**Account Aggiunto!**\n\n**Lista account collegati a te:**\n{}".format(listaAccount))

        SaveJson("giocatori.json",giocatori)

    elif "Nop" in callback_query.data:
        utente = callback_query.data.split("|")[1]
        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return
        await callback_query.message.delete()

    else:
        raise ContinuePropagation

@app.on_callback_query()
async def ListaUtenti(_,callback_query):
    if "item" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        nome = items[giocatore]["nome"]
        utente = items[giocatore]["utente"]
        codice = callback_query.data.split("|")[2]


        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        player = await get_some_player(giocatore)

        try:
            await callback_query.edit_message_text(
                "Cosa vuoi visualizzare {}?".format(player),
                reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Clan 🏰",
                                    callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Profilo 📊",
                                    callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Truppe 👮‍♂",
                                    callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Eroi 👑",
                                    callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Incantesimi 👨‍🔬",
                                    callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Risorse 🏝",
                                    callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Distruzione 🌋",
                                    callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                  InlineKeyboardButton(
                                        "Cambia Account",
                                        callback_data="sceltone|{}|{}".format(codice,utente)
                                        )
                            ]           
                        ]
                    )
            )
        except MessageIdInvalid:
            await callback_query.answer("Mi dispiace, questa funzione non funziona in questa chat..")
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def scelta(_,callback_query):
    if "sceltone" in callback_query.data:
        codice = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        if callback_query.from_user.id != int(utente):
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        markup = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        start = 0
        for item in giocatori[utente]["tag"]:

            nome = await get_some_player(item)
            convertitore = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:13,13:14,14:0}
            start = convertitore[start]
            markup[start].append(InlineKeyboardButton(nome, f"item|{item}|{codice}"))
            
            items[item] = dict()
            items[item]["nome"] = nome.name
            items[item]["utente"] = utente

        await callback_query.edit_message_text("Scegli l'account che vuoi utilizzare 🧐",reply_markup=InlineKeyboardMarkup(markup))
        SaveJson("item.json",items)

    else:
        raise ContinuePropagation

@app.on_callback_query()
async def RichiestaRegistrazione(_,callback_query):
    if callback_query.data == "Registrazionbus":
        user = str(callback_query.from_user.id)

        if user not in registrazioni:
            privato = "__[privato](tg://user?id=747455144)__"
            await callback_query.answer("Non sei registrato , avvia il bot in privato e inizia la registrazione con /registrami",show_alert = True)
            return

        if user in giàRegistrati:
            await callback_query.answer("Hai già inviato la tua richiesta di iscrizione",show_alert = True)
            return

        if registrazioni[user]["inRegistrazione"] != -1:
            await callback_query.answer("Non hai completato la registrazione sul bot",show_alert = True)
            return

        firstName = (await app.get_users(int(user))).first_name
        nome = f"[{firstName}](tg://user?id={user})"
        player = await get_some_player(registrazioni[user]["tag"])
        heroes = player.heroes
        EroeStr = f"**Lista Eroi {player.name}:**\n"
        counter = 0
        for eroe in heroes:
            counter += 1
            nomeEroe = traduzioni[eroe.name.lower()]
            livello = eroe.level
            EroeStr += f"**{nomeEroe}** __Livello {livello}__\n"
        if counter == 0:
            EroeStr = f"{player.name} non ha nessun eroe"

        registrato = (
            f'**{nome} ha richiesto di iscriversi all\'evento!**\n\n'
            f'**Contatto Preferito**: {registrazioni[user]["accountPreferito"]}\n'
            f'**Account:** {registrazioni[user]["account"]}\n'
            f'**TAG:** {registrazioni[user]["tag"]}\n'
            f'**Livello Municipio:** {player.town_hall}\n'
            f'**Codice tessera GEC:** {registrazioni[user]["GEC"]}\n\n'
            f"{EroeStr}\n"
            f'Se hai deciso di aggiungerlo all\'evento usa il comando `/gestisciEventi {registrazioni[user]["tag"]}`'
            )


        try:
            sendRegistrazione = ["Anatras02","Jokerino00",807419215,"redthemaster"]
            for admin in sendRegistrazione:
                try:
                    await app.send_message(admin,registrato)
                    await callback_query.answer("La tua registrazione è stata inviata con successo")
                except RPCError:
                    continue
            giàRegistrati.append(user)

        except FloodWait as e:
            await callback_query.answer("Riprova fra {} secondi".format(e.x))
            time.sleep(e.x)


        SaveJson("giaReg.json",giàRegistrati)
    else:
        raise ContinuePropagation
"""
Comandi
"""


@app.on_callback_query()
async def profilo(_,callback_query):
    if "stats" in callback_query.data:
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]

        if callback_query.from_user.id != int(utente):
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return
        giocatore = callback_query.data.split("|")[1]
        player = await get_some_player(giocatore)
        #info base
        nome = player.name
        LvlMunicipio = player.town_hall
        if player.league == None:
            league = "Non Classificato"
        else:
            league = player.league.name
        trofei = player.trophies
        maxTrofei = player.best_trophies
        spells = player.ordered_spells
        #info team
        if player.clan == None:
            clan = "nessuno"
            ruolo = "nessuno"
        else:
            clan = player.clan
            ruolo = player.role
        stelleWar = player.war_stars
        attacchiVinti = player.attack_wins
        difeseVinte = player.defense_wins
        donazioni = player.donations
        ricevute = player.received
        #Builder Hall
        BHLvl = player.builder_hall
        BHBestTrofei = player.best_versus_trophies
        BHTrophies = player.versus_trophies
        BHAttacchi = player.versus_attacks_wins

        messaggio = STATS.format(
            id = giocatore,
            nome = nome,
            LvlMunicipio = LvlMunicipio,
            league = league,
            trofei = trofei,
            maxTrofei = maxTrofei,
            team = clan,
            ruolo = ruolo,
            stelleWar = stelleWar,
            attacchiVinti = attacchiVinti,
            difeseVinte = difeseVinte,
            donazioni = donazioni,
            ricevute = ricevute,
            BHLvl = BHLvl,
            BHTrophies = BHTrophies,
            BHBestTrofei = BHBestTrofei,
            BHAttacchi = BHAttacchi
            )
        try:
            await callback_query.edit_message_text(
                    messaggio,        
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    ),

                            ],
                  
                        ]
                    )
                )
        except FloodWait:
            await callback_query.answer("Aspetta un attimo..") 
            return
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def Menuprincipale(_,callback_query):
    if "principale" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]

        flag = False

        if utente in giocatori:
            flag = True

        if f[f"{utente}{codice}"]["flag"]== None:
            if utente in giocatori:
                flag = "abacab"

        if callback_query.from_user.id != int(utente):
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return
        player = await get_some_player(giocatore)

        try:
            if flag == False:
                await callback_query.edit_message_text(
                    "Cosa vuoi visualizzare {}?".format(player),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Clan 🏰",
                                    callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Profilo 📊",
                                    callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Truppe 👮‍♂",
                                    callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Eroi 👑",
                                    callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Incantesimi 👨‍🔬",
                                    callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Risorse 🏝",
                                    callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Distruzione 🌋",
                                    callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],  
                            [
                              InlineKeyboardButton(
                                    "Aggiungi TAG",
                                    callback_data="aggiungiTag|{}|{}|{}".format(giocatore,utente,codice)
                                    )  
                            ]             
                        ]
                    )
                )
            elif flag == True:
                await callback_query.edit_message_text(
                    "Cosa vuoi visualizzare {}?".format(player),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Clan 🏰",
                                    callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Profilo 📊",
                                    callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Truppe 👮‍♂",
                                    callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Eroi 👑",
                                    callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Incantesimi 👨‍🔬",
                                    callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Risorse 🏝",
                                    callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Distruzione 🌋",
                                    callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Associa TAG",
                                    callback_data="asssocia|{}|{}|{}".format(giocatore,utente,codice)
                                    )                      
                            ]               
                        ]
                    )
                )
            else:
                await callback_query.edit_message_text(
                    "Cosa vuoi visualizzare {}?".format(player),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Clan 🏰",
                                    callback_data="clan|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Profilo 📊",
                                    callback_data="stats|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Truppe 👮‍♂",
                                    callback_data="truppe|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Eroi 👑",
                                    callback_data="eroe|{}|{}|{}".format(giocatore,utente,codice)
                                    )

                            ],
                            [
                                InlineKeyboardButton(
                                    "Incantesimi 👨‍🔬",
                                    callback_data="incantesimi|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Risorse 🏝",
                                    callback_data="risorse|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                                InlineKeyboardButton(
                                    "Distruzione 🌋",
                                    callback_data="distruzione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                              InlineKeyboardButton(
                                    "Cambia Account",
                                    callback_data="sceltone|{}|{}".format(codice,utente)
                                    )
                            ]     
                        ]
                    )
                )
        except FloodWait:
            await callback_query.answer("Aspetta un attimo..") 
            return

    else:
        raise ContinuePropagation

@app.on_callback_query()
async def clan(app,callback_query):
    if "clan" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]

        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        player = await get_some_player(giocatore)
        try:
            clanTag = player.clan.tag
        except AttributeError:
            try:
                await callback_query.edit_message_text(
                    f"__{player}__ non è in nessun clan 🤷‍♂",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    ),

                            ],
                  
                        ]
                    )
                    )
            except FloodWait:
                await callback_query.answer("Aspetta un attimo..") 
                return
            return
        clan = await client.get_clan("#J22V0U8Y")
        trad = {"inWar":"In guerra","friendly":"Amichevole","random":"Random","warEnded":"Guerra Finita",
            "winning":"Sta vincendo","tied":"In pareggio","losing":"Sta perdendo","won":"Vinta","tie":"Pareggiata",
            "lost":"Persa","preparation":"Preparazione","notInWar":"Non in guerra","inviteOnly":"A solo invito","open":"Aperto",
            "preparation":"Preparazione",None:""}
        clan = await client.get_clan(clanTag)
        nome = clan.name
        livello = clan.level
        membri = clan.member_count
        try:
            tipo = trad[clan.type]
        except KeyError:
            tipo = clan.type
        trofeiRichiesti = punti(clan.required_trophies)
        winStreak = clan.war_win_streak
        vinte = clan.war_wins
        pareggiate = clan.war_ties
        perse = clan.war_losses
        trofei = clan.points
        messaggio = (
            f"**__Informazioni Clan {nome}__**\n"
            f"🔰 **Tipo Clan:** {tipo}\n"
            f"👥 **Totale Membri:** {membri}\n"
            f"🏆 **Trofei Richiesti:** {trofeiRichiesti}\n"
            f"🏆 **Trofei Totali:** {trofei}\n"
            f"🌡️ **Livello:** {livello}\n"
            "\n**__Informazioni Guerra__ ⚔️**\n"
            f"🥇 **Vinte:** {vinte}\n"
            f"🥈 **Pareggiate:** {pareggiate}\n"
            f"🥉 **Perse:** {perse}\n"
            f"💥 **Serie di Vittorie:** {winStreak}\n"
            )

        messaggio = messaggio.replace("None","")

        if clan.public_war_log == False:
            war = "\n**Guerra:** __Log guerra privati__ 🔒\n"
        else:
            clanWar = await client.get_clan_war(clanTag)
            try:
                state = trad[clanWar.state]
            except KeyError:
                state = clanWar.state

            try:
                tipo = trad[clanWar.type]
                clanA = clanWar.clan
                opponent = clanWar.opponent
                numero = len(clanWar.members)
                status = trad[clanWar.status]
            except AttributeError:
                tipo = ""
                clanA = ""
                opponent = ""
                numero = ""
                status = "" 


            war = (
                f"\n**__Guerra__ **"
                f"__{clanA}__ ⚔️ __{opponent}__\n"
                f"⚠️ **Stato:** {state}\n"
                f"📊 **Status:** {status}\n"
                f"🎯 **Tipo**: {tipo}\n"
                f"👥 **Partecipanti**: {numero}\n"
                )

            war.replace("None","")


        try:
            leagueGroup = await client.get_league_group(clanTag)
            try:
                state = trad[leagueGroup.state]
            except KeyError:
                state = leagueGroup.state
            season = leagueGroup.season
            clans = leagueGroup.clans
            clanStr = ""
            for clan in clans:
                clanStr += f"__{clan}__ - Livello {clan.level}\n"

            league = (
                "\n**__Lega__**\n"
                f"⚠️ **Stato:** {state}\n"
                f"🌦️ **Stagione:** {season}\n"
                f"👥 **Clan Partecipanti:\n** {clanStr}\n"
            )
        except coc.errors.NotFound:
            league = "\n**__Lega:__** Non in corso 😴"

            league.replace("None","")


        await callback_query.edit_message_text(
            messaggio+war+league,
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Menù Principale",
                                callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                ),

                        ],
              
                    ]
                )
            )
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def incantesimi(_,callback_query):
    if "incantesimi" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]
        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        player = await get_some_player(giocatore)
        spells = player.spells
        spellStr = f"**Lista Spells {player.name}:**\n"
        counter = 0
        for spell in spells:
            counter += 1
            nome = traduzioni[spell.name.lower()]
            livello = spell.level
            if spell.is_builder_base:
                emoji = "🏫"
            else:
                emoji = ""
            spellStr += f"**{nome}** __Livello {livello}__ {emoji}\n"
        if counter == 0:
            spellStr = f"{player.name} non ha nessuna pozione."
        try:
            await callback_query.edit_message_text(
                spellStr,
                reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    ),

                            ],
                  
                        ]
                    )            
                )
        except FloodWait:
                await callback_query.answer("Aspetta un attimo..") 
                return
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def truppe(_,callback_query):
    if "truppe" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]
        player = await get_some_player(giocatore)
        troops = player.troops

        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        builderBaseStr = "\n**__Base Costruttore__** 🏫\n"
        rosaStr = "\n**Elisir Rosa** 🔮\n"
        neroStr = "\n**Elisir Nero** ⚫️\n"
        oroStr = "\n**Oro** 💰\n"
        otherStr = f"**Lista truppe di {player.name}:**\n\n**__Villaggio base__** 🏛"

        elisirNero =  ["Sgherro", "Domatore di Cinghiali","Valchiria", "Golem", "Strega", "Mastino", "Bocciatore", "Golem di Ghiaccio"]
        oro =  ["Sgretolamuri", "Dirigibile", "Sganciapietre"]
        elisirRosa = ["Barbaro", "Arciere", "Goblin", "Gigante", "Spaccamuro", "Mongolfiera", "Stregone", "Guaritore", "Drago", "P.E.K.K.A", "Cucciolo di Drago", "Minatore", "Drago Elettrico"]
        counter = 0

        #inizializza variabili controllo
        hereOro = False
        hereBH = False
        hereRos = False
        hereNer = False

        for troop in troops:
            counter += 1
            try:
                nome = traduzioni[troop.name.lower()] #traduzione
            except KeyError:
                nome = troop.name #se la traduzione non è avviabile usa nome originale

            livello = troop.level
            if troop.is_builder_base:
                builderBaseStr += f"**{nome}** __Livello {livello}__\n"
                hereBH = True
            elif nome in elisirRosa:
                rosaStr += f"**{nome}** __Livello {livello}__\n"
                hereRos = True
            elif nome in elisirNero:
                neroStr += f"**{nome}** __Livello {livello}__\n"
                hereNer = True
            elif nome in oro:
                oroStr += f"**{nome}** __Livello {livello}__\n"
                hereOro = True
            else:
                otherStr += f"**{nome}** __Livello {livello}__\n"

        if counter == 0: #se nessuna truppa esiste
            otherStr = f"{player.name} non ha nessuna truppa."
            oroStr = ""
            neroStr = ""
            rosaStr = ""
            builderBaseStr = ""

        #controlla se almeno una truppa esiste
        oroStr = here(oroStr,hereOro)
        rosaStr = here(rosaStr,hereRos)
        neroStr = here(neroStr,hereNer)
        builderBaseStr = here(builderBaseStr,hereBH)
        try:
            await callback_query.edit_message_text(
                otherStr+rosaStr+neroStr+oroStr+builderBaseStr,
                reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                            ],
                        ]
                    )
                )
        except FloodWait:
                await callback_query.answer("Aspetta un attimo..") 
                return
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def eroi(_,callback_query):
    if "eroe" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        codice = callback_query.data.split("|")[3]
        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        player = await get_some_player(giocatore)
        heroes = player.heroes
        EroeStr = f"**Lista Eroi {player.name}:**\n"
        counter = 0
        for eroe in heroes:
            counter += 1
            nome = traduzioni[eroe.name.lower()]
            livello = eroe.level
            EroeStr += f"**{nome}** __Livello {livello}__\n"
        if counter == 0:
            EroeStr = f"{player.name} non ha nessun eroe"
        try:
            await callback_query.edit_message_text(
                EroeStr,
                reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    ),
                            ],
                        ]
                    )   
                )
        except FloodWait:
            await callback_query.answer("Aspetta un attimo..") 
            return
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def risorseF(_,callback_query):
    try:
        if "risorse" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                    await callback_query.answer("Non puoi usare la tastiera degli altri!")
                    return

            player = await get_some_player(giocatore)

            if giocatore in risorsePers.keys():
                await callback_query.edit_message_text(
                    "Seleziona una scelta!",
                    reply_markup=InlineKeyboardMarkup(
                        [

                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse",
                                    callback_data="RisPers|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse Totali",
                                    callback_data="RisTot|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Visualizza Risorse Stagione",
                                    callback_data="RisStagione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Resetta",
                                    callback_data="Reset|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ]

                        ]
                    )
                )
            else:
                if f[f"{utente}{codice}"]["SoloLettura"]:
                    await callback_query.answer("Questo utente non ha è ancora registrato le proprie risorse, non puoi ancora visualizzare questo menù!",show_alert = True)
                    return
                await callback_query.edit_message_text(
                    "Premi il pulsante sottostante per iniziare 😃",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Inizia",
                                    callback_data="Iniziaa|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ]

                        ]
                    )
                )

        elif "Iniziaa" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            player = await get_some_player(giocatore)
            risorsePers[giocatore] = dict()
            achivments = player.achievements_dict
            elixir = achivments["Elixir Escapade"].value
            gold = achivments["Gold Grab"].value    
            dark = achivments["Heroic Heist"].value

            ora = convert_int(datetime.datetime.now().hour,2)
            minuti = convert_int(datetime.datetime.now().minute,2)
            schedule.clear(f"Evento {giocatore}")
            schedule.every().day.at(f"{ora}:{minuti}").do(aggiornaGiorno, giocatore).tag(f"Evento {giocatore}")
            risorsePers[giocatore]["dataSchedule"] = f"{ora}:{minuti}"
            risorsePers[giocatore]["giorni"] = 1
            risorsePers[giocatore]["startElixir"] = elixir
            risorsePers[giocatore]["startGold"] = gold
            risorsePers[giocatore]["startDark"] = dark
            risorsePers[giocatore]["startWarStars"] = player.war_stars
            risorsePers[giocatore]["startDonations"] = achivments["Friend in Need"].value

            risorsePers[giocatore]["startElixirSeason"] = elixir
            risorsePers[giocatore]["startGoldSeason"] = gold
            risorsePers[giocatore]["startDarkSeason"] = dark
            risorsePers[giocatore]["startWarStarsSeason"] = player.war_stars
            risorsePers[giocatore]["startDonationsSeason"] = achivments["Friend in Need"].value

            SaveJson("risorsePers.json",risorsePers)
            await callback_query.answer("Sei stato aggiunto!")
            await callback_query.edit_message_text(
                    "Seleziona una scelta!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse",
                                    callback_data="RisPers|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse Totali",
                                    callback_data="RisTot|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Visualizza Risorse Stagione",
                                    callback_data="RisStagione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Resetta",
                                    callback_data="Reset|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ],

                        ]
                    )
                )

        elif "RisPers" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return
            player = await get_some_player(giocatore)
            try:
                nome = player.name
                achivments = player.achievements_dict
                
                elixir = achivments["Elixir Escapade"].value - risorsePers[giocatore]["startElixir"]
                gold = achivments["Gold Grab"].value - risorsePers[giocatore]["startGold"]
                dark = achivments["Heroic Heist"].value - risorsePers[giocatore]["startDark"]
                stelle = player.war_stars - risorsePers[giocatore]["startWarStars"]
                donazioni = achivments["Friend in Need"].value - risorsePers[giocatore]["startDonations"]
                giorni = risorsePers[giocatore]["giorni"]
                elixirMedia = format_decimal(media(elixir,giorni), locale='de_DE')
                goldMedia = format_decimal(media(gold,giorni), locale='de_DE')
                darkMedia = format_decimal(media(dark,giorni), locale='de_DE')
                donazioniMedia = format_decimal(media(donazioni,giorni), locale='de_DE')

            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            if giorni == 1:
                giorno = "giorno"
            else:
                giorno = "giorni"

            messaggio = (
                f"**{nome} dopo {giorni} {giorno} è riuscito a racimolare: **\n"
                f"💶 Oro: {punti(gold)}\n"
                f"🔮 Elisir: {punti(elixir)}\n"
                f"⚫️ Nero: {punti(dark)}\n"
                f"⭐️ Stelle in Guerra: {punti(stelle)}\n"
                f"🛒 Donazioni: {punti(donazioni)}\n\n"
                "**📊 Medie Giornaliere**:\n"
                f"💶 Oro: {goldMedia}\n"
                f"🔮 Elisir: {elixirMedia}\n"
                f"⚫️ Nero: {darkMedia}\n"
                f"🛒 Donazioni: {donazioniMedia}\n\n"
                )
            
            try:
                await callback_query.edit_message_text(
                    messaggio,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="Meniu|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Aggiorna ♻️",
                                    callback_data="RisPers|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                        ]
                    )
                )
            except MessageNotModified:
                await callback_query.answer("Non c'è nulla di nuovo")

        elif "Meniu" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            await callback_query.edit_message_text(
                    "Seleziona una scelta!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse",
                                    callback_data="RisPers|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Risorse Totali",
                                    callback_data="RisTot|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Visualizza Risorse Stagione",
                                    callback_data="RisStagione|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Resetta",
                                    callback_data="Reset|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],

                        ]
                    )
                )

        elif "Reset" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            if f[f"{utente}{codice}"]["SoloLettura"] == True:
                await callback_query.answer("Stai guardando questo account solo di lettura!\n\nSe questo account è tuo associa il tag al tuo account telegram!",show_alert = True)

                return

            player = await get_some_player(giocatore)
            try:
                risorsePers[giocatore]
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            ora = convert_int(datetime.datetime.now().hour,2)
            minuti = convert_int(datetime.datetime.now().minute,2)
            schedule.clear(f"Evento {giocatore}")
            schedule.every().day.at(f"{ora}:{minuti}").do(aggiornaGiorno, giocatore).tag(f"Evento {giocatore}")

            risorsePers[giocatore] = dict()
            risorsePers[giocatore]["dataSchedule"] = f"{ora}:{minuti}"
            risorsePers[giocatore]["giorni"] = 1
            achivments = player.achievements_dict
            elixir = achivments["Elixir Escapade"].value
            gold = achivments["Gold Grab"].value    
            dark = achivments["Heroic Heist"].value

            risorsePers[giocatore]["startElixir"] = elixir
            risorsePers[giocatore]["startGold"] = gold
            risorsePers[giocatore]["startDark"] = dark
            risorsePers[giocatore]["startWarStars"] = player.war_stars
            risorsePers[giocatore]["startDonations"] = achivments["Friend in Need"].value
            SaveJson("risorsePers.json",risorsePers)
            await callback_query.answer("Dati resettati")

        elif "RisTot" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            player = await get_some_player(giocatore)
            try:
                risorsePers[giocatore]
                nome = player.name
                achivments = player.achievements_dict
                
                elixir = achivments["Elixir Escapade"].value
                gold = achivments["Gold Grab"].value
                dark = achivments["Heroic Heist"].value
                stelle = punti(player.war_stars)
                donazioni = punti(achivments["Friend in Need"].value)
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            elixir = '{0:,}'.format(elixir)
            gold = '{0:,}'.format(gold)
            dark = '{0:,}'.format(dark)

            elixir = elixir.replace(",", ".")
            gold = gold.replace(",", ".")
            dark = dark.replace(",", ".")
            
            messaggio = (
                f"**{nome} dall'inzio del gioco è riuscito a racimolare: **\n"
                f"💶 Oro: {gold}\n"
                f"🔮 Elisir: {elixir}\n"
                f"⚫️ Nero: {dark}\n\n"
                f"⭐️ Stelle in Guerra: {stelle}\n"
                f"🛒 Donazioni: {donazioni}\n"
                )
            
            try:
                await callback_query.edit_message_text(
                    messaggio,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="Meniu|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Aggiorna ♻️",
                                    callback_data="RisTot|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                        ]
                    )
                )
            except MessageNotModified:
                await callback_query.answer("Non c'è nulla di nuovo")
        
        elif "RisStagione" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            player = await get_some_player(giocatore)
            try:
                nome = player.name
                achivments = player.achievements_dict
                
                elixir = achivments["Elixir Escapade"].value - risorsePers[giocatore]["startElixirSeason"]
                gold = achivments["Gold Grab"].value - risorsePers[giocatore]["startGoldSeason"]
                dark = achivments["Heroic Heist"].value - risorsePers[giocatore]["startDarkSeason"]
                stelle = player.war_stars - risorsePers[giocatore]["startWarStarsSeason"]
                donazioni = achivments["Friend in Need"].value - risorsePers[giocatore]["startDonationsSeason"]
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return  

            data = datetime.datetime.now()
            messaggio = (
                f"**{nome} nella stagione {data.strftime('%B %Y').title()} ha racimolato:**\n"
                f"💶 Oro: {punti(gold)}\n"
                f"🔮 Elisir: {punti(elixir)}\n"
                f"⚫️ Nero: {punti(dark)}\n"
                f"⭐️ Stelle in Guerra: {punti(stelle)}\n"
                f"🛒 Donazioni: {punti(donazioni)}\n\n"
                )

            try:
                await callback_query.edit_message_text(
                    messaggio,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="Meniu|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Aggiorna ♻️",
                                    callback_data="RisStagione|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                        ]
                    )
                )
            except MessageNotModified:
                await callback_query.answer("Non c'è nulla di nuovo")

    except FloodWait:
        await callback_query.answer("Aspetta un attimo..") 
        return
    
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def distruzione(_,callback_query):
    try:
        if "distruzione" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            player = await get_some_player(giocatore)

            if giocatore in distruzioni.keys():
                await callback_query.edit_message_text(
                    "Seleziona una scelta!",
                    reply_markup=InlineKeyboardMarkup(
                        [

                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Distruzioni",
                                    callback_data="PvtDistr|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Visualizza Distruzioni Totali",
                                    callback_data="distruzioniTot|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Resetta",
                                    callback_data="ReseetDistr|{}|{}|{}".format(giocatore,utente,codice)
                                    )
                            ],
                            [
                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                    )
                            ]


                        ]
                    )
                )
            else:
                if f[f"{utente}{codice}"]["SoloLettura"]:
                    await callback_query.answer("Questo utente non ha è ancora registrato le proprie risorse, non puoi ancora visualizzare questo menù!",show_alert = True)
                    return
                await callback_query.edit_message_text(
                    "Premi il pulsante sottostante per iniziare 😃",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Inizia",
                                    callback_data="IniziaDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                            [

                                InlineKeyboardButton(  # 
                                    "Menù Principale",
                                    callback_data="principale|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ]
                        ]
                    )
                )

        elif "IniziaDistr" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]
            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            if f[f"{utente}{codice}"]["SoloLettura"] == True:
                await callback_query.answer("Stai guardando questo account solo di lettura!\n\nSe questo account è tuo associa il tag al tuo account telegram!",show_alert = True)
                return

            player = await get_some_player(giocatore)
            distruzioni[giocatore] = dict()
            achivments = player.achievements_dict

            ora = convert_int(datetime.datetime.now().hour,2)
            minuti = convert_int(datetime.datetime.now().minute,2)
            schedule.clear(f"distr {giocatore}")
            schedule.every().day.at(f"{ora}:{minuti}").do(aggiornaGiornoDistr, giocatore).tag(f"distr {giocatore}")
            distruzioni[giocatore]["dataSchedule"] = f"{ora}:{minuti}"
            distruzioni[giocatore]["giorni"] = 1
            municipio = achivments["Humiliator"].value
            mura = achivments["Wall Buster"].value
            mortai = achivments["Mortar Mauler"].value
            arcoX = achivments["X-Bow Exterminator"].value
            inferno = achivments["Firefighter"].value
            aquila = achivments["Anti-Artillery"].value

            distruzioni[giocatore]["startMunicipio"] = municipio
            distruzioni[giocatore]["startMura"] = mura
            distruzioni[giocatore]["startMortai"] = mortai
            distruzioni[giocatore]["startArco"] = arcoX
            distruzioni[giocatore]["startInferno"] = inferno
            distruzioni[giocatore]["startAquila"] = aquila
            SaveJson("distruzioni.json",distruzioni)
            await callback_query.answer("Sei stato aggiunto!")
            await callback_query.edit_message_text(
                "Seleziona una scelta!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni",
                                callback_data="PvtDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni Totali",
                                callback_data="distruzioniTot|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Resetta",
                                callback_data="ReseetDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="MenuDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ]


                    ]
                )
            )

        elif "PvtDistr" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]

            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return
            player = await get_some_player(giocatore)
            try:
                nome = player.name
                achivments = player.achievements_dict
                
                achivments = player.achievements_dict
                municipio = achivments["Humiliator"].value - distruzioni[giocatore]["startMunicipio"]
                mura = achivments["Wall Buster"].value - distruzioni[giocatore]["startMura"]
                mortai = achivments["Mortar Mauler"].value - distruzioni[giocatore]["startMortai"]
                arcoX = achivments["X-Bow Exterminator"].value - distruzioni[giocatore]["startArco"]
                inferno = achivments["Firefighter"].value - distruzioni[giocatore]["startInferno"]
                aquila = achivments["Anti-Artillery"].value - distruzioni[giocatore]["startAquila"]
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            municipio = '{0:,}'.format(municipio)
            mura = '{0:,}'.format(mura)
            mortai = '{0:,}'.format(mortai)
            arcoX = '{0:,}'.format(arcoX)
            inferno = '{0:,}'.format(inferno)
            aquila = '{0:,}'.format(aquila)

            municipio = municipio.replace(",", ".")
            mura = mura.replace(",", ".")
            mortai = mortai.replace(",", ".")
            arcoX = arcoX.replace(",", ".")
            inferno = inferno.replace(",", ".")
            aquila = aquila.replace(",", ".")
            

            giorni = distruzioni[giocatore]["giorni"]
            if giorni == 1:
                giorno = "giorno"
            else:
                giorno = "giorni"
            
            messaggio = (
                f"**{nome} dopo {giorni} {giorno} è riuscito a distruggere: **\n"
                f"🏛 Municipi: {municipio}\n"
                f"🧱 Mura: {mura}\n"
                f"🚀 Mortai: {mortai}\n"
                f"🏹 Archi X: {arcoX}\n"
                f"🗼 Torri Inferno: {inferno}\n"
                f"🦅 Artiglieria Aquila: {aquila}"
                )
            
            try:
                await callback_query.edit_message_text(
                    messaggio,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                            InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="MenuDistr|{}|{}|{}".format(giocatore,utente,codice) # Note how callback_data must be bytes
                                )
                            ],
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Aggiorna ♻️",
                                    callback_data="PvtDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                        ]
                    )
                )
            except MessageNotModified:
                await callback_query.answer("Non c'è nulla di nuovo")

        elif "MenuDistr" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]
            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return
            await callback_query.edit_message_text(
                "Seleziona una scelta!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni",
                                callback_data="PvtDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni Totali",
                                callback_data="distruzioniTot|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Resetta",
                                callback_data="ReseetDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Torna al Menù",
                                callback_data="principale|{}|{}|{}".format(giocatore,utente,codice)
                                )
                        ]


                    ]
                )
            )

        elif "ReseetDistr" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]
            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return

            if f[f"{utente}{codice}"]["SoloLettura"] == True:
                await callback_query.answer("Stai guardando questo account solo di lettura!\n\nSe questo account è tuo associa il tag al tuo account telegram!",show_alert = True)
                return
            player = await get_some_player(giocatore)
            try:
                distruzioni[giocatore]
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            ora = convert_int(datetime.datetime.now().hour,2)
            minuti = convert_int(datetime.datetime.now().minute,2)
            schedule.clear(f"distr {giocatore}")
            schedule.every().day.at(f"{ora}:{minuti}").do(aggiornaGiornoDistr, giocatore).tag(f"distr {giocatore}")
            
            distruzioni[giocatore] = dict()
            distruzioni[giocatore]["dataSchedule"] = f"{ora}:{minuti}"
            distruzioni[giocatore]["giorni"] = 1
            achivments = player.achievements_dict
            municipio = achivments["Humiliator"].value
            mura = achivments["Wall Buster"].value
            mortai = achivments["Mortar Mauler"].value
            arcoX = achivments["X-Bow Exterminator"].value
            inferno = achivments["Firefighter"].value
            aquila = achivments["Anti-Artillery"].value

            distruzioni[giocatore]["startMunicipio"] = municipio
            distruzioni[giocatore]["startMura"] = mura
            distruzioni[giocatore]["startMortai"] = mortai
            distruzioni[giocatore]["startArco"] = arcoX
            distruzioni[giocatore]["startInferno"] = inferno
            distruzioni[giocatore]["startAquila"] = aquila
            SaveJson("distruzioni.json",distruzioni)
            await callback_query.answer("Dati resettati")

        elif "distruzioniTot" in callback_query.data:
            giocatore = callback_query.data.split("|")[1]
            utente = callback_query.data.split("|")[2]
            codice = callback_query.data.split("|")[3]
            if int(utente) != callback_query.from_user.id:
                await callback_query.answer("Non puoi usare la tastiera degli altri!")
                return
            player = await get_some_player(giocatore)
            try:
                distruzioni[giocatore]
                nome = player.name
                achivments = player.achievements_dict
                
                municipio = achivments["Humiliator"].value
                mura = achivments["Wall Buster"].value
                mortai = achivments["Mortar Mauler"].value
                arcoX = achivments["X-Bow Exterminator"].value
                inferno = achivments["Firefighter"].value
                aquila = achivments["Anti-Artillery"].value

                distruzioni[giocatore]["startMunicipio"] = municipio
                distruzioni[giocatore]["startMura"] = mura
                distruzioni[giocatore]["startMortai"] = mortai
                distruzioni[giocatore]["startArco"] = arcoX
                distruzioni[giocatore]["startInferno"] = inferno
                distruzioni[giocatore]["startAquila"] = aquila
            except KeyError:
                await callback_query.answer('Non sei registrato, usa il tasto "Inizia" per iscriverti')
                return

            municipio = '{0:,}'.format(municipio)
            mura = '{0:,}'.format(mura)
            mortai = '{0:,}'.format(mortai)
            arcoX = '{0:,}'.format(arcoX)
            inferno = '{0:,}'.format(inferno)
            aquila = '{0:,}'.format(aquila)

            municipio = municipio.replace(",", ".")
            mura = mura.replace(",", ".")
            mortai = mortai.replace(",", ".")
            arcoX = arcoX.replace(",", ".")
            inferno = inferno.replace(",", ".")
            aquila = aquila.replace(",", ".")
            
            messaggio = (
                f"**{nome} dall'inzio del gioco è riuscito a distruggere: **\n"
                f"🏛 Municipi: {municipio}\n"
                f"🧱 Mura: {mura}\n"
                f"🚀 Mortai: {mortai}\n"
                f"🏹 Archi X: {arcoX}\n"
                f"🗼 Torri Inferno: {inferno}\n"
                f"🦅 Artiglieria Aquila: {aquila}"
                )
            
            try:
                await callback_query.edit_message_text(
                    messaggio,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Torna Indietro",
                                    callback_data="MenuDistr|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                            [  # First row
                                InlineKeyboardButton(  # 
                                    "Aggiorna ♻️",
                                    callback_data="distruzioniTot|{}|{}|{}".format(giocatore,utente,codice)
                                )
                            ],
                        ]
                    )
                )
            except MessageNotModified:
                await callback_query.answer("Non c'è nulla di nuovo")
    
    except FloodWait:
        await callback_query.answer("Aspetta un attimo..") 
        return
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def classifica(_,callback_query):
    if "Mun" in callback_query.data:
        key = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]
        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return
        tipoClassifica = findKey(key)
        messaggioTh4 = municipi[tipoClassifica]["messaggioTh4"]
        messaggioTh5 = municipi[tipoClassifica]["messaggioTh5"]
        messaggioTh6 = municipi[tipoClassifica]["messaggioTh6"]
        messaggioTh7 = municipi[tipoClassifica]["messaggioTh7"]
        messaggioTh8 = municipi[tipoClassifica]["messaggioTh8"]
        messaggioTh9 = municipi[tipoClassifica]["messaggioTh9"]
        messaggioTh10 = municipi[tipoClassifica]["messaggioTh10"]
        messaggioTh11 = municipi[tipoClassifica]["messaggioTh11"]
        messaggioTh12 = municipi[tipoClassifica]["messaggioTh12"]

    if "classifica" in callback_query.data:
        key = callback_query.data.split("|")[1]
        utente = callback_query.data.split("|")[2]

        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return

        tipoClassifica = findKey(key)
        valore = findAch(key)


        for giocatore in risorse:
            player = await get_some_player(giocatore)
            achivments = player.achievements_dict
            risorse[giocatore]["robo"] = achivments[valore].value - risorse[giocatore][tipoClassifica]

        classifica = []
        classifica = sorted(risorse, key=lambda x: (risorse[x]["robo"]), reverse = True)

        municipi[tipoClassifica] = dict()


        municipi[tipoClassifica]["messaggioTh4"] = f"**Classifica Municipio Livello 4 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh5"] = f"**Classifica Municipio Livello 5 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh6"] = f"**Classifica Municipio Livello 6 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh7"] = f"**Classifica Municipio Livello 7 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh8"] = f"**Classifica Municipio Livello 8 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh9"] = f"**Classifica Municipio Livello 9 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh10"] = f"**Classifica Municipio Livello 10 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh11"] = f"**Classifica Municipio Livello 11 __{key.title()}__:**\n"
        municipi[tipoClassifica]["messaggioTh12"] = f"**Classifica Municipio Livello 12 __{key.title()}__:**\n"

        municipi[tipoClassifica]["pos4"] = 1
        municipi[tipoClassifica]["pos5"] = 1
        municipi[tipoClassifica]["pos6"] = 1
        municipi[tipoClassifica]["pos7"] = 1
        municipi[tipoClassifica]["pos8"] = 1
        municipi[tipoClassifica]["pos9"] = 1
        municipi[tipoClassifica]["pos10"] = 1
        municipi[tipoClassifica]["pos11"] = 1
        municipi[tipoClassifica]["pos12"] = 1

        for giocatore in classifica:
            LvlMunicipio = risorse[giocatore]["LvlMunicipio"]
            nome = risorse[giocatore]["nome"]

            puntiVar = punti(risorse[giocatore]["robo"])
            del risorse[giocatore]["robo"]

            AggStr(LvlMunicipio,puntiVar,nome,tipoClassifica)

        time = datetime.datetime.now()
        ora = f"{convert_int(time.hour,2)}:{convert_int(time.minute,2)}:{convert_int(time.second,2)}"

        municipi[tipoClassifica]["orario"] = ora

        await callback_query.edit_message_text(
            f"Scegli il livello del municipio di cui vuoi vedere la classifica.\n\nClassifica aggiornata alle ore {ora}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(
                                "Municipio Livello 12",
                                callback_data="Mun12|{}|{}".format(key,utente)
                            )
                        ],

                        [
                            InlineKeyboardButton(
                                "Municipio Livello 11",
                                callback_data="Mun11|{}|{}".format(key,utente)
                                ),
                            InlineKeyboardButton(
                                "Municipio Livello 10",
                                callback_data="Mun10|{}|{}".format(key,utente)
                                )

                        ],
                        [
                            InlineKeyboardButton(
                                "Municipio Livello 9",
                                callback_data="Mun9|{}|{}".format(key,utente)
                                ),
                            InlineKeyboardButton(
                                "Municipio Livello 8",
                                callback_data="Mun8|{}|{}".format(key,utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Municipio Livello 7",
                                callback_data="Mun7|{}|{}".format(key,utente)
                                ),
                            InlineKeyboardButton(
                                "Municipio Livello 6",
                                callback_data="Mun6|{}|{}".format(key,utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Municipio Livello 5",
                                callback_data="Mun5|{}|{}".format(key,utente)
                                ),
                            InlineKeyboardButton(
                                "Municipio Livello 4",
                                callback_data="Mun4|{}|{}".format(key,utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Aggiorna ♻️",
                                callback_data="classifica|{}|{}".format(key,utente)
                                ),
                            InlineKeyboardButton(
                                "Torna al Menù",
                                callback_data="scelta|{}|{}".format(key,utente)
                                )
                        ]
                    ]
                )
            )


        SaveJson("municipi.json",municipi)

    elif "Mun4" in callback_query.data:
        try:
            await callback_query.edit_message_text(
                messaggioTh4,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh4[i:i+n] for i in range(0, len(messaggioTh4), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun5" in callback_query.data:
        try:
            await callback_query.edit_message_text(
                messaggioTh5,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh5[i:i+n] for i in range(0, len(messaggioTh5), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun6" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh6,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh6[i:i+n] for i in range(0, len(messaggioTh6), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun7" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh7,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh7[i:i+n] for i in range(0, len(messaggioTh7), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun8" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh8,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh8[i:i+n] for i in range(0, len(messaggioTh8), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun9" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh9,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh9[i:i+n] for i in range(0, len(messaggioTh9), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun10" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh10,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh10[i:i+n] for i in range(0, len(messaggioTh10), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun11" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh11,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh11[i:i+n] for i in range(0, len(messaggioTh11), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "Mun12" in callback_query.data:
        try:
            
            await callback_query.edit_message_text(
                messaggioTh12,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna Indietro",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )
        except MessageTooLong:
            n = 3900
            msg = [messaggioTh12[i:i+n] for i in range(0, len(messaggioTh12), n)]
            await callback_query.edit_message_text(
                msg[0] + "\n\nLa classifica era troppo lunga, ho tagliato il messaggio",
                reply_markup = InlineKeyboardMarkup(
                    [
                        [  # First row
                        InlineKeyboardButton(
                            "Torna al Menù",
                            callback_data="classifica|{}|{}".format(key,utente)
                            )
                        ]
                    ]
                )
            )

    elif "scelta" in callback_query.data:
        utente = callback_query.data.split("|")[2]

        await callback_query.edit_message_text(
        "Scegli il tipo di classifica che vuoi visualizzare!",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Elisir Nero ⚫️",
                                callback_data="classifica|elisir nero|{}".format(utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Municipi 🏛",
                                callback_data="classifica|municipi|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Mura 🧱",
                                callback_data="classifica|mura|{}".format(utente)
                                ),
                        ],
                        [
                            InlineKeyboardButton(
                                "Mortai 🚀",
                                callback_data="classifica|mortai|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Archi X 🏹",
                                callback_data="classifica|archi x|{}".format(utente)
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                "Torri Inferno 🗼",
                                callback_data="classifica|torri inferno|{}".format(utente)
                                ),
                            InlineKeyboardButton(
                                "Artiglieria Aquila 🦅",
                                callback_data="classifica|artiglierie aquila|{}".format(utente)
                                )
                        ],
                    ]
            ) 
        )
        if int(utente) != callback_query.from_user.id:
            await callback_query.answer("Non puoi usare la tastiera degli altri!")
            return
        
    else:
        raise ContinuePropagation

@app.on_callback_query()
async def EventoeRisorse(_,callback_query):
    """
    callbackqueries Evento
    """  
    if "Evento" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        player = await get_some_player(giocatore)

        try:
            risorse[giocatore]
            await callback_query.answer("Questo utente è già all'interno di un evento")
            return
        except KeyError:
            pass

        risorse[giocatore] = dict()
        achivments = player.achievements_dict
        elixir = achivments["Elixir Escapade"].value
        gold = achivments["Gold Grab"].value
        dark = achivments["Heroic Heist"].value

        municipio = achivments["Humiliator"].value
        mura = achivments["Wall Buster"].value
        mortai = achivments["Mortar Mauler"].value
        arcoX = achivments["X-Bow Exterminator"].value
        inferno = achivments["Firefighter"].value
        aquila = achivments["Anti-Artillery"].value

        risorse[giocatore]["startElixir"] = elixir
        risorse[giocatore]["startGold"] = gold
        risorse[giocatore]["startDark"] = dark

        risorse[giocatore]["startMunicipio"] = municipio
        risorse[giocatore]["startMura"] = mura
        risorse[giocatore]["startMortai"] = mortai
        risorse[giocatore]["startArco"] = arcoX
        risorse[giocatore]["startInferno"] = inferno
        risorse[giocatore]["startAquila"] = aquila

        risorse[giocatore]["nome"] = player.name

        risorse[giocatore]["LvlMunicipio"] = player.town_hall

        risorse[giocatore]["torneo"] = True
        SaveJson("risorse.json",risorse)

        messaggio = (
            f"**Valori di partenza {player.name}:**\n"
            f"🏰 Livello Municipio: {player.town_hall}\n\n"
            f"💶 Oro: {punti(gold)}\n"
            f"🔮 Elisir: {punti(elixir)}\n"
            f"⚫️ Nero: {punti(dark)}\n\n"
            f"🏛 Municipi: {punti(municipio)}\n"
            f"🧱 Mura: {punti(mura)}\n"
            f"🚀 Mortai: {punti(mortai)}\n"
            f"🏹 Archi X: {punti(arcoX)}\n"
            f"🗼 Torri Inferno: {punti(inferno)}\n"
            f"🦅 Artiglieria Aquila: {punti(aquila)}"
            )

        await callback_query.edit_message_text(
            messaggio,
            reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # 
                            "Torna al Menù",
                            callback_data="Menù|{}".format(giocatore) # Note how callback_data must be bytes
                        )
                    ],
                ]
            )
        )

    elif "Chiudi" in callback_query.data:
        await callback_query.answer("Va bene, cancello il messaggio!")
        await callback_query.message.delete()

    elif "Risorse" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        player = await get_some_player(giocatore)
        try:
            nome = player.name
            achivments = player.achievements_dict
            elixir = punti(achivments["Elixir Escapade"].value - risorse[giocatore]["startElixir"])
            gold = punti(achivments["Gold Grab"].value - risorse[giocatore]["startGold"])
            dark = punti(achivments["Heroic Heist"].value - risorse[giocatore]["startDark"])
        except KeyError:
            await callback_query.answer("Il giocatore non sta partecipando all'evento")
            return
        
        messaggio = (
            f"**{nome} finora è riuscito a racimolare: **\n"
            f"💶 Oro: {gold}\n"
            f"🔮 Elisir: {elixir}\n"
            f"⚫️ Nero: {dark}"
            )
        
        try:
            await callback_query.edit_message_text(
                messaggio,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Torna al Menù",
                                callback_data="Menù|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Aggiorna ♻️",
                                callback_data="Risorse|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                    ]
                )
            )
        except MessageNotModified:
            await callback_query.answer("Non c'è nulla di nuovo")

    elif "Distruzioni" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        player = await get_some_player(giocatore)
        try:
            achivments = player.achievements_dict
            municipio = achivments["Humiliator"].value - risorse[giocatore]["startMunicipio"]
            mura = achivments["Wall Buster"].value - risorse[giocatore]["startMura"]
            mortai = achivments["Mortar Mauler"].value - risorse[giocatore]["startMortai"]
            arcoX = achivments["X-Bow Exterminator"].value - risorse[giocatore]["startArco"]
            inferno = achivments["Firefighter"].value - risorse[giocatore]["startInferno"]
            aquila = achivments["Anti-Artillery"].value - risorse[giocatore]["startAquila"]

            nome = player.name
        except KeyError:
            await callback_query.answer("Il giocatore non sta partecipando all'evento")
            return


        municipio = '{0:,}'.format(municipio)
        mura = '{0:,}'.format(mura)
        mortai = '{0:,}'.format(mortai)
        arcoX = '{0:,}'.format(arcoX)
        inferno = '{0:,}'.format(inferno)
        aquila = '{0:,}'.format(aquila)

        municipio = municipio.replace(",", ".")
        mura = mura.replace(",", ".")
        mortai = mortai.replace(",", ".")
        arcoX = arcoX.replace(",", ".")
        inferno = inferno.replace(",", ".")
        aquila = aquila.replace(",", ".")
        
        messaggio = (
            f"**{nome} finora è riuscito a distruggere: **\n"
            f"🏛 Municipi: {municipio}\n"
            f"🧱 Mura: {mura}\n"
            f"🚀 Mortai: {mortai}\n"
            f"🏹 Archi X: {arcoX}\n"
            f"🗼 Torri Inferno: {inferno}\n"
            f"🦅 Artiglieria Aquila: {aquila}"
            )
        
        try:
            await callback_query.edit_message_text(
                messaggio,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Torna al Menù",
                                callback_data="Menù|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Aggiorna ♻️",
                                callback_data="Distruzioni|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                    ]
                )
            )
        except MessageNotModified:
            await callback_query.answer("Non c'è nulla di nuovo")

    elif "Fine" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        player = await get_some_player(giocatore)
        
        try:
            risorse[giocatore]
        except KeyError:
            await callback_query.answer("Il giocatore non sta partecipando a nessun evento!")
            return

        if risorse[giocatore]["torneo"]:
            achivments = player.achievements_dict
            achivments = player.achievements_dict
            elixir = achivments["Elixir Escapade"].value - risorse[giocatore]["startElixir"]
            gold = achivments["Gold Grab"].value - risorse[giocatore]["startGold"]
            dark = achivments["Heroic Heist"].value - risorse[giocatore]["startDark"]
            municipio = achivments["Humiliator"].value - risorse[giocatore]["startMunicipio"]
            mura = achivments["Wall Buster"].value - risorse[giocatore]["startMura"]
            mortai = achivments["Mortar Mauler"].value - risorse[giocatore]["startMortai"]
            arcoX = achivments["X-Bow Exterminator"].value - risorse[giocatore]["startArco"]
            inferno = achivments["Firefighter"].value - risorse[giocatore]["startInferno"]
            aquila = achivments["Anti-Artillery"].value - risorse[giocatore]["startAquila"]

            nome = player.name
            elixir = '{0:,}'.format(elixir)
            gold = '{0:,}'.format(gold)
            dark = '{0:,}'.format(dark)
            municipio = '{0:,}'.format(municipio)
            mura = '{0:,}'.format(mura)
            mortai = '{0:,}'.format(mortai)
            arcoX = '{0:,}'.format(arcoX)
            inferno = '{0:,}'.format(inferno)
            aquila = '{0:,}'.format(aquila)

            elixir = elixir.replace(",", ".")
            gold = gold.replace(",", ".")
            dark = dark.replace(",", ".")
            municipio = municipio.replace(",", ".")
            mura = mura.replace(",", ".")
            mortai = mortai.replace(",", ".")
            arcoX = arcoX.replace(",", ".")
            inferno = inferno.replace(",", ".")
            aquila = aquila.replace(",", ".")

            messaggio = (
                f"**A fine evento {nome} è riuscito a racimolare: **\n"
                f"💶 Oro: {gold}\n"
                f"🔮 Elisir: {elixir}\n"
                f"⚫️ Nero: {dark}\n\n"
                f"🏛 Municipi: {municipio}\n"
                f"🧱 Mura: {mura}\n"
                f"🚀 Mortai: {mortai}\n"
                f"🏹 Archi X: {arcoX}\n"
                f"🗼 Torri Inferno: {inferno}\n"
                f"🦅 Artiglieria Aquila: {aquila}"
                )
            await callback_query.edit_message_text(
                messaggio,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Torna al Menù",
                                callback_data="Menù|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                    ]
                )
            )

            del risorse[giocatore]
            SaveJson("risorse.json",risorse)
        else:
            callback_query.answer("Il giocarore non sta partecipando a nessun evento")

    elif "Menù" in callback_query.data:
        giocatore = callback_query.data.split("|")[1]
        await callback_query.edit_message_text(
                "Seleziona una scelta!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Inizio Evento",
                                callback_data="Evento|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],
                        [  # First row
                            InlineKeyboardButton(  # 
                                "Fine Evento",
                                callback_data="Fine|{}".format(giocatore) # Note how callback_data must be bytes
                            )
                        ],

                        [
                            InlineKeyboardButton(  # 
                                "Visualizza Risorse",
                                callback_data="Risorse|{}".format(giocatore) # Note how callback_data must be bytes
                                ),
                            InlineKeyboardButton(  # 
                                "Visualizza Distruzioni",
                                callback_data="Distruzioni|{}".format(giocatore) # Note how callback_data must be bytes
                                )
                        ],
                        [
                            InlineKeyboardButton(  # 
                                "Chiudi",
                                callback_data="Chiudi" # Note how callback_data must be bytes
                                )
                        ],

                    ]
                )
            )

    else:
        raise ContinuePropagation


"""
Fine Bot
"""

@app.on_message(Filters.command("sbugga") & Filters.user("Anatras02"))
async def test(_,message):
    user = message.command[1]
    try:
        risultato = (await app.get_users(user)).username
    except RPCError as e:
        risultato = e

    await message.reply(risultato)
app.run()

running = False
t1.join()

client.close()