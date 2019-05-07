import datetime

from sputnik.clients.sputnik import SputnikService, Post

RSS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="https://search.yahoo.com/mrss/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:rambler="https://news.rambler.ru" xmlns:news="https://www.google.com/schemas/sitemap-news/0.9" xmlns:video="https://www.google.com/schemas/sitemap-video/1.1" xmlns:image="https://www.google.com/schemas/sitemap-image/1.1" version="2.0">
<channel>
{data}
</channel></rss>
"""


def test_get_post_list_detect_description():
    post = SputnikService()._get_post_list(RSS_TEMPLATE.format(data="""
<item xmlns:ns0="https://sputniknews.com"><title>主要声明和“幕后”花絮：弗拉基米尔•普京和金正恩会晤的最佳瞬间</title><link>http://sputniknews.cn/russia/201904261028311515/</link><guid>http://sputniknews.cn/russia/201904261028311515/</guid><ns0:related><ns0:url>http://sputniknews.cn/politics/201904251028310757/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Fri, 26 Apr 2019 01:34:00 +0800</pubDate><description>俄罗斯卫星通讯社记者简短摘要地讲述俄朝两国领导人如何进行了历史性会晤，会晤私下里发生了什么以及为新闻媒体提供了哪些题材。</description><ns0:type>article</ns0:type><category>俄罗斯</category><enclosure length="57426" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102830/40/1028304064.jpg" /></item>
<item xmlns:ns0="https://sputniknews.com"><title>日本准备在军舰上部署登陆部队</title><link>http://sputniknews.cn/opinion/201905071028408221/</link><guid>http://sputniknews.cn/opinion/201905071028408221/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 21:22:59 +0800</pubDate><description>日本准备在其西南海域军舰上部署登陆部队再次挑动了中国神经。俄罗斯远东研究所专家瓦列里·基斯塔诺夫接受俄罗斯卫星通讯社采访评论日本《读卖新闻》有关日本或在自卫队军舰上部署陆军的报道时做出了此番表述。但他认为，日本建立新的常规作战单位不会对中日政治和经济关系的向前推进产生任何影响。</description><ns0:type>article</ns0:type><category>评论</category><enclosure length="100239" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102840/81/1028408170.jpg" /></item>
<item xmlns:ns0="https://sputniknews.com"><title>如何在空难中提高存活率？看专家怎么说</title><link>http://sputniknews.cn/society/201905071028402529/</link><guid>http://sputniknews.cn/society/201905071028402529/</guid><ns0:related><ns0:url>http://sputniknews.cn/russia/201905071028402351/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 15:04:28 +0800</pubDate><description>全俄旅客协会主席伊利亚·佐托夫周一（5月6日）向俄罗斯卫星通讯社介绍了如何在航空事故中提高生存机率。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="104449" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102711/84/1027118414.jpg" /></item>
"""))

    assert post == [
        Post(
            post_id='201904261028311515', title='主要声明和“幕后”花絮：弗拉基米尔•普京和金正恩会晤的最佳瞬间',
            link='http://sputniknews.cn/russia/201904261028311515/',
            guid='http://sputniknews.cn/russia/201904261028311515/', pub_date=datetime.datetime(2019, 4, 26, 1, 34),
            description='俄罗斯卫星通讯社记者简短摘要地讲述俄朝两国领导人如何进行了历史性会晤，会晤私下里发生了什么以及为新闻媒体提供了哪些题材。', category='俄罗斯',
            enclosure='http://cdn3.img.sputniknews.cn/images/102830/40/1028304064.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>主要声明和“幕后”花絮：弗拉基米尔•普京和金正恩会晤的最佳瞬间</title><link>http://sputniknews.cn/russia/201904261028311515/</link><guid>http://sputniknews.cn/russia/201904261028311515/</guid><ns0:related><ns0:url>http://sputniknews.cn/politics/201904251028310757/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Fri, 26 Apr 2019 01:34:00 +0800</pubDate><description>俄罗斯卫星通讯社记者简短摘要地讲述俄朝两国领导人如何进行了历史性会晤，会晤私下里发生了什么以及为新闻媒体提供了哪些题材。</description><ns0:type>article</ns0:type><category>俄罗斯</category><enclosure length="57426" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102830/40/1028304064.jpg" /></item>\n',
        ),
        Post(
            post_id='201905071028408221', title='日本准备在军舰上部署登陆部队',
            link='http://sputniknews.cn/opinion/201905071028408221/',
            guid='http://sputniknews.cn/opinion/201905071028408221/',
            pub_date=datetime.datetime(2019, 5, 7, 21, 22, 59),
            description='日本准备在其西南海域军舰上部署登陆部队再次挑动了中国神经。俄罗斯远东研究所专家瓦列里·基斯塔诺夫接受俄罗斯卫星通讯社采访评论日本《读卖新闻》有关日本或在自卫队军舰上部署陆军的报道时做出了此番表述。但他认为，日本建立新的常规作战单位不会对中日政治和经济关系的向前推进产生任何影响。',
            category='评论',
            enclosure='http://cdn3.img.sputniknews.cn/images/102840/81/1028408170.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>日本准备在军舰上部署登陆部队</title><link>http://sputniknews.cn/opinion/201905071028408221/</link><guid>http://sputniknews.cn/opinion/201905071028408221/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 21:22:59 +0800</pubDate><description>日本准备在其西南海域军舰上部署登陆部队再次挑动了中国神经。俄罗斯远东研究所专家瓦列里·基斯塔诺夫接受俄罗斯卫星通讯社采访评论日本《读卖新闻》有关日本或在自卫队军舰上部署陆军的报道时做出了此番表述。但他认为，日本建立新的常规作战单位不会对中日政治和经济关系的向前推进产生任何影响。</description><ns0:type>article</ns0:type><category>评论</category><enclosure length="100239" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102840/81/1028408170.jpg" /></item>\n',
        ),
        Post(
            post_id='201905071028402529', title='如何在空难中提高存活率？看专家怎么说',
            link='http://sputniknews.cn/society/201905071028402529/',
            guid='http://sputniknews.cn/society/201905071028402529/',
            pub_date=datetime.datetime(2019, 5, 7, 15, 4, 28),
            description='全俄旅客协会主席伊利亚·佐托夫周一（5月6日）向俄罗斯卫星通讯社介绍了如何在航空事故中提高生存机率。',
            category='社会',
            enclosure='http://cdn3.img.sputniknews.cn/images/102711/84/1027118414.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>如何在空难中提高存活率？看专家怎么说</title><link>http://sputniknews.cn/society/201905071028402529/</link><guid>http://sputniknews.cn/society/201905071028402529/</guid><ns0:related><ns0:url>http://sputniknews.cn/russia/201905071028402351/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 15:04:28 +0800</pubDate><description>全俄旅客协会主席伊利亚·佐托夫周一（5月6日）向俄罗斯卫星通讯社介绍了如何在航空事故中提高生存机率。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="104449" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102711/84/1027118414.jpg" /></item>\n\n',
        )
    ]


def test_get_post_list_split_description():
    post = SputnikService()._get_post_list(RSS_TEMPLATE.format(
        data="""<item xmlns:ns0="https://sputniknews.com"><title>俄驻叙调解中心：武装分子两次袭击叙赫梅米姆空军基地</title><link>http://sputniknews.cn/military/201905071028399317/</link><guid>http://sputniknews.cn/military/201905071028399317/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 05:30:36 +0800</pubDate><description>俄罗斯卫星通讯社莫斯科电 俄罗斯驻叙利亚冲突各方调解中心负责人维克托∙库普奇申对媒体表示，武装分子两次使用火箭炮袭击叙利亚赫梅米姆空军基地。</description><ns0:type>article</ns0:type><category>军事</category><enclosure length="62303" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/101653/32/1016533204.jpg" /></item>"""))

    assert post == [
        Post(
            post_id='201905071028399317', title='俄驻叙调解中心：武装分子两次袭击叙赫梅米姆空军基地',
            link='http://sputniknews.cn/military/201905071028399317/',
            guid='http://sputniknews.cn/military/201905071028399317/',
            pub_date=datetime.datetime(2019, 5, 7, 5, 30, 36),
            description='俄罗斯驻叙利亚冲突各方调解中心负责人维克托∙库普奇申对媒体表示，武装分子两次使用火箭炮袭击叙利亚赫梅米姆空军基地。', category='军事',
            enclosure='http://cdn3.img.sputniknews.cn/images/101653/32/1016533204.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>俄驻叙调解中心：武装分子两次袭击叙赫梅米姆空军基地</title><link>http://sputniknews.cn/military/201905071028399317/</link><guid>http://sputniknews.cn/military/201905071028399317/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 05:30:36 +0800</pubDate><description>俄罗斯卫星通讯社莫斯科电 俄罗斯驻叙利亚冲突各方调解中心负责人维克托∙库普奇申对媒体表示，武装分子两次使用火箭炮袭击叙利亚赫梅米姆空军基地。</description><ns0:type>article</ns0:type><category>军事</category><enclosure length="62303" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/101653/32/1016533204.jpg" /></item>\n',
        )
    ]


def test_get_post_list_get_image():
    post = SputnikService()._get_post_list(RSS_TEMPLATE.format(data="""
    <item xmlns:ns0="https://sputniknews.com"><title>香港手工麻将技艺濒临失传</title><link>http://sputniknews.cn/video/201904251028308048/</link><guid>http://sputniknews.cn/video/201904251028308048/</guid><ns0:priority>3</ns0:priority><pubDate>Thu, 25 Apr 2019 18:35:00 +0800</pubDate><description>63岁的张顺景是香港为数不多的手工麻将雕刻大师之一。</description><ns0:type>video</ns0:type><category>视频</category><enclosure source_name="Sputnik" type="video/x-flv" url="https://nfw.ria.ru/flv/file.aspx?ID=89657692&amp;type=flv" /><enclosure type="image/png" url="http://cdn3.img.sputniknews.cn/images/102830/86/1028308672.png" /></item>
    <item xmlns:ns0="https://sputniknews.com"><title>在布鲁塞尔市中心意外出土一个10世纪的城市</title><link>http://sputniknews.cn/society/201905071028399279/</link><guid>http://sputniknews.cn/society/201905071028399279/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 03:41:00 +0800</pubDate><description>在布鲁塞尔市中心的未来市政厅的施工现场，人们看到的不是被拆掉的停车场，而是历史至少有千年的古建筑遗址。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="177145" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102839/82/1028398293.jpg" /></item>
    <item xmlns:ns0="https://sputniknews.com"><title>俄中摩托车手北京启程踏上“友谊之路”征程</title><link>http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/</link><guid>http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/</guid><ns0:priority>3</ns0:priority><pubDate>Sun, 28 Apr 2019 16:17:00 +0800</pubDate><description>俄驻华大使杰尼索夫4月27日在俄罗斯驻中国大使馆举行仪式上宣布，莫斯科-北京“友谊之路”俄中联合摩托车骑行活动正式启动。俄中摩托车骑手从北京出发踏上9000公里“友谊之路”，献礼两国建交70周年。</description><ns0:type>video</ns0:type><category>多媒体</category><enclosure source_name="Sputnik" type="video/x-flv" url="https://nfw.ria.ru/flv/file.aspx?ID=57848371&amp;type=flv" /><enclosure type="image/png" url="http://cdn3.img.sputniknews.cn/images/102833/28/1028332824.png" /></item>
    <item xmlns:ns0="https://sputniknews.com"><title>哈萨克斯坦中央选举委员会首次把女性作为总统候选人进行登记</title><link>http://sputniknews.cn/politics/201905041028380002/</link><guid>http://sputniknews.cn/politics/201905041028380002/</guid><ns0:related><ns0:url>http://sputniknews.cn/society/201905031028373510/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Sat, 04 May 2019 21:59:00 +0800</pubDate><description>俄罗斯卫星通讯社记者报道称，哈萨克斯坦中央选举委员会本周六（5月4日）历史上首次把女性作为国家总统候选人进行登记。</description><ns0:type>article</ns0:type><category>政治</category><enclosure length="83037" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102837/99/1028379979.jpg" /></item>
    <item xmlns:ns0="https://sputniknews.com"><title>俄罗斯在北京世园会上展出布良斯克人参</title><link>http://sputniknews.cn/society/201904301028346373/</link><guid>http://sputniknews.cn/society/201904301028346373/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 30 Apr 2019 07:03:32 +0800</pubDate><description>俄罗斯卫星通讯社北京电 俄罗斯在北京2019世界园艺博览会框架内于自己的展馆中展出了布良斯克人参。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="135386" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102834/63/1028346329.jpg" /></item>
    """))

    assert post == [
        Post(
            post_id='201904251028308048', title='香港手工麻将技艺濒临失传', link='http://sputniknews.cn/video/201904251028308048/',
            guid='http://sputniknews.cn/video/201904251028308048/', pub_date=datetime.datetime(2019, 4, 25, 18, 35),
            description='63岁的张顺景是香港为数不多的手工麻将雕刻大师之一。', category='视频',
            enclosure='http://cdn3.img.sputniknews.cn/images/102830/86/1028308672.png',
            text='<item xmlns:ns0="https://sputniknews.com"><title>香港手工麻将技艺濒临失传</title><link>http://sputniknews.cn/video/201904251028308048/</link><guid>http://sputniknews.cn/video/201904251028308048/</guid><ns0:priority>3</ns0:priority><pubDate>Thu, 25 Apr 2019 18:35:00 +0800</pubDate><description>63岁的张顺景是香港为数不多的手工麻将雕刻大师之一。</description><ns0:type>video</ns0:type><category>视频</category><enclosure source_name="Sputnik" type="video/x-flv" url="https://nfw.ria.ru/flv/file.aspx?ID=89657692&amp;type=flv" /><enclosure type="image/png" url="http://cdn3.img.sputniknews.cn/images/102830/86/1028308672.png" /></item>\n    ',
        ),
        Post(
            post_id='201905071028399279', title='在布鲁塞尔市中心意外出土一个10世纪的城市',
            link='http://sputniknews.cn/society/201905071028399279/',
            guid='http://sputniknews.cn/society/201905071028399279/',
            pub_date=datetime.datetime(2019, 5, 7, 3, 41),
            description='在布鲁塞尔市中心的未来市政厅的施工现场，人们看到的不是被拆掉的停车场，而是历史至少有千年的古建筑遗址。', category='社会',
            enclosure='http://cdn3.img.sputniknews.cn/images/102839/82/1028398293.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>在布鲁塞尔市中心意外出土一个10世纪的城市</title><link>http://sputniknews.cn/society/201905071028399279/</link><guid>http://sputniknews.cn/society/201905071028399279/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 03:41:00 +0800</pubDate><description>在布鲁塞尔市中心的未来市政厅的施工现场，人们看到的不是被拆掉的停车场，而是历史至少有千年的古建筑遗址。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="177145" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102839/82/1028398293.jpg" /></item>\n    ',
        ),
        Post(
            post_id='201904281028332955', title='俄中摩托车手北京启程踏上“友谊之路”征程',
            link='http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/',
            guid='http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/',
            pub_date=datetime.datetime(2019, 4, 28, 16, 17),
            description='俄驻华大使杰尼索夫4月27日在俄罗斯驻中国大使馆举行仪式上宣布，莫斯科-北京“友谊之路”俄中联合摩托车骑行活动正式启动。俄中摩托车骑手从北京出发踏上9000公里“友谊之路”，献礼两国建交70周年。',
            category='多媒体',
            enclosure='http://cdn3.img.sputniknews.cn/images/102833/28/1028332824.png',
            text='<item xmlns:ns0="https://sputniknews.com"><title>俄中摩托车手北京启程踏上“友谊之路”征程</title><link>http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/</link><guid>http://sputniknews.cn/china-russia-diplomatic-mm/201904281028332955/</guid><ns0:priority>3</ns0:priority><pubDate>Sun, 28 Apr 2019 16:17:00 +0800</pubDate><description>俄驻华大使杰尼索夫4月27日在俄罗斯驻中国大使馆举行仪式上宣布，莫斯科-北京“友谊之路”俄中联合摩托车骑行活动正式启动。俄中摩托车骑手从北京出发踏上9000公里“友谊之路”，献礼两国建交70周年。</description><ns0:type>video</ns0:type><category>多媒体</category><enclosure source_name="Sputnik" type="video/x-flv" url="https://nfw.ria.ru/flv/file.aspx?ID=57848371&amp;type=flv" /><enclosure type="image/png" url="http://cdn3.img.sputniknews.cn/images/102833/28/1028332824.png" /></item>\n    ',
        ),
        Post(
            post_id='201905041028380002', title='哈萨克斯坦中央选举委员会首次把女性作为总统候选人进行登记',
            link='http://sputniknews.cn/politics/201905041028380002/',
            guid='http://sputniknews.cn/politics/201905041028380002/', pub_date=datetime.datetime(2019, 5, 4, 21, 59),
            description='俄罗斯卫星通讯社记者报道称，哈萨克斯坦中央选举委员会本周六（5月4日）历史上首次把女性作为国家总统候选人进行登记。', category='政治',
            enclosure='http://cdn3.img.sputniknews.cn/images/102837/99/1028379979.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>哈萨克斯坦中央选举委员会首次把女性作为总统候选人进行登记</title><link>http://sputniknews.cn/politics/201905041028380002/</link><guid>http://sputniknews.cn/politics/201905041028380002/</guid><ns0:related><ns0:url>http://sputniknews.cn/society/201905031028373510/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Sat, 04 May 2019 21:59:00 +0800</pubDate><description>俄罗斯卫星通讯社记者报道称，哈萨克斯坦中央选举委员会本周六（5月4日）历史上首次把女性作为国家总统候选人进行登记。</description><ns0:type>article</ns0:type><category>政治</category><enclosure length="83037" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102837/99/1028379979.jpg" /></item>\n    ',
        ),
        Post(
            post_id='201904301028346373', title='俄罗斯在北京世园会上展出布良斯克人参',
            link='http://sputniknews.cn/society/201904301028346373/',
            guid='http://sputniknews.cn/society/201904301028346373/',
            pub_date=datetime.datetime(2019, 4, 30, 7, 3, 32),
            description='俄罗斯在北京2019世界园艺博览会框架内于自己的展馆中展出了布良斯克人参。', category='社会',
            enclosure='http://cdn3.img.sputniknews.cn/images/102834/63/1028346329.jpg',
            text='<item xmlns:ns0="https://sputniknews.com"><title>俄罗斯在北京世园会上展出布良斯克人参</title><link>http://sputniknews.cn/society/201904301028346373/</link><guid>http://sputniknews.cn/society/201904301028346373/</guid><ns0:priority>3</ns0:priority><pubDate>Tue, 30 Apr 2019 07:03:32 +0800</pubDate><description>俄罗斯卫星通讯社北京电 俄罗斯在北京2019世界园艺博览会框架内于自己的展馆中展出了布良斯克人参。</description><ns0:type>article</ns0:type><category>社会</category><enclosure length="135386" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102834/63/1028346329.jpg" /></item>\n    \n',
        )
    ]
