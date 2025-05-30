#!/usr/bin/env python
"""
微信公众号发布API使用示例

这个文件展示了如何使用API接口发布文章到微信公众号
"""

import requests
import json
import time
from typing import Optional

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

class WeChatPublishAPI:
    """微信公众号发布API客户端"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    def get_templates(self) -> dict:
        """获取模板列表"""
        response = self.session.get(f"{self.base_url}/templates")
        return response.json()
    
    def get_template_content(self, template_id: str) -> dict:
        """获取模板内容"""
        response = self.session.get(f"{self.base_url}/templates/{template_id}")
        return response.json()
    
    def get_wechat_config(self) -> dict:
        """获取微信配置信息"""
        response = self.session.get(f"{self.base_url}/config/wechat")
        return response.json()
    
    def publish_article(
        self,
        content: str,
        template_id: Optional[str] = None,
        title: Optional[str] = None,
        digest: Optional[str] = None,
        author: Optional[str] = None,
        appid: Optional[str] = None,
        appsecret: Optional[str] = None
    ) -> dict:
        """发布文章（同步）"""
        data = {
            "content": content,
            "template_id": template_id,
            "title": title,
            "digest": digest,
            "author": author,
            "appid": appid,
            "appsecret": appsecret
        }
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        response = self.session.post(
            f"{self.base_url}/publish",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def publish_article_async(
        self,
        content: str,
        template_id: Optional[str] = None,
        title: Optional[str] = None,
        digest: Optional[str] = None,
        author: Optional[str] = None,
        appid: Optional[str] = None,
        appsecret: Optional[str] = None
    ) -> dict:
        """发布文章（异步）"""
        data = {
            "content": content,
            "template_id": template_id,
            "title": title,
            "digest": digest,
            "author": author,
            "appid": appid,
            "appsecret": appsecret
        }
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        response = self.session.post(
            f"{self.base_url}/publish-async",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        return response.json()


def example_1_basic_publish():
    """示例1: 基础文章发布"""
    print("=" * 50)
    print("示例1: 基础文章发布")
    print("=" * 50)
    
    api = WeChatPublishAPI()
    
    # 检查API健康状态
    health = api.health_check()
    print(f"API健康状态: {health}")
    
    if health.get("status") != "healthy":
        print("❌ API服务不健康，请检查配置")
        return
    
    # 准备文章内容
    article_content = """
    <h1>AI技术发展趋势</h1>
    <p>人工智能技术正在快速发展，为各行各业带来革命性的变化。</p>
    <h2>主要发展方向</h2>
    <ul>
        <li>大语言模型的突破</li>
        <li>多模态AI的兴起</li>
        <li>AI在垂直领域的应用</li>
    </ul>
    <p>未来，AI将更加智能化、人性化，为人类创造更大的价值。</p>
    """
    
    # 发布文章
    try:
        result = api.publish_article(
            content=article_content,
            title="AI技术发展趋势分析",
            digest="探讨人工智能技术的最新发展趋势和未来展望",
            author="AI研究员"
        )
        
        print(f"发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("status") == "success":
            print("✅ 文章发布成功！")
            if result.get("article_url"):
                print(f"📖 文章链接: {result['article_url']}")
        else:
            print(f"❌ 文章发布失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 发布过程中出错: {str(e)}")


def example_2_template_publish():
    """示例2: 使用模板发布文章"""
    print("=" * 50)
    print("示例2: 使用模板发布文章")
    print("=" * 50)
    
    api = WeChatPublishAPI()
    
    # 获取可用模板
    # templates = api.get_templates()
    # print(f"可用模板: {json.dumps(templates, ensure_ascii=False, indent=2)}")
    
    # if templates.get("total", 0) == 0:
    #     print("❌ 没有可用的模板")
    #     return
    
    # # 选择第一个模板
    # template_id = templates["templates"][0]["id"]
    # print(f"选择模板: {template_id}")
    
    # 准备文章内容
    article_content = """
    <div class="_18p7x" data-testid="article"><div class="dpu8C _2kCxD  "><!--30--><!--30--><!--29--><!--31--><!--32--><!--33--><!--34--><!--35--><!--36--><!--37--><!--38--><!--39--><!--40--><!--41--><p style="margin-top: 0px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none"><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">《OpenAI最新模型实测：普通人如何用ChatGPT月入5位数？》</strong></p></div><div class="dpu8C _2kCxD  "><!--43--><!--43--><!--42--><!--44--><!--45--><!--46--><!--47--><!--48--><!--49--><!--50--><!--51--><!--52--><!--53--><!--54--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">当杭州的跨境电商卖家小林用GPT-5生成商品描述时，单日销售额突破2万元；北京的自由撰稿人阿杰通过AI辅助写作，连续3个月稿费破5万——这些真实案例背后，藏着普通人用AI创收的「财富密码」。但真相远比想象中复杂：有人用AI月入3万却因版权纠纷被告，有人投入万元买课最终血本无归。当OpenAI最新模型开启「创作民主化」时代，普通人究竟该如何驾驭这匹技术野马？</p></div><div class="_3hMwG _2kCxD  "><!--55--><!--56--><div class="_1NCGf"><img src="https://pics1.baidu.com/feed/023b5bb5c9ea15cee8d6b90e9387d3fc3a87b210.jpeg@f_auto?token=879fc9c62f0f1f4a5f2f0d06363a6ecc" width="1242" class="_1g4Ex _1i_Oe "><!--59--></div><!--57--><!--60--><!--61--><!--62--><!--63--><!--64--><!--65--><!--66--><!--67--><!--68--></div><div class="dpu8C _2kCxD  "><!--70--><!--70--><!--69--><!--71--><!--72--><!--73--><!--74--><!--75--><!--76--><!--77--><!--78--><!--79--><!--80--><!--81--><span class="bjh-a" data-bjh-src="https://m.baidu.com/s?word=%23%E5%A4%8F%E5%AD%A3%E5%9B%BE%E6%96%87%E6%BF%80%E5%8A%B1%E8%AE%A1%E5%88%92%23&amp;topic_id=174556224219837241&amp;sa=edit&amp;sfrom=1023524a&amp;append=1&amp;newwindow=0&amp;upqrade=1" data-bjh-type="topic" data-bjh-id="174556224219837241" data-bjh-cover="">#夏季图文激励计划#</span></div><div class="dpu8C _2kCxD  "><!--83--><!--83--><!--82--><!--84--><!--85--><!--86--><!--87--><!--88--><!--89--><!--90--><!--91--><!--92--><!--93--><!--94--><h3>一、技术解码：GPT-5的「钞能力」究竟在哪？</h3></div><div class="dpu8C _2kCxD  "><!--96--><!--96--><!--95--><!--97--><!--98--><!--99--><!--100--><!--101--><!--102--><!--103--><!--104--><!--105--><!--106--><!--107--><h3>1. 从「工具」到「合伙人」的质变</h3></div><div class="dpu8C _2kCxD  "><!--109--><!--109--><!--108--><!--110--><!--111--><!--112--><!--113--><!--114--><!--115--><!--116--><!--117--><!--118--><!--119--><!--120--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">GPT-5新增的「多模态商业引擎」，能同时处理文本、图像、视频内容。某MCN机构实测显示，用GPT-5生成短视频脚本+配乐建议，单条视频制作成本从800元降至120元，完播率提升47%。更惊人的是其「商业嗅觉」：输入产品参数后，模型能自动生成适配TikTok、Instagram等平台的营销方案。</p></div><div class="dpu8C _2kCxD  "><!--122--><!--122--><!--121--><!--123--><!--124--><!--125--><!--126--><!--127--><!--128--><!--129--><!--130--><!--131--><!--132--><!--133--><h3>2. 数据标注的「黄金矿脉」</h3></div><div class="dpu8C _2kCxD  "><!--135--><!--135--><!--134--><!--136--><!--137--><!--138--><!--139--><!--140--><!--141--><!--142--><!--143--><!--144--><!--145--><!--146--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">OpenAI官方推出的「DataPro」接口，允许用户通过AI清洗、标注数据集。深圳某AI训练师透露：“用GPT-5标注跨境电商评论数据，准确率比人工高23%，日薪可达800元。”但暗藏陷阱：未经清洗的指令可能导致AI生成歧视性内容，某卖家因此损失12万美元广告费。</p></div><div class="dpu8C _2kCxD  "><!--148--><!--148--><!--147--><!--149--><!--150--><!--151--><!--152--><!--153--><!--154--><!--155--><!--156--><!--157--><!--158--><!--159--><h3>3. 代码生成的「降维打击」</h3></div><div class="dpu8C _2kCxD  "><!--161--><!--161--><!--160--><!--162--><!--163--><!--164--><!--165--><!--166--><!--167--><!--168--><!--169--><!--170--><!--171--><!--172--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">GPT-5的「Copilot Pro」功能，能根据自然语言描述生成完整项目代码。杭州某初创公司用其开发企业管理系统，开发周期从6个月压缩至17天，节省成本45万元。但代码版权争议随之而来：某开发者因直接商用GPT生成的代码被告侵权。</p></div><div class="dpu8C _2kCxD  "><!--174--><!--174--><!--173--><!--175--><!--176--><!--177--><!--178--><!--179--><!--180--><!--181--><!--182--><!--183--><!--184--><!--185--><h3>二、实战策略：四个「合法变现」赛道深度拆解</h3></div><div class="dpu8C _2kCxD  "><!--187--><!--187--><!--186--><!--188--><!--189--><!--190--><!--191--><!--192--><!--193--><!--194--><!--195--><!--196--><!--197--><!--198--><h3>1. 跨境电商的「内容核弹」</h3></div><div class="dpu8C _2kCxD  "><!--200--><!--200--><!--199--><!--201--><!--202--><!--203--><!--204--><!--205--><!--206--><!--207--><!--208--><!--209--><!--210--><!--211--><ul style="list-style-type: disc" class=" list-paddingleft-2"><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">选品文案</strong><span>：输入产品特征，GPT-5可生成适配不同国家的广告文案。某卖家用其优化亚马逊Listing，转化率提升39%。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">客服自动化</strong><span>：训练专属AI客服，处理60%的常规咨询。需注意：需定期校准模型，避免文化误解（如将“白色”误译为“葬礼色”）。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">案例</strong><span>：义乌小商品卖家通过GPT生成多语言产品页，月均广告费节省1.2万美元。</span></p></li></ul></div><div class="dpu8C _2kCxD  "><!--213--><!--213--><!--212--><!--214--><!--215--><!--216--><!--217--><!--218--><!--219--><!--220--><!--221--><!--222--><!--223--><!--224--><h3>2. 知识付费的「杠杆效应」</h3></div><div class="dpu8C _2kCxD  "><!--226--><!--226--><!--225--><!--227--><!--228--><!--229--><!--230--><!--231--><!--232--><!--233--><!--234--><!--235--><!--236--><!--237--><ul style="list-style-type: disc" class=" list-paddingleft-2"><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">课程开发</strong><span>：用GPT-5生成课程大纲、案例库。某职场导师用其制作《AI营销课》，售价299元，销量破万份。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">自媒体矩阵</strong><span>：批量生成知乎/公众号爆文。需警惕：过度依赖AI易触发平台原创检测。某账号因AI内容占比超70%被封禁。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">数据</strong><span>：优质AI+人工润色的内容，完读率比纯AI高31%，粉丝互动量提升58%。</span></p></li></ul></div><div class="dpu8C _2kCxD  "><!--239--><!--239--><!--238--><!--240--><!--241--><!--242--><!--243--><!--244--><!--245--><!--246--><!--247--><!--248--><!--249--><!--250--><h3>3. 本地服务的「智能升级」</h3></div><div class="dpu8C _2kCxD  "><!--252--><!--252--><!--251--><!--253--><!--254--><!--255--><!--256--><!--257--><!--258--><!--259--><!--260--><!--261--><!--262--><!--263--><ul style="list-style-type: disc" class=" list-paddingleft-2"><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">餐饮行业</strong><span>：生成个性化菜单、自动接单系统。成都某火锅店用GPT设计套餐，客单价提升22%。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">教育培训</strong><span>：自动生成题库、作文批改。某K12机构用其节省教师60%的作业批改时间。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">风险提示</strong><span>：医疗、法律等专业领域需谨慎，某牙科诊所因AI误诊建议被起诉。</span></p></li></ul></div><div class="dpu8C _2kCxD  "><!--265--><!--265--><!--264--><!--266--><!--267--><!--268--><!--269--><!--270--><!--271--><!--272--><!--273--><!--274--><!--275--><!--276--><h3>4. 数字艺术的「版权蓝海」</h3></div><div class="dpu8C _2kCxD  "><!--278--><!--278--><!--277--><!--279--><!--280--><!--281--><!--282--><!--283--><!--284--><!--285--><!--286--><!--287--><!--288--><!--289--><ul style="list-style-type: disc" class=" list-paddingleft-2"><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">NFT创作</strong><span>：用GPT生成故事背景，Midjourney生成图像。某数字艺术家靠AI作品月入4.5万美元。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">品牌IP设计</strong><span>：快速生成吉祥物、slogan。需注意：需二次创作规避版权风险。某茶饮品牌因直接使用AI设计logo被判赔偿12万元。</span></p></li><li><p><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">新趋势</strong><span>：AI生成游戏MOD（模组）已形成地下交易市场，单日交易额超百万。</span></p></li></ul></div><div class="dpu8C _2kCxD  "><!--291--><!--291--><!--290--><!--292--><!--293--><!--294--><!--295--><!--296--><!--297--><!--298--><!--299--><!--300--><!--301--><!--302--><h3>三、暗礁预警：普通人踩过的「AI创富陷阱」</h3></div><div class="dpu8C _2kCxD  "><!--304--><!--304--><!--303--><!--305--><!--306--><!--307--><!--308--><!--309--><!--310--><!--311--><!--312--><!--313--><!--314--><!--315--><h3>1. 算力通胀：免费午餐的终结</h3></div><div class="dpu8C _2kCxD  "><!--317--><!--317--><!--316--><!--318--><!--319--><!--320--><!--321--><!--322--><!--323--><!--324--><!--325--><!--326--><!--327--><!--328--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">早期用户能用GPT-3.5免费生成内容，但GPT-5企业版API价格已达$0.01/千token。某自媒体团队算过账：日均生成5000字内容，月成本高达1.8万元，压缩了利润空间。</p></div><div class="dpu8C _2kCxD  "><!--330--><!--330--><!--329--><!--331--><!--332--><!--333--><!--334--><!--335--><!--336--><!--337--><!--338--><!--339--><!--340--><!--341--><h3>2. 模型幻觉：AI的「善意谎言」</h3></div><div class="dpu8C _2kCxD  "><!--343--><!--343--><!--342--><!--344--><!--345--><!--346--><!--347--><!--348--><!--349--><!--350--><!--351--><!--352--><!--353--><!--354--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">GPT-5仍会编造虚假数据。某跨境电商卖家按AI建议的「爆款包装」生产，结果因材质虚假宣传被罚8万元。更危险的是金融领域：某散户根据AI分析买入股票，亏损超50万元。</p></div><div class="dpu8C _2kCxD  "><!--356--><!--356--><!--355--><!--357--><!--358--><!--359--><!--360--><!--361--><!--362--><!--363--><!--364--><!--365--><!--366--><!--367--><h3>3. 职业空心化：被替代的「中间商」</h3></div><div class="dpu8C _2kCxD  "><!--369--><!--369--><!--368--><!--370--><!--371--><!--372--><!--373--><!--374--><!--375--><!--376--><!--377--><!--378--><!--379--><!--380--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">传统内容中介（如营销公司、代运营）正被AI取代。某4A公司裁员30%，原因正是客户转向使用AI生成工具。但新的职业机会涌现：AI训练师、数据标注师等岗位需求激增200%。</p></div><div class="dpu8C _2kCxD  "><!--382--><!--382--><!--381--><!--383--><!--384--><!--385--><!--386--><!--387--><!--388--><!--389--><!--390--><!--391--><!--392--><!--393--><h3>四、未来战场：普通人如何构建「AI护城河」？</h3></div><div class="dpu8C _2kCxD  "><!--395--><!--395--><!--394--><!--396--><!--397--><!--398--><!--399--><!--400--><!--401--><!--402--><!--403--><!--404--><!--405--><!--406--><h3>1. 垂直领域的「数据壁垒」</h3></div><div class="dpu8C _2kCxD  "><!--408--><!--408--><!--407--><!--409--><!--410--><!--411--><!--412--><!--413--><!--414--><!--415--><!--416--><!--417--><!--418--><!--419--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">在细分领域（如宠物殡葬、汉服定制）积累独家数据，训练专属模型。某宠物博主用自家猫咪照片训练AI，生成的内容转化率比通用模型高41%。</p></div><div class="dpu8C _2kCxD  "><!--421--><!--421--><!--420--><!--422--><!--423--><!--424--><!--425--><!--426--><!--427--><!--428--><!--429--><!--430--><!--431--><!--432--><h3>2. 人机协作的「混合智能」</h3></div><div class="dpu8C _2kCxD  "><!--434--><!--434--><!--433--><!--435--><!--436--><!--437--><!--438--><!--439--><!--440--><!--441--><!--442--><!--443--><!--444--><!--445--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none">日本某设计团队采用「AI初稿+人工迭代」模式，作品获奖率提升60%。关键在于：将AI作为「创意外脑」，专注人类擅长的策略思考。</p></div><div class="dpu8C _2kCxD  "><!--447--><!--447--><!--446--><!--448--><!--449--><!--450--><!--451--><!--452--><!--453--><!--454--><!--455--><!--456--><!--457--><!--458--><h3>3. 法律合规的「免疫系统」</h3></div><div class="dpu8C _2kCxD  "><!--460--><!--460--><!--459--><!--461--><!--462--><!--463--><!--464--><!--465--><!--466--><!--467--><!--468--><!--469--><!--470--><!--471--><ul style="list-style-type: disc" class=" list-paddingleft-2"><li><p>注册AI生成内容的版权</p></li><li><p>在内容中标注「AI辅助」</p></li><li><p>购买商业保险应对侵权风险<br>某MCN机构因合规措施完善，AI内容收益是行业平均值的3倍。</p></li></ul></div><div class="dpu8C _2kCxD  "><!--473--><!--473--><!--472--><!--474--><!--475--><!--476--><!--477--><!--478--><!--479--><!--480--><!--481--><!--482--><!--483--><!--484--><p style="margin-top: 8px;border: 0px;vertical-align: baseline;word-break: break-word;word-wrap: break-word;overflow-wrap: break-word;caret-color: rgba(0, 0, 0, 0.9);color: rgba(0, 0, 0, 0.9);orphans: auto;text-indent: 0px;text-transform: none;white-space: normal;widows: auto;word-spacing: 0px;-webkit-text-size-adjust: auto;-webkit-text-stroke-width: 0px;text-decoration: none"><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">结语</strong><span>：当GPT-5打开「人人皆可创作」的潘多拉魔盒，普通人面对的不是财富自由捷径，而是一场认知升级的硬仗。真正的「月入5位数」，不在于AI有多智能，而在于你能否在技术狂潮中守住这三条底线：</span><strong style="margin: 0px;padding: 0px;border: 0px;vertical-align: baseline">用AI放大独特价值，用法律守护创作成果，用人性温度对抗算法冰冷</strong><span>。毕竟，在AI统治的内容世界里，能让人类脱颖而出的，永远是那些机器永远学不会的「非标品」——比如对痛点的深刻共情，对趋势的敏锐直觉，以及对商业本质的透彻理解。</span></p></div><!--28--><!--485--><!--486--><div class="_3hMwG"><div class="_26vAC _3Q1DN"></div></div></div>
    """
    
    # 使用模板发布文章
    try:
        result = api.publish_article(
            content=article_content,
            template_id="template9"
        )
        
        print(f"发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("status") == "success":
            print("✅ 使用模板发布文章成功！")
        else:
            print(f"❌ 发布失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 发布过程中出错: {str(e)}")


def example_3_async_publish():
    """示例3: 异步发布文章"""
    print("=" * 50)
    print("示例3: 异步发布文章")
    print("=" * 50)
    
    api = WeChatPublishAPI()
    
    # 准备文章内容
    article_content = """
    <h1>异步发布测试文章</h1>
    <p>这是一篇用于测试异步发布功能的文章。</p>
    <p>异步发布可以避免长时间等待，提高用户体验。</p>
    """
    
    # 异步发布文章
    try:
        result = api.publish_article_async(
            content=article_content,
            title="异步发布测试",
            digest="测试异步发布功能的文章",
            author="测试员"
        )
        
        print(f"异步发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("status") == "processing":
            task_id = result.get("task_id")
            print(f"✅ 文章已提交异步发布，任务ID: {task_id}")
            print("📝 请查看日志了解发布进度")
        else:
            print(f"❌ 提交异步任务失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 异步发布过程中出错: {str(e)}")


def example_4_custom_wechat_config():
    """示例4: 使用自定义微信配置发布"""
    print("=" * 50)
    print("示例4: 使用自定义微信配置发布")
    print("=" * 50)
    
    api = WeChatPublishAPI()
    
    # 获取当前微信配置
    wechat_config = api.get_wechat_config()
    print(f"当前微信配置: {json.dumps(wechat_config, ensure_ascii=False, indent=2)}")
    
    # 准备文章内容
    article_content = """
    <h1>自定义配置发布测试</h1>
    <p>这篇文章使用自定义的微信公众号配置进行发布。</p>
    <p>可以指定特定的AppID和AppSecret来发布到不同的公众号。</p>
    """
    
    # 注意：这里需要替换为实际的微信公众号配置
    # 在实际使用中，请确保AppID和AppSecret是有效的
    custom_appid = "your_custom_appid"
    custom_appsecret = "your_custom_appsecret"
    
    print("⚠️  注意：此示例需要有效的微信公众号配置才能成功")
    print("请在实际使用时替换为真实的AppID和AppSecret")
    
    # 使用自定义配置发布（仅作演示，实际需要有效配置）
    # try:
    #     result = api.publish_article(
    #         content=article_content,
    #         title="自定义配置发布测试",
    #         digest="使用自定义微信配置发布的测试文章",
    #         author="配置测试员",
    #         appid=custom_appid,
    #         appsecret=custom_appsecret
    #     )
    #     
    #     print(f"发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    # except Exception as e:
    #     print(f"❌ 发布过程中出错: {str(e)}")


def main():
    """运行所有示例"""
    print("🚀 微信公众号发布API使用示例")
    print("请确保API服务器已启动 (python api_server.py)")
    print()
    
    try:
        # 运行示例
        # example_1_basic_publish()
        # time.sleep(2)
        
        example_2_template_publish()
        # time.sleep(2)
        
        # example_3_async_publish()
        # time.sleep(2)
        
        # example_4_custom_wechat_config()
        
    except KeyboardInterrupt:
        print("\n👋 示例运行被用户中断")
    except Exception as e:
        print(f"\n❌ 运行示例时出错: {str(e)}")
    
    print("\n✨ 示例运行完成")


if __name__ == "__main__":
    main()