import random
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")
client = discord.Client()

client = commands.Bot(command_prefix='!')

class Case:
    def __init__(self,value,reveal):
        self.value = value
        self.reveal = reveal
        self.flag = False

class game_data:
    def __init__(self,user_id,matrice_max,nbr_mines,status,is_in_game):
        self.user_id = user_id
        self.matrice_max = matrice_max
        self.nbr_mines = nbr_mines
        self.matrice = []
        self.is_in_game = is_in_game
        self.status = 0
        self.restant = 0

Game_Data = game_data(0,0,0,0,False)

def init_mine(matrice,bord_sup):
    """
    Permet d'init une matrice de X*X
    """
    for i in range(0,15):
        
        line = [Case(0,False) for i in range(0,bord_sup)] # create new addr
        matrice.append(line)

def put_axis_number(matrice,x,y,bord_sup):
    """
    Place les nombres autour des mines
    """
    if x != 0:        
        if matrice[x-1][y].value != -1:
            matrice[x-1][y].value += 1
    
    if x != bord_sup - 1:
        if matrice[x+1][y].value != -1:
            matrice[x+1][y].value += 1 
    
    if y != bord_sup - 1:
        if matrice[x][y+1].value != -1:
            matrice[x][y+1].value += 1

    if y != 0:
       if matrice[x][y-1].value != -1:
            matrice[x][y-1].value += 1   
    
    if x != 0 and y != bord_sup - 1:
        if matrice[x-1][y+1].value != -1:
            matrice[x-1][y+1].value += 1
         
    if x != bord_sup and y != bord_sup - 1:
        if matrice[x+1][y+1].value != -1:
            matrice[x+1][y+1].value += 1
    
    if x != 0 and y != 0:
        if matrice[x-1][y-1].value != -1:
            matrice[x-1][y-1].value += 1

    if x != bord_sup - 1 and y != 0 :
        if matrice[x+1][y-1].value != -1:
            matrice[x+1][y-1].value += 1

def place_random_mines(matrice,bord_sup,nbr_mine):
    """
    Place de facon aleatoire des mines sans remise
    Une mine est represente par -1, autour sont des chiffres
    """
    
    list_choice   = [i for i in range(0,bord_sup * bord_sup)]
    result_random = random.sample(list_choice,nbr_mine)
   
    for i in range(0,nbr_mine):

        x_tmp = int(result_random[i] / bord_sup)
        y_tmp = result_random[i] % bord_sup
        matrice[x_tmp][y_tmp].value = -1
        put_axis_number(matrice,x_tmp,y_tmp,bord_sup)

def debug_print_matrice(matrice,bord_sup):
    """
    end print matrice...
    """
    buff = []
    for i in range(0,bord_sup):
        for j in range(0,bord_sup):
            buff.append(convert_number_into_emoji(matrice[i][j].value))
        buff.append('\n')
    return ''.join(buff)

def print_matrice(matrice,bord_sup):
    """
    Renvoie une chaine de caractere du jeu 
    """
    buff = []
    for i in range(0,bord_sup):
        for j in range(0,bord_sup):
            if matrice[i][j].reveal == True :
                buff.append(convert_number_into_emoji(matrice[i][j].value))
            else:
                if matrice[i][j].flag == True:
                    buff.append(':triangular_flag_on_post:')
                else:
                    buff.append(':blue_square:')
        buff.append('\n')
    return ''.join(buff)

def convert_number_into_emoji(number_ascii):
    """
    Converti l'affichage logique en affichage utilisateur
    """
    if number_ascii == -1:
        return ':red_square:'
    elif number_ascii == 0:
        return ':zero:'
    elif number_ascii == 1:
        return ':one:'
    elif number_ascii == 2:
        return ':two:'
    elif number_ascii == 3:
        return ':three:'
    elif number_ascii == 4:
        return ':four:'
    elif number_ascii == 5:
        return ':five:'
    elif number_ascii == 6:
        return ':six:'
    elif number_ascii == 7:
        return ':seven:'
    elif number_ascii == 8:
        return ':eight:'
    return 'error'

def recursive_reveal(Game_Data,X,Y):
    """
    Permet de reveler recursivement les cases 0
    """
    for i in range(-1,2):
        for j in range(-1,2):
            if not((X + i) > Game_Data.matrice_max - 1 or (X + i) < 0 or (Y + j) > Game_Data.matrice_max - 1 or (Y + j) < 0):
                if Game_Data.matrice[X+i][Y+j].reveal != True:
                    Game_Data.restant -= 1
                    Game_Data.matrice[X+i][Y+j].reveal = True
                    if Game_Data.matrice[X+i][Y+j].value == 0:
                        recursive_reveal(Game_Data,X+i,Y+j)
                        
@client.command(aliases=['D'])
async def demine(input_event,argX,argY):
    """
    Pour reveler la cases des coordonnées données en entrée
    """
    global Game_Data
    if Game_Data.is_in_game == True:
        X = int(argY)
        Y = int(argX)
        if X < 0 or X > Game_Data.matrice_max - 1 or Y < 0 or Y > Game_Data.matrice_max -1 or Game_Data.matrice[X][Y].reveal == True or Game_Data.matrice[X][Y].flag == True:
            await input_event.channel.send("Concentre-toi")
        else:
            if Game_Data.matrice[X][Y].value == -1:
                Game_Data.status = -1
            else:
                Game_Data.matrice[X][Y].reveal = True
                Game_Data.restant -= 1
                if Game_Data.matrice[X][Y].value == 0:
                    recursive_reveal(Game_Data,X,Y)

                await input_event.channel.send(print_matrice(Game_Data.matrice,Game_Data.matrice_max))
       
        await input_event.channel.send(Game_Data.restant)
        if(Game_Data.restant == 0):
            Game_Data.status = 1

        if(Game_Data.status == -1):
            await input_event.channel.send("Tu as perdu")
            await input_event.channel.send(debug_print_matrice(Game_Data.matrice,Game_Data.matrice_max))
            Game_Data.is_in_game = False
            Game_Data.matrice = [] # new addr
        
        if(Game_Data.status == 1):
            await input_event.channel.send("Tu as gagné")
            Game_Data.is_in_game = False
            Game_Data.matrice = [] 
    else:
        await input_event.channel.send("do !start")

@client.command(aliases=['F'])
async def flag(input_event,argX,argY):
    """
    Pour mettre un drapeau la ou peut se trouver une mine
    """
    global Game_Data
    if Game_Data.is_in_game == True:
        X = int(argY)
        Y = int(argX)
        if X < 0 or X > Game_Data.matrice_max - 1 or Y < 0 or Y > Game_Data.matrice_max -1 or Game_Data.matrice[X][Y].reveal == True:
            await input_event.channel.send("Concentre-toi...")
        else:
            Game_Data.matrice[X][Y].flag = not(Game_Data.matrice[X][Y].flag)
            await input_event.channel.send(print_matrice(Game_Data.matrice,Game_Data.matrice_max))
    else:
       await input_event.channel.send("do !start") 

@client.command(aliases=['A'])
async def aide(message):
    """ 
    affichage de l'aide
    """
    await message.channel.send("!G ou !gourou_demineur pour commencer une nouvelle partie")
    await message.channel.send("Les coords commencent par 0 et non 1")
    await message.channel.send("!F ou !flag argX argY pour placer un drapeau ou peut se trouver une mine")
    await message.channel.send("!D ou !demine argX argY pour deminer une case")

@client.command(aliases=['G'])
async def gourou_demineur(message):
    """
    Initialise le jeu 
    """
    global Game_Data
    if(Game_Data.is_in_game == False):
        # register id 
        Game_Data.nbr_mines = 10
        Game_Data.matrice_max = 10
        Game_Data.status = 0
        Game_Data.restant = (Game_Data.matrice_max * Game_Data.matrice_max) - Game_Data.nbr_mines
        init_mine(Game_Data.matrice,Game_Data.matrice_max)
        place_random_mines(Game_Data.matrice,Game_Data.matrice_max, Game_Data.nbr_mines)
        Game_Data.is_in_game = True
        await message.channel.send("MineSweeper 1.0")
        await message.channel.send("!A pour afficher les commandes")
        await message.channel.send(print_matrice(Game_Data.matrice,Game_Data.matrice_max))
    else:
        await message.channel.send("Game is running")

@client.command(aliases=['C'])
async def cheat(input_event,code):
    """
    permet de tricher
    """
    global Game_Data
    if int(code) == 1010:
        await input_event.channel.send(debug_print_matrice(Game_Data.matrice,Game_Data.matrice_max))
    else:
        await input_event.channel.send("Wrong code")

@client.command(aliases=['E'])
async def exit(message):
    """
    permet de quitter le jeu
    """
    global Game_Data
    Game_Data.is_in_game = False
    Game_Data.matrice = [] 
    await message.channel.send("Fin de jeu")

def main():
    client.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()
