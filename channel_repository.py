from typing import Dict
from models import Channel

class ChannelRepository:
    def __init__(self):
        self.channels: Dict[str, Channel] = {
            #company
            "UCJFZiqLMntJufDCHc6bQixg": Channel(name="hololive ホロライブ - VTuber Group", weight=1.0),
            "UC10wVt6hoQiwySRhz7RdOUA": Channel(name="hololive DEV_IS", weight=1.0),
            "UCfrWoRGlawPQDQxxeIDRP0Q": Channel(name="hololive Indonesia", weight=1.0),
            "UCotXwY6s8pWmuWd_snKYjhg": Channel(name="hololive English", weight=1.0),
            "UCozx5csNhCx1wsVq3SZVkBQ": Channel(name="holoAN", weight=3.5),
            "UCGSOfFtVCTBfmGxHK5OD8ag": Channel(name="Ankimo Ch. あん肝チャンネル", weight=1.0),
            "UCu2DMOGLeR_DSStCyeQpi5Q": Channel(name="YAGOO Channel", weight=1.0),
            "UCKYyiJwNg2nV7hM86U5_wvw": Channel(name="Omegaα hololive-EN", weight=1.0),
            "UCl7xaOxJUq7GsD4M8N68FaA": Channel(name="HLZNTL ホリゾンタル", weight=1.0),
            "UCNoxM_Kxoa-_gOtoyjbux7Q": Channel(name="hololive English Shorts", weight=1.0),
            "UCnVbtCwr-5LXxUlGxsgD7sQ": Channel(name="Midnight Grand Orchestra", weight=1.0),
            #JPGen0
            "UC0TXe_LYZ4scaW2XMyi5_kw": Channel(name="AZKi Channel", weight=3.31),
            "UC5CwaMl1eIgY8h02uZw7u8A": Channel(name="Suisei Channel", weight=3.31),
            "UCp6993wxpyDPHUpavwDFqgg": Channel(name="SoraCh. ときのそらチャンネル", weight=3.31),
            "UCDqI2jOz0weumE8s7paEk6g": Channel(name="Roboco Ch. - ロボ子", weight=3.31),
            "UC-hM6YJuNYVAmUWxeIr9FeA": Channel(name="Miko Ch. さくらみこ", weight=3.31),
            #JPGen1
            "UC1CfXB_kRs3C-zaeTG3oGyg": Channel(name="HAACHAMA Ch 赤井はあと", weight=3.31),
            "UCD8HOxPs4Xvsm8H0ZxXGiBw": Channel(name="Mel Channel 夜空メルチャンネル", weight=3.31),
            "UCFTLzh12_nrtzqBPsTCqenA": Channel(name="アキロゼCh。Vtuber/ホロライブ所属", weight=3.31),
            "UCdn5BQ06XqgXoAxIhbqw5Rg": Channel(name="フブキCh。白上フブキ", weight=3.31),
            "UCQ0UDLQCjY0rmuxCDE38FGg": Channel(name="Matsuri Channel 夏色まつり", weight=3.31),
            #JPGen2
            "UC1opHUrw8rvnsadT-iGp7Cg": Channel(name="Aqua Ch. 湊あくあ", weight=3.31),
            "UCXTpFs_3PqI41qX2d9tL2Rw": Channel(name="Shion Ch. 紫咲シオン", weight=3.31),
            "UC1suqwovbL1kzsoaZgFZLKg": Channel(name="Choco Ch. 癒月ちょこ", weight=3.31),
            "UC7fk0CB07ly8oSl0aqKkqFg": Channel(name="Nakiri Ayame Ch. 百鬼あやめ", weight=3.31),
            "UCvzGlP9oQwU--Y0r9id_jnA": Channel(name="Subaru Ch. 大空スバル", weight=3.31),
            #JPGamer
            "UChAnqc_AY5_I3Px5dig3X1Q": Channel(name="Korone Ch. 戌神ころね", weight=3.31),
            "UCvaTdHTWBGv3MKj3KVqJVCw": Channel(name="Okayu Ch. 猫又おかゆ", weight=3.31),
            "UCp-5t9SrOQwXMU7iIjQfARg": Channel(name="Mio Channel 大神ミオ", weight=3.31),
            #JPGen3
            "UC1DCedRgGHBdm81E1llLhOQ": Channel(name="Pekora Ch. 兎田ぺこら", weight=3.31),
            "UCl_gCybOJRIgOXw6Qb4qJzQ": Channel(name="Rushia Ch. 潤羽るしあ", weight=3.31),
            "UCCzUftO8KOVkV4wQG1vkUvg": Channel(name="Marine Ch. 宝鐘マリン", weight=3.31),
            "UCvInZx9h3jC2JzsIzoOebWg": Channel(name="Flare Ch. 不知火フレア", weight=3.31),
            "UCdyqAaZDKHXg4Ahi7VENThQ": Channel(name="Noel Ch. 白銀ノエル", weight=3.31),
            #JPGen4
            "UC1uv2Oq6kNxgATlCiez59hw": Channel(name="Towa Ch. 常闇トワ", weight=3.31),
            "UCqm3BQLlJfvkTsX_hvm0UmA": Channel(name="Watame Ch. 角巻わため", weight=3.31),
            "UCa9Y57gfeY0Zro_noHRVrnw": Channel(name="Luna Ch. 姫森ルーナ", weight=3.31),
            "UCZlDXzGoo7d44bwdNObFacg": Channel(name="Kanata Ch. 天音かなた", weight=3.31),
            "UCS9uQI-jC3DE0L4IpXyvr6w": Channel(name="Coco Ch. 桐生ココ" , weight=3.31),
            #JPGen5
            "UCAWSyEs_Io8MtpY3m-zqILA": Channel(name="Nene Ch.桃鈴ねね", weight=3.31),
            "UCFKOVgVbGmX65RxO3EtH3iw": Channel(name="Lamy Ch. 雪花ラミィ", weight=3.31),
            "UCgZuwn-O7Szh9cAgHqJ6vjw": Channel(name="Aloe Ch.魔乃アロエ", weight=3.31),
            "UCK9V2B22uJYu3N7eR_BT9QA": Channel(name="Polka Ch. 尾丸ポルカ", weight=3.31),
            "UCUKD-uaobj9jiqB-VXt71mA": Channel(name="Shishiro Botan Ch. 獅白ぼたん", weight=3.31),
            #holoX
            "UC6eWCld0KwmyHFbAqK3V-Rw": Channel(name="Koyori ch. 博衣こより - holoX -", weight=3.31),
            "UCENwRMx5Yh42zWpzURebzTw": Channel(name="Laplus ch. ラプラス・ダークネス - holoX -", weight=3.31),
            "UCIBY1ollUsauvVi4hW4cumw": Channel(name="Chloe ch. 沙花叉クロヱ - holoX -", weight=3.31),
            "UC_vMYWcDjmfdpH6r4TTn1MQ": Channel(name="Iroha ch. 風真いろは -holoX-", weight=3.31),
            "UCs9_O1tRPMQTHQ-N_L6FU2g": Channel(name="Lui ch. 鷹嶺ルイ - holoX -", weight=3.31),
            #ReGLOSS
            "UC1iA6_NT4mtAcIII6ygrvCw": Channel(name="Hajime Ch. 轟はじめ ‐ ReGLOSS", weight=3.31),
            "UCdXAk5MpyLD8594lm_OvtGQ": Channel(name="Raden Ch. 儒烏風亭らでん ‐ ReGLOSS", weight=3.31),
            "UCMGfV7TVTmHhEErVJg1oHBQ": Channel(name="Ao Ch. 火威青 ‐ ReGLOSS", weight=3.31),
            "UCWQtYtq9EOB4-I5P-3fh8lA": Channel(name="Kanade Ch. 音乃瀬奏 ‐ ReGLOSS", weight=3.31),
            "UCtyWhCj3AqKh2dXctLkDtng": Channel(name="Ririka Ch. 一条莉々華 ‐ ReGLOSS", weight=3.31),
            #FLOW GLOW
            "UC9LSiN9hXI55svYEBrrK-tw": Channel(name="Riona Ch. 響咲リオナ - FLOW GLOW", weight=3.31),
            "UCuI_opAVX6qbxZY-a-AxFuQ": Channel(name="Niko Ch. 虎金妃笑虎 - FLOW GLOW", weight=3.31),
            "UCjk2nKmHzgH5Xy-C5qYRd5A": Channel(name="Su Ch. 水宮枢 - FLOW GLOW", weight=3.31),
            "UCKMWFR6lAstLa7Vbf5dH7ig": Channel(name="Chihaya Ch. 輪堂 千速 - FLOW GLOW", weight=3.31),
            "UCGzTVXqMQHa4AgJVJIVvtDQ": Channel(name="Vivi Ch. 綺々羅々ヴィヴィ - FLOW GLOW", weight=3.31),
            #ENGen1
            "UCHsx4Hqa-1ORjQTh9TYDhww": Channel(name="Takanashi Kiara Ch. hololive-EN", weight=1.0),
            "UCL_qhgtOy0dy1Agp8vkySQg": Channel(name="Mori Calliope Ch. hololive-EN", weight=1.0),
            "UCMwGHR0BTZuLsmjY_NT5Pwg": Channel(name="Ninomae Ina'nis Ch. hololive-EN", weight=1.0),
            "UCoSrY_IQQVpmIRZ9Xf-y93g": Channel(name="Gawr Gura Ch. hololive-EN", weight=1.0),
            "UCyl1z3jo3XHR1riLFKG5UAg": Channel(name="Amelia Watson Ch. hololive-EN", weight=1.0),
            #ENGen2
            "UC8rcEBzJSleTkf_-agPM20g": Channel(name="IRyS Ch. hololive-EN", weight=1.0),
            "UC3n5uGu18FoCy23ggWWp8tA": Channel(name="Nanashi Mumei Ch. hololive-EN", weight=1.0),
            "UCgmPnx-EEeOrZSg5Tiw7ZRQ": Channel(name="Hakos Baelz Ch. hololive-EN", weight=1.0),
            "UCmbs8T6MWqUHP1tIQvSgKrg": Channel(name="Ouro Kronii Ch. hololive-EN", weight=1.0),
            "UCO_aKKYxn4tvrqPjcTzZ6EQ": Channel(name="Ceres Fauna Ch. hololive-EN", weight=1.0),
            #ENGen3
            "UC9p_lqQ0FEDz327Vgf5JwqA": Channel(name="Koseki Bijou Ch. hololive-EN", weight=1.0),
            "UC_sFNM0z0MWm9A6WlKPuMMg": Channel(name="Nerissa Ravencroft Ch. hololive-EN", weight=1.0),
            "UCgnfPPb9JI3e9A4cXHnWbyg": Channel(name="Shiori Novella Ch. hololive-EN", weight=1.0),
            "UCt9H_RpQzhxzlyBxFqrdHqA": Channel(name="FUWAMOCO Ch. hololive-EN", weight=1.0),
            #ENGen4
            "UCW5uhrG1eCBYditmhL0Ykjw": Channel(name="Elizabeth Rose Bloodflame Ch. hololive-EN", weight=1.0),
            "UCDHABijvPBnJm7F-KlNME3w": Channel(name="Gigi Murin Ch. hololive-EN", weight=1.0),
            "UCvN5h1ShZtc7nly3pezRayg": Channel(name="Cecilia Immergreen Ch. hololive-EN", weight=1.0),
            "UCl69AEx4MdqMZH7Jtsm7Tig": Channel(name="Raora Panthera Ch. hololive-EN", weight=1.0),
            #IDGen1
            "UCAoy6rzhSf4ydcYjJw3WoVg": Channel(name="Airani Iofifteen Channel hololive-ID", weight=1.1),
            "UCP0BspO_AMEe3aQqqpo89Dg": Channel(name="Moona Hoshinova hololive-ID", weight=1.1),
            "UCOyYb1c43VlX9rc_lT6NKQw": Channel(name="Ayunda Risu Ch. hololive-ID", weight=1.1),
            #IDGen2
            "UC727SQYUvx5pDDGQpTICNWg": Channel(name="Anya Melfissa Ch. hololive-ID", weight=1.1),
            "UChgTyjG-pdNvxxhdsXfHQ5Q": Channel(name="Pavolia Reine Ch. hololive-ID", weight=1.1),
            "UCYz_5n-uDuChHtLo7My1HnQ": Channel(name="Kureiji Ollie Ch. hololive-ID", weight=1.1),
            #IDGen3
            "UCjLEmnpCNeisMxy134KPwWw": Channel(name="Kobo Kanaeru Ch. hololive-ID", weight=1.1),
            "UCTvHWSfBZgtxE4sILOaurIQ": Channel(name="Vestia Zeta Ch. hololive-ID", weight=1.1),
            "UCZLZ8Jjx_RN2CXloOmgTHVg": Channel(name="Kaela Kovalskia Ch. hololive-ID", weight=1.2),
            #CH
            "UCgNVXGlZIFK96XdEY20sVjg": Channel(name="Civia Ch.", weight=1.0),
            #SubChannels
            "UCLbtM3JZfRTg8v2KGag-RMw": Channel(name="AkiRose Ch.アキ・ローゼンタールSub", weight=3.31),
            "UCHj_mh57PVMXhAUDphUQDFA": Channel(name="HAACHAMA DARKWEB CH", weight=3.31),
            #NewLifes
            "UC9ruVYPv7yJmV0Rh0NKA-Lw": Channel(name="kson ONAIR", weight=3.31),
            "UC54JqsuIbMw_d1Ieb4hjKoQ": Channel(name="みけねこch", weight=3.81), #Mikoneko
            "UC7YXqPO3eUnxbJ6rN0z2z1Q": Channel(name="DELUTAYA Δ.", weight=3.81),
            "UC5gs8EbpwbfQvrhizJx60TA": Channel(name="飴宮なずな - Amemiya Nazuna - VSHOJO", weight=3.81),
            "UCz4jhqrCfthF8NnldZeK_rw": Channel(name="Rica Ch. / 利香", weight=3.81),
            "UCrV1Hf5r8P148idjoSfrGEQ": Channel(name="Sakuna Ch. 結城さくな", weight=3.81),
            "UC6T7TJZbW6nO-qsc5coo8Pg": Channel(name="dooby", weight=1.5),
            "UCIfAvpeIWGHb0duCkMkmm2Q": Channel(name="Nimi Nightmare", weight=1.5),
            "UClS3cnIUM9yzsBPQzeyX_8Q": Channel(name="Ruka Ch. 雨海ルカ", weight=3.81),
            "UCLIpj4TmXviSTNE_U5WG_Ug": Channel(name="Roa Ch. 海月雲ろあ", weight=3.81),
            "UCxsZ6NCzjU_t4YSxQLBcM5A": Channel(name="saba", weight=1.5),
            #Illustrators
            "UCt30jJgChL8qeT9VPadidSw": Channel(name="しぐれうい", weight=3.31), #Shigure UI
            "UCbfv8uuUXt3RSJGEwxny5Rw": Channel(name="カグラナナchannel／ななかぐら", weight=1.0), #Kagura Nana
            "UCvNn6mRroGDctnqU-FUsszg": Channel(name="Nachoneko", weight=1.0),
            "UCim0N3tvLijU_I3jbJeJV8g": Channel(name="るるどらいおん / rurudo", weight=1.0),
            #Nijisanji
            "UCoztvTULBYd3WmStqYeoHcA": Channel(name="笹木咲 / Sasaki Saku", weight=1.0),
            "UCdpUojq0KWZCN9bxXnZwz5w": Channel(name="アルス・アルマル -ars almal- 【にじさんじ", weight=1.0),
            "UC_4tXjqecqox5Uc05ncxpxg": Channel(name="椎名唯華 / Shiina Yuika", weight=1.0),
            "UCBURM8S4LH7cRZ0Clea9RDA": Channel(name="Reimu Endou【NIJISANJI EN", weight=1.0),
            "UCCVwhI5trmaSxfcze_Ovzfw": Channel(name="夢月ロア🌖Yuzuki Roa", weight=1.0),
            "UCerkculBD7YLc_vOGrF7tKg": Channel(name="魔使マオ -matsukai mao-", weight=1.0),
            #ES
            "UCzkwiov0OShlyRPdzwf0Xrg": Channel(name="夜巡ハナ / Hana Yomeguri Ch", weight=3.31),
            "UCp4G83RMBDN0EgZFSUDK7zw": Channel(name="Meica05 Ch. idol-ES", weight=3.31),
            "UC-jcaCw_DWLuWpcxVUjP2Sw": Channel(name="Nisha Nixyeva Ch.", weight=3.31),
            "UC4R6ddhBJp2bjQHVNxgNQSA": Channel(name="Akugaki Koa Ch. idol-ES", weight=3.31),
            "UCsFgdazMeQtf8lHvISB1DLQ": Channel(name="kyOresu", weight=1.0),
            #Others
            "UC7gxU6NXjKF1LrgOddPzgTw": Channel(name="Banzoin Hakka Ch. HOLOSTARS-EN", weight=1.0),
            "UCAr7rLi_Wn09G-XfTA07d4g": Channel(name="天神 子兎音 Tenjin Kotone", weight=1.0),
            "UCWCc8tO-uUl_7SJXIKJACMw": Channel(name="神楽めあ / KaguraMea", weight=1.0),
            "UC6sdN8CPm7v3UeV2mlqXmVw": Channel(name="Tororo Ch. 猫麦とろろ", weight=1.0),
            "UCtNeQ8cUwvAAhBbVbwfGWpg": Channel(name="Apricot (Froot)", weight=1.0),
            "UCLHmLrj4pHHg3-iBJn_CqxA": Channel(name="Neuro-Sama", weight=1.0),
            "UCqe0-vqZwAvZUb22wCMu1fA": Channel(name="音ノ乃のの / NononoNono", weight=1.0),
            "UC9V3Y3_uzU5e-usObb6IE1w": Channel(name="星川サラ / Sara Hoshikawa", weight=3.31),
            }

    def get_channel_by_id(self, channel_id: str) -> Channel:
        return self.channels.get(channel_id)

    def get_all_channel_ids(self) -> list:
        return list(self.channels.keys())

    def get_channel_weight(self, channel_id: str) -> float:
        channel = self.get_channel_by_id(channel_id)
        return channel.weight if channel else 1.0