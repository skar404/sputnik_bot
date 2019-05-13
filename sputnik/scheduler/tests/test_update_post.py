import datetime

import gino
from asynctest import patch

from sputnik.clients.sputnik import Post
from sputnik.models.main import DataBase
from sputnik.models.post import PostModel
from sputnik.scheduler.update_post import update_post

POST_LIST = [
    Post(
        post_id='201905081028410278', title='欧盟外交与安全政策高级代表：委内瑞拉问题联络小组打算加强与俄美中的协调',
        link='http://sputniknews.cn/politics/201905081028410278/',
        guid='http://sputniknews.cn/politics/201905081028410278/', pub_date=datetime.datetime(2019, 5, 8, 6, 57, 44
                                                                                              ),
        description='欧盟外交与安全政策高级代表莫盖里尼5月7日表示，委内瑞拉问题联络小组打算加强与俄美的协调与联络，近日已与莫斯科和华盛顿进行了磋商。', category='政治',
        enclosure='http://cdn3.img.sputniknews.cn/images/102563/94/1025639449.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>欧盟外交与安全政策高级代表：委内瑞拉问题联络小组打算加强与俄美中的协调</title><link>http://sputniknews.cn/politics/201905081028410278/</link><guid>http://sputniknews.cn/politics/201905081028410278/</guid><ns0:related><ns0:url>http://sputniknews.cn/politics/201905011028359869/</ns0:url><ns0:url>http://sputniknews.cn/politics/201905081028410061/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Wed, 08 May 2019 06:57:44 +0800</pubDate><description>俄罗斯卫星通讯社布鲁塞尔5月8日电 欧盟外交与安全政策高级代表莫盖里尼5月7日表示，委内瑞拉问题联络小组打算加强与俄美的协调与联络，近日已与莫斯科和华盛顿进行了磋商。</description><ns0:type>article</ns0:type><category>政治</category><enclosure length="86230" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102563/94/1025639449.jpg" /></item>',
        short_link='http://sptnkne.ws/mwdA'
    ),
    Post(
        post_id='201905081028410061', title='欧盟外长：国际联络小组呼吁不要企图使用武力解决委内瑞拉问题',
        link='http://sputniknews.cn/politics/201905081028410061/',
        guid='http://sputniknews.cn/politics/201905081028410061/', pub_date=datetime.datetime(2019, 5, 8, 5, 59
                                                                                              ),
        description='欧盟外交与安全政策高级代表莫盖里尼7日在哥斯达黎加举行的委内瑞拉问题国际联络小组会议结束后表示，该联络小组呼吁避免企图武力解决委内瑞拉局势。', category='政治',
        enclosure='http://cdn3.img.sputniknews.cn/images/102640/45/1026404581.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>欧盟外长：国际联络小组呼吁不要企图使用武力解决委内瑞拉问题</title><link>http://sputniknews.cn/politics/201905081028410061/</link><guid>http://sputniknews.cn/politics/201905081028410061/</guid><ns0:related><ns0:url>http://sputniknews.cn/politics/201905011028359869/</ns0:url><ns0:url>http://sputniknews.cn/russia/201905041028378430/</ns0:url></ns0:related><ns0:priority>2</ns0:priority><pubDate>Wed, 08 May 2019 05:59:00 +0800</pubDate><description>俄罗斯卫星通讯社布鲁塞尔电 欧盟外交与安全政策高级代表莫盖里尼7日在哥斯达黎加举行的委内瑞拉问题国际联络小组会议结束后表示，该联络小组呼吁避免企图武力解决委内瑞拉局势。</description><ns0:type>article</ns0:type><category>政治</category><enclosure length="102338" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102640/45/1026404581.jpg" /></item>',
        short_link='http://sptnkne.ws/mwcP'
    ),
    Post(
        post_id='201905081028409578', title='第一滴血：饥饿的熊猎食俄罗斯人', link='http://sputniknews.cn/russia/201905081028409578/',
        guid='http://sputniknews.cn/russia/201905081028409578/', pub_date=datetime.datetime(2019, 5, 8, 2, 26
                                                                                            ),
        description='在俄罗斯的勘察加半岛，发生了这个季节以来的第一起熊攻击人事件。一个和朋友一起去捕鱼的当地居民死在熊掌之下。调查发现，此后，猎人们追踪了这只熊，并将其击毙。', category='俄罗斯',
        enclosure='http://cdn3.img.sputniknews.cn/images/101335/40/1013354036.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>第一滴血：饥饿的熊猎食俄罗斯人</title><link>http://sputniknews.cn/russia/201905081028409578/</link><guid>http://sputniknews.cn/russia/201905081028409578/</guid><ns0:related><ns0:url>http://sputniknews.cn/videoclub/201806081025606205/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Wed, 08 May 2019 02:26:00 +0800</pubDate><description>在俄罗斯的勘察加半岛，发生了这个季节以来的第一起熊攻击人事件。一个和朋友一起去捕鱼的当地居民死在熊掌之下。调查发现，此后，猎人们追踪了这只熊，并将其击毙。</description><ns0:type>article</ns0:type><category>俄罗斯</category><enclosure length="92827" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/101335/40/1013354036.jpg" /></item>',
        short_link='http://sptnkne.ws/mvZb'
    ),
    Post(
        post_id='201905071028407388', title='俄外长：有人说CNN做“假新闻”，现在你们还提假问题',
        link='http://sputniknews.cn/russia/201905071028407388/',
        guid='http://sputniknews.cn/russia/201905071028407388/', pub_date=datetime.datetime(2019, 5, 7, 19, 46
                                                                                            ),
        description='环球网援引“今日俄罗斯”(RT)报道，6日，俄罗斯外长拉夫罗夫出席在芬兰举行的北极理事会期间，与美国国务卿蓬佩奥会面，并召开了简短记者会。', category='俄罗斯',
        enclosure='http://cdn3.img.sputniknews.cn/images/102815/03/1028150353.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>俄外长：有人说CNN做“假新闻”，现在你们还提假问题</title><link>http://sputniknews.cn/russia/201905071028407388/</link><guid>http://sputniknews.cn/russia/201905071028407388/</guid><ns0:related><ns0:url>http://sputniknews.cn/politics/201901071027293801/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 19:46:00 +0800</pubDate><description>环球网援引“今日俄罗斯”(RT)报道，6日，俄罗斯外长拉夫罗夫出席在芬兰举行的北极理事会期间，与美国国务卿蓬佩奥会面，并召开了简短记者会。</description><ns0:type>article</ns0:type><category>俄罗斯</category><enclosure length="54564" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102815/03/1028150353.jpg" /></item>',
    ),
    Post(
        post_id='201905071028400051', title='20家中国公司和组织将参加阿穆尔国际展会论坛',
        link='http://sputniknews.cn/economics/201905071028400051/',
        guid='http://sputniknews.cn/economics/201905071028400051/', pub_date=datetime.datetime(2019, 5, 7, 7, 44
                                                                                               ),
        description='据俄罗斯阿穆尔国际展会论坛（AmurExpoForum-2019）组织者对卫星通讯社表示，20家中国公司、组织和政府机构将参加该论坛。', category='经济',
        enclosure='http://cdn3.img.sputniknews.cn/images/101557/74/1015577419.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>20家中国公司和组织将参加阿穆尔国际展会论坛</title><link>http://sputniknews.cn/economics/201905071028400051/</link><guid>http://sputniknews.cn/economics/201905071028400051/</guid><ns0:related><ns0:url>http://sputniknews.cn/russia_china_relations/201903231027997011/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 07:44:00 +0800</pubDate><description>俄罗斯卫星通讯社莫斯科5月7日电 据俄罗斯阿穆尔国际展会论坛（AmurExpoForum-2019）组织者对卫星通讯社表示，20家中国公司、组织和政府机构将参加该论坛。</description><ns0:type>article</ns0:type><category>经济</category><enclosure length="116726" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/101557/74/1015577419.jpg" /></item>',
        short_link='http://sptnkne.ws/mvBd'
    ),
    Post(
        post_id='201905071028400731', title='华媒：辽宁省禁止电子产品进入学校', link='http://sputniknews.cn/china/201905071028400731/',
        guid='http://sputniknews.cn/china/201905071028400731/', pub_date=datetime.datetime(2019, 5, 7, 10, 7, 26
                                                                                           ),
        description='据沈阳晚报消息，辽宁省教育厅等九部门印发《辽宁省落实教育部等九部门关于中小学生减负措施实施方案》，规定所有公办、民办义务教育学校都要严格遵守义务教育免试入学规定。', category='中国',
        enclosure='http://cdn3.img.sputniknews.cn/images/102757/08/1027570884.jpg',
        text='<item xmlns:ns0="https://sputniknews.com"><title>华媒：辽宁省禁止电子产品进入学校</title><link>http://sputniknews.cn/china/201905071028400731/</link><guid>http://sputniknews.cn/china/201905071028400731/</guid><ns0:related><ns0:url>http://sputniknews.cn/opinion/201805291025514904/</ns0:url><ns0:url>http://sputniknews.cn/china/201903061027855706/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 10:07:26 +0800</pubDate><description>据沈阳晚报消息，辽宁省教育厅等九部门印发《辽宁省落实教育部等九部门关于中小学生减负措施实施方案》，规定所有公办、民办义务教育学校都要严格遵守义务教育免试入学规定。</description><ns0:type>article</ns0:type><category>中国</category><enclosure length="98301" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102757/08/1027570884.jpg" /></item>',
        short_link='http://sptnkne.ws/mvBV'
    ),
]


@patch('sputnik.clients.sputnik.SputnikService.get_post', return_value=POST_LIST)
@patch('sputnik.clients.sputnik.SputnikService.get_short_link', return_value='http://sptnkne.ws/mvPO')
async def test_update_post(_mock_get_post, _mock_get_short_link, cli):
    await DataBase.gino.create_all()

    await PostModel.create(
        **{
            'guid': 'http://sputniknews.cn/china/201905071028400731/',
            'category': '中国',
            'description': '据沈阳晚报消息，辽宁省教育厅等九部门印发《辽宁省落实教育部等九部门关于中小学生减负措施实施方案》，规定所有公办、民办义务教育学校都要严格遵守义务教育免试入学规定。',
            'link': 'http://sputniknews.cn/china/201905071028400731/',
            'post_id': '201905071028400731',
            'pub_date': datetime.datetime(2019, 5, 7, 10, 7, 26),
            'text': '<item xmlns:ns0="https://sputniknews.com"><title>华媒：辽宁省禁止电子产品进入学校</title><link>http://sputniknews.cn/china/201905071028400731/</link><guid>http://sputniknews.cn/china/201905071028400731/</guid><ns0:related><ns0:url>http://sputniknews.cn/opinion/201805291025514904/</ns0:url><ns0:url>http://sputniknews.cn/china/201903061027855706/</ns0:url></ns0:related><ns0:priority>3</ns0:priority><pubDate>Tue, 07 May 2019 10:07:26 +0800</pubDate><description>据沈阳晚报消息，辽宁省教育厅等九部门印发《辽宁省落实教育部等九部门关于中小学生减负措施实施方案》，规定所有公办、民办义务教育学校都要严格遵守义务教育免试入学规定。</description><ns0:type>article</ns0:type><category>中国</category><enclosure length="98301" type="image/jpeg" url="http://cdn3.img.sputniknews.cn/images/102757/08/1027570884.jpg" /></item>',
            'title': '华媒：辽宁省禁止电子产品进入学校'
        }
    )

    await update_post()

    await DataBase.gino.drop_all()
