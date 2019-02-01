Question 1-4:
python .\review_analysis_q1_4.py

Question 5:
python .\review_analysis_q5.py


sample output:
Filling NaNs with empty strings : Done
Combining review title and text : Done
Making Corpus:
storing the corpus to HD: Donepus: 100.00% Donee
: Done took  31.2 seconds <------------------------------------ TIME 

example review:  Nice : I got the rooster version and the colors are simply gorgeous.  i'm not so much into wearing a farm animal image, but the colors are just too striking to pass this up. the sweater is tts, but with a slightly baggy fit. i did not find it scratchy.
corpus tokenized and cleaned review:  nice get rooster version color simply gorgeous not much wear farm animal image but color strike pas sweater ut but slightly baggy fit not find scratchy

Making document frequency matrix from corpus: : Done
Making document tfidf matrix: : Done
performing LSA on the reviews: : Done
for Query:  ['dissapointed', 'ugly', 'hate', 'reveal', 'bad', 'fit', 'horrible', 'fade', 'return', 'hate', 'not', 'upset', 'old', 'costly', 'pricey', 'hate', 'horrible', 'expensive', 'bad', 'flaw', 'cheap', 'lubricous', 'use', 'fit']
Checking Documents for similarity using TF-IDF: 100.00% Done, took 13.99 seconds <------------------------------------ TIME 
******************* ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************
m
 Sr: *** 1 ***  Index:  6       Similarity:  0.2583367541798979
Stars 5
Review:  Cagrcoal shimmer fun : I aded this in my basket at hte last mintue to see what it would look like in person. (store pick up). i went with teh darkler color only because i am so pale :-) hte color is really gorgeous, and turns out it mathced everythiing i was trying on with it prefectly. it is a little baggy on me and hte xs is hte msallet size (bummer, no petite). i decided to jkeep it though, because as i said, it matvehd everything. my ejans, pants, and the 3 skirts i waas trying on (of which i ]kept all ) oops.

 Sr: *** 2 ***  Index:  10413   Similarity:  0.25536093903292595
Stars 5
Review:  Fun and flirty : So pretty, love hte design on this one.
i tried on hte regualr size, adn will not need a petite, it hit me jsut above my knee. younger gals may oprefer shorter, however.

the aottern is also nice. the cut is flowy and flattering, nothing bad to say about htis dress...

 Sr: *** 3 ***  Index:  19775   Similarity:  0.24513037121805753
Stars 1
Review:  Horrible fit : This shirt looked cute until i tried it on... worst fit ever. im thin, and this style of top is usually quite flattering, but this one missed the mark big time.

 Sr: *** 4 ***  Index:  18462   Similarity:  0.24309447039189389
Stars 2
Review:  Horrible quality : I love maeve dresses and have always gotten a lot of wear out of them while still looking great. this dress does not meet those standards. on the 2nd wear of this dress the zipper completely broke. i had to take it to a dry cleaner to get replaced at a pricey cost for a pricey dress, i'm dissapointed.

 Sr: *** 5 ***  Index:  9583    Similarity:  0.23793569762474273
Stars 1
Review:  Ugly shirt : Really unattractive shirt. nothing good i can say about it. horrible fit. i can't imagine this would look good on anyone.

 Sr: *** 6 ***  Index:  12548   Similarity:  0.22974769297921546
Stars 4
Review:  Cute, but hate the side zipper : I love charlie trousers. i must have 8 pair. i sometimes have bought a particular style in every color. that being said, i love these for the fabric, and general overall fit. pattern is on trend in color and versatility. i wore them out on saturday to a casual restaurant, and today at work with a business like blouse and cardigan. but, i hate the side zip. i generally hate invisible zippers period, because they tend to get caught at seams, and i have had them break on other garments. this one is

 Sr: *** 7 ***  Index:  6949    Similarity:  0.22579039829331338
Stars 2
Review:  Awkward : Maybe i shouldn't have sized up to an xl but i'm not sure a smaller size would have solved the weird fit. the vee is quite low and i'm busty. it'll be really low if you're smaller on top. the fit from back to front where it ties looked horrible on me. not tight at all. it's almost balloon like around the hem and from the side view, i looked like a really wide green apple. i hate leaving a bad review because i know someone may love it but i wouldn't recommend it.

 Sr: *** 8 ***  Index:  10553   Similarity:  0.21943733021656045
Stars 4
Review:  Pretty but short : I tried on the 00p in the store as a return, adn though it would fit (super stretchy)hte dress ended up mid thigh for me... gorgeous design and make though, the buttoning is incredible, buttons and clasps to keep the dress closed. love love, wish htey still had my size (0p or 2p ) to try if hte length would be better (or regular size)

 Sr: *** 9 ***  Index:  18021   Similarity:  0.21720272442790167
Stars 1
Review:  Horrible fabric! : The fabric of this vest is identical to a old white dish cloth! the cut of this vest is also bad! will be sent back!

 Sr: *** 10 *** Index:  6434    Similarity:  0.21434879456276773
Stars 5
Review:  Amazing unique : I want to hate these jeans because they are so expensive but every time i try these on they just look so cool.
they seem to be handmade so the flowers are not in the same spot on each pair.

 Sr: *** 11 *** Index:  12501   Similarity:  0.20593405291614789
Stars 4
Review:  Long in the back : Another really cute iop (i tried on the blue), but if you are short, you definitely ned a petite size. sofy fabric, and pretty pattern, like hte tie nexk. too bad they sold out in my size...

******************* ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************
x
Checking Documents for similarity using LSA: 100.00% Done, took 2.81 seconds <------------------------------------ TIME 
*********** ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************
m
Sr: 1   Index:  18940   Similarity:  0.9879239721559387
Stars 1
Review:  Very strange fit : I'm returning this cardigan. it doesn't fit me at all. it's shapeless and loose.

Sr: 2   Index:  3745    Similarity:  0.9837521092218378
Stars 2
Review:  Does not have a straight line fit : The fabric of this top is lovely. the fit not so. it does not fit as shown on the model. the fit is very large around the middle and fits more like a "swing" top. i am 5'9" slim build. i ordered my usual size medium. shoulders and back fit perfectly. too much material around the middle. had it had a straight cut to it, as shown, i'd keep it. because it doesn't it's going back.

Sr: 3   Index:  22452   Similarity:  0.9815788568647569
Stars 3
Review:  Just ok : I wanted to love this sweater but the fit is off slightly. i ordered my regular size xs and the chest/shoulder area fits nice but the waist comes very tight and not flattering to wear unless style similar to the model with a tucked in look. nice color and decent quality fabric but not my favorite fit. going back to the store.

Sr: 4   Index:  6903    Similarity:  0.9802459610688715
Stars 5
Review:  Amazing dress! : I was hesitant to buy this dress with all the reviews regarding poor fit, particularly in the bust area, but it's so unique that i decided to give it a try anyway by ordering a petite size. i was pleasantly surprised to find that it fits beautifully in my usual size. i did not find the bust to be small at all, and the overall fit was very slimming and flattering. for reference, i am 5'2" 110lbs 32dd, and the size 2p looks great and is very comfortable.  the 0p might have worked too. the material

Sr: 5   Index:  14824   Similarity:  0.9795955015897172
Stars 1
Review:  Weird fit : I am 5' 7" - 110 lbs. ordered my normal xs and the bottom portion was way over sized. it fit like a parachute, you could fit about 12 of me in the bottoms and very short. nice quality material, but extremely awkward fit.

Sr: 6   Index:  732     Similarity:  0.9793171137713487
Stars 1
Review:  Not for me : The fit is not as shown on the website. will be returning.

Sr: 7   Index:  6029    Similarity:  0.9792897171068491
Stars 5
Review:  Cute bohemian dress : I saw this dress and had to have it. it is very cute and comfortable. i have fuller hips, so i'm not sure about the stripe across the widest section of my body. the arm holes are a little gaping as well as other reviewers have mentioned. i bought the medium which fits well everywhere, but the arm holes. i think the small would fit me everywhere, but the hips. so, i'm on the fence of whether to keep it. i do like the dress and it is of good quality; it just may not be the right fit for me. i'm a

Sr: 8   Index:  644     Similarity:  0.9766028951599641
Stars 5
Review:  Great fit : These fit me really well. i tend to have a problem finding trousers that fit my more muscular legs and my waist. usually, if it fits my legs the waist is too big. the trousers have some stretch for a better fit. the only downside is that i had go them hemmed (bought regular size).

Sr: 9   Index:  5331    Similarity:  0.975574958389217
Stars 3
Review:  Not flattering on me : I ordered this online and was disappointed with the fit when it arrived. i ordered the xs and it was still oversize to the point of being unflattering. i am tall 5'9" about 130 pounds and have a fairly thin torso and look best in cloths that have some shape. if you like a loose fit this might be for you. the material is thicker and warm and comfortable. i would suggest ordering down a size.

Sr: 10  Index:  8903    Similarity:  0.9735269956269679
Stars 1
Review:  Poor fit : The fit of this sweater did not flatter my body-type. the top half did not fit well; the armpit area was loose fitting and the neckline was awkward.

Sr: 11  Index:  12940   Similarity:  0.9731105667403084
Stars 5
Review:  Love : There's a free people version of this top and this by far surpasses the fit of it. i'm 5'3 and purchased the xl and it fits me exactly like the model. i would say it is tts and extremely soft.

*********** ENTER m TO SHOW THE NEXT 10 SIMILAR DOCUMENTS, x to exit: *******************
x



Sample output for question 5: python .\review_analysis_q5.py

Filling NaNs with empty strings : Done
Combining review title and text : Done
Importing pre-processed corpus
: Done
Enter a porduct ID: 1060
Making document frequency matrix from corpus: : Done
Using POS tags to extract nouns: Done
Generating 1 - word features: Done
Counting Frequencies
Progress: 100% Done                             .0 mins 0 secss

1137 possible new 1 -word features
discard 205 features not with mminimum required frequency
Generating 2 - word features: Done
Counting Frequencies
Progress: 100% Done                             .0 mins 0 secss

401 possible new 2 -word features
discard 359 features not with mminimum required frequency
Generating 3 - word features: Done
Counting Frequencies
Progress: 100% Done                             .0 mins 0 secs

5 possible new 3 -word features
discard 5 features not with mminimum required frequency
sorting n-word features based on frequency for each n-gram: Done
storing results in a test file named output_q5.txt: Done
9 fit well
         sentiment: 55/100      it fit well on my curvierathletic frame
         sentiment: 70/100      i usually wear a in pants but the large fit well
         sentiment: 55/100      i usually wear an and i purchased a medium and they fit well
         sentiment: 25/100      my measurements are b and i was shocked how well this fits in a regular
         sentiment: 77/100      the small fit me well hanging straight as pictured not too snug or uncomfortable
         sentiment: 55/100      it fit me well everywhere except in the crotch where i was given a slight wedgie
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
         sentiment: 89/100      nice quality is great fits very well at waste i am lb bought size p and its good
         sentiment: 22/100      fit so well and unique pattern at the ankle however as is the case with many white pants so disappointed when i tried them on at home and could see my underwear nude color
7 regular size
         sentiment: 0/100       i do think they run a bit small in the waist because they were a bit too tight in my regular size
         sentiment: 0/100       i tried this in sizes regular petite and regular
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
         sentiment: 0/100       i prefer the regular size for elevenses pants because the
         sentiment: 0/100       i tried the size regular in store
         sentiment: 0/100       i usually order petite but tried on regular size in the store
         sentiment: -15/100     my regular size crushed my girls flattening them and pushing them up over the top of the jumpsuit
4 perfect fit
         sentiment: 87/100      this is a perfect fit for my body shape and when on it looks like a lovely dress
         sentiment: 73/100      im and a bit busty and the medium fit perfect
         sentiment: 88/100      these fit perfect and look great
         sentiment: 73/100      bought the petite and the fit is perfect
4 hip waist
         sentiment: 0/100       i typically wear a medium pounds b waist hip
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
4 size petite
         sentiment: -22/100     i often order petite pants and they work but for this item the crotch was too high for me to wear a petite size and the legs were short enough to look awkward
         sentiment: 20/100      i got the size not petite cut they were sold out
         sentiment: 0/100       the size small was still too large so i ordered a size small petite
         sentiment: 0/100       i tried this in sizes regular petite and regular
3 size fit
         sentiment: 85/100      they are true to the manufacturers sizing i own another pair of pants from elevenses in the same size which runs somewhat large im tall weigh pounds and the size fit perfectly
         sentiment: 54/100      true to size and fit not only that the fabric is very soft and good quality very interesting style of the jumpsuit looks much better in person
         sentiment: 55/100      size regular fit me well on the waist and hips im waist hips
3 perfect length
         sentiment: 57/100      perfect length a
         sentiment: 81/100      perfect i am the length is perfect i can wear it with flat
         sentiment: 57/100      i am and the length is perfect to wear with heels
3 super comfy
         sentiment: 91/100      super comfy super soft super comfy pants
         sentiment: 91/100      super comfy super soft super comfy pants
         sentiment: 91/100      super comfy super soft super comfy pants
2 type body
         sentiment: 27/100      i have a high waist and hourglass shape so jumpers are very hard to find that fit my body type
         sentiment: 76/100      wonderful fit and flatters any body type
2 quality issue
         sentiment: 54/100      loved but both in my store had quality issues i really wanted this
         sentiment: 64/100      i dont want to pay shipping for one that hopefully isnt damaged in the last year ive had multiple quality control issues with retailer
2 jumpsuit love
         sentiment: 93/100      love i love this jumpsuit and definitely feel too confident in it
         sentiment: 63/100      i loved this jumpsuit
2 gateway jumpsuit
         sentiment: 0/100       the gateway jumpsuit im calling this the gateway jumpsuit for all those ladies who are wondering about this whole jumpsuit trend and how they feel about ityou know who you are
         sentiment: 0/100       the gateway jumpsuit im calling this the gateway jumpsuit for all those ladies who are wondering about this whole jumpsuit trend and how they feel about ityou know who you are
2 side pocket
         sentiment: 63/100      and the best park it has side pockets
         sentiment: 44/100      pockets on side are also useful yet discreet
2 fit flatter
         sentiment: 70/100      the stripes are brighter and the fit more flattering
         sentiment: 76/100      wonderful fit and flatters any body type
2 piece clothe
         sentiment: 44/100      i have traveling plans this summer and i am thinking this could be an easy thing to take along with me one piece clothing that will travel very we
         sentiment: 91/100      i really dont like wearing one piece clothing but this one its just so comfy and it looks great i wear it with the straps or strapless and it looks different as you can wear it classy or casual
2 style love
         sentiment: 70/100      love style great fit but so long
         sentiment: 63/100      needs some work i love the style and color of this jumpsuit
2 comfort style
         sentiment: 79/100      i definitely recommend these for anyone who wants both comfort and style
         sentiment: 73/100      very happy with the style and comfort of this jumpsuit
2 spring summer
         sentiment: 0/100       will be able to wear these in the spring summer and into fall
         sentiment: -32/100     these arent super thick or anything so i think theyll do just fine during the spring and summer months when i just need a pair of pants to put on really quick or just to lounge around in
2 tie way
         sentiment: 0/100       there were strings hanging out of the lacy areas and the waist tie ties way higher than
         sentiment: 0/100       there were strings hanging out of the lacy areas and the waist tie ties way higher than
2 side zip
         sentiment: -40/100     the only problem was they are a side zip pant which i didnt know when ordering
         sentiment: 15/100      the fabric is thick but not bulky the side zip is flattering and the buttons add a touch of flair which make the pants look very tailored
2 need belt
         sentiment: 61/100      lovely feminine needs belt for definition id been eyeing this for months loving the look but afraid itd be too young for me im
         sentiment: 63/100      i tried it on in the store and loved it with one caveat it hangs rather like a sack so i think it needs a belt for waist definition
2 jumpsuit fit
         sentiment: 0/100       as soon as i read the reviews i went on and placed an order for size im ft tall lb and it has been very difficult to find a jumpsuit to fit my long torso
         sentiment: 55/100      i seldom find jumpsuits that fit my frame but his one fits perfectly
2 tall person
         sentiment: 87/100      very nice just as pictured this is a very nice jumpsuit reviewers were correct stating that torso is long fit better a taller person
         sentiment: 0/100       maybe on a tall person im only
2 deal breaker
         sentiment: 0/100       this was a deal breaker for me
         sentiment: 0/100       the rise was a bit short but not a deal breaker however they were very long and i hoped that i had shoes that were high enough
2 cute person
         sentiment: 45/100      so much cuter in person
         sentiment: 45/100      cuter in person
