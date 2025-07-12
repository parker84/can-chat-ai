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
      Here are some of the best yoga pants options, with a focus on Canadian products and Canadian-owned brands where possible:              
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## 1. Lululemon Align High Rise Leggings                                                                                               
      - **Brand:** Lululemon (Iconic Canadian brand, Vancouver-based)                                                                        
      - **Price:** About $112 CAD (list price on Amazon)                                                                                     
      - **Rating:** 4.5/5 overall from multiple reviewers                                                                                    
      - **Reviews:** Highly praised for comfort, excellent stretch, breathability, and a sleek fit that supports yoga practice seamlessly.   
      Reviewers note it stays in place well without squeezing too tightly.                                                                   
      - **Features:**                                                                                                                        
        - 4-way stretch fabric (81% nylon, 19% Lycra elastane)                                                                               
        - Moisture wicking and breathable                                                                                                    
        - Lightweight and soft "naked sensation" fabric                                                                                      
        - Hidden waistband pocket                                                                                                            
        - Sizes 0-20                                                                                                                         
      - **Made in Canada:** Yes, Lululemon is a Canadian company, though manufacturing is global.                                            
                                                                                                                                             
      **Link:** [Lululemon Align High Rise](https://www.lululemon.com)                                                                       
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## 2. Daub + Design Two-Tone Yoga Pants                                                                                                
      - **Brand:** Daub + Design (Vancouver-based Canadian brand)                                                                            
      - **Price:** Varies (Sold on their website)                                                                                            
      - **Rating:** Positive reviews emphasizing stylish prints and sustainable comfy fabric                                                 
      - **Reviews:** Known for unique prints and softness, ideal for both activewear and everyday comfort.                                   
      - **Features:**                                                                                                                        
        - Sustainable fabrics                                                                                                                
        - Unique prints and two-tone designs                                                                                                 
        - Sizes XS to XL                                                                                                                     
        - Focus on comfort and versatile style                                                                                               
      - **Made in Canada:** Designed and based in Canada, local manufacturing details on their site.                                         
                                                                                                                                             
      **Link:** [Daub + Design](https://daubanddesign.com) (Please verify latest for yoga pants)                                             
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## 3. Azur High-Waisted Yoga Pants                                                                                                     
      - **Brand:** Azur (Canadian brand focused on inclusive sizing)                                                                         
      - **Price:** Varies, typically mid-range                                                                                               
      - **Rating:** Well-reviewed for flattering fit and inclusive sizing up to 18                                                           
      - **Reviews:** Customers love the comfort and flattering shapes designed for curves; good for yoga and activewear.                     
      - **Features:**                                                                                                                        
        - High-waisted design                                                                                                                
        - Sizes 0-18 for bottoms                                                                                                             
        - Colorful options like lavender and eggplant                                                                                        
        - Focused on fit for all body types                                                                                                  
      - **Made in Canada:** Canadian designed with operations in Canada.                                                                     
                                                                                                                                             
      **Link:** [Azur](https://azurfit.com)                                                                                                  
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## 4. Beyond Yoga Spacedye Out Of Pocket High Waisted Midi                                                                             
      - **Brand:** Beyond Yoga (American brand, but well loved in Canada with wide availability)                                             
      - **Price:** Approx. $69 – $99 USD (~$90 – $130 CAD depending on retailer)                                                             
      - **Rating:** 4/5 from users and reviewers                                                                                             
      - **Reviews:** Very soft and comfortable leggings ideal for yoga, casual wear, and travel. Excellent tummy control, flattering fit, and
      useful side pockets.                                                                                                                   
      - **Features:**                                                                                                                        
        - 87% polyester, 13% spandex                                                                                                         
        - Moisture-wicking, 4-way stretch                                                                                                    
        - UV Protection                                                                                                                      
        - Hip pockets                                                                                                                        
        - Sizes XXS-4X                                                                                                                       
      - **Made in Canada:** No (American brand), but widely available in Canada.                                                             
                                                                                                                                             
      **Link:** [Beyond Yoga](https://beyondyoga.com)                                                                                        
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## 5. Titika Active Couture (Toronto-Based Brand)                                                                                      
      - **Brand:** Titika (Canadian-owned, Toronto-based)                                                                                    
      - **Price:** Mid-range to higher end, depending on styles                                                                              
      - **Rating:** Positive reviews for fit and flexible, stylish activewear                                                                
      - **Reviews:** Known for stylish, fun designs with local roots and emphasis on quality and fit.                                        
      - **Features:**                                                                                                                        
        - Activewear pieces, including yoga pants and leggings                                                                               
        - Flexible production with some local control                                                                                        
        - Varied designs, some with built-in bras or lace accents                                                                            
      - **Made in Canada:** Designed in Toronto, production partly local.                                                                    
                                                                                                                                             
      **Link:** [Titika](https://titikacture.com)                                                                                            
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      ## Summary Recommendation:                                                                                                             
                                                                                                                                             
      - For iconic, trusted quality and Canadian roots: **Lululemon Align High Rise** (top pick, though pricier)                             
      - For unique, Canadian designed, and sustainable: **Daub + Design**                                                                    
      - For inclusive sizing and flattering fit: **Azur**                                                                                    
      - For very soft casual and yoga wear: **Beyond Yoga Spacedye** (widely available in Canada but not Canadian-made)                      
      - For Toronto-based flexible activewear: **Titika**                                                                                    
                                                                                                                                             
      ---                                                                                                                                    
                                                                                                                                             
      If you would like, I can also focus search on more budget-friendly options, plus-size sizes, or specific Canadian regions like Toronto,
      Vancouver, or Quebec. Would you like me to? 
        """),
    },
    
]




