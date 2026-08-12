"""Verified capstone query/return evidence shared across weekly reviews.

Only exact pairs recorded in the corrected canonical notebooks are included.
Weeks 5, 7, 8, 10, 11, 12, and 13 do not add a new verified return in the
available repository evidence; their reviews therefore reuse the latest
recoverable cumulative dataset and report the gap explicitly.
"""

from __future__ import annotations

DIMENSIONS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}

EARLY_QUERIES = {
    1: [[.375440,.950714],[.536429,.835362],[.614168,.334143],[.872626,.321598]],
    2: [[.375440,.950714],[.978752,.932731],[.000006,.334143],[.197553,.808683]],
    3: [[.444444,.666666,.333333],[.657452,.998464,.817253],[.670026,.057881,.658241],[.650132,.218327,.110542]],
    4: [[.555555,.444444,.222222,.111111],[.006280,.281840,.932013,.960202],[.394519,.361122,.256803,.461856],[.715715,.504442,.275065,.552962]],
    5: [[.224189,.846480,.879484,.878515],[.255841,.841692,.888984,.860260],[.255842,.841692,.888985,.860266],[0.,0.,0.,0.]],
    6: [[.728186,.154693,.732552,.693997,.564013],[.433654,.486678,.282753,.972905,.323321],[.495070,.097152,.672921,.000007,.351268],[.973181,.022807,.714484,.145453,.974790]],
    7: [[.045091,.528666,.329265,.105350,.434667,.641164],[.243848,.900100,.696978,.193630,.374149,.826324],[.143585,.302559,.571101,.194533,.395561,.815792],[.045103,.016167,.773003,.156031,.147073,.616114]],
    8: [[.273673,.260400,.073937,.078562,.862321,.230729,.106880,.352588],[.163160,.184786,.152644,.083802,.999322,.544113,.184124,.123846],[.088894,.525132,.030986,.992538,.870819,.217060,.011239,.447691],[.356502,.157574,.172997,.610561,.106477,.260297,.411421,.904740]],
}

EARLY_OUTPUTS = {
    1: [-1.560646704467778e-117,1.674933466363685e-36,-1.0755942664604116e-32,-2.4666412561217706e-107],
    2: [-.03182956281754251,.022666631114895516,.04868370128566149,.038774938576018964],
    3: [-.04090761844901528,-.08987474979637637,-.18323876643005035,-.08251349582236739],
    4: [-8.727516493155957,-31.73535839431216,-1.9810750402526334,-9.312811809021998],
    5: [1088.8535114737463,1035.6341457754475,1035.6647479285914,163.1225],
    6: [-1.1520351120911565,-.8782405650300305,-1.339542402620705,-2.4375082517089726],
    7: [1.0510148516295004,.308765180253091,2.149905456773691,1.2087334449610816],
    8: [9.8157087929671,9.9399041910574,8.9636037557014,9.2540644925525],
}

WEEK_6_QUERIES = {1:[.897714,.081699],2:[.555332,.360931],3:[.522231,.090709,.451742],4:[.713766,.198601,.014095,.068347],5:[.754614,.504566,.432986,.307039],6:[.824244,.022732,.960907,.041715,.897560],7:[.052337,.910075,.727790,.075231,.386516,.492629],8:[.110992,.462977,.255313,.963757,.895383,.716713,.030436,.083412]}
WEEK_6_OUTPUTS = {1:7.651210225556565e-239,2:.22078072799826579,3:-.05739710166867316,4:-17.92630659900679,5:.9401160531598542,6:-2.5293691850310744,7:.19078262729854223,8:9.1386093133071}

WEEK_9_QUERIES = {1:[.421410,.935804],2:[.995366,.102732],3:[.449035,.664262,.290384],4:[.889493,.002958,.445975,.774547],5:[.319924,.675406,.431628,1.],6:[.711755,.175670,.738396,.689597,.562717],7:[.018603,.530937,.376818,.094048,.443567,.614974],8:[.321258,.232284,.021301,0.,.895967,.249315,.054463,.073967]}
WEEK_9_OUTPUTS = {1:-3.089423814911752e-96,2:.049406460222616564,3:-.08189344986566433,4:-23.42280313862202,5:430.8031249775375,6:-1.1717131510084098,7:1.009840334573839,8:9.6998918101966}

# Number of early exact pairs recoverable at each review point.
EARLY_PAIR_COUNT = {2: 1, 3: 2, 4: 2, 5: 4, 6: 2, 7: 4, 8: 2, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4}
INCLUDE_WEEK_6 = {7, 8, 9, 10, 11, 12, 13}
INCLUDE_WEEK_9 = {10, 11, 12, 13}
EVIDENCE_GAPS = {
    2: "No gap in the Week 1 return used for this review.",
    3: "No gap in the Week 2 return used for this review.",
    4: "Week 3 returned observations are unavailable; evidence remains confirmed through Week 2.",
    5: "The four early exact pairs are recoverable, but their original weekly archive provenance is incomplete.",
    6: "Weeks 3–5 returns are incomplete; this review uses the two early confirmed pairs.",
    7: "Week 5 return is unavailable; the dataset contains four early pairs plus the exact Week 6 pair.",
    8: "Weeks 3–5 and 7 returns are unavailable; the latest exact pair is Week 6.",
    9: "Week 8 return is unavailable; four early pairs and the Week 6 pair are recoverable.",
    10: "Weeks 5, 7, 8, and 10 returns are unavailable; Week 9 is the latest exact pair.",
    11: "Weeks 5, 7, 8, and 10 returns are unavailable. The local Week 11 arrays contain duplicate sentinel values, cross-function outputs, and altered coordinates, so they are quarantined; Week 9 is the latest exact pair.",
    12: "The corrupted Week 11 arrays remain quarantined and no verified Week 11 or Week 12 return is present; this review inherits the latest exact evidence.",
    13: "The corrupted Week 11 arrays remain quarantined and no verified Week 11–13 return is present; this review inherits the latest exact evidence.",
}

def recorded_pairs(week: int, function: int):
    """Return exact non-starter pairs recoverable for a weekly review."""
    if week not in EARLY_PAIR_COUNT or function not in DIMENSIONS:
        raise ValueError("week must be 2..13 and function must be 1..8")
    count = EARLY_PAIR_COUNT[week]
    pairs = list(zip(EARLY_QUERIES[function][:count], EARLY_OUTPUTS[function][:count]))
    if week in INCLUDE_WEEK_6:
        pairs.append((WEEK_6_QUERIES[function], WEEK_6_OUTPUTS[function]))
    if week in INCLUDE_WEEK_9:
        pairs.append((WEEK_9_QUERIES[function], WEEK_9_OUTPUTS[function]))
    return pairs
