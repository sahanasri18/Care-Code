"""Seed data module: each entry is a list of (name, address, city, pincode, phone, lat, lng, dept_key)."""

STATES = []
"""Seed data: Tamil Nadu (~95 hospitals: metro, medical colleges, DH, private)."""
STATES.append(("Tamil Nadu", [

# (name, address, city, pincode, phone, lat, lng, dept_key)
    # ---- Chennai (25) ----
    ("Apollo Hospitals", "21 Greams Lane, Off Greams Road", "Chennai", "600006", "+91 44 2829 3333", 13.0674, 80.2516, "PR2"),
    ("Fortis Malar Hospital", "52, 1st Main Road, Gandhi Nagar, Adyar", "Chennai", "600020", "+91 44 4933 9444", 13.0017, 80.2565, "PR"),
    ("Sri Ramachandra Medical Center", "1 Ramachandra Nagar, Porur", "Chennai", "600116", "+91 44 2476 8402", 13.0364, 80.1532, "PR"),
    ("MIOT International", "4/112 Mount Poonamallee Road, Manapakkam", "Chennai", "600089", "+91 44 4200 2288", 13.0172, 80.1727, "PR2"),
    ("Kauvery Hospital", "199 Luz Church Road, Mylapore", "Chennai", "600004", "+91 44 4000 2244", 13.0358, 80.2676, "PR"),
    ("Billroth Hospitals", "43 Lakshmi Talkies Road, Shenoy Nagar", "Chennai", "600030", "+91 44 2664 1234", 13.0827, 80.2330, "DH"),
    ("Vijaya Hospitals", "180 NSK Salai, Vadapalani", "Chennai", "600026", "+91 44 4000 0500", 13.0526, 80.2064, "PR"),
    ("Global Hospitals & Health City", "439 Cheran Nagar, Perumbakkam", "Chennai", "600100", "+91 44 6630 0300", 12.9256, 80.2111, "PR2"),
    ("Apollo Children's Hospital", "15 Shafee Mohammed Road, Teynampet", "Chennai", "600006", "+91 44 2829 5000", 13.0304, 80.2461, "CH"),
    ("Chettinad Hospital & Research Institute", "Rajiv Gandhi Salai, Kelambakkam", "Chennai", "603103", "+91 44 4741 1000", 12.8023, 80.2261, "MC"),
    ("Rajiv Gandhi Government General Hospital", "Park Town, E.V.R. Periyar Salai", "Chennai", "600003", "+91 44 2530 5000", 13.0800, 80.2750, "MC"),
    ("Government Stanley Medical College Hospital", "Old Jail Road, Royapuram", "Chennai", "600001", "+91 44 2528 1400", 13.1020, 80.2830, "MC"),
    ("Government Kilpauk Medical College Hospital", "Poonamallee High Road, Kilpauk", "Chennai", "600010", "+91 44 2642 5252", 13.0860, 80.2360, "MC"),
    ("SIMS Hospital", "Shivaji Garden, 1 Jawaharlal Nehru Salai, Vadapalani", "Chennai", "600026", "+91 44 4000 0500", 13.0470, 80.2050, "PR"),
    ("Dr. Mehta's Hospitals", "No. 2, McNichols Road, Chetpet", "Chennai", "600031", "+91 44 4227 1000", 13.0720, 80.2450, "PR"),
    ("Government Royapettah Hospital", "Royapettah High Road, Royapettah", "Chennai", "600014", "+91 44 2848 3563", 13.0570, 80.2660, "DH"),
    ("Hindu Mission Hospital", "14 Christian College Road, Tambaram West", "Chennai", "600045", "+91 44 2226 3555", 12.9240, 80.1200, "PR"),
    ("Sooriya Hospital", "16 IT Highway, Mugappair East", "Chennai", "600037", "+91 44 4061 8000", 13.0830, 80.1830, "PR"),
    ("Sundaram Medical Foundation", "4th Avenue, Shanthi Colony, Anna Nagar", "Chennai", "600040", "+91 44 2626 8044", 13.0890, 80.2140, "PR"),
    ("Frontier Lifeline Hospital", "R-30-C Ambattur Industrial Estate, Mogappair", "Chennai", "600058", "+91 44 4201 7575", 13.0800, 80.1850, "PR"),
    ("Sankara Nethralaya", "18 College Road, Nungambakkam", "Chennai", "600006", "+91 44 4227 1500", 13.0580, 80.2410, "EYE"),
    ("Agarwal Eye Hospital", "19 Cathedral Road, T. Nagar", "Chennai", "600086", "+91 44 2811 3373", 13.0370, 80.2390, "EYE"),
    ("Institute of Child Health & Hospital", "Hall's Road, Egmore", "Chennai", "600008", "+91 44 2819 3700", 13.0770, 80.2590, "CH"),
    ("ESI Hospital", "ESI Hospital Road, K.K. Nagar", "Chennai", "600078", "+91 44 2474 0131", 13.0430, 80.1950, "DH"),
    ("Lifeline Hospitals", "149 Luz Church Road, Mylapore", "Chennai", "600004", "+91 44 2499 4444", 13.0330, 80.2660, "PR"),
    # ---- Coimbatore (8) ----
    ("PSG Institute of Medical Sciences", "Peelamedu, Avinashi Road", "Coimbatore", "641004", "+91 422 434 5200", 11.0189, 76.9647, "MC"),
    ("Kovai Medical Center & Hospital", "Avinashi Road, Civil Aerodrome Post", "Coimbatore", "641014", "+91 422 432 3800", 11.0250, 76.9960, "PR2"),
    ("Ganga Medical Centre & Hospitals", "313 Mettupalayam Road, Ramnagar", "Coimbatore", "641043", "+91 422 248 5000", 11.0180, 76.9570, "ORTH"),
    ("KG Hospital", "Arts College Road, Opp. Tamil Nadu Police Housing", "Coimbatore", "641018", "+91 422 221 2111", 11.0100, 76.9550, "PR"),
    ("Sri Gokulam Hospitals", "737 100 Feet Road, Gandhipuram", "Coimbatore", "641012", "+91 422 435 4444", 11.0177, 76.9698, "PR"),
    ("Apollo Speciality Hospitals", "Nava India Road, Sowripalayam", "Coimbatore", "641028", "+91 422 432 3700", 11.0350, 77.0000, "PR"),
    ("Government Coimbatore Medical College Hospital", "Trichy Road, Sidhapudur", "Coimbatore", "641018", "+91 422 222 4400", 11.0030, 76.9700, "MC"),
    ("Gem Hospital", "45 Government Arts College Road", "Coimbatore", "641018", "+91 422 222 1114", 11.0120, 76.9560, "PR"),
    # ---- Madurai (6) ----
    ("Government Rajaji Hospital", "Palanganatham Road, Corridor", "Madurai", "625020", "+91 452 253 1720", 9.9170, 78.1160, "MC"),
    ("Meenakshi Mission Hospital", "Lake Area, Melur Road", "Madurai", "625107", "+91 452 258 7890", 9.9330, 78.1180, "PR"),
    ("Apollo Speciality Hospitals", "Lake View Road, KK Nagar", "Madurai", "625020", "+91 452 258 0523", 9.9400, 78.1230, "PR"),
    ("Velammal Medical College Hospital", "Anuppanadi, Madurai", "Madurai", "625009", "+91 452 711 1000", 9.8820, 78.1310, "MC"),
    ("Aravind Eye Hospital", "1 Anna Nagar, Madurai", "Madurai", "625020", "+91 452 435 6100", 9.9540, 78.1270, "EYE"),
    ("Devaki Hospitals", "Mahaboobpalayam Road, Madurai", "Madurai", "625001", None, 9.9280, 78.1120, "PR"),
    # ---- Tiruchirappalli (5) ----
    ("K.A.P. Viswanatham Government Medical College Hospital", "Williams Road, Cantonment", "Tiruchirappalli", "620001", "+91 431 241 1721", 10.7970, 78.6860, "MC"),
    ("Apollo Speciality Hospitals", "Door No. 15, W.B. Road, Crawford", "Tiruchirappalli", "620001", "+91 431 407 0700", 10.8170, 78.7040, "PR"),
    ("Kauvery Hospital", "16, Woraiyur Main Road", "Tiruchirappalli", "620003", "+91 431 277 7777", 10.8110, 78.6870, "PR"),
    ("Seethapathy Clinic & Hospital", "47 Nandi Koil Street, Thillai Nagar", "Tiruchirappalli", "620018", None, 10.8070, 78.6940, "PR"),
    ("Chennai Medical College Hospital & Research Centre", "NH-45, Irungalur", "Tiruchirappalli", "620105", "+91 431 274 5999", 10.9370, 78.6810, "MC"),
    # ---- Salem (4) ----
    ("Government Mohan Kumaramangalam Medical College Hospital", "Old Bus Stand Road, Salem", "Salem", "636001", "+91 427 231 1670", 11.6650, 78.1340, "MC"),
    ("Manipal Hospital", "1/126, Salem Main Road, Meyyanur", "Salem", "636004", "+91 427 228 8288", 11.6400, 78.1550, "PR"),
    ("Hindusthan Hospital", "Hindusthan Gardens, 100 Feet Road, Salem", "Salem", "636002", "+91 427 241 0100", 11.6590, 78.1580, "PR"),
    ("Salem Hospital", "41 Saradha College Road, Salem", "Salem", "636007", "+91 427 233 1133", 11.6520, 78.1510, "DH"),
    # ---- Vellore (4) ----
    ("Christian Medical College (CMC)", "IDA Scudder Road, Vellore", "Vellore", "632004", "+91 416 228 2222", 12.9240, 79.1290, "MC"),
    ("Government Vellore Medical College Hospital", "Adukkamparai, Vellore", "Vellore", "632011", "+91 416 226 1418", 12.9030, 79.1330, "MC"),
    ("Apollo KH Hospital", "Karigiri, Katpadi Road", "Vellore", "632106", "+91 416 229 9393", 12.9300, 79.1010, "PR"),
    ("Karigiri Hospital", "S.L.R. Sanatorium, Karigiri", "Vellore", "632106", "+91 416 226 4510", 12.9310, 79.1060, "DH"),
    # ---- Tirunelveli (3) ----
    ("Tirunelveli Medical College Hospital", "High Grounds, Palayamkottai", "Tirunelveli", "627011", "+91 462 257 3001", 8.7300, 77.7200, "MC"),
    ("Apollo Speciality Hospitals", "Gangaikondan, Tirunelveli", "Tirunelveli", "627352", "+91 462 400 0100", 8.7000, 77.7870, "PR"),
    ("Lifeline Multispeciality Hospital", "12-13, NSR Road, Tirunelveli Junction", "Tirunelveli", "627001", None, 8.7190, 77.7520, "PR"),
    # ---- Thanjavur (2) ----
    ("Thanjavur Medical College Hospital", "Medical College Road, Thanjavur", "Thanjavur", "613004", "+91 4362 231 703", 10.7900, 79.1180, "MC"),
    ("Raja Mirasudar Hospital", "Raja Mirasudar Street, Thanjavur", "Thanjavur", "613001", None, 10.7900, 79.1400, "PR"),
    # ---- Erode (2) ----
    ("Government District Headquarters Hospital", "Hospital Road, Erode", "Erode", "638001", "+91 424 221 5656", 11.3410, 77.7200, "DH"),
    ("Kongunad Hospital", "VOC Park Road, Erode", "Erode", "638011", None, 11.3380, 77.7100, "PR"),
    # ---- Tiruppur (2) ----
    ("KG Hospital", "Kamanaiken Palayam, Tiruppur", "Tiruppur", "641604", "+91 421 247 7777", 11.1080, 77.3440, "PR"),
    ("Government District Hospital", "Tiruppur", "Tiruppur", "641601", None, 11.1100, 77.3410, "DH"),
    # ---- Thoothukudi (2) ----
    ("Government Thoothukudi Medical College Hospital", "Ettayapuram Road, Thoothukudi", "Thoothukudi", "628008", "+91 461 232 2830", 8.7700, 78.1300, "MC"),
    ("Hindu Mission Hospital", "WGC Road, Thoothukudi", "Thoothukudi", "628002", None, 8.7620, 78.1360, "DH"),
    # ---- Dindigul (2) ----
    ("Government District Headquarters Hospital", "Dindigul", "Dindigul", "624001", None, 10.3540, 77.9820, "DH"),
    ("Sugam Hospital", "Palani Road, Dindigul", "Dindigul", "624003", None, 10.3620, 77.9760, "PR"),
    # ---- Cuddalore (2) ----
    ("Government District Hospital", "Bharathi Road, Cuddalore", "Cuddalore", "607001", None, 11.7450, 79.7700, "DH"),
    ("Rajah Muthiah Medical College Hospital", "Annamalai Nagar, Chidambaram", "Cuddalore", "608002", "+91 4144 239 929", 11.3990, 79.6930, "MC"),
    # ---- Villupuram (2) ----
    ("Government Medical College Hospital", "Kandachipuram, Villupuram", "Villupuram", "605602", None, 11.9400, 79.4900, "MC"),
    ("A.R. Hospital", "Salem Road, Villupuram", "Villupuram", "605602", None, 11.9370, 79.4940, "PR"),
    # ---- Kanyakumari (2) ----
    ("Kanyakumari Government Medical College Hospital", "Asaripallam, Nagercoil", "Nagercoil", "629201", "+91 4652 252 333", 8.1960, 77.4300, "MC"),
    ("CSI Mission Hospital", "Neyyoor, Kanyakumari District", "Nagercoil", "629802", "+91 4651 222 341", 8.2240, 77.3410, "DH"),
    # ---- Karur (1) ----
    ("Government District Hospital", "K.P. Nagar, Karur", "Karur", "639001", None, 10.9580, 78.0810, "DH"),
    # ---- Namakkal (1) ----
    ("Government District Hospital", "Tiruchengode Road, Namakkal", "Namakkal", "637001", None, 11.2190, 78.1670, "DH"),
    # ---- Virudhunagar (1) ----
    ("Government District Headquarters Hospital", "Madurai Road, Virudhunagar", "Virudhunagar", "626001", None, 9.5860, 77.9570, "DH"),
    # ---- Ramanathapuram (1) ----
    ("Government District Headquarters Hospital", "Ramanathapuram", "Ramanathapuram", "623501", None, 9.3633, 78.8368, "DH"),
    # ---- Pudukkottai (1) ----
    ("Government District Headquarters Hospital", "Anna Salai, Pudukkottai", "Pudukkottai", "622001", None, 10.3813, 78.8178, "DH"),
    # ---- Sivaganga (1) ----
    ("Government District Headquarters Hospital", "Sivaganga", "Sivaganga", "630561", None, 9.8470, 78.4810, "DH"),
    # ---- Theni (1) ----
    ("Government Medical College Hospital", "Theni", "Theni", "625531", None, 10.0100, 77.4770, "MC"),
    # ---- Perambalur (1) ----
    ("Government District Headquarters Hospital", "Perambalur", "Perambalur", "621212", None, 11.2330, 78.8730, "DH"),
    # ---- Ariyalur (1) ----
    ("Government District Headquarters Hospital", "Ariyalur", "Ariyalur", "621704", None, 11.1360, 79.0760, "DH"),
    # ---- Kanchipuram (2) ----
    ("Government District Hospital", "Kanchipuram", "Kanchipuram", "631501", None, 12.8350, 79.7020, "DH"),
    ("Meenakshi Medical College & RI", "Enathur, Kanchipuram", "Kanchipuram", "631552", "+91 44 2727 0100", 12.8470, 79.6870, "MC"),
    # ---- Chengalpattu (2) ----
    ("Chengalpattu Medical College Hospital", "Chengalpattu", "Chengalpattu", "603001", "+91 44 2742 1918", 12.6900, 79.9880, "MC"),
    ("Shree Balaji Medical College Hospital", "Chromepet, Chennai", "Chengalpattu", "600044", "+91 44 2245 4700", 12.9520, 80.1470, "MC"),
    # ---- Tiruvallur (1) ----
    ("Government District Headquarters Hospital", "Tiruvallur", "Tiruvallur", "602001", None, 13.1430, 79.9090, "DH"),
    # ---- Krishnagiri (1) ----
    ("Government District Headquarters Hospital", "Krishnagiri", "Krishnagiri", "635001", None, 12.5270, 78.2140, "DH"),
    # ---- Dharmapuri (1) ----
    ("Government District Headquarters Hospital", "Dharmapuri", "Dharmapuri", "636705", None, 12.1280, 78.1580, "DH"),
    # ---- Udhagamandalam (1) ----
    ("Government District Headquarters Hospital", "Udhagamandalam", "Udhagamandalam", "643001", None, 11.4100, 76.6950, "DH"),
    # ---- Tenkasi (1) ----
    ("Government District Headquarters Hospital", "Tenkasi", "Tenkasi", "627811", None, 8.9590, 77.3150, "DH"),
    # ---- Ranipet (1) ----
    ("Government District Headquarters Hospital", "Ranipet", "Ranipet", "632401", None, 12.9300, 79.3350, "DH"),
    # ---- Kallakurichi (1) ----
    ("Government District Headquarters Hospital", "Kallakurichi", "Kallakurichi", "606202", None, 11.7390, 78.9600, "DH"),
    # ---- Mayiladuthurai (1) ----
    ("Government District Headquarters Hospital", "Mayiladuthurai", "Mayiladuthurai", "609001", None, 11.1010, 79.6520, "DH"),
    # ---- Tiruvannamalai (1) ----
    ("Government District Headquarters Hospital", "Tiruvannamalai", "Tiruvannamalai", "606601", None, 12.2300, 79.0730, "DH"),
]))
