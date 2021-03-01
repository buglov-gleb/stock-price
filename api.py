# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

import re
import requests
import random

reDict = {'TSLA' : r'(\bт[еэ]сл.{1,2}\b|\bte?sla.{0,1}\b)', 'SBER.ME' : r'(\bсбер[ -]?банк.{0,2}\b|\bсбер.{0,2}\b)'}
#norms = {'Leninsk Kuznetsky': 'Ленинск-Кузнецкий', 'Abakan': 'Абакан', 'Abaza': 'Абаза', 'Abdulino': 'Абдулино', 'Abinsk': 'Абинск', 'Achinsk': 'Ачинск', 'Adygeysk': 'Адыгейск', 'Agidel': 'Агидель', 'Agryz': 'Агрыз', 'Ak-Dovurak': 'Ак-Довурак', 'Akhtubinsk': 'Ахтубинск', 'Aksay': 'Аксай', 'Alagir': 'Алагир', 'Alapayevsk': 'Алапаевск', 'Alatyr': 'Алатырь', 'Aldan': 'Алдан', 'Aleksin': 'Алексин', 'Alexandrov': 'Александров', 'Alexandrovsk': 'Александровск', 'Aleysk': 'Алейск', 'Almetyevsk': 'Альметьевск', 'Alzamay': 'Алзамай', 'Amursk': 'Амурск', 'Anadyr': 'Анадырь', 'Anapa': 'Анап', 'Andreapol': 'Андреаполь', 'Angarsk': 'Ангарск', 'Aniva': 'Анива', 'Anzhero-Sudzhensk': 'Анжеро-Судженск', 'Apatity': 'Апатиты', 'Aprelevka': 'Апрелевка', 'Apsheronsk': 'Апшеронск', 'Aramil': 'Арамиль', 'Ardatov': 'Ардатов', 'Ardon': 'Ардон', 'Argun': 'Аргун', 'Arkadak': 'Аркадак', 'Arkhangelsk': 'Архангельск', 'Armavir': 'Армавир', 'Arsenyev': 'Арсеньев', 'Arsk': 'Арск', 'Arzamas': 'Арзамас', 'Asbest': 'Асбест', 'Asha': 'Аша', 'Asino': 'Асино', 'Astrakhan': 'Астрахань', 'Atkarsk': 'Аткарск', 'Aznakayevo': 'Азнакаево', 'Azov': 'Азов', 'Belozersk': 'Белозерск', 'Berdsk': 'Бердск', 'Berezniki': 'Березники', 'Beslan': 'Беслан', 'Bezhetsk': 'Бежецк', 'Bikin': 'Бикин', 'Bilibino': 'Билибино', 'Birobidzhan': 'Биробиджан', 'Birsk': 'Бирск', 'Biryuch': 'Бирюч', 'Biryusinsk': 'Бирюсинск', 'Biysk': 'Бийск', 'Blagodarny': 'Благодарный', 'Blagoveshchensk': 'Благовещенск', 'Bobrov': 'Бобров', 'Bodaybo': 'Бодайбо', 'Bogdanovich': 'Богданович', 'Bogoroditsk': 'Богородицк', 'Bogorodsk': 'Богородск', 'Bogotol': 'Боготол', 'Boguchar': 'Богучар', 'Boksitogorsk': 'Бокситогорск', 'Bolgar': 'Болгар', 'Bolkhov': 'Болхов', 'Bologoye': 'Бологое', 'Bolokhovo': 'Болохово', 'Bolotnoye': 'Болотное', 'Bolshoy Kamen': 'Большой Камень', 'Bor': 'Бор', 'Borisoglebsk': 'Борисоглебск', 'Borodino': 'Бородино', 'Borovichi': 'Боровичи', 'Borovsk': 'Боровск', 'Borzya': 'Борзя', 'Bratsk': 'Братск', 'Bronnitsy': 'Бронницы', 'Bryansk': 'Брянск', 'Bugulma': 'Бугульма', 'Buguruslan': 'Бугуруслан', 'Buinsk': 'Буинск', 'Buturlinovka': 'Бутурлиновка', 'Buy': 'Буй', 'Buynaksk': 'Буйнакск', 'Buzuluk': 'Бузулук', 'Chadan': 'Чадан', 'Chapayevsk': 'Чапаевск', 'Chaplygin': 'Чаплыгин', 'Chebarkul': 'Чебаркул', 'Cheboksary': 'Чебоксар', 'Chegem': 'Чегем', 'Chekalin': 'Чекалин', 'Chekhov': 'Чехов', 'Chelyabinsk': 'Челябинск', 'Cherdyn': 'Чердынь', 'Cheremkhovo': 'Черемхово', 'Cherepanovo': 'Черепаново', 'Cherepovets': 'Череповец', 'Cherkessk': 'Черкесск', 'Chernogolovka': 'Черноголовка', 'Chernogorsk': 'Черногорск', 'Chernushka': 'Чернушка', 'Chernyakhovsk': 'Черняховск', 'Chistopol': 'Чистополь', 'Chita': 'Чита', 'Chkalovsk': 'Чкаловск', 'Chudovo': 'Чудово', 'Chukhloma': 'Чухлома', 'Chulym': 'Чулым', 'Chusovoy': 'Чусовой', 'Dagestanskiye Ogni': 'Дагестанские Огни', 'Dalmatovo': 'Далматово', 'Dalnegorsk': 'Дальнегорск', 'Dalnerechensk': 'Дальнереченск', 'Danilov': 'Данилов', 'Dankov': 'Данков', 'Davlekanovo': 'Давлеканово', 'Dedovsk': 'Дедовск', 'Degtyarsk': 'Дегтярск', 'Demidov': 'Демидов', 'Derbent': 'Дербент', 'Desnogorsk': 'Десногорск', 'Digora': 'Дигора', 'Dimitrovgrad': 'Димитровград', 'Divnogorsk': 'Дивногорск', 'Dmitrov': 'Дмитров', 'Dobryanka': 'Добрянка', 'Dolgoprudny': 'Долгопрудный', 'Dolinsk': 'Долинск', 'Domodedovo': 'Домодедово', 'Donetsk': 'Донецк', 'Donskoy': 'Донской', 'Dorogobuzh': 'Дорогобуж', 'Drezna': 'Дрезна', 'Dubna': 'Дубн', 'Dubovka': 'Дубовка', 'Dudinka': 'Дудинк', 'Dukhovshchina': 'Духовщина', 'Dyatkovo': 'Дятьково', 'Dyurtyuli': 'Дюртюли', 'Dzerzhinsk': 'Дзержинск', 'Elektrogorsk': 'Электрогорск', 'Elektrostal': 'Электросталь', 'Elektrougli': 'Электроугли', 'Elista': 'Элиста', 'Engels': 'Энгельс', 'Ertil': 'Эртиль', 'Fatezh': 'Фатеж', 'Fokino': 'Фокино', 'Frolovo': 'Фролово', 'Fryazino': 'Фрязино', 'Furmanov': 'Фурманов', 'Gadzhiyevo': 'Гаджиево', 'Gagarin': 'Гагарин', 'Galich': 'Галич', 'Gatchina': 'Гатчина', 'Gavrilov Posad': 'Гаврилов Посад', 'Gavrilov Yam': 'Гаврилов-Ям', 'Gdov': 'Гдов', 'Gelendzhik': 'Геленджик', 'Glazov': 'Глазов', 'Golitsyno': 'Голицыно', 'Gorno Altaysk': 'Горно-Алтайск', 'Gornozavodsk': 'Горнозаводск', 'Gornyak': 'Горняк', 'Gorodets': 'Городец', 'Gorodishche': 'Городище', 'Gorodovikovsk': 'Городовиковск', 'Gorokhovets': 'Гороховец', 'Grayvoron': 'Грайворон', 'Gremyachinsk': 'Гремячинск', 'Grozny': 'Грозный', 'Gryazi': 'Грязи', 'Gryazovets': 'Грязовец', 'Gubakha': 'Губаха', 'Gubkin': 'Губкин', 'Gudermes': 'Гудермес', 'Gukovo': 'Гуково', 'Gulkevichi': 'Гулькевичи', 'Guryevsk': 'Гурьевск', 'Gus Khrustalny': 'Гусь-Хрустальный', 'Gusev': 'Гусев', 'Gvardeysk': 'Гвардейск', 'Igarka': 'Игарка', 'Insar': 'Инсар', 'Inta': 'Инта', 'Inza': 'Инза', 'Ipatovo': 'Ипатово', 'Irbit': 'Ирбит', 'Irkutsk': 'Иркутск', 'Ishimbay': 'Ишимбай', 'Isilkul': 'Исилькуль', 'Iskitim': 'Искитим', 'Istra': 'Истра', 'Ivangorod': 'Ивангород', 'Ivanovo': 'Иваново', 'Ivanteyevka': 'Ивантеевка', 'Ivdel': 'Ивдель', 'Izberbash': 'Избербаш', 'Izhevsk': 'Ижевск', 'Izobilny': 'Изобильный', 'Kachkanar': 'Качканар', 'Kadnikov': 'Кадников', 'Kalach na Donu': 'Калач-на-Дону', 'Kalachinsk': 'Калачинск', 'Kaliningrad': 'Калининград', 'Kalininsk': 'Калининск', 'Kaltan': 'Калтан', 'Kaluga': 'Калуга', 'Kalyazin': 'Калязин', 'Kambarka': 'Камбарка', 'Kamenka': 'Каменка', 'Kamen na Obi': 'Камень-на-Оби', 'Kamennogorsk': 'Каменногорск', 'Kamensk Shakhtinsky': 'Каменск-Шахтинский', 'Kamensk Uralsky': 'Каменск-Уральский', 'Kameshkovo': 'Камешково', 'Kamyshin': 'Камышин', 'Kamyshlov': 'Камышлов', 'Kamyzyak': 'Камызяк', 'Kanash': 'Канаш', 'Kandalaksha': 'Кандалакша', 'Kansk': 'Канск', 'Karabanovo': 'Карабаново', 'Karabash': 'Карабаш', 'Karabulak': 'Карабулак', 'Karachayevsk': 'Карачаевск', 'Karachev': 'Карачев', 'Karasuk': 'Карасук', 'Kargat': 'Каргат', 'Kargopol': 'Каргополь', 'Karpinsk': 'Карпинск', 'Kartaly': 'Карталы', 'Kashin': 'Кашин', 'Kashira': 'Кашира', 'Kasimov': 'Касимов', 'Kasli': 'Касли', 'Kaspiysk': 'Каспийск', 'Katav Ivanovsk': 'Катав-Ивановск', 'Kataysk': 'Катайск', 'Kazan': 'Казань', 'Kedrovy': 'Кедровый', 'Kem': 'Кемь', 'Kemerovo': 'Кемерово', 'Khabarovsk': 'Хабаровск', 'Khadyzhensk': 'Хадыженск', 'Khanty Mansiysk': 'Ханты-Мансийск', 'Kharabali': 'Харабали', 'Kharovsk': 'Харовск', 'Khasavyurt': 'Хасавюрт', 'Khilok': 'Хилок', 'Khimki': 'Химки', 'Kholm': 'Холм', 'Kholmsk': 'Холмск', 'Khotkovo': 'Хотьково', 'Khvalynsk': 'Хвалынск', 'Kimovsk': 'Кимовск', 'Kimry': 'Кимры', 'Kinel': 'Кинель', 'Kineshma': 'Кинешма', 'Kingisepp': 'Кингисепп', 'Kirensk': 'Киренск', 'Kireyevsk': 'Киреевск', 'Kirillov': 'Кириллов', 'Kirishi': 'Кириши', 'Kirov': 'Киров', 'Kirovgrad': 'Кировград', 'Kirovo Chepetsk': 'Кирово-Чепецк', 'Kirovsk': 'Кировск', 'Kirsanov': 'Кирсанов', 'Kirzhach': 'Киржач', 'Kiselevsk': 'Киселёвск', 'Kislovodsk': 'Кисловодск', 'Kizel': 'Кизел', 'Kizilyurt': 'Кизилюрт', 'Kizlyar': 'Кизляр', 'Klimovsk': 'Климовск', 'Klin': 'Клин', 'Klintsy': 'Клинцы', 'Knyaginino': 'Княгинино', 'Kodinsk': 'Кодинск', 'Kokhma': 'Кохма', 'Kolchugino': 'Кольчугино', 'Kologriv': 'Кологрив', 'Kolomna': 'Коломна', 'Kolpashevo': 'Колпашево', 'Kolpino': 'Колпино', 'Kommunar': 'Коммунар', 'Komsomolsk on Amur': 'Комсомольск-на-Амуре', 'Kondopoga': 'Кондопога', 'Kondrovo': 'Кондрово', 'Konstantinovsk': 'Константиновск', 'Kopeysk': 'Копейск', 'Korablino': 'Кораблино', 'Korenovsk': 'Кореновск', 'Korkino': 'Коркино', 'Korocha': 'Короча', 'Korsakov': 'Корсаков', 'Koryazhma': 'Коряжма', 'Kostomuksha': 'Костомукша', 'Kostroma': 'Кострома', 'Kotelnich': 'Котельнич', 'Kotelniki': 'Котельники', 'Kotelnikovo': 'Котельниково', 'Kotlas': 'Котлас', 'Kotovo': 'Котово', 'Kotovsk': 'Котовск', 'Kovdor': 'Ковдор', 'Kovrov': 'Ковров', 'Kovylkino': 'Ковылкино', 'Kozelsk': 'Козельск', 'Kozlovka': 'Козловка', 'Kozmodemyansk': 'Козьмодемьянск', 'Krasavino': 'Красавино', 'Krasnoarmeysk': 'Красноармейск', 'Krasnodar': 'Краснодар', 'Krasnogorsk': 'Красногорск', 'Krasnokamensk': 'Краснокаменск', 'Krasnokamsk': 'Краснокамск', 'Krasnoslobodsk': 'Краснослободск', 'Krasnoufimsk': 'Красноуфимск', 'Krasnouralsk': 'Красноуральск', 'Krasnovishersk': 'Красновишерск', 'Krasnoyarsk': 'Красноярск', 'Krasnoye Selo': 'Красное Село', 'Krasnozavodsk': 'Краснозаводск', 'Krasnoznamensk': 'Краснознаменск', 'Krasny Kholm': 'Красный Холм', 'Krasny Kut': 'Красный Кут', 'Krasny Sulin': 'Красный Сулин', 'Kremenki': 'Кремёнки', 'Kronstadt': 'Кронштадт', 'Kropotkin': 'Кропоткин', 'Krymsk': 'Крымск', 'Kstovo': 'Кстово', 'Kubinka': 'Кубинка', 'Kudymkar': 'Кудымкар', 'Kulebaki': 'Кулебаки', 'Kumertau': 'Кумертау', 'Kungur': 'Кунгур', 'Kupino': 'Купино', 'Kurchatov': 'Курчатов', 'Kurgan': 'Курган', 'Kurganinsk': 'Курганинск', 'Kurilsk': 'Курильск', 'Kurlovo': 'Курлово', 'Kurovskoye': 'Куровское', 'Kursk': 'Курск', 'Kurtamysh': 'Куртамыш', 'Kushva': 'Кушва', 'Kuvandyk': 'Кувандык', 'Kuvshinovo': 'Кувшиново', 'Kuybyshev': 'Куйбышев', 'Kuznetsk': 'Кузнецк', 'Kyakhta': 'Кяхта', 'Kyshtym': 'Кыштым', 'Kyzyl': 'Кызыл', 'Labinsk': 'Лабинск', 'Labytnangi': 'Лабытнанги', 'Ladushkin': 'Ладушкин', 'Laishevo': 'Лаишево', 'Lakhdenpokhya': 'Лахденпохья', 'Lakinsk': 'Лакинск', 'Lebedyan': 'Лебедянь', 'Leninogorsk': 'Лениногорск', 'Leninsk': 'Ленинск', 'Lensk': 'Ленск', 'Lermontov': 'Лермонтов', 'Lesnoy': 'Лесной', 'Lesosibirsk': 'Лесосибирск', 'Lesozavodsk': 'Лесозаводск', 'Lgov': 'Льгов', 'Likhoslavl': 'Лихославль', 'Likino Dulyovo': 'Ликино-Дулёво', 'Lipetsk': 'Липецк', 'Lipki': 'Липки', 'Liski': 'Лиски', 'Livny': 'Ливны', 'Lobnya': 'Лобня', 'Lodeynoye Pole': 'Лодейное Поле', 'Lomonosov': 'Ломоносов', 'Losino Petrovsky': 'Лосино-Петровский', 'Luga': 'Луга', 'Lukhovitsy': 'Луховицы', 'Lukoyanov': 'Лукоянов', 'Luza': 'Луза', 'Lyantor': 'Лянтор', 'Lyskovo': 'Лысково', 'Lysva': 'Лысьва', 'Lytkarino': 'Лыткарино', 'Lyuban': 'Любань', 'Lyubertsy': 'Люберцы', 'Lyudinovo': 'Людиново', 'Magadan': 'Магадан', 'Magas': 'Магас', 'Magnitogorsk': 'Магнитогорск', 'Makarov': 'Макаров', 'Makaryev': 'Макарьев', 'Makhachkala': 'Махачкала', 'Makushino': 'Макушино', 'Malaya Vishera': 'Малая Вишера', 'Malgobek': 'Малгобек', 'Malmyzh': 'Малмыж', 'Maloarkhangelsk': 'Малоархангельск', 'Maloyaroslavets': 'Малоярославец', 'Mamadysh': 'Мамадыш', 'Mamonovo': 'Мамоново', 'Manturovo': 'Мантурово', 'Mariinsky Posad': 'Мариинский Посад', 'Mariinsk': 'Мариинск', 'Marks': 'Маркс', 'Maykop': 'Майкоп', 'Mayskiy': 'Майский', 'Mednogorsk': 'Медногорск', 'Medvezhyegorsk': 'Медвежьегорск', 'Medyn': 'Медынь', 'Megion': 'Мегион', 'Melenki': 'Меленки', 'Meleuz': 'Мелеуз', 'Mendeleyevsk': 'Менделеевск', 'Menzelinsk': 'Мензелинск', 'Meshchovsk': 'Мещовск', 'Mezen': 'Мезень', 'Mezhdurechensk': 'Междуреченск', 'Mezhgorye': 'Межгорье', 'Mglin': 'Мглин', 'Miass': 'Миасс', 'Michurinsk': 'Мичуринск', 'Mikhaylov': 'Михайлов', 'Mikhaylovka': 'Михайловка', 'Mikhaylovsk': 'Михайловск', 'Millerovo': 'Миллерово', 'Mineralnye Vody': 'Минеральные Воды', 'Minusinsk': 'Минусинск', 'Minyar': 'Миньяр', 'Mirny': 'Мирный', 'Mogocha': 'Могоча', 'Monchegorsk': 'Мончегорск', 'Morozovsk': 'Морозовск', 'Morshansk': 'Моршанск', 'Mosalsk': 'Мосальск', 'Moscow': 'Москва', 'Mozdok': 'Моздок', 'Mozhaysk': 'Можайск', 'Mozhga': 'Можга', 'Mtsensk': 'Мценск', 'Murashi': 'Мураши', 'Muravlenko': 'Муравленко', 'Murmansk': 'Мурманск', 'Murom': 'Муром', 'Myshkin': 'Мышкин', 'Myski': 'Мыски', 'Mytishchi': 'Мытищи', 'Naberezhnye Chelny': 'Набережные Челны', 'Nadym': 'Надым', 'Nakhodka': 'Находка', 'Nalchik': 'Нальчик', 'Narimanov': 'Нариманов', 'Naro Fominsk': 'Наро-Фоминск', 'Nartkala': 'Нарткала', 'Naryan Mar': 'Нарьян-Мар', 'Naukan': 'Наукан', 'Navashino': 'Навашино', 'Navoloki': 'Наволоки', 'Nazarovo': 'Назарово', 'Nazran': 'Назрань', 'Nazyvayevsk': 'Называевск', 'Neftegorsk': 'Нефтегорск', 'Neftekamsk': 'Нефтекамск', 'Neftekumsk': 'Нефтекумск', 'Nefteyugansk': 'Нефтеюганск', 'Nelidovo': 'Нелидово', 'Neman': 'Неман', 'Nerchinsk': 'Нерчинск', 'Nerekhta': 'Нерехта', 'Neryungri': 'Нерюнгри', 'Nesterov': 'Нестеров', 'Nevel': 'Невель', 'Nevelsk': 'Невельск', 'Nevinnomyssk': 'Невинномысск', 'Nevyansk': 'Невьянск', 'Nikolayevsk on Amur': 'Николаевск-на-Амуре', 'Nikolsk': 'Никольск', 'Nikolskoye': 'Никольское', 'Nizhnekamsk': 'Нижнекамск', 'Nizhneudinsk': 'Нижнеудинск', 'Nizhnevartovsk': 'Нижневартовск', 'Nizhniye Sergi': 'Нижние Серги', 'Nizhny Lomov': 'Нижний Ломов', 'Nizhny Novgorod': 'Нижний Новгород', 'Nizhny Tagil': 'Нижний Тагил', 'Nizhnyaya Salda': 'Нижняя Салда', 'Nizhnyaya Tura': 'Нижняя Тура', 'Noginsk': 'Ногинск', 'Nolinsk': 'Нолинск', 'Norilsk': 'Норильск', 'Novaya Ladoga': 'Новая Ладога', 'Novaya Lyalya': 'Новая Ляля', 'Novoaleksandrovsk': 'Новоалександровск', 'Novoaltaysk': 'Новоалтайск', 'Novoanninskiy': 'Новоаннинский', 'Novocheboksarsk': 'Новочебоксарск', 'Novocherkassk': 'Новочеркасск', 'Novodvinsk': 'Новодвинск', 'Novokhopersk': 'Новохопёрск', 'Novokubansk': 'Новокубанск', 'Novokuybyshevsk': 'Новокуйбышевск', 'Novokuznetsk': 'Новокузнецк', 'Novomichurinsk': 'Новомичуринск', 'Novomoskovsk': 'Новомосковск', 'Novopavlovsk': 'Новопавловск', 'Novorossiysk': 'Новороссийск', 'Novorzhev': 'Новоржев', 'Novoshakhtinsk': 'Новошахтинск', 'Novosibirsk': 'Новосибирск', 'Novosil': 'Новосиль', 'Novosokolniki': 'Новосокольники', 'Novotroitsk': 'Новотроицк', 'Novoulyanovsk': 'Новоульяновск', 'Novouralsk': 'Новоуральск', 'Novouzensk': 'Новоузенск', 'Novovoronezh': 'Нововоронеж', 'Novozybkov': 'Новозыбков', 'Novy Oskol': 'Новый Оскол', 'Novy Urengoy': 'Новый Уренгой', 'Noyabrsk': 'Ноябрьск', 'Nurlat': 'Нурлат', 'Nyagan': 'Нягань', 'Nyandoma': 'Няндома', 'Nyazepetrovsk': 'Нязепетровск', 'Nytva': 'Нытва', 'Nyurba': 'Нюрба', 'Obluchye': 'Облучье', 'Obninsk': 'Обнинск', 'Oboyan': 'Обоянь', 'Ocher': 'Очёр', 'Odintsovo': 'Одинцово', 'Okha': 'Оха', 'Okhansk': 'Оханск', 'Oktyabrsky': 'Октябрьский', 'Okulovka': 'Окуловка', 'Olenegorsk': 'Оленегорск', 'Olonets': 'Олонец', 'Olekminsk': 'Олёкминск', 'Omsk': 'Омск', 'Omutninsk': 'Омутнинск', 'Onega': 'Онега', 'Opochka': 'Опочка', 'Orekhovo Zuyevo': 'Орехово-Зуево', 'Orel': 'Орёл', 'Orenburg': 'Оренбург', 'Orlov': 'Орлов', 'Orsk': 'Орск', 'Osinniki': 'Осинники', 'Ostashkov': 'Осташков', 'Ostrogozhsk': 'Острогожск', 'Ostrov': 'Остров', 'Ostrovnoy': 'Островной', 'Otradnoye': 'Отрадное', 'Otradny': 'Отрадный', 'Ozersk': 'Озёрск', 'Ozherelye': 'Ожерелье', 'Ozery': 'Озёры', 'Pallasovka': 'Палласовка', 'Partizansk': 'Партизанск', 'Pavlovo': 'Павлово', 'Pavlovsk': 'Павловск', 'Pavlovsky Posad': 'Павловский Посад', 'Pechora': 'Печора', 'Pechory': 'Печоры', 'Penza': 'Пенза', 'Pereslavl Zalessky': 'Переславль-Залесский', 'Peresvet': 'Пересвет', 'Perevoz': 'Перевоз', 'Perm': 'Пермь', 'Pervomaysk': 'Первомайск', 'Pervouralsk': 'Первоуральск', 'Pestovo': 'Пестово', 'Petergof': 'Петергоф', 'Petropavlovsk Kamchatsky': 'Петропавловск-Камчатский', 'Petrov Val': 'Петров Вал', 'Petrovsk': 'Петровск', 'Petrovsk Zabaykalsky': 'Петровск-Забайкальский', 'Petrozavodsk': 'Петрозаводск', 'Petukhovo': 'Петухово', 'Petushki': 'Петушки', 'Pevek': 'Певек', 'Pikalevo': 'Пикалёво', 'Pionerskiy': 'Пионерский', 'Pitkyaranta': 'Питкяранта', 'Plast': 'Пласт', 'Plavsk': 'Плавск', 'Pochep': 'Почеп', 'Pochinok': 'Починок', 'Podolsk': 'Подольск', 'Podporozhye': 'Подпорожье', 'Pokhvistnevo': 'Похвистнево', 'Pokrov': 'Покров', 'Pokrovsk': 'Покровск', 'Polessk': 'Полесск', 'Polevskoy': 'Полевской', 'Polyarny': 'Полярный', 'Polyarnye Zori': 'Полярные Зори', 'Polysayevo': 'Полысаево', 'Porkhov': 'Порхов', 'Poronaysk': 'Поронайск', 'Poshekhonye': 'Пошехонье', 'Povorino': 'Поворино', 'Pravdinsk': 'Правдинск', 'Primorsko Akhtarsk': 'Приморско-Ахтарск', 'Priozersk': 'Приозерск', 'Privolzhsk': 'Приволжск', 'Prokhladny': 'Прохладный', 'Prokopyevsk': 'Прокопьевск', 'Proletarsk': 'Пролетарск', 'Protvino': 'Протвино', 'Pskov': 'Псков', 'Puchezh': 'Пучеж', 'Pudozh': 'Пудож', 'Pugachev': 'Пугачев', 'Pushchino': 'Пущино', 'Pushkino': 'Пушкино', 'Pushkin': 'Пушкин', 'Pustoshka': 'Пустошка', 'Pyatigorsk': 'Пятигорск', 'Pytalovo': 'Пыталово', 'Raduzhny': 'Радужный', 'Ramenskoye': 'Раменское', 'Rasskazovo': 'Рассказово', 'Raychikhinsk': 'Райчихинск', 'Reutov': 'Реутов', 'Revda': 'Ревда', 'Rezh': 'Реж', 'Rodniki': 'Родники', 'Roshal': 'Рошаль', 'Roslavl': 'Рославль', 'Rossosh': 'Россошь', 'Rostov on Don': 'Ростов-на-Дону', 'Rtishchevo': 'Ртищево', 'Rubtsovsk': 'Рубцовск', 'Rudnya': 'Рудня', 'Ruza': 'Руза', 'Ruzayevka': 'Рузаевка', 'Ryazan': 'Рязань', 'Ryazhsk': 'Ряжск', 'Rybinsk': 'Рыбинск', 'Rybnoye': 'Рыбное', 'Rylsk': 'Рыльск', 'Rzhev': 'Ржев', 'Safonovo': 'Сафоново', 'Saint Petersburg': 'Санкт-Петербург', 'Salair': 'Салаир', 'Salavat': 'Салават', 'Salekhard': 'Салехард', 'Salsk': 'Сальск', 'Samara': 'Самара', 'Saransk': 'Саранск', 'Sarapul': 'Сарапул', 'Saratov': 'Саратов', 'Sarov': 'Саров', 'Sasovo': 'Сасово', 'Satka': 'Сатка', 'Sayanogorsk': 'Саяногорск', 'Sayansk': 'Саянск', 'Sebezh': 'Себеж', 'Segezha': 'Сегежа', 'Seltso': 'Сельцо', 'Semikarakorsk': 'Семикаракорск', 'Semiluki': 'Семилуки', 'Semenov': 'Семёнов', 'Sengiley': 'Сенгилей', 'Serafimovich': 'Серафимович', 'Serdobsk': 'Сердобск', 'Sergach': 'Сергач', 'Sergiyev Posad': 'Сергиев Посад', 'Serov': 'Серов', 'Serpukhov': 'Серпухов', 'Sertolovo': 'Сертолово', 'Sestroretsk': 'Сестрорецк', 'Severobaykalsk': 'Северобайкальск', 'Severodvinsk': 'Северодвинск', 'Severo Kurilsk': 'Северо-Курильск', 'Severomorsk': 'Североморск', 'Severouralsk': 'Североуральск', 'Seversk': 'Северск', 'Sevsk': 'Севск', 'Shadrinsk': 'Шадринск', 'Shagonar': 'Шагонар', 'Shakhtyorsk': 'Шахтерск', 'Shakhty': 'Шахты', 'Shakhunya': 'Шахунья', 'Sharya': 'Шарья', 'Sharypovo': 'Шарыпово', 'Shatsk': 'Шацк', 'Shatura': 'Шатура', 'Shcherbinka': 'Щербинка', 'Shchigry': 'Щигры', 'Shchuchye': 'Щучье', 'Shchekino': 'Щёкино', 'Shchelkovo': 'Щёлково', 'Shebekino': 'Шебекино', 'Shelekhov': 'Шелехов', 'Shenkursk': 'Шенкурск', 'Shikhany': 'Шиханы', 'Shilka': 'Шилка', 'Shimanovsk': 'Шимановск', 'Shlisselburg': 'Шлиссельбург', 'Shumerlya': 'Шумерля', 'Shumikha': 'Шумиха', 'Shuya': 'Шуя', 'Sibay': 'Сибай', 'Skopin': 'Скопин', 'Skovorodino': 'Сковородино', 'Slantsy': 'Сланцы', 'Slavgorod': 'Славгород', 'Slavsk': 'Славск', 'Slavyansk na Kubani': 'Славянск-на-Кубани', 'Slobodskoy': 'Слободской', 'Slyudyanka': 'Слюдянка', 'Smolensk': 'Смоленск', 'Snezhinsk': 'Снежинск', 'Snezhnogorsk': 'Снежногорск', 'Sobinka': 'Собинка', 'Sochi': 'Сочи', 'Sokol': 'Сокол', 'Sokolniki': 'Сокольники', 'Soligalich': 'Солигалич', 'Solikamsk': 'Соликамск', 'Sol Iletsk': 'Соль-Илецк', 'Solnechnogorsk': 'Солнечногорск', 'Soltsy': 'Сольцы', 'Solvychegodsk': 'Сольвычегодск', 'Sorochinsk': 'Сорочинск', 'Sorsk': 'Сорск', 'Sortavala': 'Сортавала', 'Sosenskiy': 'Сосенский', 'Sosnogorsk': 'Сосногорск', 'Sosnovka': 'Сосновка', 'Sosnovoborsk': 'Сосновоборск', 'Sosnoviy Bor': 'Сосновый Бор', 'Sovetsk': 'Советск', 'Sovetskaya Gavan': 'Советская Гавань', 'Sovetskiy': 'Советский', 'Spas Demensk': 'Спас-Деменск', 'Spas Klepiki': 'Спас-Клепики', 'Spassk Dalny': 'Спасск-Дальний', 'Spassk Ryazansky': 'Спасск-Рязанский', 'Spassk': 'Спасск', 'Srednekolymsk': 'Среднеколымск', 'Sredneuralsk': 'Среднеуральск', 'Sretensk': 'Сретенск', 'Staraya Kupavna': 'Старая Купавна', 'Staraya Russa': 'Старая Русса', 'Staritsa': 'Старица', 'Starodub': 'Стародуб', 'Stary Oskol': 'Старый Оскол', 'Stavropol': 'Ставрополь', 'Sterlitamak': 'Стерлитамак', 'Strezhevoy': 'Стрежевой', 'Stroitel': 'Строитель', 'Strunino': 'Струнино', 'Stupino': 'Ступино', 'Sudogda': 'Судогда', 'Sudzha': 'Суджа', 'Sukhinichi': 'Сухиничи', 'Sukhoy Log': 'Сухой Лог', 'Suoyarvi': 'Суоярви', 'Surazh': 'Сураж', 'Surgut': 'Сургут', 'Surovikino': 'Суровикино', 'Sursk': 'Сурск', 'Susuman': 'Сусуман', 'Suvorov': 'Суворов', 'Suzdal': 'Суздаль', 'Svetlogorsk': 'Светлогорск', 'Svetlograd': 'Светлоград', 'Svetly': 'Светлый', 'Svetogorsk': 'Светогорск', 'Svirsk': 'Свирск', 'Svobodny': 'Свободный', 'Syasstroy': 'Сясьстрой', 'Sychevka': 'Сычёвка', 'Syktyvkar': 'Сыктывкар', 'Sysert': 'Сысерть', 'Syzran': 'Сызрань', 'Taganrog': 'Таганрог', 'Taldom': 'Талдом', 'Talitsa': 'Талица', 'Tambov': 'Тамбов', 'Tara': 'Тара', 'Tarko Sale': 'Тарко-Сале', 'Tarusa': 'Таруса', 'Tashtagol': 'Таштагол', 'Tatarsk': 'Татарск', 'Tavda': 'Тавда', 'Tayga': 'Тайга', 'Tayshet': 'Тайшет', 'Teberda': 'Теберда', 'Temnikov': 'Темников', 'Temryuk': 'Темрюк', 'Terek': 'Терек', 'Tetyushi': 'Тетюши', 'Teykovo': 'Тейково', 'Tikhoretsk': 'Тихорецк', 'Tikhvin': 'Тихвин', 'Timashevsk': 'Тимашёвск', 'Tobolsk': 'Тобольск', 'Toguchin': 'Тогучин', 'Tolyatti': 'Тольятти', 'Tomari': 'Томари', 'Tommot': 'Томмот', 'Tomsk': 'Томск', 'Topki': 'Топки', 'Toropets': 'Торопец', 'Torzhok': 'Торжок', 'Tosno': 'Тосно', 'Totma': 'Тотьма', 'Troitsk': 'Троицк', 'Trubchevsk': 'Трубчевск', 'Trekhgorny': 'Трёхгорный', 'Tsimlyansk': 'Цимлянск', 'Tsivilsk': 'Цивильск', 'Tuapse': 'Туапсе', 'Tula': 'Тула', 'Turan': 'Туран', 'Turinsk': 'Туринск', 'Tutayev': 'Тутаев', 'Tuymazy': 'Туймазы', 'Tver': 'Тверь', 'Tynda': 'Тында', 'Tyrnyauz': 'Тырныауз', 'Tyukalinsk': 'Тюкалинск', 'Tyumen': 'Тюмень', 'Uchaly': 'Учалы', 'Udachny': 'Удачный', 'Udomlya': 'Удомля', 'Ufa': 'Уфа', 'Uglegorsk': 'Углегорск', 'Uglich': 'Углич', 'Ukhta': 'Ухта', 'Ulan Ude': 'Улан-Удэ', 'Ulyanovsk': 'Ульяновск', 'Unecha': 'Унеча', 'Uren': 'Урень', 'Urus Martan': 'Урус-Мартан', 'Uryupinsk': 'Урюпинск', 'Urzhum': 'Уржум', 'Usinsk': 'Усинск', 'Usman': 'Усмань', 'Usolye Sibirskoye': 'Усолье-Сибирское', 'Ussuriysk': 'Уссурийск', 'Ust Dzheguta': 'Усть-Джегута', 'Ust Ilimsk': 'Усть-Илимск', 'Ust Katav': 'Усть-Катав', 'Ust Kut': 'Усть-Кут', 'Ust Labinsk': 'Усть-Лабинск', 'Ustyuzhna': 'Устюжна', 'Uvarovo': 'Уварово', 'Uyar': 'Уяр', 'Uzhur': 'Ужур', 'Uzlovaya': 'Узловая', 'Valuyki': 'Валуйки', 'Velikiye Luki': 'Великие Луки', 'Velikiy Novgorod': 'Великий Новгород', 'Velikiy Ustyug': 'Великий Устюг', 'Velizh': 'Велиж', 'Velsk': 'Вельск', 'Venyov': 'Венёв', 'Vereshchagino': 'Верещагино', 'Vereya': 'Верея', 'Verkhneuralsk': 'Верхнеуральск', 'Verkhniy Tagil': 'Верхний Тагил', 'Verkhniy Ufaley': 'Верхний Уфалей', 'Verkhnyaya Pyshma': 'Верхняя Пышма', 'Verkhnyaya Salda': 'Верхняя Салда', 'Verkhnyaya Tura': 'Верхняя Тура', 'Verkhoturye': 'Верхотурье', 'Verkhoyansk': 'Верхоянск', 'Vesyegonsk': 'Весьегонск', 'Vetluga': 'Ветлуга', 'Vichuga': 'Вичуга', 'Vidnoye': 'Видное', 'Vikhorevka': 'Вихоревка', 'Vilyuchinsk': 'Вилючинск', 'Vilyuysk': 'Вилюйск', 'Vladikavkaz': 'Владикавказ', 'Vladimir': 'Владимир', 'Vladivostok': 'Владивосток', 'Volchansk': 'Волчанск', 'Volgodonsk': 'Волгодонск', 'Volgograd': 'Волгоград', 'Volgorechensk': 'Волгореченск', 'Volkhov': 'Волхов', 'Volodarsk': 'Володарск', 'Vologda': 'Вологда', 'Volokolamsk': 'Волоколамск', 'Volosovo': 'Волосово', 'Volsk': 'Вольск', 'Volzhskiy': 'Волжский', 'Volzhsk': 'Волжск', 'Vorkuta': 'Воркута', 'Voronezh': 'Воронеж', 'Vorsma': 'Ворсма', 'Voskresensk': 'Воскресенск', 'Votkinsk': 'Воткинск', 'Vsevolozhsk': 'Всеволожск', 'Vuktyl': 'Вуктыл', 'Vyatskiye Polyany': 'Вятские Поляны', 'Vyazemskiy': 'Вяземский', 'Vyazma': 'Вязьма', 'Vyazniki': 'Вязники', 'Vyborg': 'Выборг', 'Vyksa': 'Выкса', 'Vyshniy Volochek': 'Вышний Волочёк', 'Vysokovsk': 'Высоковск', 'Vytegra': 'Вытегра', 'Yadrin': 'Ядрин', 'Yakhroma': 'Яхрома', 'Yakutsk': 'Якутск', 'Yalutorovsk': 'Ялуторовск', 'Yanaul': 'Янаул', 'Yaransk': 'Яранск', 'Yaroslavl': 'Ярославль', 'Yarovoye': 'Яровое', 'Yartsevo': 'Ярцево', 'Yasnogorsk': 'Ясногорск', 'Yasny': 'Ясный', 'Yefremov': 'Ефремов', 'Yegoryevsk': 'Егорьевск', 'Yekaterinburg': 'Екатеринбург', 'Yelabuga': 'Елабуга', 'Yelets': 'Елец', 'Yelizovo': 'Елизово', 'Yelnya': 'Ельня', 'Yemanzhelinsk': 'Еманжелинск', 'Yemva': 'Емва', 'Yeniseysk': 'Енисейск', 'Yermolino': 'Ермолино', 'Yershov': 'Ершов', 'Yessentuki': 'Ессентуки', 'Yeysk': 'Ейск', 'Yoshkar Ola': 'Йошкар-Ола', 'Yubileyny': 'Юбилейный', 'Yugorsk': 'Югорск', 'Yukhnov': 'Юхнов', 'Yurga': 'Юрга', 'Yuryevets': 'Юрьевец', 'Yuryev Polskiy': 'Юрьев-Польский', 'Yuryuzan': 'Юрюзань', 'Yuzha': 'Южа', 'Yuzhno Sakhalinsk': 'Южно-Сахалинск', 'Yuzhno Sukhokumsk': 'Южно-Сухокумск', 'Yuzhnouralsk': 'Южноуральск', 'Zadonsk': 'Задонск', 'Zainsk': 'Заинск', 'Zakamensk': 'Закаменск', 'Zaozerny': 'Заозёрный', 'Zaozersk': 'Заозёрск', 'Zapadnaya Dvina': 'Западная Двина', 'Zapolyarny': 'Заполярный', 'Zaraysk': 'Зарайск', 'Zarechny': 'Заречный', 'Zarinsk': 'Заринск', 'Zavitinsk': 'Завитинск', 'Zavodoukovsk': 'Заводоуковск', 'Zavolzhsk': 'Заволжск', 'Zavolzhye': 'Заволжье', 'Zelenodolsk': 'Зеленодольск', 'Zelenogorsk': 'Зеленогорск', 'Zelenogradsk': 'Зеленоградск', 'Zelenograd': 'Зеленоград', 'Zelenokumsk': 'Зеленокумск', 'Zernograd': 'Зерноград', 'Zeya': 'Зея', 'Zheleznodorozhny': 'Железнодорожный', 'Zheleznogorsk': 'Железногорск', 'Zheleznogorsk Ilimskiy': 'Железногорск-Илимский', 'Zheleznovodsk': 'Железноводск', 'Zherdevka': 'Жердевка', 'Zhigulevsk': 'Жигулёвск', 'Zhirnovsk': 'Жирновск', 'Zhizdra': 'Жиздра', 'Zhukovka': 'Жуковка', 'Zhukovskiy': 'Жуковский', 'Zima': 'Зима', 'Zlatoust': 'Златоуст', 'Zlynka': 'Злынка', 'Zmeinogorsk': 'Змеиногорск', 'Zubtsov': 'Зубцов', 'Zuyevka': 'Зуевка', 'Zvenigorod': 'Звенигород', 'Zvenigovo': 'Звенигово', 'Zverevo': 'Зверево'}


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        },
        "session_state": {
            "city": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': get_random_stock(user_id)
        }

        res['response']['text'] = 'Привет! Подскажи, цену какой акции ты хочешь посмотреть?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    for i in reDict:
        if re.search(reDict[i], req['request']['original_utterance'], re.IGNORECASE):
            api_result = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/' + i + '?modules=price')
            if api_result:
                api_response = json.loads(api_result.content.decode('utf-8'))
                regularMarketPrice = res['quoteSummary']['result'][0]['price']['regularMarketPrice']['fmt']
                currency = res['quoteSummary']['result'][0]['price']['currency']

                res['response']['text'] = 'Сейчас стоимость акций ' + reDict[i] +  " " + regularMarketPrice + " " + currency + "."
                res['response']['buttons'] = [{'title': "Подробнее", 'hide': True}]
                res['session_state']['city'] = i
            else:
                res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
            return

'''    if req['state']['session']['city'] and req['request']['original_utterance'].lower() in [
        'подробнее', 'подробно', 'еще', 'ещё', 'больше'
    ]:
        params = {
          'access_key': '3af61219c67daf3a9bbc914733fdb090',
          'query': req['state']['session']['city']
        }
        api_result = requests.get('http://api.weatherstack.com/current', params)
        api_response = api_result.json()
        if api_response:
            wind_speed = str(int(round(api_response['current']['wind_speed'] * 1000 / 3600)))
            res['response']['text'] = 'Скорость ветра ' + wind_speed + ' м/с, ' + 'влажность ' + str(api_response['current']['humidity']) + '%.'
        else:
            res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
        res['session_state']['city'] = req['state']['session']['city']
        return'''


    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что вы умеете'
    ]:
        sessionStorage[user_id] = {
            'suggests': get_random_stock(user_id)
        }
        res['response']['text'] = 'Я умею всего-ничего, подсказывать стоимость акций!'
        res['response']['buttons'] = get_suggests(user_id)
        #res['session_state']['city'] = req['state']['session']['city']
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи GameStop!' % (
        req['request']['original_utterance']
    )
    #res['session_state']['city'] = req['state']['session']['city']

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][2:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
#    if len(suggests) < 2:
#        suggests.append({
#            "title": "Холодновато!",
#            "url": "https://thenorthface.com",
#            "hide": True
#        })

    return suggests

def get_random_stock(user_id):
    randomStocks = random.sample(list(reDict.keys()), 2)
    return randomStocks
