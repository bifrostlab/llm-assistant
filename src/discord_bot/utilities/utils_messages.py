def message_split(message: str) -> list[str]:
  """
  Split the message into a list of messages of length 2000. With meaningfull sentence
  """
  messages = []
  message = message.strip()

  while len(message) > 2000:
    last_period = message[:2000].rfind(".")
    if last_period == -1:
      last_period = message[:2000].rfind(" ")
    messages.append(message[: last_period + 1])
    message = message[last_period + 1 :]

  messages.append(message)

  return messages


# Test

message = """
PwC’s Threat Intelligence team is seeking junior and mid-level threat intelligence analysts who have a passion and aptitude for understanding malicious activity and developing internal and external reporting. We are ideally looking for analysts with a strong background in either technical or strategic intelligence PwC serves more than 200,000 clients in 152 countries, and we use our vantage point as one of the largest international professional services networks to provide global threat intelligence services, tailored and delivered locally to our clients. Our research underpins our security services and is used by public and private sector organisations around the world to protect networks, provide situational awareness and inform strategy. We focus on the identification of novel intrusion techniques and tracking of several hundred threat actors, ranging from organised crime groups to state affiliated espionage actors, originating from more than 27 countries, and we provide: Subscription and bespoke research services to public and private sector intelligence clients globally; Intelligence support to, and collection from incident response and managed threat hunting teams; Insight to our adversary emulation team on novel tools and techniques used by cyber threat actors; and, Access to cutting edge research to inform and underpin all services provided by PwC’s several thousand strong cyber security consulting practice.

As a threat intelligence analyst within PwC’s Threat Intelligence practice you’ll delve into threat actor campaigns and incident response cases relevant to PwC’s vast client base, ranging from NGOs to the world’s largest corporations.

You’ll develop a deep understanding of the tools and techniques used by threat actors, help our clients understand the threats they face, and enable them to better defend their networks. You could be involved in monitoring C2 infrastructure for an actor, targeted attack activity in a specific region, the evolution of specific malware families, and everything in between.

You’ll also get the chance to work on bespoke threat assessments, defining the threats to Critical National Infrastructure, to defining strategic collection requirements, generating intelligence reporting as part of our subscription intelligence service or in response to RFIs, you will have the opportunity to lead interactions with a wide ranging internal and external consumer base.

Technical Responsibilities

Developing collection and tracking techniques to identify new threat actors and campaigns, monitor the activity of known actors, and methodically attribute new activity from both open and closed data sources using a variety of bespoke, commercial and open source tools and systems;
Participating in analysis surges to renew and further develop knowledge on new and existing threat actors;
Applying a robust analytical methodology to support conclusions in relation to specific threat actors, and an ability to rationalise and articulate your conclusions;
Understanding of network protocols, attack lifecycles and actor tradecraft;
Supporting the generation of analytic content, detection concepts, and network and host based detection methods; and
Researching and developing new tools and scripts to continually update or improve our threat intelligence automation processes, collection methods and analytical capability.


It’s time to move forward. And upward. 

You want to grow, reach new heights and move up the corporate ladder.

We’ll give you a career-boosting role that:

Is strong on growth and reward
Provides strong mentors and plenty of networking opportunities 
Helps you learn and grow with our internal Academy, study support.
Gives you the chance to explore, with overseas secondments and our Together Anywhere policy that lets you work up to 4 weeks from anywhere in Australia
Helps you prioritise your life outside of work, with lifestyle and wellness stipends up to $500 a year
Has competitive and transparent salary packages with the opportunity for yearly bonuses and promotions


Jaimie Bonehill is the Recruitment Manager for the role. As the team experiences high volumes of applications, we appreciate your patience to allow for a timely and fair process for all.

Desirable but not essential skills:

An understanding of common analysis techniques and frameworks used in CTI, such as threat modeling techniques like the Diamond model, Kill Chain, and F3EAD;
Knowledge of open source and commercial platforms, tools and frameworks used within threat intelligence teams, such as threat intelligence platforms, malware sandboxes and reverse engineering tools, such as Ghidra or IDA Pro;
Experience with Maltego, including custom transforms, and its use in mapping out intrusion sets;
Baseline knowledge of threat actors, attribution concepts, and high profile cyber incidents; and
An understanding or knowledge of related regional geopolitics/wider security landscape.

"""
message = message_split(message)
len(message)
message[2]