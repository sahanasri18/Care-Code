"""Seed data module: each entry is a list of (name, address, city, pincode, phone, lat, lng, dept_key)."""

STATES = []
"""Seed data: east & northeast (West Bengal, Bihar, Odisha, Jharkhand, Assam, NE states, Andaman & Nicobar)."""
STATES.append(("West Bengal", [

# (name, address, city, pincode, phone, lat, lng, dept_key)
    ("Fortis Hospital", "730 Anandapur, EM Bypass", "Kolkata", "700107", "+91 33 6621 4444", 22.5050, 88.4036, "PR2"),
    ("AMRI Hospitals", "P-4 & 5, CIT Scheme LXXVI, Sector 1, Salt Lake City", "Kolkata", "700064", "+91 33 6680 0000", 22.5787, 88.4206, "PR"),
    ("Apollo Gleneagles Hospital", "58 Canal Circular Road", "Kolkata", "700054", "+91 33 2320 3040", 22.5740, 88.3956, "PR2"),
    ("Medica Superspecialty Hospital", "127 Mukundapur, EM Bypass", "Kolkata", "700099", "+91 33 6624 0000", 22.5040, 88.4090, "PR"),
    ("Peerless Hospital", "360 Panchasayar, Garia", "Kolkata", "700094", "+91 33 2411 5555", 22.4624, 88.4040, "PR"),
    ("R.G. Kar Medical College & Hospital", "1 Khudiram Bose Sarani", "Kolkata", "700004", "+91 33 2555 6580", 22.5880, 88.3580, "MC"),
    ("Institute of Post Graduate Medical Education & Research (SSKM)", "244 AJC Bose Road", "Kolkata", "700020", "+91 33 2204 1270", 22.5350, 88.3380, "MC"),
    ("NRS Medical College & Hospital", "138 AJC Bose Road", "Kolkata", "700014", "+91 33 2286 0721", 22.5620, 88.3490, "MC"),
    ("Howrah District Hospital", "Howrah", "Howrah", "711101", None, 22.5880, 88.3180, "DH"),
    ("IQ City Medical College", "Durgapur", "Durgapur", "713206", "+91 343 655 4444", 23.4960, 87.3240, "MC"),
    ("AMRI Hospital", "Durgapur", "Durgapur", "713206", "+91 343 253 3040", 23.4830, 87.3410, "PR"),
    ("North Bengal Medical College", "Sushrutanagar, Siliguri", "Siliguri", "734012", "+91 353 269 6175", 26.7040, 88.3750, "MC"),
    ("Neotia Getwel Multispeciality Hospital", "Dokra, Naxalbari, Siliguri", "Siliguri", "734009", "+91 353 660 3333", 26.7140, 88.3970, "PR"),
    ("Asansol District Hospital", "Asansol", "Asansol", "713301", None, 23.6900, 86.9700, "DH"),
    ("Kharagpur District Hospital", "Kharagpur", "Kharagpur", "721301", None, 22.3390, 87.3200, "DH"),
    ("Burdwan Medical College", "Bardhaman", "Bardhaman", "713104", "+91 342 265 9683", 23.2350, 87.8610, "MC"),
    ("Malda Medical College & Hospital", "Malda", "Malda", "732101", "+91 3512 252 695", 25.0030, 88.1410, "MC"),
    ("Jalpaiguri District Hospital", "Jalpaiguri", "Jalpaiguri", "735101", None, 26.5240, 88.7330, "DH"),
    ("Darjeeling District Hospital", "Darjeeling", "Darjeeling", "734101", None, 27.0410, 88.2630, "DH"),
    ("Midnapore Medical College & Hospital", "Medinipur", "Medinipur", "721101", "+91 3222 275 496", 22.4220, 87.3200, "MC"),
    ("Bankura Sammilani Medical College", "Bankura", "Bankura", "722101", "+91 3242 251 449", 23.2320, 87.0650, "MC"),
    ("Murshidabad Medical College & Hospital", "Berhampore", "Berhampore", "742101", "+91 3482 259 138", 24.0990, 88.2690, "MC"),
]))

STATES.append(("Bihar", [
    ("Patna Medical College & Hospital", "Ashok Rajpath, Patna", "Patna", "800004", "+91 612 230 0070", 25.6000, 85.1690, "MC"),
    ("AIIMS Patna", "Phulwarisharif, Patna", "Patna", "801507", "+91 612 245 1000", 25.6100, 85.1410, "MC"),
    ("Paras HMRI Hospital", "Patliputra Colony, Patna", "Patna", "800013", "+91 612 415 0000", 25.6040, 85.1250, "PR"),
    ("Ruban Memorial Hospital", "Bailey Road, Patna", "Patna", "801503", "+91 612 297 2700", 25.6080, 85.1010, "PR"),
    ("Anugrah Narayan Magadh Medical College", "Gaya", "Gaya", "823001", "+91 631 222 5775", 24.7900, 85.0000, "MC"),
    ("Jawaharlal Nehru Medical College", "Bhagalpur", "Bhagalpur", "812001", "+91 641 250 1011", 25.2450, 86.9920, "MC"),
    ("Sri Krishna Medical College", "Muzaffarpur", "Muzaffarpur", "842004", "+91 621 227 2211", 26.1250, 85.3900, "MC"),
    ("Darbhanga Medical College", "Laheriasarai, Darbhanga", "Darbhanga", "846003", "+91 6272 243 500", 26.1520, 85.8970, "MC"),
    ("Purnia District Hospital", "Purnia", "Purnia", "854301", None, 25.7800, 87.4750, "DH"),
    ("Saran District Hospital", "Chapra", "Chapra", "841301", None, 25.7800, 84.7500, "DH"),
    ("Government Medical College", "Bettiah, West Champaran", "Bettiah", "845438", "+91 6254 241 381", 26.8020, 84.5030, "MC"),
    ("Munger District Hospital", "Munger", "Munger", "811201", None, 25.3800, 86.4650, "DH"),
    ("Arrah District Hospital", "Arrah", "Arrah", "802301", None, 25.5570, 84.6630, "DH"),
    ("Narayan Medical College & Hospital", "Jamuhar, Sasaram", "Sasaram", "821310", "+91 6184 200 501", 24.9800, 83.9400, "MC"),
]))

STATES.append(("Odisha", [
    ("AIIMS Bhubaneswar", "Sijua, Patrapada, Bhubaneswar", "Bhubaneswar", "751019", "+91 674 237 6400", 20.2440, 85.7950, "MC"),
    ("Kalinga Institute of Medical Sciences (KIMS)", "Patia, Bhubaneswar", "Bhubaneswar", "751024", "+91 674 272 5111", 20.2830, 85.7930, "MC"),
    ("SUM Ultimate Medicare (SUMUM)", "K-8, Kalinga Nagar, Bhubaneswar", "Bhubaneswar", "751003", "+91 674 230 6666", 20.2890, 85.8060, "PR"),
    ("Apollo Hospitals", "Plot No 251, Sainik School Road, Bhubaneswar", "Bhubaneswar", "751005", "+91 674 666 6600", 20.2770, 85.8240, "PR"),
    ("SCB Medical College & Hospital", "Manglabag, Cuttack", "Cuttack", "753007", "+91 671 250 4444", 20.4600, 85.8860, "MC"),
    ("Acharya Harihar Regional Cancer Centre", "Manglabag, Cuttack", "Cuttack", "753007", "+91 671 250 5531", 20.4600, 85.8750, "ONC"),
    ("Ispat General Hospital", "Sector 19, Rourkela", "Rourkela", "769005", "+91 661 264 1300", 22.2400, 84.8400, "DH"),
    ("MKCG Medical College & Hospital", "Berhampur", "Berhampur", "760004", "+91 680 224 4024", 19.3150, 84.7930, "MC"),
    ("Veer Surendra Sai Institute of Medical Sciences", "Burla, Sambalpur", "Sambalpur", "768017", "+91 663 243 0352", 21.4700, 83.9700, "MC"),
    ("District Headquarters Hospital", "Puri", "Puri", "752001", None, 19.8100, 85.8290, "DH"),
    ("District Headquarters Hospital", "Balasore", "Balasore", "756001", None, 21.4930, 86.9330, "DH"),
    ("District Headquarters Hospital", "Panikoili, Jajpur", "Jajpur", "755001", None, 20.8500, 86.1100, "DH"),
    ("District Headquarters Hospital", "Angul", "Angul", "759122", None, 20.8400, 85.1000, "DH"),
    ("Pandit Raghunath Murmu Medical College", "Baripada", "Baripada", "757001", "+91 6792 252 551", 21.9400, 86.7400, "MC"),
    ("District Headquarters Hospital", "Bhadrak", "Bhadrak", "756100", None, 21.0550, 86.5140, "DH"),
    ("District Headquarters Hospital", "Jharsuguda", "Jharsuguda", "768201", None, 21.8600, 84.0100, "DH"),
]))

STATES.append(("Jharkhand", [
    ("Rajendra Institute of Medical Sciences (RIMS)", "Bariatu Road, Ranchi", "Ranchi", "834009", "+91 651 254 0261", 23.3640, 85.3250, "MC"),
    ("Orchid Medical Centre", "5 Main Road, Ranchi", "Ranchi", "834001", "+91 651 236 0333", 23.3450, 85.3100, "PR"),
    ("Tata Main Hospital", "Tata Main Road, Jamshedpur", "Jamshedpur", "831001", "+91 657 242 6000", 22.8030, 86.1820, "DH"),
    ("Brahmananda Narayana Multispeciality Hospital", "Dhatkidih, Jamshedpur", "Jamshedpur", "831001", "+91 657 664 6666", 22.7920, 86.1970, "PR"),
    ("Patliputra Medical College & Hospital", "Dhanbad", "Dhanbad", "826001", "+91 326 230 0231", 23.7930, 86.4300, "MC"),
    ("Bokaro General Hospital", "Sector 4, Bokaro Steel City", "Bokaro", "827004", "+91 6542 235 000", 23.6760, 86.1480, "DH"),
    ("District Hospital", "Hazaribagh", "Hazaribagh", "825301", None, 23.9940, 85.3630, "DH"),
    ("AIIMS Deoghar", "Deoghar", "Deoghar", "814152", "+91 6432 213 111", 24.4640, 86.7050, "MC"),
    ("District Hospital", "Giridih", "Giridih", "815301", None, 24.1870, 86.3000, "DH"),
]))

STATES.append(("Assam", [
    ("Gauhati Medical College & Hospital", "Bhangagarh, Guwahati", "Guwahati", "781032", "+91 361 252 9929", 26.1500, 91.7600, "MC"),
    ("Apollo Excelcare Hospital", "Ganeshguri, Guwahati", "Guwahati", "781006", "+91 361 712 9000", 26.1520, 91.7440, "PR"),
    ("GNRC Hospitals", "Six Mile, Guwahati", "Guwahati", "781022", "+91 361 223 2222", 26.1530, 91.7750, "PR"),
    ("Down Town Hospital", "G.S. Road, Dispur, Guwahati", "Guwahati", "781006", "+91 361 712 2222", 26.1660, 91.7710, "PR"),
    ("Assam Medical College & Hospital", "Dibrugarh", "Dibrugarh", "786002", "+91 373 230 0100", 27.4830, 94.9100, "MC"),
    ("Silchar Medical College & Hospital", "Ghungoor, Silchar", "Silchar", "788014", "+91 3842 264 217", 24.8270, 92.7900, "MC"),
    ("Jorhat Civil Hospital", "Jorhat", "Jorhat", "785001", None, 26.7580, 94.2170, "DH"),
    ("Tezpur Medical College & Hospital", "Tezpur", "Tezpur", "784001", "+91 3712 271 740", 26.6530, 92.7800, "MC"),
    ("Nagaon Civil Hospital", "Nagaon", "Nagaon", "782001", None, 26.3480, 92.6840, "DH"),
    ("Bongaigaon Civil Hospital", "Bongaigaon", "Bongaigaon", "783380", None, 26.4780, 90.5580, "DH"),
    ("Dhubri Civil Hospital", "Dhubri", "Dhubri", "783301", None, 26.0220, 89.9710, "DH"),
    ("North Lakhimpur Civil Hospital", "Lakhimpur", "Lakhimpur", "787001", None, 27.2400, 94.1150, "DH"),
]))

STATES.append(("Arunachal Pradesh", [
    ("Rajiv Gandhi Government Hospital", "Itanagar", "Itanagar", "791111", "+91 360 221 2191", 27.1020, 93.6200, "DH"),
    ("Tomo Riba Institute of Health & Medical Sciences", "Naharlagun, Itanagar", "Itanagar", "791110", "+91 360 224 5725", 27.0930, 93.5980, "MC"),
    ("District Hospital", "Pasighat, East Siang", "Pasighat", "791102", None, 28.0660, 95.3260, "DH"),
    ("District Hospital", "Tawang", "Tawang", "790104", None, 27.5880, 91.8690, "DH"),
]))

STATES.append(("Manipur", [
    ("Regional Institute of Medical Sciences (RIMS)", "Lamphelpat, Imphal", "Imphal", "795004", "+91 385 241 4190", 24.8070, 93.9240, "MC"),
    ("Jawaharlal Nehru Institute of Medical Sciences (JNIMS)", "Porompat, Imphal", "Imphal", "795005", "+91 385 246 1056", 24.8170, 93.9390, "MC"),
    ("District Hospital", "Churachandpur", "Churachandpur", "795128", None, 24.3340, 93.6910, "DH"),
    ("District Hospital", "Thoubal", "Thoubal", "795138", None, 24.6300, 93.9900, "DH"),
]))

STATES.append(("Meghalaya", [
    ("North Eastern Indira Gandhi Regional Institute of Health & Medical Sciences (NEIGRIHMS)", "Mawdiangdiang, Shillong", "Shillong", "793018", "+91 364 253 8024", 25.5420, 91.8900, "MC"),
    ("Civil Hospital", "Shillong", "Shillong", "793001", "+91 364 222 4522", 25.5680, 91.8770, "DH"),
    ("Civil Hospital", "Tura", "Tura", "794001", None, 25.5140, 90.2080, "DH"),
    ("Civil Hospital", "Jowai", "Jowai", "793150", None, 25.4400, 92.2010, "DH"),
]))

STATES.append(("Mizoram", [
    ("Civil Hospital", "Aizawl", "Aizawl", "796001", "+91 389 232 3398", 23.7270, 92.7170, "DH"),
    ("Zoram Medical College", "Falkawn, Aizawl", "Aizawl", "796017", "+91 389 233 4879", 23.7250, 92.7030, "MC"),
    ("District Hospital", "Lunglei", "Lunglei", "796701", None, 22.8920, 92.7350, "DH"),
    ("District Hospital", "Champhai", "Champhai", "796321", None, 23.4560, 93.3290, "DH"),
]))

STATES.append(("Nagaland", [
    ("Naga Hospital Authority", "Kohima", "Kohima", "797001", "+91 370 224 2588", 25.6750, 94.1090, "DH"),
    ("Christian Institute of Health Sciences & Research (CIHSR)", "Meriema, Dimapur", "Dimapur", "797112", "+91 3862 242 030", 25.8920, 93.7460, "PR"),
    ("District Hospital", "Dimapur", "Dimapur", "797112", None, 25.9000, 93.7200, "DH"),
    ("District Hospital", "Mokokchung", "Mokokchung", "798601", None, 26.3260, 94.5120, "DH"),
]))

STATES.append(("Tripura", [
    ("Agartala Government Medical College", "Agartala", "Agartala", "799006", "+91 381 235 4247", 23.8340, 91.2870, "MC"),
    ("IGM District Hospital", "Agartala", "Agartala", "799001", None, 23.8280, 91.2750, "DH"),
    ("District Hospital", "Udaipur, Gomati", "Udaipur", "799120", None, 23.5320, 91.4790, "DH"),
    ("District Hospital", "Dharmanagar", "Dharmanagar", "799250", None, 24.3740, 92.1630, "DH"),
]))

STATES.append(("Sikkim", [
    ("Sir Thutob Namgyal Memorial (STNM) Hospital", "Tadong, Gangtok", "Gangtok", "737102", "+91 3592 231 577", 27.3310, 88.6130, "DH"),
    ("Central Referral Hospital", "Tadong, Gangtok", "Gangtok", "737102", "+91 3592 231 424", 27.3370, 88.6260, "MC"),
    ("District Hospital", "Namchi", "Namchi", "737126", None, 27.1680, 88.3500, "DH"),
    ("District Hospital", "Gyalshing", "Gyalshing", "737111", None, 27.2900, 88.2580, "DH"),
]))

STATES.append(("Andaman and Nicobar Islands", [
    ("G.B. Pant Hospital", "Port Blair", "Port Blair", "744101", "+91 3192 232 519", 11.6230, 92.7340, "DH"),
    ("District Hospital", "Mayabunder", "Mayabunder", "744204", None, 12.9330, 92.9200, "DH"),
]))
