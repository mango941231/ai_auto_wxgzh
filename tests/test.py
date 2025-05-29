# test.py

import sys
import os

# 获取当前文件（b.py）的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 找到项目根目录（即 A 和 B 的父目录）
project_root = os.path.dirname(current_dir)
# 将根目录添加到 Python 搜索路径
sys.path.append(project_root)

from src.ai_auto_wxgzh.utils import log  # noqa 402
from src.ai_auto_wxgzh.utils import utils  # noqa 402
from src.ai_auto_wxgzh.tools.wx_publisher import WeixinPublisher  # noqa 402
from src.ai_auto_wxgzh.config.config import Config  # noqa 402

article = """<div class="article-content"><h1>已收7005万亩！全国“三夏”大规模小麦机收全面展开</h1><div class="article-meta"><span>2025-05-27 06:58</span><span class="dot">·</span><span class="name"><a>人民日报</a></span></div><div><article class="syl-article-base syl-page-article tt-article-content syl-device-pc"><p><strong>原标题：全国“三夏”大规模小麦机收全面展开</strong></p><img src="https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/d93af2b98cd44e09bb73e0d8cb3ecdbc~tplv-tt-origin-web:gif.jpeg?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1748940620&x-signature=hii5TvIlhDy7nBsISrVp09XoDVI%3D" img_width="400" img_height="450" image_type="1" mime_type="image/jpeg" web_uri="tos-cn-i-tjoges91tu/d247dfca652bd452c27fc50e54b30f4f" class="syl-page-img" style="height: auto;" data-src="https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/d93af2b98cd44e09bb73e0d8cb3ecdbc~tplv-tt-origin-web:gif.jpeg?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1748940620&x-signature=hii5TvIlhDy7nBsISrVp09XoDVI%3D"><p>夏收来临，江苏省宿迁市泗洪县各地抢抓农时，机械化减损抢收，确保应收尽收。图为5月24日，泗洪县重岗街道林场社区的麦田里，农户抓住晴好天气，驾驶收割机抢收小麦。周 鹏摄（影像中国）</p><p>记者从农业农村部获悉：截至5月26日17时，各地已收夏粮小麦7005万亩，日机收面积连续3天超过400万亩，全国“三夏”大规模小麦机收全面展开。当前麦收进度已近两成，其中西南地区及湖北麦收进入尾声，河南进度过三成，安徽、江苏等地已开收。</p><p>据调度，今年“三夏”全国将投入各类农机具超1700万台（套），压茬推进夏收、夏种和夏管机械化作业。其中联合收割机80多万台、参与跨区作业的超20万台，能够满足夏收正常作业需求。每秒9—10公斤大喂入量联合收割机已成为跨区作业主流机型，配备北斗定位、作业监测等功能的智能化联合收割机更多投入生产一线，将为机收快速高效推进提供有力支撑。</p><p>农业农村部联合交通运输、公安、气象、石油石化等部门单位共同加强农机作业服务保障。目前，麦收重点省份已设立跨区作业接待服务站3400多个，在高速公路收费站开通农机绿色通道4800多个，对跨区农机进一步简化核验程序、一律快速免费放行；组织设立农机优先优惠加油通道5800多个，全域加力开展“送油下乡”和“送油到田”服务，全力保障作业用油供给。</p><p>为切实强化农机应急救灾能力，有效应对强降雨、连阴雨等不利天气影响，农业农村部加强组织动员，指导麦收省份提前制定农机应急工作预案，签订区域互助合作协议，及时组织开展抢收抢烘作业。目前，麦收重点省份已建设区域农机社会化服务中心3900多家、区域农业应急救灾中心2020多家、常态化农机应急作业服务队6900多支。5月22日，河南、湖北等地发生大范围强降雨天气，当地农业农村部门积极组织开展雨前抢收，采取人歇机不歇等方式连续作战，24小时内机收超800万亩。</p><p>(来源:人民日报)</p></article></div></div>"""


def pub2wx(article):
    config = Config.get_instance()
    if not config.load_config():
        log.print_log("加载配置失败，请检查是否有配置！")
        return
    elif not config.validate_config():
        log.print_log(f"配置填写有错误：{config.error_message}")
        return

    try:
        title, digest = utils.extract_html(article)
    except Exception as e:
        return f"从文章中提取标题、摘要信息出错: {e}", article
    if title is None:
        return "无法提取文章标题，请检查文章是否成功生成？", article

    publisher = WeixinPublisher(
        config.wechat_credentials[0]["appid"],
        config.wechat_credentials[0]["appsecret"],
        config.wechat_credentials[0]["author"],
    )

    image_url = publisher.generate_img(
        "主题：" + title.split("|")[-1] + "，内容：" + digest,
        "900*384",
    )

    if image_url is None:
        log.print_log("生成图片出错，使用默认图片")

    # 封面图片
    media_id, _, err_msg = publisher.upload_image(image_url)
    if media_id is None:
        return f"封面{err_msg}，无法发布文章", article

    # 这里需要将文章中的图片url替换为上传到微信返回的图片url
    try:
        image_urls = utils.extract_image_urls(article)
        for image_url in image_urls:
            local_filename = utils.download_and_save_image(
                image_url,
                utils.get_current_dir("image"),
            )
            if local_filename:
                _, url, _ = publisher.upload_image(local_filename)
                article = article.replace(image_url, url)
    except Exception as e:
        log.print_log(f"上传配图出错，影响阅读，可继续发布文章:{e}")

    add_draft_result, err_msg = publisher.add_draft(article, title, digest, media_id)
    if add_draft_result is None:
        # 添加草稿失败，不再继续执行
        return f"{err_msg}，无法发布文章", article

    publish_result, err_msg = publisher.publish(add_draft_result.publishId)
    if publish_result is None:
        return f"{err_msg}，无法继续发布文章", article

    article_url = publisher.poll_article_url(publish_result.publishId)
    if article_url is not None:
        # 该接口需要认证，将文章添加到菜单中去，用户可以通过菜单“最新文章”获取到
        ret = publisher.create_menu(article_url)
        if not ret:
            log.print_log(f"{ret}（公众号未认证，发布已成功）")
    else:
        log.print_log("无法获取到文章URL，无法创建菜单（可忽略，发布已成功）")

    # 只有下面执行成功，文章才会显示到公众号列表，否则只能通过后台复制链接分享访问
    # 通过群发使得文章显示到公众号列表 ——> 该接口需要认证
    ret, media_id = publisher.media_uploadnews(article, title, digest, media_id)
    if media_id is None:
        return f"{ret}，无法显示到公众号文章列表（公众号未认证，发布已成功）", article

    ret = publisher.message_mass_sendall(media_id)
    if ret is not None:
        return (
            f"{ret}，无法显示到公众号文章列表（公众号未认证，发布已成功）",
            article,
        )

    return "成功发布文章到微信公众号", article


# 测试直接发布文章
log.print_log(pub2wx(article))
# log.print_log(utils.decompress_html(article))
# log.print_log(utils.extract_html(article))
