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
    <div class="_18p7x" data-testid="article"><div class="_3hMwG _2kCxD  "><!--29--><!--30--><div class="_1NCGf"><img src="https://pics4.baidu.com/feed/bba1cd11728b4710803eb211e8942af2fd032347.jpeg@f_auto?token=03e0e238229cdcdff72a3765cba6f6c4" width="1242" class="_1g4Ex _1i_Oe "><!--33--></div><!--31--><!--34--><!--35--><!--36--><!--37--><!--38--><!--39--><!--40--><!--41--><!--42--></div><div class="dpu8C _2kCxD  "><!--44--><!--44--><!--43--><!--45--><!--46--><!--47--><!--48--><!--49--><!--50--><!--51--><!--52--><!--53--><!--54--><!--55--><p><span>大家最近都看到了这个新闻，</span><span><span>OpenAI </span><span>要求</span></span><span>用户在</span><span><span>通过</span><span> </span><span>API </span></span><span>来</span><span>访问</span><span>他们家</span><span>最先进模型</span><span>时突然要求</span><span>实名认证</span><span>。</span><span>大家也许在想，这又是在作什么妖呢？今天就带大家来深度解析其背后最深层的原因。依我看，最根本的原因</span><span>是</span><span>为了平衡</span><span>技术开放与安全管控，</span><span>说白了就是</span><span>既</span><span>得</span><span>应对滥用风险，</span><span>又得</span><span>反映了行业监管与商业化策略。</span><span>下面</span><span>从多维度展开</span><span>说说</span><span>。</span><span> </span><br></p></div><div class="dpu8C _2kCxD  "><!--57--><!--57--><!--56--><!--58--><!--59--><!--60--><!--61--><!--62--><!--63--><!--64--><!--65--><!--66--><!--67--><!--68--><h3>一、政策核心目的：安全防御与风险控制</h3></div><div class="dpu8C _2kCxD  "><!--70--><!--70--><!--69--><!--71--><!--72--><!--73--><!--74--><!--75--><!--76--><!--77--><!--78--><!--79--><!--80--><!--81--><p><strong><span><span>1. </span><span>应对滥用行为的直接手段</span></span></strong><span><span>  </span></span></p></div><div class="dpu8C _2kCxD  "><!--83--><!--83--><!--82--><!--84--><!--85--><!--86--><!--87--><!--88--><!--89--><!--90--><!--91--><!--92--><!--93--><!--94--><p><span><span>OpenAI </span><span>指出，</span></span><span>确实存在</span><span><span>极少数开发者滥用</span><span> </span><span>API </span><span>从事违规活动</span></span><span>。</span><span><span>例如</span><span> </span><span>2024 </span><span>年监测到超过 </span><span>2000 </span><span>次通过 </span><span>API </span><span>实施的深度伪造攻击尝试。</span></span><span>如果搞了这招</span><span>实名认证</span><span>，</span><span>通过身份绑定，</span><span>就可以</span><span>追溯责任主体，</span><span>同时也能</span><span><span>有效降低模型被用于生成虚假信息、恶意内容或进行网络攻击的风险。这一措施与</span><span> </span><span>OpenAI </span><span>在 </span><span>AI </span><span>峰会上公布的</span></span><span>“</span><span>监控滥用行为</span><span>”“</span><span>模型测试与评估</span><span>”</span><span>等十大安全策略形成协同。</span><span> </span></p></div><div class="_3hMwG _2kCxD  "><!--95--><!--96--><div class="_1NCGf"><img src="https://pics3.baidu.com/feed/e4dde71190ef76c6356f2b70b64c14f5ae516792.jpeg@f_auto?token=99ce1e478c5630f99a646a02c166d3cb" width="751" class="_1g4Ex _1i_Oe "><!--99--></div><!--97--><!--100--><!--101--><!--102--><!--103--><!--104--><!--105--><!--106--><!--107--><!--108--></div><div class="dpu8C _2kCxD  "><!--110--><!--110--><!--109--><!--111--><!--112--><!--113--><!--114--><!--115--><!--116--><!--117--><!--118--><!--119--><!--120--><!--121--><p><strong><span><span>2. </span><span>合规框架下的主动适配  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--123--><!--123--><!--122--><!--124--><!--125--><!--126--><!--127--><!--128--><!--129--><!--130--><!--131--><!--132--><!--133--><!--134--><p><span><span>随着全球</span><span> </span><span>AI </span><span>监管趋严（如中国《生成式人工智能服务管理暂行办法》要求服务提供者履行内容审核、数据安全等义务），</span><span>OpenAI </span><span>通过实名认证强化对开发者的合规管理，确保其 </span><span>API </span><span>使用符合各国法律要求。例如，中国企业若通过微软 </span><span>Azure OpenAI </span><span>接入服务，需同时满足数据跨境、算法备案等多重合规条件。</span></span><span>说白了就是你要搞这方面，就得服管。</span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--136--><!--136--><!--135--><!--137--><!--138--><!--139--><!--140--><!--141--><!--142--><!--143--><!--144--><!--145--><!--146--><!--147--><h3><span><span> </span></span><span>二、对开发者生态的双重影响</span></h3></div><div class="dpu8C _2kCxD  "><!--149--><!--149--><!--148--><!--150--><!--151--><!--152--><!--153--><!--154--><!--155--><!--156--><!--157--><!--158--><!--159--><!--160--><p><strong><span><span>1. </span><span>资源分配的</span></span><span>“</span><span>筛选效应</span><span>”</span></strong><span>  </span></p></div><div class="dpu8C _2kCxD  "><!--162--><!--162--><!--161--><!--163--><!--164--><!--165--><!--166--><!--167--><!--168--><!--169--><!--170--><!--171--><!--172--><!--173--><p><span><span>已验证组织可优先访问多模态、长上下文处理等前沿功能，并可能获得更宽松的</span><span> </span><span>API </span><span>速率限制。这一机制可能加速行业分化：具备合规能力的大型企业或机构将获得技术优势，而资源有限的初创企业（尤其是非洲、东南亚等地的开发者）可能因证件限制被进一步边缘化，加剧</span></span><span>“</span><span>技术鸿沟</span><span>”</span><span>。</span><span>其实翻译成人话，就是说强的更强，弱的更弱，更易形成壁垒。</span></p></div><div class="_3hMwG _2kCxD  "><!--174--><!--175--><div class="_1NCGf"><img src="https://pics6.baidu.com/feed/42166d224f4a20a4d9e08c8fbd08712d730ed062.jpeg@f_auto?token=02bcdc19858e0690552ff54d4e49a2ab" width="1242" class="_1g4Ex _1i_Oe "><!--178--></div><!--176--><!--179--><!--180--><!--181--><!--182--><!--183--><!--184--><!--185--><!--186--><!--187--></div><div class="dpu8C _2kCxD  "><!--189--><!--189--><!--188--><!--190--><!--191--><!--192--><!--193--><!--194--><!--195--><!--196--><!--197--><!--198--><!--199--><!--200--><p><span> </span><strong><span><span>2. </span><span>合规成本与灵活性挑战  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--202--><!--202--><!--201--><!--203--><!--204--><!--205--><!--206--><!--207--><!--208--><!--209--><!--210--><!--211--><!--212--><!--213--><p><span><span>实名认证要求开发者提交政府签发的身份证件，且每个证件每</span><span> </span><span>90 </span><span>天仅能绑定一个组织。这对跨国分布式团队构成挑战，例如中国开发者可能因证件签发地不在支持列表或数据跨境限制，面临更高的接入门槛。此外，未通过验证的开发者虽可继续使用现有模型（如 </span><span>GPT-4</span><span>），但无法参与新模型的早期测试，可能影响技术迭代速度。</span></span></p></div><div class="dpu8C _2kCxD  "><!--215--><!--215--><!--214--><!--216--><!--217--><!--218--><!--219--><!--220--><!--221--><!--222--><!--223--><!--224--><!--225--><!--226--><p><span>也就是说传统的在一个地方办公的团队模式是符合要求的，因为好监管，而</span><span>跨国分布式团队</span><span>你就别干了，太难管了。这个跨国式分布式团队说的就是团队里面的成员分布在各个国家各个城市，大家都是远程工作，线上沟通工作进度和内容。</span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--228--><!--228--><!--227--><!--229--><!--230--><!--231--><!--232--><!--233--><!--234--><!--235--><!--236--><!--237--><!--238--><!--239--><h3><span><span> </span></span><span>三、隐私与伦理争议</span></h3></div><div class="dpu8C _2kCxD  "><!--241--><!--241--><!--240--><!--242--><!--243--><!--244--><!--245--><!--246--><!--247--><!--248--><!--249--><!--250--><!--251--><!--252--><p><strong><span><span>1. </span><span>数据收集的敏感性  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--254--><!--254--><!--253--><!--255--><!--256--><!--257--><!--258--><!--259--><!--260--><!--261--><!--262--><!--263--><!--264--><!--265--><p><span><span>实名认证需提交身份证件照片及面部识别视频，引发用户对隐私泄露的担忧。尽管</span><span> </span><span>OpenAI </span><span>承诺数据加密存储并遵循 </span><span>GDPR </span><span>等法规，但开发者仍质疑其</span></span><span>“</span><span>监控色彩</span><span>”</span><span>，担心个人信息被用于商业分析或第三方共享。</span></p></div><div class="_3hMwG _2kCxD  "><!--266--><!--267--><div class="_1NCGf"><img src="https://pics1.baidu.com/feed/7acb0a46f21fbe0916114539473ae53c8744ad3e.jpeg@f_auto?token=94b1f259351f076515b52b25e264ca87" width="1242" class="_1g4Ex _1i_Oe "><!--270--></div><!--268--><!--271--><!--272--><!--273--><!--274--><!--275--><!--276--><!--277--><!--278--><!--279--></div><div class="dpu8C _2kCxD  "><!--281--><!--281--><!--280--><!--282--><!--283--><!--284--><!--285--><!--286--><!--287--><!--288--><!--289--><!--290--><!--291--><!--292--><p><span><span>别说</span><span>AI</span><span>大模型了，现在普通的一个</span><span>APP</span><span>都要用户提交身份证件照片和面部识别视频，对于咱们用户来说除非你不用这个</span><span>APP</span><span>，否则根本就无法和平台抗衡。用户担心隐私泄露，也只能识单方面发发牢骚。</span></span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--294--><!--294--><!--293--><!--295--><!--296--><!--297--><!--298--><!--299--><!--300--><!--301--><!--302--><!--303--><!--304--><!--305--><p><strong><span><span>2. </span><span>技术垄断的隐忧  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--307--><!--307--><!--306--><!--308--><!--309--><!--310--><!--311--><!--312--><!--313--><!--314--><!--315--><!--316--><!--317--><!--318--><p><span><span>开源社区批评</span><span> </span><span>OpenAI</span></span><span>“</span><span>以安全之名行垄断之实</span><span>”</span><span>，认为实名认证可能成为技术封闭的前奏。例如，未来模型的训练数据、算法框架可能进一步向已验证组织倾斜，削弱行业竞争。</span></p></div><div class="dpu8C _2kCxD  "><!--320--><!--320--><!--319--><!--321--><!--322--><!--323--><!--324--><!--325--><!--326--><!--327--><!--328--><!--329--><!--330--><!--331--><p><span><span>这和我们古话说的</span><span>“强者恒强”一个道理，先起来的占据更多的资源和优势。</span></span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--333--><!--333--><!--332--><!--334--><!--335--><!--336--><!--337--><!--338--><!--339--><!--340--><!--341--><!--342--><!--343--><!--344--><h3><span><span> </span></span><span>四、商业化与行业趋势</span></h3></div><div class="dpu8C _2kCxD  "><!--346--><!--346--><!--345--><!--347--><!--348--><!--349--><!--350--><!--351--><!--352--><!--353--><!--354--><!--355--><!--356--><!--357--><p><strong><span><span>1. </span><span>企业服务分层的信号  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--359--><!--359--><!--358--><!--360--><!--361--><!--362--><!--363--><!--364--><!--365--><!--366--><!--367--><!--368--><!--369--><!--370--><p><span><span>实名认证可能是</span><span> </span><span>OpenAI </span><span>企业服务分层的第一步。通过</span></span><span>“</span><span>已验证组织</span><span>”</span><span><span>状态，</span><span>OpenAI </span><span>可将先进模型的访问权限与商业价值绑定，未来或推出</span></span><span>“</span><span>高级认证</span><span>”</span><span><span>收费服务，拓展</span><span> </span><span>B </span><span>端市场。这一策略与微软、谷歌等竞品的 </span><span>API </span><span>定价模式（如按调用量收费）形成呼应，反映行业从</span></span><span>“</span><span>普惠开放</span><span>”</span><span>向</span><span>“</span><span>价值变现</span><span>”</span><span>的转型。</span></p></div><div class="dpu8C _2kCxD  "><!--372--><!--372--><!--371--><!--373--><!--374--><!--375--><!--376--><!--377--><!--378--><!--379--><!--380--><!--381--><!--382--><!--383--><p><span><span>也就是开始搞</span><span>VIP</span><span>啦，后续就是不充钱没法用。</span></span><span> </span></p></div><div class="_3hMwG _2kCxD  "><!--384--><!--385--><div class="_1NCGf"><img src="https://pics2.baidu.com/feed/5ab5c9ea15ce36d3b70a56c414a9d388e850b1a6.jpeg@f_auto?token=497f8c1e1722e059de10916945551830" width="1242" class="_1g4Ex _1i_Oe "><!--388--></div><!--386--><!--389--><!--390--><!--391--><!--392--><!--393--><!--394--><!--395--><!--396--><!--397--></div><div class="dpu8C _2kCxD  "><!--399--><!--399--><!--398--><!--400--><!--401--><!--402--><!--403--><!--404--><!--405--><!--406--><!--407--><!--408--><!--409--><!--410--><p><strong><span><span>2. </span><span>全球 </span><span>AI </span><span>治理的缩影  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--412--><!--412--><!--411--><!--413--><!--414--><!--415--><!--416--><!--417--><!--418--><!--419--><!--420--><!--421--><!--422--><!--423--><p><span><span>实名认证并非</span><span> </span><span>OpenAI </span><span>独有，微软 </span><span>Azure OpenAI</span><span>、谷歌 </span><span>Vertex AI </span><span>等平台也逐步强化身份验证与权限管理。这种趋势既源于技术滥用的现实威胁，也受到各国监管政策（如欧盟 </span><span>AI </span><span>法案）的驱动。例如，中国《生成式人工智能服务管理暂行办法》要求服务提供者对用户身份进行核验，并建立投诉举报机制，与 </span><span>OpenAI </span><span>的措施形成跨国监管协同。</span></span></p></div><div class="dpu8C _2kCxD  "><!--425--><!--425--><!--424--><!--426--><!--427--><!--428--><!--429--><!--430--><!--431--><!--432--><!--433--><!--434--><!--435--><!--436--><p><span>从网络安全的角度来看，还是</span><span><span>全球</span><span> </span><span>AI </span><span>治理</span></span><span>必然的一条路线。</span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--438--><!--438--><!--437--><!--439--><!--440--><!--441--><!--442--><!--443--><!--444--><!--445--><!--446--><!--447--><!--448--><!--449--><h3><span><span> </span></span><span>五、未来演进的可能性</span></h3></div><div class="dpu8C _2kCxD  "><!--451--><!--451--><!--450--><!--452--><!--453--><!--454--><!--455--><!--456--><!--457--><!--458--><!--459--><!--460--><!--461--><!--462--><p><strong><span><span>1. </span><span>动态调整与地域扩展  </span></span></strong></p></div><div class="dpu8C _2kCxD  "><!--464--><!--464--><!--463--><!--465--><!--466--><!--467--><!--468--><!--469--><!--470--><!--471--><!--472--><!--473--><!--474--><!--475--><p><span><span>OpenAI </span><span>已承诺逐步扩大支持地域范围，并探索</span></span><span>“</span><span>去中心化验证</span><span>”</span><span>方案（如区块链技术）以降低对传统身份证件的依赖。这可能缓解部分开发者的合规压力，但需平衡安全性与技术可行性。</span><span>想要发展，就不能局限在一个地方。</span><span> </span></p></div><div class="_3hMwG _2kCxD  "><!--476--><!--477--><div class="_1NCGf"><img src="https://pics6.baidu.com/feed/738b4710b912c8fcc60c6c46d0597b4ad7882123.jpeg@f_auto?token=c9dc748b5c0f26449ad7cabc61d0f69d" width="974" class="_1g4Ex _1i_Oe "><!--480--></div><!--478--><!--481--><!--482--><!--483--><!--484--><!--485--><!--486--><!--487--><!--488--><!--489--></div><div class="dpu8C _2kCxD  "><!--491--><!--491--><!--490--><!--492--><!--493--><!--494--><!--495--><!--496--><!--497--><!--498--><!--499--><!--500--><!--501--><!--502--><p><strong><span><span>2. </span><span>从</span></span><span>“</span><span>强制认证</span><span>”</span><span>到</span><span>“</span><span>风险分级</span><span>”</span><span> </span></strong><span> </span></p></div><div class="dpu8C _2kCxD  "><!--504--><!--504--><!--503--><!--505--><!--506--><!--507--><!--508--><!--509--><!--510--><!--511--><!--512--><!--513--><!--514--><!--515--><p><span><span>随着</span><span> </span><span>AI </span><span>模型风险评估体系的完善，</span><span>OpenAI </span><span>或参考欧盟的</span></span><span>“</span><span>分类分级监管</span><span>”</span><span>思路，根据模型能力（如生成内容的影响力）动态调整认证要求。例如，仅对具备舆论属性或社会动员能力的模型实施严格身份核验。</span><span>就是说具体情况具体分析，不会非得都用一个认证标准。</span><span> </span></p></div><div class="dpu8C _2kCxD  "><!--517--><!--517--><!--516--><!--518--><!--519--><!--520--><!--521--><!--522--><!--523--><!--524--><!--525--><!--526--><!--527--><!--528--><h3><span><span> </span></span><span>总结</span></h3></div><div class="dpu8C _2kCxD  "><!--530--><!--530--><!--529--><!--531--><!--532--><!--533--><!--534--><!--535--><!--536--><!--537--><!--538--><!--539--><!--540--><!--541--><p><span><span>OpenAI </span><span>的实名认证政策是技术发展与社会风险博弈的产物，其本质是通过身份绑定实现</span></span><span>“</span><span>责任可追溯</span><span>”</span><span>，</span><span>出现了问题能找到对应的人，</span><span><span>以应对</span><span> </span><span>AI </span><span>滥用的全球性挑战。对于开发者而言，这一政策既是合规门槛，也是</span></span><span>有</span><span><span>技术红利的；对于行业而言，它标志着</span><span> </span><span>AI </span><span>服务从</span></span><span>“</span><span>野蛮生长</span><span>”</span><span>向</span><span>“</span><span>有序治理</span><span>”</span><span><span>的转型。未来，政策的效果将取决于</span><span> </span><span>OpenAI </span><span>在安全管控、隐私保护与技术普惠之间的平衡能力，以及全球监管框架的协同程度。</span></span></p></div><div class="dpu8C _2kCxD  "><!--543--><!--543--><!--542--><!--544--><!--545--><!--546--><!--547--><!--548--><!--549--><!--550--><!--551--><!--552--><!--553--><!--554--><p><strong><span style="background-color: rgb(255, 255, 255)">读完了本篇深度好文，快收藏转发给朋友看吧！您觉得我分析得思路如何？请在评论区留言，咱们共同探讨!</span></strong></p></div><div class="dpu8C _2kCxD  "><!--555--><!--556--><!--557--><!--558--><!--559--><!--560--><!--561--><!--562--><!--563--><!--564--><!--565--><div class="_1CFoW"><div>事件发生于2025-04-14 国外,国外</div></div><!--566--></div><!--28--><!--568--><!--569--><div class="_3hMwG"><div class="_26vAC "><!--571--><span data-testid="report-btn">举报/反馈</span></div></div></div>
    """
    
    # 使用模板发布文章
    try:
        result = api.publish_article(
            content=article_content,
            template_id="template9",
            title="深度解析：为什么OpenAI -API 访问其最先进模型需实名认证？",
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