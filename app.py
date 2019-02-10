from flask import Flask, render_template, request, flash #czy to dobre?
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
thief = Characters('thief', 2, '')
all_characters.append(thief)
magician = Characters('magician', 3, '')
all_characters.append(magician)
king = Characters('king', 4, '')
all_characters.append(king)
bishop = Characters('bishop', 5, '')
all_characters.append(bishop)
merchant = Characters('merchant', 6, '')
all_characters.append(merchant)
architect = Characters('architect', 7, '')
all_characters.append(architect)
warlord = Characters('warlord', 8, '')
all_characters.append(warlord)

choice = ''
apprem = ''
resources = False
skill = False
build = False
first = None

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'


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
    return render_template("new_round.html")

def play():
    return render_template("new_round.html")

@app.route('/new_round')
def new_round():
    global round
    round = 1
    global crowned
    global next_player
    global free_characters
    global victim
    global robbed
    victim = ''
    robbed = ''
    next_player = crowned
    free_characters = all_characters.copy()
    player1.characters = []
    player2.characters = []
    while len(player1.districts_built) < 8 and len(player2.districts_built) < 8:
            return render_template("now.html", next_player=next_player)
    else: return summary()


@app.route("/phases")
def phases():
    global crowned
    global next_player
    global round
    global opponent
    global victim
    global robbed
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
    global free_characters
    global crowned
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


@app.route("/game/<int:a>")
def game(a=1):
    global next_player
    global character
    for x in range(a,10):
        if x == 9:
            return play()
        for y in player1.characters:
            if x == y.level:
                next_player = player1
                character = y
                return game_round()
        for y in player2.characters:
            if x == y.level:
                next_player = player2
                character = y
                return game_round()


@app.route("/game_round/")
def game_round():
    global next_player
    global victim
    global robbed
    global character
    if next_player is player1:
        opponent = player2
    elif next_player is player2:
        opponent = player1
    if character.name == victim:
        var='victim'
        return render_template("character.html", var=var, character=character, next_player=next_player, victim=victim,
                               robbed=robbed, level=character.level)
    if character.name == robbed:
        a = next_player.money
        opponent.money += a
        next_player.money = 0
        var='robbed'
        return render_template("character.html", var=var, character=character, next_player=next_player, vitim=victim,
                               robbed=robbed, level=character.level)
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
    resources = True
    skill = True
    build = True
    if next_player == player1:
        opponent = player2
    else: opponent = player1
    architect_count=0
    for i in all_characters:
        if i.name == character:
            return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                           level=i.level, architect_count=architect_count)


@app.route('/resource/<string:character1>')
def resources(character1):
    global victim
    global robbed
    global next_player
    global character
    character = character1
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
    global crowned
    architect_count=0
    if mod == 'money':
        next_player.money += 2
        resources = False
        for i in all_characters:
            if i.name==character:
                return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                               crowned=crowned, resources=resources, skill=skill, build=build, vitim=victim, robbed=robbed,
                               architect_count=architect_count, level=i.level)
    elif mod == 'district':
        a = free_districts[0]
        b = free_districts[1]
        c = 0
        observatory = False
        if observatory in next_player.districts_built:
            observatory = True
            c = free_districts[2]
        for i in all_characters:
            if i.name==character:
                return render_template("district_choice.html", a=a, b=b, c=c, next_player=next_player, character=character,
                                       opponent=opponent, crowned=crowned, vitim=victim, robbed=robbed,
                                       architect_count=architect_count, observatory=observatory)


@app.route("/district/<string:dischoi>/<string:unchoi>/<string:character>")
def district_choice(dischoi, unchoi, character):
    global free_districts
    global resources
    global skill
    global build
    global next_player
    global crowned
    global victim
    global robbed
    global all_characters
    architect_count=0
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
    for i in all_characters:
        if i.name == character:
            return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                           architect_count=architect_count, level=i.level)


@app.route('/build/<string:district>/<string:architect_count>')
def build(district, architect_count=0):
    global first
    global next_player
    global resources
    global skill
    global build
    global character
    global crowned
    global victim
    global robbed
    architect_count=int(architect_count)
    for x in next_player.districts_in_hand:
        if x.name == district:
            district = x
            break
    if district.price > next_player.money:
        flash("Nie stać cię na tę dzielnicę!")
    repeat = False
    for x in next_player.districts_built:
        if x.name == district.name:
            repeat = True
    if repeat == False:
        next_player.districts_in_hand.remove(district)
        next_player.districts_built.append(district)
        factory_yon = False
        build = False
        for x in next_player.districts_built:
            if x == factory:
                factory_yon = True
        if district.archetype == 'special' and factory_yon == True:
            next_player.money -= (district.price-1)
        else:
            next_player.money -= district.price
    else: flash('Nie możesz wybudować dwóch takich samych dzielnic!')
    if next_player.districts_built == 8:
        if first == None:
            first = next_player
    if architect_count>0 and architect_count<=4:
        architect_count-=1
        build = True
        for i in all_characters:
            if i.name == character:
                return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                        architect_count=architect_count, level=i.level)
    elif skill == True:
        for i in all_characters:
            if i.name == character:
                return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect_count=architect_count, level=i.level)
    else:
        for i in all_characters:
            if i.name == character:
                character=i
        return game(character.level+1)


@app.route('/skill/<string:character>')
def skill(character):
    global next_player
    global all_characters
    global skill
    global crowned
    for i in all_characters:
        if i.name == character:
            character = i
    character.skill_used = True
    skill = False
    if player1==next_player:
        opponent=player2
    else:
        opponent=player1
    architect_count=0
    if character == assassin:
        return render_template("assassin.html", all_characters=all_characters, next_player=next_player, character=character,
                               opponent=opponent, crowned=crowned, resources=resources, skill=skill, build=build,
                               victim=victim, robbed=robbed, architect_count=architect_count)
    elif character == thief:
        return render_template("thief.html", all_characters=all_characters, next_player=next_player,
                               character=character, opponent=opponent, crowned=crowned, resources=resources, skill=skill,
                               build=build, victim=victim, robbed=robbed, architect_count=architect_count)
    elif character == magician:
        return render_template("magician.html", all_characters=all_characters, next_player=next_player,
                               character=character, opponent=opponent, crowned=crowned, resources=resources, skill=skill,
                               build=build, victim=victim, robbed=robbed, architect_count=architect_count)
    elif character == king:
        return king_skill()
    elif character == bishop:
        return bishop_skill()
    elif character == merchant:
        return merchant_skill()
    elif character == architect:
        return architect_skill()
    elif character == warlord:
        return warlord_skill()


@app.route('/assassin/<string:victim1>')
def assassin_skill(victim1):
    global next_player
    global all_characters
    global resources
    global skill
    global build
    global victim
    victim = victim1
    character=assassin.name
    architect_count=0
    if build==True:
        return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect_count=architect_count, level=assassin.level)
    else: return game(2)


@app.route('/thief/<string:robbed1>')
def thief_skill(robbed1):
    global robbed
    global victim
    architect_count=0
    robbed = robbed1
    character = thief.name
    if build==True:
        return render_template("game.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed1,
                               architect_count=architect_count, level=thief.level)
    else: return game(3)


@app.route("/magician/<string:god>")
def magician_skill(god):
    global free_districts
    global next_player
    global crowned
    architect_count=0
    if player1 == next_player:
        opponent = player2
    else: opponent = player1
    if god == 'gamer':
        b = player1.districts_in_hand
        player1.districts_in_hand = player2.districts_in_hand
        player2.districts_in_hand = b
        if build == True:
            return render_template("game.html", next_player=next_player, character=magician.name, opponent=opponent,
                                   crowned=crowned, resources=resources, skill=skill, build=build, victim=victim,
                                   robbed=robbed, architect=architect, level=magician.level, architect_count=architect_count)
        else:
            return game(4)
    elif god == 'deck':
        return render_template("magician_deck.html", next_player=next_player, character=character, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect_count=architect_count)


@app.route("/magician_deck", methods=['POST'])
def magician_deck():
    global victim
    global robbed
    global next_player
    c=0
    character = magician
    if next_player.name == player1.name:
        next_player = player1
    else: next_player = player2
    for y in range(len(next_player.districts_in_hand)):
        for x in next_player.districts_in_hand:
            if x.name in request.form.getlist('card'):
                e = x
                c+=1
                next_player.districts_in_hand.remove(e)
                free_districts.append(e)
    for d in range(c):
        g = random.choice(free_districts)
        next_player.districts_in_hand.append(g)
        free_districts.remove(g)
    architect_count=0
    if build==True:
        return render_template("game.html", next_player=next_player.name, character=character.name, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect=architect, level=magician.level, architect_count=architect_count)
    else: return game(4)

@app.route("/king")
def king_skill():
    global crowned
    global next_player
    global build
    global victim
    global robbed
    crowned = next_player
    architect_count=0
    for x in next_player.districts_built:
        if x.archetype == 'noble':
            next_player.money += 1
    if school_of_magic in next_player.districts_built:
        next_player.money += 1
    if build==True:
        return render_template("game.html", next_player=next_player, character=king.name, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect=architect, level=king.level, architect_count=architect_count)
    else: return game(5)


@app.route("/bishop")
def bishop_skill():
    global next_player
    global build
    global victim
    global robbed
    character = bishop
    architect_count=0
    for x in next_player.districts_built:
        if x.archetype == 'religious':
            next_player.money += 1
    if school_of_magic in next_player.districts_built:
        next_player.money += 1
    if build==True:
        return render_template("game.html", next_player=next_player, character=character.name, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect=architect, level=bishop.level, architect_count=architect_count)
    else: return game(6)


@app.route("/merchant")
def merchant_skill():
    global next_player
    global build
    global victim
    global robbed
    for x in next_player.districts_built:
        if x.archetype == 'trade':
            next_player.money += 1
    next_player.money += 1
    if school_of_magic in next_player.districts_built:
        next_player.money += 1
    architect_count=0
    if build==True:
        return render_template("game.html", next_player=next_player, character=character.name, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect_count=architect_count, level=merchant.level)
    else: return game(7)


@app.route("/architect")
def architect_skill():
    global free_districts
    global next_player
    global victim
    global robbed
    global resources
    character = architect
    a = random.choice(free_districts)
    b = random.choice(free_districts)
    next_player.districts_in_hand.append(a)
    next_player.districts_in_hand.append(b)
    free_districts.remove(a)
    free_districts.remove(b)
    architect_count = 3
    if build == True:
        architect_count = 4
    return render_template("game.html", next_player=next_player, character=character.name, opponent=opponent,
                               crowned=crowned, resources=resources, skill=skill, build=build, victim=victim,
                               robbed=robbed, architect_count=architect_count, level=architect.level)


@app.route("/warlord")
def warlord_skill():
    global next_player
    global crowned
    global victim
    global robbed
    for x in next_player.districts_built:
        if x.archetype == 'military':
            next_player.money += 1
    if school_of_magic in next_player.districts_built:
        next_player.money += 1
    if next_player is player1:
        opponent = player2
    elif next_player is player2:
        opponent = player1
    return render_template("warlord.html", next_player=next_player, opponent=opponent, crowned=crowned, victim=victim,
                           robbed=robbed, character=warlord, level=warlord.level)


@app.route("/warlord_destroy/<string:ruin>")
def warlord_destroy(ruin):
    global next_player
    global victim
    global robbed
    global crowned
    global build
    if next_player is player1:
        opponent = player2
    elif next_player is player2:
        opponent = player1
    if bishop not in opponent.characters:
        for x in opponent.districts_built:
            if x.name == ruin:
                ruin = x
                opponent.districts_built.remove(ruin)
                next_player.money -= (ruin.price - 1)
        if graveyard in opponent.districts_built:
            return render_template("graveyard.html", imie=next_player.imie, imie2=opponent.imie, district=ruin.name)
    else: flash('Nie możesz zburzyć dzielnicy biskupa!')
    architect_count=0
    if build==True:
        return render_template("game.html", next_player=next_player, character=warlord.name, opponent=opponent,
                           crowned=crowned, resources=resources, skill=skill, build=build, victim=victim, robbed=robbed,
                               architect_count=architect_count, level=warlord.level)
    else: phases() #nowa gra


@app.route('/yes/<string:district_reborn>')
def yes(district_reborn):
    global next_player
    global build
    if player1 == next_player:
        opponent = player2
    else: opponent = player1
    for x in all_districts:
        if district_reborn == x.name:
            district_reborn = x
    opponent.districts_in_hand.append(district_reborn)
    opponent.money -=1
    architect_count = 0
    if build == True:
        return render_template("game.html", next_player=next_player, character=warlord.name, opponent=opponent,
                               crowned=crowned, resources=resources, skill=skill, build=build, victim=victim,
                               robbed=robbed, architect_count=architect_count, level=warlord.level)
    else:
        phases()  # nowa gra


@app.route('/no')
def no():
    global next_player
    architect_count = 0
    if build == True:
        return render_template("game.html", next_player=next_player, character=warlord.name, opponent=opponent,
                               crowned=crowned, resources=resources, skill=skill, build=build, victim=victim,
                               robbed=robbed, architect_count=architect_count, level=warlord.level)
    else:
        phases()  # nowa gra


def end(player1):
    global first
    result = 0
    for x in player1.districts_built:
        result += x.price
    # tu dodać ekstra punkty
    archetypes = []
    for x in player1.districts_built:
        archetypes.append(x.archetype)
    if len(archetypes) == 4:
        result += 3
    if len(player1.districts_built) == 8:
        result += 3
        if first is player1:
            result += 4
    if map_room in player1.districts_built:
        result += len(player1.districts_in_hand)
    if imperial_treasury in player1.districts_built:
        result += player1.money
    if dragon_gate in player1.districts_built:
        result += 2
    if university in player1.districts_built:
        result += 2
    if wishing_well in player1.districts_built:
        special = []
        for x in player1.districts_built:
            if x.archetype == 'special':
                special.append(x)
        result += len(special)-1
    return result


def summary():
    a = end(player1)
    b = end(player2)
    if a > b:
        wol1 = 'zwycięzcą'
        wol2 = 'przegranym'
    elif b > a:
        wol1 = 'przegranym'
        wol2 = 'zwycięzcą'
    else:
        wol1 = 'zwycięzcą'
        wol2 = 'zwycięzcą'
    return render_template("results.html", player1=player1.name, player2=player2.name, a=a, b=b, wol1=wol1, wol2=wol2)


if __name__ == "__main__":
    app.run(debug=True, port=5036, host='0.0.0.0')
