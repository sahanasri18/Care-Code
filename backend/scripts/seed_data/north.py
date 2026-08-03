"""Seed data module: each entry is a list of (name, address, city, pincode, phone, lat, lng, dept_key)."""

STATES = []
"""Seed data: north (Delhi, Uttar Pradesh, Haryana, Punjab, Rajasthan, J&K, Uttarakhand, Himachal, Chandigarh, Ladakh)."""
STATES.append(("Delhi", [

# (name, address, city, pincode, phone, lat, lng, dept_key)
    ("Indraprastha Apollo Hospitals", "Mathura Road, Sarita Vihar", "New Delhi", "110076", "+91 11 2692 5801", 28.5284, 77.2893, "PR2"),
    ("AIIMS", "Ansari Nagar, East Gate, Aurobindo Marg", "New Delhi", "110029", "+91 11 2658 8500", 28.5672, 77.2100, "MC"),
    ("Fortis Escorts Heart Institute", "Okhla Road", "New Delhi", "110025", "+91 11 4713 5000", 28.5570, 77.2651, "PR"),
    ("Max Super Speciality Hospital", "1 Press Enclave Road, Saket", "New Delhi", "110017", "+91 11 2651 5050", 28.5254, 77.2164, "PR2"),
    ("BLK-Max Super Speciality Hospital", "Pusa Road, Rajendra Place", "New Delhi", "110005", "+91 11 3040 3040", 28.6427, 77.1803, "PR2"),
    ("Sir Ganga Ram Hospital", "Rajinder Nagar", "New Delhi", "110060", "+91 11 4225 4000", 28.6422, 77.1923, "PR2"),
    ("Dr. Ram Manohar Lohia Hospital", "Baba Kharak Singh Marg", "New Delhi", "110001", "+91 11 2374 1640", 28.6280, 77.2110, "MC"),
    ("Safdarjung Hospital", "Aurobindo Marg", "New Delhi", "110029", "+91 11 2670 7444", 28.5670, 77.2030, "MC"),
    ("Lady Hardinge Medical College", "Shaheed Bhagat Singh Marg, DIZ Area", "New Delhi", "110001", "+91 11 2340 8260", 28.6390, 77.2080, "MC"),
    ("Guru Tegh Bahadur Hospital", "Dilshad Garden", "New Delhi", "110095", "+91 11 2258 6300", 28.6860, 77.3020, "MC"),
    ("Max Super Speciality Hospital", "Shalimar Bagh", "New Delhi", "110088", "+91 11 4112 2233", 28.7170, 77.1580, "PR"),
    ("Fortis Hospital", "Shalimar Bagh", "New Delhi", "110088", "+91 11 4530 2222", 28.7220, 77.1600, "PR"),
    ("Batra Hospital", "1 Tughlakabad Institutional Area", "New Delhi", "110062", "+91 11 2995 8747", 28.5500, 77.2220, "PR"),
    ("Holy Family Hospital", "Okhla Road", "New Delhi", "110025", "+91 11 2684 7027", 28.5800, 77.2700, "PR"),
    ("Rajiv Gandhi Cancer Institute", "Sector 5, Rohini", "New Delhi", "110085", "+91 11 4702 2222", 28.7000, 77.1220, "ONC"),
]))

STATES.append(("Uttar Pradesh", [
    ("King George's Medical University (KGMU)", "Chowk, Lucknow", "Lucknow", "226003", "+91 522 225 7432", 26.8730, 80.9160, "MC"),
    ("Sanjay Gandhi Postgraduate Institute of Medical Sciences", "Raebareli Road, Lucknow", "Lucknow", "226014", "+91 522 249 4000", 26.9100, 80.9900, "MC"),
    ("Medanta Hospital", "Sector A, Bargawan, Lucknow", "Lucknow", "226028", "+91 522 400 7000", 26.7800, 80.9500, "PR"),
    ("Sahara Hospital", "Viraj Khand, Gomti Nagar, Lucknow", "Lucknow", "226010", "+91 522 401 1000", 26.8500, 80.9400, "PR"),
    ("Apollomedics Super Speciality Hospital", "Kanpur Road, Lucknow", "Lucknow", "226012", "+91 522 678 1000", 26.7800, 80.9360, "PR"),
    ("Dr. Ram Manohar Lohia Institute of Medical Sciences", "Vibhuti Khand, Gomti Nagar, Lucknow", "Lucknow", "226010", "+91 522 491 8400", 26.8420, 80.9770, "MC"),
    ("Jaypee Hospital", "Sector 128, Noida", "Noida", "201304", "+91 120 456 0000", 28.6100, 77.3700, "PR2"),
    ("Fortis Hospital", "B-22, Sector 62, Noida", "Noida", "201309", "+91 120 240 0222", 28.5700, 77.3230, "PR"),
    ("Yatharth Super Speciality Hospital", "Greater Noida West, Noida", "Noida", "201308", "+91 120 464 1600", 28.5530, 77.3350, "PR"),
    ("GSVM Medical College", "Kanpur", "Kanpur", "208002", "+91 512 255 5312", 26.4630, 80.3350, "MC"),
    ("Regency Hospital", "A-2, Sarvodaya Nagar, Kanpur", "Kanpur", "208005", "+91 512 229 0066", 26.4740, 80.3070, "PR"),
    ("Govind Ballabh Pant Hospital", "Swaroop Nagar, Kanpur", "Kanpur", "208002", "+91 512 254 1450", 26.4670, 80.3400, "MC"),
    ("Sir Sunderlal Hospital (BHU)", "Banaras Hindu University, Varanasi", "Varanasi", "221005", "+91 542 236 8800", 25.3200, 82.9900, "MC"),
    ("Heritage Hospital", "Mahmoorganj, Varanasi", "Varanasi", "221010", "+91 542 236 5888", 25.3330, 82.9770, "PR"),
    ("District Hospital", "Kabasu, Varanasi", "Varanasi", "221002", None, 25.3120, 82.9870, "DH"),
    ("Sarojini Naidu Medical College", "Agra", "Agra", "282002", "+91 562 252 7827", 27.1900, 78.0000, "MC"),
    ("Pushpanjali Hospital", "Shilpgram Road, Agra", "Agra", "282007", "+91 562 404 2333", 27.1770, 78.0040, "PR"),
    ("Kailash Hospital", "Daresi Road, Agra", "Agra", "282002", "+91 562 285 3127", 27.1850, 78.0160, "PR"),
    ("Motilal Nehru Medical College", "Allahabad", "Prayagraj", "211001", "+91 532 240 0066", 25.4520, 81.8330, "MC"),
    ("Swaroop Rani Nehru Hospital", "Allahabad", "Prayagraj", "211002", "+91 532 265 1790", 25.4510, 81.8380, "DH"),
    ("Columbia Asia Hospital", "Vaishali, Ghaziabad", "Ghaziabad", "201010", "+91 120 461 7777", 28.6400, 77.4000, "PR"),
    ("Max Hospital", "Vaishali, Ghaziabad", "Ghaziabad", "201012", "+91 120 494 9999", 28.6770, 77.4250, "PR"),
    ("Lala Lajpat Rai Memorial Medical College", "Meerut", "Meerut", "250004", "+91 121 276 0480", 29.0100, 77.7400, "MC"),
    ("Subharti Medical College", "Delhi-Haridwar Bypass, Meerut", "Meerut", "250005", "+91 121 243 9000", 28.9470, 77.7110, "MC"),
    ("Rohilkhand Medical College & Hospital", "Pilibhit Bypass Road, Bareilly", "Bareilly", "243006", "+91 581 258 3001", 28.4120, 79.3990, "MC"),
    ("Sri Ram Murti Smarak Institute of Medical Sciences", "Bareilly-Lucknow Road, Bareilly", "Bareilly", "243202", "+91 581 258 2282", 28.3510, 79.4300, "MC"),
    ("Baba Raghav Das Medical College", "Gorakhpur", "Gorakhpur", "273013", "+91 551 220 1490", 26.7480, 83.3850, "MC"),
    ("AIIMS Gorakhpur", "Kunjrauli, Gorakhpur", "Gorakhpur", "273008", "+91 551 227 7000", 26.7630, 83.3570, "MC"),
    ("Jawaharlal Nehru Medical College (AMU)", "Aligarh Muslim University, Aligarh", "Aligarh", "202002", "+91 571 270 0910", 27.9170, 78.0880, "MC"),
    ("Maharani Laxmi Bai Medical College", "Jhansi", "Jhansi", "284128", "+91 510 236 1428", 25.4480, 78.5540, "MC"),
    ("Teerthankar Mahaveer Medical College", "Moradabad", "Moradabad", "244001", "+91 591 246 0111", 28.8330, 78.7700, "MC"),
    ("District Hospital", "Mathura", "Mathura", "281001", None, 27.4900, 77.6740, "DH"),
    ("District Hospital", "Saharanpur", "Saharanpur", "247001", None, 29.9640, 77.5480, "DH"),
    ("District Hospital", "Ayodhya", "Ayodhya", "224001", None, 26.7950, 82.1990, "DH"),
    ("District Hospital", "Firozabad", "Firozabad", "283203", None, 27.1500, 78.4010, "DH"),
    ("District Hospital", "Muzaffarnagar", "Muzaffarnagar", "251001", None, 29.4710, 77.7040, "DH"),
    ("Uttar Pradesh University of Medical Sciences", "Saifai, Etawah", "Etawah", "206130", "+91 5688 276 306", 26.7000, 79.0180, "MC"),
]))

STATES.append(("Haryana", [
    ("Medanta - The Medicity", "Sector 38, Gurugram", "Gurugram", "122001", "+91 124 414 1414", 28.4310, 77.0820, "PR2"),
    ("Artemis Hospital", "Sector 51, Gurugram", "Gurugram", "122001", "+91 124 451 1111", 28.4170, 77.0830, "PR"),
    ("Fortis Memorial Research Institute", "Sector 44, Gurugram", "Gurugram", "122002", "+91 124 478 9000", 28.4630, 77.0800, "PR2"),
    ("Max Hospital", "Sector 45, Gurugram", "Gurugram", "122003", "+91 124 417 2000", 28.4550, 77.0490, "PR"),
    ("Fortis Escorts Hospital", "Neelam Bata Road, Faridabad", "Faridabad", "121001", "+91 129 419 3000", 28.4100, 77.3100, "PR"),
    ("Sarvodaya Hospital", "Sector 8, Faridabad", "Faridabad", "121006", "+91 129 401 0000", 28.4070, 77.3250, "PR"),
    ("Government Medical College", "Hisar", "Hisar", "125001", "+91 1662 237 100", 29.1380, 75.7110, "MC"),
    ("Maharaja Agrasen Medical College", "Hisar", "Hisar", "125001", "+91 1662 288 411", 29.1500, 75.7180, "MC"),
    ("Pt. B.D. Sharma PGIMS", "Rohtak", "Rohtak", "124001", "+91 1262 213 088", 28.9000, 76.5820, "MC"),
    ("Government Medical College", "Ambala", "Ambala", "134003", "+91 171 264 4030", 30.3740, 76.7830, "MC"),
    ("Kalpana Chawla Government Medical College", "Karnal", "Karnal", "132001", "+91 184 226 7744", 29.6850, 76.9900, "MC"),
    ("Government Medical College", "Panipat", "Panipat", "132103", None, 29.3950, 76.9600, "MC"),
    ("District Civil Hospital", "Kurukshetra", "Kurukshetra", "136118", None, 29.9700, 76.8780, "DH"),
    ("District Civil Hospital", "Yamunanagar", "Yamunanagar", "135001", None, 30.1300, 77.2850, "DH"),
]))

STATES.append(("Punjab", [
    ("Christian Medical College & Hospital", "Brown Road, Ludhiana", "Ludhiana", "141008", "+91 161 502 5500", 30.9020, 75.8570, "MC"),
    ("Dayanand Medical College & Hospital", "Tagore Nagar, Ludhiana", "Ludhiana", "141001", "+91 161 230 0510", 30.9140, 75.8720, "MC"),
    ("Fortis Hospital", "BRS Nagar, Ludhiana", "Ludhiana", "141012", "+91 161 510 2222", 30.8980, 75.8440, "PR"),
    ("Government Medical College", "Amritsar", "Amritsar", "143001", "+91 183 222 2700", 31.6300, 74.8630, "MC"),
    ("Fortis Hospital", "Ranjit Avenue, Amritsar", "Amritsar", "143001", "+91 183 508 1000", 31.6160, 74.8490, "PR"),
    ("Civil Hospital", "Jalandhar", "Jalandhar", "144001", None, 31.3260, 75.5770, "DH"),
    ("Patel Hospital", "Nakodar Road, Jalandhar", "Jalandhar", "144003", "+91 181 262 0111", 31.3320, 75.5700, "PR"),
    ("Government Rajindra Hospital", "Patiala", "Patiala", "147001", "+91 175 221 0650", 30.3450, 76.3820, "MC"),
    ("AIIMS Bathinda", "Bathinda", "Bathinda", "151001", "+91 164 268 2000", 30.1900, 74.9500, "MC"),
    ("Fortis Hospital", "Sector 62, Phase 8, Mohali", "Mohali", "160062", "+91 172 509 2222", 30.7040, 76.7190, "PR"),
    ("Civil Hospital", "Hoshiarpur", "Hoshiarpur", "146001", None, 31.5300, 75.9160, "DH"),
    ("Civil Hospital", "Gurdaspur", "Gurdaspur", "143521", None, 32.0400, 75.4020, "DH"),
    ("Civil Hospital", "Ferozepur", "Ferozepur", "152001", None, 30.9250, 74.6120, "DH"),
    ("Civil Hospital", "Moga", "Moga", "142001", None, 30.8160, 75.1690, "DH"),
    ("Civil Hospital", "Sangrur", "Sangrur", "148001", None, 30.2460, 75.8440, "DH"),
]))

STATES.append(("Rajasthan", [
    ("Sawai Man Singh Hospital", "J.L.N. Marg, Jaipur", "Jaipur", "302004", "+91 141 256 6251", 26.8980, 75.8230, "MC"),
    ("Fortis Escorts Hospital", "Jawahar Lal Nehru Marg, Jaipur", "Jaipur", "302017", "+91 141 254 7000", 26.9120, 75.7990, "PR"),
    ("Narayana Multispeciality Hospital", "Lalkothi, Jaipur", "Jaipur", "302015", "+91 141 272 4444", 26.9210, 75.8350, "PR"),
    ("Santokba Durlabhji Hospital", "Bhawani Singh Marg, Jaipur", "Jaipur", "302015", "+91 141 256 6251", 26.8870, 75.8050, "PR"),
    ("J.K. Lone Hospital", "Sawai Man Singh Marg, Jaipur", "Jaipur", "302004", "+91 141 256 5773", 26.8940, 75.8300, "CH"),
    ("Mathura Das Mathur Hospital", "Jodhpur", "Jodhpur", "342001", "+91 291 274 0198", 26.2870, 73.0160, "MC"),
    ("AIIMS Jodhpur", "Basni Phase 2, Jodhpur", "Jodhpur", "342005", "+91 291 274 0764", 26.2570, 73.0410, "MC"),
    ("R.N.T. Medical College", "Udaipur", "Udaipur", "313001", "+91 294 241 1203", 24.5710, 73.6960, "MC"),
    ("Apex Hospitals", "Sector 11, Udaipur", "Udaipur", "313001", "+91 294 241 3000", 24.5860, 73.7120, "PR"),
    ("MBS Hospital", "Kota", "Kota", "324001", "+91 744 247 0907", 25.1650, 75.8350, "MC"),
    ("PBM Hospital", "Bikaner", "Bikaner", "334001", "+91 151 220 2543", 28.0230, 73.3250, "MC"),
    ("Jawaharlal Nehru Hospital", "Ajmer", "Ajmer", "305001", "+91 145 242 0203", 26.4490, 74.6450, "DH"),
    ("Government Hospital", "Alwar", "Alwar", "301001", None, 27.5630, 76.6200, "DH"),
    ("District Hospital", "Bharatpur", "Bharatpur", "321001", None, 27.2180, 77.4900, "DH"),
    ("District Hospital", "Sikar", "Sikar", "332001", None, 27.6150, 75.1390, "DH"),
    ("District Hospital", "Jaisalmer", "Jaisalmer", "345001", None, 26.9160, 70.9090, "DH"),
    ("District Hospital", "Bhilwara", "Bhilwara", "311001", None, 25.3510, 74.6340, "DH"),
    ("District Hospital", "Pali", "Pali", "306401", None, 25.7720, 73.3230, "DH"),
    ("District Hospital", "Sri Ganganagar", "Sri Ganganagar", "335001", None, 29.9060, 73.8810, "DH"),
]))

STATES.append(("Jammu and Kashmir", [
    ("SMHS Hospital", "Gogji Bagh, Srinagar", "Srinagar", "190010", "+91 194 247 9401", 34.0860, 74.8050, "MC"),
    ("Sher-i-Kashmir Institute of Medical Sciences (SKIMS)", "Soura, Srinagar", "Srinagar", "190011", "+91 194 240 1013", 34.0510, 74.8400, "MC"),
    ("Government Medical College Hospital", "Karan Nagar, Srinagar", "Srinagar", "190010", "+91 194 245 2131", 34.0960, 74.8180, "MC"),
    ("Government Medical College Hospital", "Bakshi Nagar, Jammu", "Jammu", "180001", "+91 191 257 5130", 32.7180, 74.8660, "MC"),
    ("Apollo Hospital", "Jammu", "Jammu", "180011", "+91 191 247 8021", 32.7150, 74.8720, "PR"),
    ("Shri Mata Vaishno Devi Narayana Superspeciality Hospital", "Kakryal, Katra", "Jammu", "182320", "+91 1991 234 444", 32.9200, 74.9400, "PR"),
    ("District Hospital", "Anantnag", "Anantnag", "192101", None, 33.7310, 75.1470, "DH"),
    ("District Hospital", "Baramulla", "Baramulla", "193101", None, 34.2040, 74.3440, "DH"),
    ("District Hospital", "Udhampur", "Udhampur", "182101", None, 32.9200, 75.1380, "DH"),
]))

STATES.append(("Uttarakhand", [
    ("Government Doon Medical College", "Patel Nagar, Dehradun", "Dehradun", "248001", "+91 135 264 8422", 30.3290, 78.0510, "MC"),
    ("Max Hospital", "Mussoorie Road, Dehradun", "Dehradun", "248001", "+91 135 662 0000", 30.3390, 78.0860, "PR"),
    ("Synergy Institute of Medical Sciences", "Dehradun", "Dehradun", "248001", "+91 135 663 6000", 30.3200, 77.9990, "MC"),
    ("Government Medical College", "Haridwar", "Haridwar", "249401", None, 29.9440, 78.1600, "MC"),
    ("AIIMS Rishikesh", "Virbhadra Road, Rishikesh", "Rishikesh", "249203", "+91 135 246 3000", 30.1190, 78.2950, "MC"),
    ("District Hospital", "Nainital", "Nainital", "263001", None, 29.3790, 79.4520, "DH"),
    ("District Hospital", "Rudrapur", "Rudrapur", "263153", None, 28.9850, 79.4060, "DH"),
    ("District Hospital", "Haldwani", "Haldwani", "263139", None, 29.2250, 79.5210, "DH"),
    ("District Hospital", "Almora", "Almora", "263601", None, 29.5980, 79.6580, "DH"),
]))

STATES.append(("Himachal Pradesh", [
    ("Indira Gandhi Medical College", "Ridge, Shimla", "Shimla", "171001", "+91 177 265 5265", 31.0960, 77.1740, "MC"),
    ("Kamla Nehru Hospital", "Lakkar Bazar, Shimla", "Shimla", "171001", "+91 177 265 2511", 31.1040, 77.1650, "DH"),
    ("Zonal Hospital", "Dharamshala, Kangra", "Dharamshala", "176215", "+91 1892 223 521", 32.2190, 76.3200, "DH"),
    ("Netaji Subhash Chandra Bose Medical College", "Mandi", "Mandi", "175001", "+91 1905 235 520", 31.7080, 76.9300, "MC"),
    ("Civil Hospital", "Kullu", "Kullu", "175101", None, 31.9560, 77.1080, "DH"),
    ("Civil Hospital", "Solan", "Solan", "173212", None, 30.9040, 77.0960, "DH"),
    ("Civil Hospital", "Una", "Una", "174303", None, 31.4680, 76.2690, "DH"),
    ("Civil Hospital", "Hamirpur", "Hamirpur", "177001", None, 31.6900, 76.5240, "DH"),
]))

STATES.append(("Chandigarh", [
    ("Post Graduate Institute of Medical Education & Research (PGIMER)", "Sector 12, Chandigarh", "Chandigarh", "160012", "+91 172 274 6015", 30.7650, 76.7660, "MC"),
    ("Government Medical College & Hospital", "Sector 32, Chandigarh", "Chandigarh", "160030", "+91 172 266 5253", 30.7250, 76.7860, "MC"),
    ("Silver Oaks Hospital", "Sector 36, Chandigarh", "Chandigarh", "160036", "+91 172 260 1500", 30.7090, 76.7100, "PR"),
]))

STATES.append(("Ladakh", [
    ("Sonam Norboo Memorial Hospital", "Leh", "Leh", "194101", "+91 1982 252 285", 34.1640, 77.5850, "DH"),
    ("District Hospital", "Kargil", "Kargil", "194103", None, 34.5580, 76.1260, "DH"),
]))
