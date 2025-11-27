import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
from collections import Counter

# Curated NICHE blogs - personal/enthusiast sites, NOT general news
TOPIC_URLS = {
    "Food": [
        "https://thepetitecook.com/",
        "https://www.closetcooking.com/",
        "https://erinliveswhile.com/",
        "https://bakingmischief.com/",
        "https://acozykitchen.com/",
        "https://smittenkitchen.com/",
        "https://minimalistbaker.com/",
        "https://cloudykitchen.com/",
        "https://www.saltandlavender.com/",
        "https://katesbetterbite.com/",
        "https://giangiskitchen.com/",
        "https://cookieandkate.com/",
        "https://www.loveandlemons.com/",
        "https://www.twopeasandtheirpod.com/",
        "https://www.acouplecooks.com/",
        "https://greenkitchenstories.com/",
        "https://www.wellplated.com/",
        "https://www.theendlessmeal.com/",
        "https://www.eatingbirdfood.com/",
        "https://www.thehealthymaven.com/",
        "https://spoonfulofflavor.com/",
        "https://www.feastingathome.com/",
        "https://www.thefirstmess.com/",
        "https://www.aspicyperspective.com/",
        "https://downshiftology.com/",
        "https://natashaskitchen.com/",
        "https://ohsheglows.com/",
        "https://rainbowplantlife.com/",
        "https://thefullhelping.com/",
        "https://glow-diaries.com/",
        "https://veganricha.com/"
    ],
    "Music": [
        "https://santarosarecords.com/",
        "https://varioussmallflames.co.uk/",
        "https://obscuresound.com/",
        "https://www.indieshuffle.com/",
        "https://atwoodmagazine.com/",
        "https://www.alfitude.com/",
        "https://www.ear-to-the-ground.com/",
        "https://www.gorillavsbear.com/",
        "https://earmilk.com/",
        "https://www.cougarmicrobes.com/",
        "https://thissongissick.com/",
        "https://neonmusic.co.uk/",
        "https://www.thelineofbestfit.com/",
        "https://thewildhoneypie.com/",
        "https://indieisnotagenre.com/",
        "https://indiecentralmusic.com/",
        "https://aquariumdrunkard.com/",
        "https://fortheloveof bands.com/",
        "https://pigeonsandplanes.com/",
        "https://indiemusicfilter.com/",
        "https://ra.co/",
        "https://5mag.net/",
        "https://deephouseamsterdam.com/",
        "https://deepershadesofhouse.com/",
        "https://xlr8r.com/",
        "https://trommelmusic.com/",
        "https://www.electronicbeats.net/",
        "https://www.dancingastronaut.com/",
        "https://mixmag.net/",
        "https://magneticmag.com/",
        "https://edmtunes.com/"
    ],
    "Travel": [
        "https://www.adventurouskate.com/",
        "https://absolutelylucy.com/",
        "https://heyciarajourney.com/",
        "https://www.jessiejourney.com/",
        "https://theblondeabroad.com/",
        "https://bemytravelmuse.com/",
        "https://www.danflyingsolo.com/",
        "https://expertvagabond.com/",
        "https://www.thebrokebackpacker.com/",
        "https://www.goatsontheroad.com/",
        "https://www.nomadicmatt.com/",
        "https://theplanetd.com/",
        "https://fullsuitcase.com/",
        "https://www.twowanderingsoles.com/",
        "https://coupletraveltheworld.com/",
        "https://www.thepoortraveler.net/",
        "https://travelingwellforless.com/",
        "https://indietraveller.co/",
        "https://www.thebarefootnomad.com/",
        "https://voyagefox.net/",
        "https://jetsetchristina.com/",
        "https://globeguide.ca/",
        "https://jonesaroundtheworld.com/",
        "https://traveloffpath.com/",
        "https://hippie-inheels.com/",
        "https://www.alexinwanderland.com/",
        "https://www.atlasandboots.com/",
        "https://bucketlistly.blog/",
        "https://www.backcountryemily.com/",
        "https://www.thatgirlmags.com/",
        "https://www.ivytrekker.com/",
        "https://www.tessatrek.com/"
    ],
    "Sport": [
        "https://themastermindsite.com/",
        "https://spielverlagerung.com/",
        "https://totalfootballanalysis.com/",
        "https://breakingthelines.com/",
        "https://www.thefalse9.com/",
        "https://holdingmidfield.com/",
        "https://diamondfootballtactics.com/",
        "https://analyticsfc.co.uk/",
        "https://www.the-footballanalyst.com/",
        "https://www.zonalmarking.net/",
        "https://statsbomb.com/",
        "https://www.fangraphs.com/",
        "https://www.arseblog.com/",
        "https://runningthepipe.com/",
        "https://marathonhandbook.com/",
        "https://stephpiruns.com/",
        "https://cleverhiker.com/",
        "https://www.backcountryemily.com/",
        "https://theplayerstribune.com/",
        "https://coachingtoolbox.net/",
        "https://www.runnersworld.com/",
        "https://backpacker.com/",
        "https://www.backpackermagazine.com/",
        "https://www.cleverhiker.com/",
        "https://www.thatgirlmags.com/",
        "https://www.ivytrekker.com/",
        "https://www.tessatrek.com/",
        "https://www.onthegofitnesspro.com/",
        "https://www.trailmothersgroup.org/",
        "https://www.forevershewanders.com/"
    ],
    "Art": [
        "https://www.booooooom.com/",
        "https://www.thisiscolossal.com/",
        "https://www.thejealouscurator.com/",
        "https://art21.org/",
        "https://www.juxtapoz.com/",
        "https://aesthetica.art/",
        "https://www.beautifulbizarre.net/",
        "https://fromlight2art.com/",
        "https://www.artsyshark.com/",
        "https://designyoutrust.com/",
        "https://www.creativeboom.com/",
        "https://emptyeasel.com/",
        "https://artbizsuccess.com/",
        "https://www.designboom.com/",
        "https://www.contemporaryartdaily.com/",
        "https://www.itsnicethat.com/",
        "https://www.streetartnews.net/",
        "https://www.widewalls.ch/",
        "https://www.artnews.com/",
        "https://hyperallergic.com/",
        "https://www.artforum.com/",
        "https://artobserved.com/",
        "https://spoke-art.com/",
        "https://mymodernmet.com/",
        "https://weandthecolor.com/",
        "https://streetartutopia.com/",
        "https://streetartnyc.org/",
        "https://www.streetartaddict.nl/",
        "https://www.hookedblog.co.uk/",
        "https://vandalog.com/",
        "https://www.inspiringcity.com/"
    ]
}

def fetch_blog_keywords(url):
    """Fetch a blog and extract keywords using TextBlob."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text()
        
        # Use TextBlob to extract noun phrases (keywords)
        blob = TextBlob(text)
        phrases = [p.lower() for p in blob.noun_phrases if len(p) > 3]
        
        # Get sentiment
        sentiment = blob.sentiment.polarity
        
        return phrases, sentiment
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return [], 0.0

def train_topic_models():
    """Train topic models by analyzing blogs and extracting common keywords."""
    topic_models = {}
    
    for topic, urls in TOPIC_URLS.items():
        print(f"\nTraining {topic}...")
        all_keywords = []
        all_sentiments = []
        
        for url in urls:
            print(f"  Analyzing: {url}")
            keywords, sentiment = fetch_blog_keywords(url)
            all_keywords.extend(keywords)
            all_sentiments.append(sentiment)
        
        # Find most common keywords
        keyword_counts = Counter(all_keywords)
        top_keywords = [kw for kw, count in keyword_counts.most_common(50)]
        
        # Average sentiment
        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0
        
        topic_models[topic] = {
            "keywords": top_keywords,
            "avg_sentiment": avg_sentiment
        }
        
        print(f"  Found {len(top_keywords)} keywords")
    
    # Save to JSON
    with open('topic_models.json', 'w') as f:
        json.dump(topic_models, f, indent=2)
    
    print("\nTopic models saved to topic_models.json")

if __name__ == "__main__":
    train_topic_models()
