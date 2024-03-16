




def hello(name, lang):
    hi = None
    if lang == 'rus':
        hi = f'Добро пожаловать в игру, <b>{name}</b>! чтобы продолжить, нажми на 🎅🏿'

    elif lang == 'eng':
        hi = f'Welcome to the game, <b>{name}</b>! to continue, click on 🎅🏿'

    return hi



# russian
def types_lang(lang):
    type_lang = None
    if lang == 'rus':
        type_lang = ('профиль🙎🏿‍♂️','✨моя компания✨','Написать получателю👹','начать игру!','Сброс настроек💣', 'Завершить')

    elif lang == 'eng':
        type_lang = ('profile🙎🏿‍♂️','✨my company✨','Write to the recipient👹','start the game!','Reset settings💣', 'Complete')
    return type_lang

def words_list(lang):
    words = None
    if lang == 'eng':
        words = ('You need to register',
                 'Come up with a username!',
                 'Enter the name of the team, (if it already exists, you will join it)',
                 'Here is a list of teams available for connection:',
                 'Name busy! enter another',
                 'Cool, you were able to register!\nTo continue, click on Santa Claus again)',
                 'Now click on Santa Claus again!',
                 'No exit allowed during the game!',
                 'You give the player:',
                 'odd number of players!!',
                 'Мы отправили получателю приглашение в анонимный чат - ожидайте! :)',
                 'You haven`t started the game yet!',
                 'If there are any problems -\n write the command /start',
                 'A message from Santa for you🎅!!',
                 'Message sent!',
                 'ready',
                 'The game is over - recreate your profile if you want to play more😉',
                 'Restart',
                 'Game over',
                 'You need to click on Santa Claus!',
                 'Вас приглашают в анонимную беседу',
                 'Согласиться',
                 'Отказаться',
                 )
    elif lang == 'rus':
        words = ('Вам необходимо зарегистрироваться',
                  'Придумай имя пользователя!',
                  'Введите название команды, (если она уже существует, вы к ней присоединитесь)',
                  'Вот список команд, доступных для подключения:',
                  ' имя занято! введите другой',
                  'Круто, вы смогли зарегистрироваться!\nЧтобы продолжить, нажмите на Деда Мороза еще раз)',
                  'Теперь снова нажмите на Деда Мороза!',
                  'Во время игры выход запрещен!',
                  'Вы даете игроку:',
                  'нечетное количество игроков!!',
                  'Написать сообщение получателю :)',
                  'Вы еще не начали игру!',
                  'Если есть проблемы -\n пишем команду /start',
                  'Послание от Санты для тебя🎅!!',
                  'Сообщение отправлено!',
                  'готовый',
                  'Игра окончена — создайте заново свой профиль, если хотите играть еще😉',
                  'Restart',
                  'Игра окончена, можно выходить!',
                  'Вам нужно нажать на Деда Мороза!'
                  )
    return words

def profil_lang(lang):
    infos = None
    if lang == 'eng':
        infos = ('😼Name:', '🏆Level:', '🎮team:', '👹recipient')
    elif lang == 'rus':
        infos = ('😼Имя:', '🏆Уровень:', '🎮команда:', '👹получатель')
    return infos