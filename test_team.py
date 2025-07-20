from typing import Optional

import pytest
from textwrap import dedent
from agno.agent import RunResponse
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.eval.reliability import ReliabilityEval, ReliabilityResult
from agno.run.team import TeamRunResponse

from team import get_agent_team

NUM_CALLS = 10
RELIABILITY_MIN = 7
ACCURACY_MIN = 7

team = get_agent_team()

Q_AND_A = [
    {
        "question": "What is the capital of Canada?",
        "answer": "Ottawa"
    },
    {
        "question": "I'm in the market for some jeans",
        "answer": dedent("""
            I found several Canadian brands that sell jeans.

            Yoga Jeans This Quebec-based brand makes sustainably-crafted jeans in a variety of styles and washes.

            Naked and Famous Denim This Montreal-based label has built a cult following with its raw, untreated denim jeans and jackets.

            Duer This Vancouver-based brand makes rainproof and fleece-lined jeans.

            Decade Studio This Vancouver brand makes ethically-made jeans in Portugal with premium rigid denim.

            Lola Jeans This Montreal-based brand crafts ultra-flattering denim using organic cotton, recycled fabrics and low-usage to waterless production methods.

            Silver Jeans This Canadian denim icon has been delivering heritage craftsmanship and effortlessly cool fits since the ‘90s.

            Big Bill This brand makes work jeans that are manufactured in Canada.

            Would you like to know more about any of these brands?
        """),
    },
    # {
    #     "question": "I'm in the market for some new music",
    #     "answer": dedent("""
    #         I found several Canadian artists that make music.
    #     """),
    # },
    {
        "question": "help me find some new yoga pants",
        "answer": dedent("""
Here are some top Canadian and Canadian-loved yoga pants options carefully selected for quality, comfort, and style, including iconic        
      Canadian brands and highly rated Canadian-owned businesses:                                                                                  
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 1. Lululemon Align High Rise Leggings                                                                                                     
      *Price:* \$112                                                                                                                               
      *Rating:* 4.8/5 (based on thousands of reviews)                                                                                              
      *Description:* These leggings are a beloved classic from Vancouver-based Lululemon, designed with buttery-soft Nulu fabric that feels like a 
      second skin. They offer excellent four-way stretch, breathability, and a comfortable high-rise waistband that stays put without squeezing.   
      Great for yoga and everyday wear.                                                                                                            
      *Features:* Moisture-wicking, sweat-resistant, hidden waistband pocket, h-shaped gusset for mobility                                         
      [Buy directly from Lululemon Canada](https://shop.lululemon.com/p/women-pant/Align-Pant-High-Rise/_/prod9740016)                             
                                                                                                                                                   
      **Canadian ownership:** Lululemon is a Canadian company, headquartered in Vancouver, BC, and a global leader in yoga and activewear.         
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 2. Beyond Yoga Spacedye Out of Pocket High Waisted Midi Legging                                                                           
      *Price:* \$97                                                                                                                                
      *Rating:* 4.5/5                                                                                                                              
      *Description:* Known for dreamy softness and exceptional comfort, Beyond Yoga's Canadian-designed leggings feature flattering high-rise fit  
      and convenient hip pockets. The fabric blends polyester and spandex to offer breathability with a lounge-worthy feel. Perfect for yoga and   
      casual comfort.                                                                                                                              
      *Features:* High-rise waistband, moisture-wicking, UV protection, hip pockets, sizes XXS-4XL                                                 
      [Buy from Beyond Yoga](https://beyondyoga.com/products/spacedye-out-of-pocket-midi)                                                          
                                                                                                                                                   
      **Canadian ownership:** Beyond Yoga was founded in the US but has substantial Canadian market presence. (Note: They are not headquartered in 
      Canada.)                                                                                                                                     
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 3. Daub + Design Yoga Leggings (Two-tone & Prints)                                                                                        
      *Price:* Approximately \$120 (varies by style)                                                                                               
      *Rating:* 4.6/5                                                                                                                              
      *Description:* Based in Vancouver, Daub + Design offers yoga leggings with unique prints and sustainable, super-soft fabrics that are both   
      stylish and functional. Great for those who want to break away from plain leggings. Durable and comfortable for yoga and everyday.           
      *Features:* Sustainable fabrics, custom textile designs, high stretch with secure waistbands                                                 
      [Shop Daub + Design](https://daubanddesign.com)                                                                                              
                                                                                                                                                   
      **Canadian ownership:** Daub + Design is a Canadian-owned and operated activewear company based in Vancouver.                                
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 4. Titika Active Couture Yoga Pants                                                                                                       
      *Price:* \$85 - \$130 (varies on style)                                                                                                      
      *Rating:* 4.4/5                                                                                                                              
      *Description:* Toronto-based Titika offers fashionable, flattering yoga pants with innovative details like built-in bras, lace trims, and    
      fresh designs updated regularly. Manufactured with strict quality control, these pants are made for comfort and style.                       
      *Features:* Stretchy, stylish cuts, made in controlled Asian factories, variety of unique prints and styles                                  
      [Shop Titika](https://titika.com)                                                                                                            
                                                                                                                                                   
      **Canadian ownership:** Titika is a Canadian-owned business founded in Toronto.                                                              
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 5. Michi Power Leggings                                                                                                                   
      *Price:* Approx. \$150                                                                                                                       
      *Rating:* 4.5/5                                                                                                                              
      *Description:* Based in Toronto, Michi offers luxe, fashion-forward athletic leggings with intricate lace and mesh details alongside top     
      performance fabrics. Their leggings are perfect for those who want to blend yoga with edgy style.                                            
      *Features:* Designer details, moisture-wicking, flattering cuts, made ethically in Canada                                                    
      [Shop Michi](https://michiactive.com)                                                                                                        
                                                                                                                                                   
      **Canadian ownership:** Michi is a Toronto-based Canadian company focused on local manufacturing.                                            
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 6. Seed Athletic Pants (Sustainable Line)                                                                                                 
      *Price:* Approx. \$135                                                                                                                       
      *Rating:* 4.3/5                                                                                                                              
      *Description:* Calgary-based Seed uses mainly hemp and organic cotton fabrics with plant-based dyes. The pants are eco-friendly, sustainable,
      and designed with natural fibres for softness and function.                                                                                  
      *Features:* Organic fabrics, plant-based dyes, sustainable production, sizes 00-24                                                           
      [Seed on their official site](https://seedathletics.com)                                                                                     
                                                                                                                                                   
      **Canadian ownership:** Seed is a Canadian-owned sustainable clothing company based in Calgary, Alberta.                                     
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 7. Respecterre Yoga Pants                                                                                                                 
      *Price:* From \$90 ($CAD)                                                                                                                    
      *Rating:* 4.5/5                                                                                                                              
      *Description:* Quebec-based Respecterre makes sustainably produced yoga apparel in eco-villages with a focus on minimal waste and local      
      manufacturing. Their leggings are comfortable and eco-conscious for mindful yogis.                                                           
      *Features:* Made to order, OEKO-TEX certified fabrics, plastic-free packaging options                                                        
      [Shop Respecterre](https://respecterre.eco/en)                                                                                               
                                                                                                                                                   
      **Canadian ownership:** Respecterre is Canadian, based in Quebec, committed to local eco-friendly production.                                
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## 8. Old Navy High-Waisted PowerSoft 7/8 Leggings (Budget-Friendly Canadian Option)                                                         
      *Price:* Starting at \$40                                                                                                                    
      *Rating:* 4.4/5                                                                                                                              
      *Description:* Popular for providing good stretch and support at an affordable price, these leggings are great for yoga novices or casual    
      use. Lightweight and comfortable, they feature a high waistband that stays in place.                                                         
      *Features:* 77% polyester, 23% elastane, supportive waistband, various colors                                                                
      [Buy from Old Navy Canada](https://oldnavy.gapcanada.ca)                                                                                     
                                                                                                                                                   
      **Canadian ownership:** Old Navy is a US-based company but widely available and popular in Canada.                                           
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## Product Comparison Table                                                                                                                  
                                                                                                                                                   
      | Brand                   | Price (CAD) | Rating | Material                    | Features                                       | Canadian   
      Owned/Made                      |                                                                                                            
      |-------------------------|-------------|--------|-----------------------------|------------------------------------------------|------------
      -----------------------------|                                                                                                               
      | Lululemon Align High Rise| \$112       | 4.8    | 81% nylon, 19% Lycra        | Moisture wicking, 4-way stretch, hidden pocket | Canadian  
      owned, Vancouver-based         |                                                                                                             
      | Beyond Yoga Spacedye    | \$97        | 4.5    | 87% polyester, 13% spandex  | UV protection, hip pockets, soft stretchy      | Not        
      Canadian owned, strong Canadian presence |                                                                                                   
      | Daub + Design           | ~\$120      | 4.6    | Sustainable fabric blends   | Unique prints, sustainable, comfortable         | Canadian  
      owned, Vancouver               |                                                                                                             
      | Titika Active Couture   | \$85-$130   | 4.4    | Mix (produced in Canada & Asia) | Fashionable, built-in bras, quality control     |       
      Canadian owned, Toronto                 |                                                                                                    
      | Michi                   | ~\$150      | 4.5    | High-quality, designer fabric | Lace & mesh details, local production          | Canadian 
      owned, Toronto                 |                                                                                                             
      | Seed                    | ~\$135      | 4.3    | Hemp, organic cotton         | Plant dyes, sustainable production             | Canadian  
      owned, Calgary                 |                                                                                                             
      | Respecterre             | From \$90   | 4.5    | OEKO-TEX certified fabrics  | Made to order, eco-friendly                      | Canadian 
      owned, Quebec                  |                                                                                                             
      | Old Navy PowerSoft 7/8  | From \$40   | 4.4    | Polyester/elastane          | High-waisted, budget-friendly                    | Not      
      Canadian owned                     |                                                                                                         
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### Summary of Canadian Ownership and Local Production:                                                                                      
                                                                                                                                                   
      - **Lululemon, Daub + Design, Titika, Michi, Seed, Respecterre**: Canadian owned and operated businesses, with Canadian-based manufacturing  
      or design.                                                                                                                                   
      - **Beyond Yoga**: Popular in Canada but US-owned.                                                                                           
      - **Old Navy**: US brand but very popular and accessible for Canadian shoppers.                                                              
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      If you'd like, I can help find yoga pants that are specifically made or sold locally in a region like Toronto, Vancouver, or Quebec. Would   
      you prefer that? 
        """),
    },
    {
        "question": "help me find my next car (suv)",
        "answer": dedent("""
            Here are the best SUVs made in Canada in 2025, ranked and detailed with relevant information from Canadian sources and expert reviews:       
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 1. 2025 Honda CR-V                                                                                                                       
      **Description:** The Honda CR-V is one of the top-selling compact SUVs, known for reliability, fuel efficiency, and spacious interiors.      
      **Price:** Starting at \$31,495                                                                                                              
      **Rating:** 10/10 (Car and Driver)                                                                                                           
      **Reviews:** Highly rated for comfort, fuel economy (28-30 MPG combined), and smooth handling.                                               
      **Features:** Gas and hybrid powertrain options, advanced safety features, infotainment system with Apple CarPlay and Android Auto, roomy    
      cargo space.                                                                                                                                 
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Honda of Canada Manufacturing, Alliston, Ontario.                                                                             
      - Canada produces both gas and hybrid versions here.                                                                                         
      - 214,095 units produced in 2024.                                                                                                            
      - Large percentage for US and Canadian markets.                                                                                              
      [Source - Cam Clark Ford](https://www.camclarkfordrichmond.com/blog/what-cars-made-in-canada​/)                                               
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
      [Source - Car and Driver](https://www.caranddriver.com/rankings/best-suvs)                                                                   
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 2. 2025 Toyota RAV4                                                                                                                      
      **Description:** Canada’s best-selling SUV, popular for its reliability, hybrid option, and strong resale value.                             
      **Price:** Starting at \$33,685                                                                                                              
      **Rating:** 3.8/5 (Driving.ca user rating)                                                                                                   
      **Reviews:** Praised for solid build quality, fuel efficiency in hybrid, and an overall package fit for families.                            
      **Features:** Gas and hybrid models, AWD options, Toyota Safety Sense, large cargo hold.                                                     
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Toyota Motor Manufacturing Canada, Cambridge and Woodstock, Ontario.                                                          
      - Most-produced vehicle in Canada in 2024 with 368,577 units.                                                                                
      - Plug-in hybrid imported from Japan, but gas/hybrid SUVs are local.                                                                         
      [Source - AutoTrader](https://www.autotrader.ca/editorial/20250403/made-in-canada-what-cars-are-manufactured-in-canada)                      
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 3. 2024 Chrysler Pacifica                                                                                                                
      **Description:** A family-friendly minivan with strong safety scores and modern technology, available in gas and plug-in hybrid versions.    
      **Price:** Around \$43,000+ (varies by trim)                                                                                                 
      **Rating:** Appreciated for versatility and comfort (user rating ~3.8/5)                                                                     
      **Reviews:** Praised for smooth ride, spacious interior, and plug-in capability.                                                             
      **Features:** Hybrid and gas powertrains, Uconnect infotainment, advanced driver assists.                                                    
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Stellantis Windsor Assembly, Windsor, Ontario.                                                                                
      - 107,668 units produced in 2024.                                                                                                            
      - The only Stellantis minivans assembled globally here.                                                                                      
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
      [Source - Cam Clark Ford](https://www.camclarkfordrichmond.com/blog/what-cars-made-in-canada​/)                                               
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 4. 2025 Chevrolet Silverado (Pickup but notable)                                                                                         
      **Description:** Though a pickup truck, one of the most popular light trucks built in Canada and relevant to many SUV buyers who consider    
      trucks.                                                                                                                                      
      **Price:** Starting at \$51,855                                                                                                              
      **Rating:** 3.63/5 (Driving.ca)                                                                                                              
      **Reviews:** Known for power, towing capacity, and durability.                                                                               
      **Features:** Multiple engines including V8, towing packages, modern tech options.                                                           
      **Made in Canada Details:**                                                                                                                  
      - Assembled at General Motors Oshawa Assembly, Oshawa, Ontario.                                                                              
      - 152,190 units produced in 2024.                                                                                                            
      - GM also builds electric delivery vans, BrightDrop, in Ingersoll, Ontario.                                                                  
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
      [Source - AutoTrader](https://www.autotrader.ca/editorial/20250403/made-in-canada-what-cars-are-manufactured-in-canada)                      
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 5. 2025 Lexus RX                                                                                                                         
      **Description:** A luxury mid-size SUV assembled in Canada with gas and hybrid options.                                                      
      **Price:** Starting around \$50,000+ (exact prices vary by trim)                                                                             
      **Rating:** High customer satisfaction for luxury and smoothness.                                                                            
      **Reviews:** Praised for refinement, comfortable ride, and feature-rich cabin.                                                               
      **Features:** Hybrid and gas engines, luxury finishes, Lexus Safety System+.                                                                 
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Toyota Motor Manufacturing Cambridge South, Ontario.                                                                          
      - Approximately 111,220 units produced in 2024 locally.                                                                                      
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
      [Source - AutoTrader](https://www.autotrader.ca/editorial/20250403/made-in-canada-what-cars-are-manufactured-in-canada)                      
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 6. 2025 Lexus NX                                                                                                                         
      **Description:** A compact luxury SUV offering gas and hybrid power, assembled in Canada.                                                    
      **Price:** Starting at around \$42,000                                                                                                       
      **Rating:** Positive reviews for technology, comfort, and fuel efficiency.                                                                   
      **Features:** AWD, hybrid options, Lexus safety features.                                                                                    
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Toyota Motor Manufacturing Cambridge North, Ontario.                                                                          
      - 53,787 units produced in Canada in 2024.                                                                                                   
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 7. 2025 Dodge Charger Daytona EV                                                                                                         
      **Description:** A Canadian assembled electric 2-door muscle car SUV-coupe crossover variant, showing Canadian innovation and EV production. 
      **Price:** Starting at around \$45,000 (anticipated)                                                                                         
      **Rating:** Growing EV market presence, with excellent reviews for performance.                                                              
      **Features:** Electric powertrain, performance enhancements, modern infotainment.                                                            
      **Made in Canada Details:**                                                                                                                  
      - Assembled at Stellantis Windsor Assembly, Windsor, Ontario since mid-2024.                                                                 
      [Source - Driving.ca](https://driving.ca/car-culture/lists/canadian-made-car-models-built-assembly-tariff)                                   
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ## Summary Table of Canadian Made SUVs                                                                                                       
                                                                                                                                                   
      | Rank | Model                  | Price Start  | Rating        | Key Features                                      | Assembly Location       
      (Canada)                      |                                                                                                              
      |-------|-------------------------|--------------|---------------|--------------------------------------------------|------------------------
      ------------------------|                                                                                                                    
      | 1     | 2025 Honda CR-V         | \$31,495     | 10/10 (C&D)   | Gas/hybrid, safety, infotainment, cargo space    | Honda Alliston, Ontario
      |                                                                                                                                            
      | 2     | 2025 Toyota RAV4        | \$33,685     | 3.8/5 (User)  | Gas/hybrid, AWD, Toyota Safety Sense             | Cambridge & Woodstock, 
      Ontario                  |                                                                                                                   
      | 3     | 2024 Chrysler Pacifica  | ~\$43,000+   | ~3.8/5 (User) | Minivan, plug-in hybrid, family features         | Windsor, Ontario       
      |                                                                                                                                            
      | 4     | 2025 Chevrolet Silverado| \$51,855     | 3.63/5 (User) | Pickup – multiple engines, towing capacity         | Oshawa, Ontario      
      |                                                                                                                                            
      | 5     | 2025 Lexus RX           | ~\$50,000+   | High          | Luxury, hybrid & gas, advanced safety             | Cambridge South,      
      Ontario                        |                                                                                                             
      | 6     | 2025 Lexus NX           | ~\$42,000    | Positive      | Compact luxury, hybrid & gas                       | Cambridge North,     
      Ontario                        |                                                                                                             
      | 7     | 2025 Dodge Charger Daytona EV | ~\$45,000 (est) | Growing EV market | Electric performance coupe                        | Windsor, 
      Ontario                                |                                                                                                     
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      If you're seeking SUVs made locally in Canada, these are your best options reflecting Canadian manufacturing excellence, from reliable       
      mainstream to luxury and electric innovations.                                                                                               
                                                                                                                                                   
      Let me know if you want more detail on any model or segment!  
        """),
    },
    {
        "question": "Help me find my next binge like schitts creek and kim's convenience",
        "answer": dedent("""
      Here are some great Canadian TV shows you might enjoy if you liked "Schitt's Creek" and "Kim's Convenience," both comedies with strong       
      character-driven stories, warmth, and humor:                                                                                                 
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 1. Kim's Convenience                                                                                                                     
      - **Description:** A heartwarming comedy about the Kim family, Korean-Canadians running a convenience store in Toronto. The series blends    
      humor with family dynamics, depicting flawed but lovable characters and exploring immigrant family life and generational conflicts.          
      - **Where to Watch:** Formerly on Netflix Canada; currently streaming on [CBC Gem (Canadian streaming platform)](https://gem.cbc.ca/).       
      - **Source:** BuzzFeed highlights _Kim's Convenience_ as a delightfully funny, character-driven Canadian sitcom with heart.                  
      ([BuzzFeed](https://www.buzzfeed.com/laurengarafano/shows-to-watch-after-schitts-creek))                                                     
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 2. Workin' Moms                                                                                                                          
      - **Description:** A Canadian comedy about four working mothers balancing careers, motherhood, and personal challenges with both humor and   
      honesty. It’s praised for realistic, refreshingly imperfect characters.                                                                      
      - **Where to Watch:** [Netflix](https://www.netflix.com/title/80198136) (availability may vary by region) and [CBC Gem](https://gem.cbc.ca/).
      - **Source:** TV Guide calls this a sleeper hit with strong Canadian humor, offering a brutal yet funny take on motherhood. ([TV             
      Guide](https://www.tvguide.com/news/shows-like-schitts-creek-watch-next-netflix-hulu/))                                                      
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 3. Letterkenny                                                                                                                           
      - **Description:** Set in a small rural community in Ontario, this show humorously portrays the lives and interactions of farmers, hockey    
      players, and local “skids” with witty and fast-paced dialogue. Known for its unique style and turn of phrase.                                
      - **Where to Watch:** Hulu (US) and [CBC Gem (Canada)](https://gem.cbc.ca/).                                                                 
      - **Source:** BuzzFeed notes its small-town setting and comedy similar to _Schitt’s Creek_.                                                  
      ([BuzzFeed](https://www.buzzfeed.com/laurengarafano/shows-to-watch-after-schitts-creek))                                                     
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 4. Corner Gas                                                                                                                            
      - **Description:** A classic Canadian sitcom about quirky characters in the small town of Dog River, Saskatchewan. The show is lighthearted, 
      warm, and respectful of its small-town characters, blending gentle humor with community charm.                                               
      - **Where to Watch:** Amazon Prime Video (purchase) and [CBC Gem](https://gem.cbc.ca/).                                                      
      - **Source:** Vulture describes _Corner Gas_ as a refreshing small-town character comedy with quirky humor.                                  
      ([Vulture](https://www.vulture.com/article/best-canadian-sitcoms-streaming.html))                                                            
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### 5. The Amazing Gayl Pile                                                                                                                 
      - **Description:** A darker, surreal Canadian comedy series about a man struggling to keep afloat his late mother's low-rent home-shopping   
      channel. The show combines absurd humor with character-driven narrative.                                                                     
      - **Where to Watch:** [GaylPile.com](http://gaylpile.com) (official website)                                                                 
      - **Source:** Vulture includes this as one of the best Canadian comedies with a unique tone.                                                 
      ([Vulture](https://www.vulture.com/article/best-canadian-sitcoms-streaming.html))                                                            
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### Where to watch Canadian shows like Schitt’s Creek and Kim’s Convenience:                                                                 
                                                                                                                                                   
      Since many Canadian shows, including _Schitt’s Creek_ and _Kim’s Convenience_, have left Netflix Canada, the best place to stream a wide     
      range of Canadian TV currently is [CBC Gem](https://gem.cbc.ca/), CBC’s free streaming platform with ads or a paid ad-free option. It houses 
      several iconic Canadian series and supports Canadian creators directly.                                                                      
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### Additional Recommended Shows:                                                                                                            
                                                                                                                                                   
      - **Second Jen** — Follows two Asian-Canadian women navigating personal and cultural challenges. ([Available on                              
      DailyMotion](https://www.dailymotion.com/))                                                                                                  
      - **Mr. D** — Comedy about a less-than-qualified high school teacher dealing with students and staff. (Available on Hulu)                    
      - **Kim's Convenience** and **Schitt’s Creek** themselves are also worth re-watching on CBC Gem.                                             
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### Summary                                                                                                                                  
                                                                                                                                                   
      If you loved the character-driven, heartfelt yet funny spirit of _Schitt's Creek_ and _Kim's Convenience_, I strongly recommend checking out:
                                                                                                                                                   
      - **Kim’s Convenience** (CBC Gem)                                                                                                            
      - **Workin’ Moms** (Netflix/CBC Gem)                                                                                                         
      - **Letterkenny** (Hulu/CBC Gem)                                                                                                             
      - **Corner Gas** (Amazon/CBC Gem)                                                                                                            
      - **Second Jen** (DailyMotion)                                                                                                               
                                                                                                                                                   
      These shows offer a mix of heartfelt family stories, sharp comedy, and unique Canadian perspectives.                                         
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      ### Sources                                                                                                                                  
                                                                                                                                                   
      - BuzzFeed: [21 Underrated Shows That "Schitt's Creek" Fans Will                                                                             
      Love](https://www.buzzfeed.com/laurengarafano/shows-to-watch-after-schitts-creek)                                                            
      - TV Guide: [9 Shows Like Schitt's Creek](https://www.tvguide.com/news/shows-like-schitts-creek-watch-next-netflix-hulu/)                    
      - The Star: [4 great Canadian TV shows not called ‘Schitt’s                                                                                  
      Creek’](https://www.thestar.com/entertainment/television/theres-so-much-more-to-canadian-tv-than-schitts-creek-here-are-four-great-shows/arti
      cle_8c674881-4b54-43a7-8602-94658dccffa8.html)                                                                                               
      - Vulture: [25 Best Canadian Sitcoms to Stream](https://www.vulture.com/article/best-canadian-sitcoms-streaming.html)                        
      - CBC Gem Streaming Platform: https://gem.cbc.ca/                                                                                            
                                                                                                                                                   
      ---                                                                                                                                          
                                                                                                                                                   
      Enjoy exploring these great Canadian TV shows that celebrate the diversity and humor of Canadian life!    
        """),
    }
    {
        "question": "I'm looking for a new umbrella",
        "answer": dedent("""
      Here are some recommended Canadian umbrella options that are made or assembled in Canada or come from Canadian owned and operated
      businesses:                                                                                                                      
                                                                                                                                       
      1. **Midtown Umbrellas**                                                                                                         
         - Canadian company designing, assembling, and shipping umbrellas from Canada.                                                 
         - Product range includes market, cantilever, tilt, and LED patio umbrellas.                                                   
         - Proudly Canadian with free shipping and returns, and 10-year warranty.                                                      
         - Website: https://www.midtownumbrellas.ca/                                                                                   
                                                                                                                                       
      2. **Vancouver Umbrella Inc.**                                                                                                   
         - Women-owned, family-run Canadian business since 1932.                                                                       
         - Design and assembly in British Columbia with emphasis on durable construction, custom branding options, and sustainable     
      materials.                                                                                                                       
         - Offers rain, patio, and golf umbrellas.                                                                                     
         - Website: https://vancouverumbrella.com/                                                                                     
                                                                                                                                       
      3. **Cheeky Umbrella**                                                                                                           
         - Canadian owned and operated based in Vancouver, BC.                                                                         
         - Manufacture their own exclusive line of umbrellas with focus on quality frames and fabrics.                                 
         - Offer custom logo printing on umbrellas and patio umbrellas.                                                                
         - Website: https://cheekyumbrella.com/                                                                                        
                                                                                                                                       
      4. **Urban Nature Store**                                                                                                        
         - Offers designer umbrellas featuring Canadian artist designs and some made in Canada or designed in Canada.                  
         - Umbrellas with unique artwork, folding design, and modern features.                                                         
         - Website: https://www.urbannaturestore.ca/collections/umbrellas                                                              
                                                                                                                                       
      5. **Barrington Brolly**                                                                                                         
         - Established in Gibsons, BC since 1995.                                                                                      
         - Handmade umbrellas and parasols with focus on art and fashion.                                                              
         - Quality often produced in small batch, boutique style.                                                                      
         - Website: [Listed on Made in Canada Directory]                                                                               
                                                                                                                                       
      6. **My Outdoor Room (Umbrellas approximately 95% made in Canada)**                                                              
         - Located in Tillsonburg, ON                                                                                                  
         - Offers umbrellas that are mostly Canadian made.                                                                             
         - Website: [Listed on Made in Canada Directory]                                                                               
                                                                                                                                       
      ---                                                                                                                              
                                                                                                                                       
      | Brand / Company       | Price Range           | Rating / Warranty          | Features                                 | Link   
      | Canadian Owned / Made                  |                                                                                       
      |----------------------|---------------------|---------------------------|------------------------------------------|------------
      ----------------------------------|--------------------------------------|                                                       
      | Midtown Umbrellas     | From CA\$499.99+    | 10-year limited warranty  | Patio & Market umbrellas, Wind resistant |           
      https://www.midtownumbrellas.ca/             | Designed & assembled in Canada       |                                            
      | Vancouver Umbrella    | Custom pricing       | Lifetime limited warranty | Custom brand umbrellas, sustainable      |          
      https://vancouverumbrella.com/                | Designed & assembled in Canada       |                                           
      | Cheeky Umbrella       | Custom pricing       | 1-year Quality Guarantee  | Custom logo umbrellas, premium frames    |          
      https://cheekyumbrella.com/                    | Canadian owned & operated            |                                          
      | Urban Nature Store    | CA\$32.95 - \$41.95  | Not posted                | Artist-designed, folding, auto open/close|          
      https://www.urbannaturestore.ca/collections/umbrellas | Some designed/made in Canada         |                                   
      | Barrington Brolly     | Boutique pricing     | Not posted                | Handmade, art and fashion umbrellas      | Made in  
      Canada Directory listing              | Made in Gibsons, BC                  |                                                   
      | My Outdoor Room       | Not specified        | Not posted                | 95% Canadian made                        | Made in  
      Canada Directory listing              | Mostly Canadian made                 |                                                   
                                                                                                                                       
      ---                                                                                                                              
                                                                                                                                       
      If you desire umbrellas fully or mostly made in Canada, I recommend Midtown Umbrellas, Vancouver Umbrella, and Cheeky Umbrella as
      the top choices. They offer quality, warranty, and local ownership or manufacture. Urban Nature Store offers beautiful           
      artist-designed umbrellas with some Canadian design influence.                                                                   
                                                                                                                                       
      Let me know if you want details on specific models or other umbrella types!  
        """),
    }
]




