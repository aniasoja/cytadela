from flask import Flask, render_template, request
import random

class Districts:
    def __init__(self, name, archetype, price, description):
        self.name = name
        self.archetype = archetype
        self.price = price
        self.description = description


class Characters:
    def __init__(self, name, level, description):
        self.name = name
        self.level = level
        self.description = description
        self.skill_used = False


class King(Characters):
    def skill(self, player):
        global crowned
        crowned = player
        for x in player.districts_in_hand:
            if x.archetype == 'noble':
                player.money += 1


class Bishop(Characters):
    def skill(self, player):
        for x in player.districts_in_hand:
            if x.archetype == 'religious':
                player.money += 1


class Merchant(Characters):
    def skill(self, player):
        for x in player.districts_in_hand:
            if x.archetype == 'trade':
                player.money += 1
        player.money += 1


class Architect(Characters):
    def skill(self, player):
        global free_districts
        a = random.choice(free_districts)
        b = random.choice(free_districts)
        player.districts_in_hand.append(a)
        player.districts_in_hand.append(b)
        free_districts.remove(a)
        free_districts.remove(b)
        c = 0
        for c in range(1, 4):
            d = input('Czy chcesz wybudować dodatkową dzielnicę?')
            if d == 'y':
                build(player)
            else:
                break


class Warlord(Characters):
    def skill(self, player):
        for x in player.districts_in_hand:
            if x.archetype == 'military':
                player.money += 1
        if player is player1:
            other_player = player2
        elif player is player2:
            other_player = player1
        for x in other_player.districts_built:
            print(x.name)
        ruin = input('Jaką dzielnicę przeciwnika chcesz zburzyć za cenę o 1 mniejsza niż jej budowa?')
        for x in other_player.districts_built:
            if x.name == ruin:
                ruin = x
        other_player.districts_built.remove(ruin)
        player.money -= (ruin.price - 1)

class Players:
    def __init__(self, name):
        self.name = name
        self.money = 2
        self.districts_built = []

    def start_round(name):
        name.money = 2
        name.districts_built = []
        name.districts_in_hand = []
        for x in range(1, 5):
            a = random.choice(free_districts)
            name.districts_in_hand.append(a)
            free_districts.remove(a)
        name.computer = False
        name.crown = False
        name.characters = []

player1 = Players('player1')
player2 = Players('player2')
crowned = ''
next_player = ''
opponent = ''

all_districts = []
free_districts = []
dragon_gate = Districts('dragon_gate', 'special', 6, '')
all_districts.append(dragon_gate)
map_room = Districts('map_room', 'special', 5, '')
all_districts.append(map_room)
imperial_treasury = Districts('imperial_treasury', 'special', 4, '')
all_districts.append(imperial_treasury)
factory = Districts('factory', 'special', 6, '')
all_districts.append(factory)
wishing_well = Districts('wishing_well', 'special', 5, '')
all_districts.append(wishing_well)
school_of_magic = Districts('school_of_magic', 'special', 6, '')
all_districts.append(school_of_magic)
quarry = Districts('quarry', 'special', 5,'')
all_districts.append(quarry)
observatory = Districts('observatory', 'special', 5, '')
all_districts.append(observatory)
graveyard = Districts('graveyard', 'special', 5, '')
all_districts.append(graveyard)
university = Districts('university', 'special', 6, '')
all_districts.append(university)
ball_room = Districts('ball_room', 'special', 6,'')
all_districts.append(ball_room)
museum = Districts('museum', 'special', 4, '')
all_districts.append(museum)
battlefield = Districts('battlefield', 'military', 3, '')
for x in range(4):
    all_districts.append(battlefield)
prison = Districts('prison', 'military', 2, '')
for x in range(4):
    all_districts.append(prison)
fortress = Districts('fortress', 'military', 5,'')
for x in range(3):
    all_districts.append(fortress)
watchtower = Districts('watchtower', 'military', 1, '')
for x in range(4):
    all_districts.append(watchtower)
manor = Districts('manor', 'noble', 3, '')
for x in range(6):
    all_districts.append(manor)
castle = Districts('castle', 'noble', 4, '')
for x in range(5):
    all_districts.append(castle)
palace = Districts('palace', 'noble', 5, '')
for x in range(4):
    all_districts.append(palace)
market = Districts('market', 'trade', 2, '')
for x in range(5):
    all_districts.append(market)
town_hall = Districts('town_hall', 'trade', 5, '')
for x in range(3):
    all_districts.append(town_hall)
trading_post = Districts('trading_post', 'trade', 2, '')
for x in range(4):
    all_districts.append(trading_post)
harbor = Districts('harbor', 'trade', 4, '')
for x in range(4):
    all_districts.append(harbor)
docks = Districts('docks', 'trade', 3, '')
for x in range(4):
    all_districts.append(docks)
tavern = Districts('tavern', 'trade', 1, '')
for x in range(6):
    all_districts.append(tavern)
church = Districts('church', 'religious', 2, '')
for x in range(4):
    all_districts.append(church)
monastery = Districts('monastery', 'religious', 3, '')
for x in range(4):
    all_districts.append(monastery)
temple = Districts('temple', 'religious', 1, '')
for x in range(4):
    all_districts.append(temple)
cathedral = Districts('cathedral', 'religious', 5, '')
for x in range(3):
    all_districts.append(cathedral)
free_districts = all_districts.copy()
random.shuffle(free_districts)

all_characters = []
free_characters = []
victim = ''
robbed = ''
assassin = Characters('assassin', 1, '')
all_characters.append(assassin)
thief = Thief('thief', 2, '')
all_characters.append(thief)
magician = Magician('magician', 3, '')
all_characters.append(magician)
king = King('king', 4, '')
all_characters.append(king)
bishop = Bishop('bishop', 5, '')
all_characters.append(bishop)
merchant = Merchant('merchant', 6, '')
all_characters.append(merchant)
architect = Architect('architect', 7, '')
all_characters.append(architect)
warlord = Warlord('warlord', 8, '')
all_characters.append(warlord)
free_characters = all_characters.copy()

choice = ''
apprem = ''
round = 1
resources = False
skill = False
build = False

app = Flask(__name__)


@app.route("/")
def start():
    global victim
    global robbed
    return render_template("home.html", vitim=victim, robbed=robbed)


@app.route("/players/<string:par>")
def players(par):
    global crowned
    global next_player
    Players.start_round(player1)
    Players.start_round(player2)
    if par == '2players':
        crowned = random.choice([player1, player2])
        if player1 is crowned:
            next_player = player1
        elif player2 is crowned:
            next_player = player2
        return render_template("pass_names.html")


@app.route('/names', methods=['POST'])
def names():
    player1.imie = request.form['player1']
    player2.imie = request.form['player2']
    while len(player1.districts_built) < 8 and len(player2.districts_built) < 8:
            return render_template("now.html", next_player=next_player)


@app.route("/phases")
def phases():
    global crowned
    global next_player
    global round
    global opponent
    global victim
    global robbed
    print(next_player.name+"1")
    print(round)
    if round>8:
        return game()
    if round % 2 == 1:
        if round == 1:
            a = random.choice(free_characters)
            round+=1
            return choose_cards('remove', a)
        else:
            global choice
            global apprem
            choice = 'odrzucasz'
            apprem = 'remove'
            round+=1
            if player1 is next_player:
                opponent = player2
            else: opponent = player1
            return render_template("card_choice.html", free_characters=free_characters, next_player=next_player,
                                   crowned=crowned, choice=choice, apprem=apprem, opponent=opponent, victim=victim,
                                   robbed=robbed)
    else:
        choice = 'wybierasz'
        apprem = 'append'
        round+=1
        if player1 is next_player:
            opponent = player2
        else:
            opponent = player1
        return render_template("card_choice.html", free_characters=free_characters, next_player=next_player,
                           crowned=crowned, choice=choice, apprem=apprem, opponent=opponent, vitim=victim, robbed=robbed)


@app.route("/choose_cards/<string:apprem>/<string:choice>")
def choose_cards(apprem, choice):
    global next_player
    print(next_player.name+"2")
    global free_characters
    for x in free_characters:
        if choice == x.name:
            choice = x
    if apprem == 'append':
        next_player.characters.append(choice)
        if next_player is player1:
            next_player = player2
        else:
            next_player = player1
    free_characters.remove(choice)
    if apprem == 'remove':
        return phases()
    return render_template("now.html", next_player=next_player, crowned=crowned, round=round)


@app.route("/game")
def game():
    global next_player
    global character
    for y in all_characters:
        if y in player1.characters:
            next_player = player1
            return game_round(y)
        if y in player2.characters:
            next_player = player2
            return game_round(y)


@app.route("/game_round/<string:character>")
def game_round(character):
    global next_player
    global victim
    global robbed
    if next_player is player1:
        opponent = player2
    elif next_player is player2:
        opponent = player1
    if character is victim:
        var='victim'
        return render_template("character.html", var=var, character=character, next_player=next_player, victim=victim,
                               robbed=robbed)
    if character is robbed:
        a = next_player.money
        opponent.money += a
        next_player.money = 0
        var='robbed'
        return render_template("character.html", var=var, character=character, next_player=next_player, vitim=victim,
                               robbed=robbed)
    return render_template("character.html", character=character, next_player=next_player, victim=victim, robbed=robbed)


@app.route("/player_round/<string:character>")
def player_round(character):
    global crowned
    global victim
    global robbed
    global resources
    global skill
    global build
    global next_player
    print(next_player.name+"5")
    resources = True
    skill = True
    build = True
    if next_player == player1:
        opponent = player2
    else: opponent = player1
    return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed)


@app.route('/resource/<string:character>')
def resources(character):
    global victim
    global robbed
    global next_player
    print(next_player.name+" 6")
    if player1 == next_player:
        opponent = player2
    else: opponent = player1
    return render_template("resources.html", next_player=next_player, opponent=opponent, character=character,
                           victim=victim, robbed=robbed)


@app.route("/resources/<string:mod>/<string:character>")
def mod_func(mod, character):
    global free_districts
    global next_player
    global victim
    global robbed
    global resources
    global skill
    global build
    if mod == 'money':
        next_player.money += 2
        resources = False
        return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                               crowned=crowned, resources=resources, skill=skill, build=build, vitim=victim, robbed=robbed)
    if mod == 'district':
        a = free_districts[0]
        b = free_districts[1]
        return render_template("district_choice.html", a=a, b=b, next_player=next_player, character=character, opponent=opponent,
                               crowned=crowned, vitim=victim, robbed=robbed)


@app.route("/district/<string:dischoi>/<string:unchoi>/<string:character>")
def district_choice(dischoi,unchoi, character):
    global free_districts
    global resources
    global skill
    global build
    global next_player
    global crowned
    global victim
    global robbed
    if next_player == player1:
        opponent = player2
    else: opponent = player1
    for i in free_districts:
        if i.name == dischoi:
            dischoi = i
    for i in free_districts:
        if i.name == unchoi:
            unchoi = i
    next_player.districts_in_hand.append(dischoi)
    free_districts.remove(dischoi)
    free_districts.remove(unchoi)
    free_districts.append(unchoi)
    resources = False
    return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed)


@app.route('/build/<string:district>')
def build(district):
    global first
    global next_player
    for x in next_player.districts_in_hand:
        if x.name == district:
            district = x
            break
    if district.price > next_player.money:
        flash("Nie stać cię na tę dzielnicę!")
    else:
        next_player.districts_in_hand.remove(district)
        next_player.districts_built.append(district)
        next_player.money -= district.price
    if next_player.districts_built == 8:
        if first == None:
            first = next_player


@app.route('/skill/<string:character>')
def skill(character):
    global next_player
    global all_characters
    global skill
    for i in all_characters:
        if i.name == character:
            character = i
    character.skill_used = True
    skill = False
    return render_template("{{ character }}.html", all_characters=all_characters)


@app.route('/assassin/<string:victim>')
def assassin(victim):
    global next_player
    global all_characters
    global resources
    global skill
    global build
    for x in all_characters:
        if victim == x.name:
            victim = x
    if build==True:
        return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed)


@app.route('/thief/<string:victim>')
def thief(victim):
    global robbed
    for x in all_characters:
        if robbed == x.name:
            robbed = x


@app.route("/magician/<string:god>")
def magician(god):
    global free_districts
    if god == 'gamer':
        b = player1.districts_in_hand
        player1.districts_in_hand = player2.districts_in_hand
        player2.districts_in_hand = b
    elif god == 'deck':
        return render_template("magician_deck.html")


@app.route("/magician_deck")
def magician_deck()
        c = input('Ile kart swoich dzielnic chcesz wymienić?\n')
        c = int(c)
        for d in range(1, c + 1):
                for f in player.districts_in_hand:
                    print(f.name)
                e = input('Którą dzielnicę chcesz wymienić?\n')
                for x in player.districts_in_hand:
                    if e == x.name:
                        e = x
                player.districts_in_hand.remove(e)
                free_districts.append(e)
            for d in range(1, c + 1):
                g = random.choice(free_districts)
                player.districts_in_hand.append(g)
if __name__ == "__main__":
    app.run(debug=True)