import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def get_organic_solution(disease_name):
    solutions = {
        "Powdery Mildew":'''Cow Milk Spray (cheap & very effective)\n
Mix 1 liter cow milk + 9 liters water.
Add a few drops of soap for sticking.
Spray every 7–10 days on both sides of leaves.\n
Baking Soda Spray\n
Mix 1 tablespoon baking soda + 1 teaspoon vegetable oil + 5 g soap + 1 liter water.
Spray weekly.\n
Neem Oil Spray\n
Mix 30 ml neem oil + 5 g soap + 10 liters water.
Spray in evening to avoid leaf burn.\n
Cultural Practices\n
Burn infected leaves.
Keep spacing between plants to improve airflow.
Avoid excess nitrogen fertilizers (they make plants more susceptible).''',

"Yellow leaf curl virus":'''Neem Seed Kernel Extract (NSKE 5%)\n
Take 500 g neem seed kernel powder.
Soak overnight in 10 liters water.
Filter and spray. Repeat every 7 days.\n
Garlic-Chili Spray\n
Crush 50 g garlic + 50 g green chili, soak in 1 liter water overnight.
Filter and dilute with 10 liters water.
Spray on leaves to repel whiteflies.\n
Yellow Sticky Traps\n
Take yellow plastic sheets or cardboard.
Apply grease or castor oil.
Hang in fields (1 trap per 10 sq.m). Whiteflies stick to it.\n
Crop Management\n
Plant marigold around tomato/chili field → attracts whiteflies away.
Remove infected plants immediately.''',

"Early Blight":'''Trichoderma viride / harzianum (Bio-fungicide)\n
Mix 50 g Trichoderma powder with 10 kg compost or FYM.
Apply near root zone at planting.
Prevents fungal attack.\n
Bordeaux Mixture (1% solution)\n
Mix 100 g copper sulfate + 100 g lime in 10 liters water.
Spray at 15-day intervals.
Use only when disease starts (copper should not be overused).\n
Neem Cake Application\n
Apply 250 kg/acre in soil. Improves resistance to fungus.
Mulching
Use straw mulch to stop soil splash of fungus to leaves.''',

"Bacterial leaf spot":'''Garlic Extract Spray\n
Crush 100 g garlic.
Soak in 1 liter water overnight.
Filter and dilute in 10 liters water.
Spray every 7 days.\n
Neem Oil + Soap Spray\n
30 ml neem oil + 5 g soap + 10 liters water.\n
Cow Urine Spray\n
Mix 1 liter cow urine + 9 liters water.
Spray weekly – acts as antibacterial + growth booster.\n
Cultural Control\n
Avoid overhead irrigation.
Remove infected leaves.
Rotate crops (avoid continuous chili/tomato).''',

"Anthracnose":'''Trichoderma + Compost Application\n
Mix 2 kg Trichoderma with 100 kg compost.
Apply around root zone.\n
Neem Seed Extract Spray\n
Same as above (NSKE 5%).\n
Baking Soda Spray\n
Same formula as Powdery Mildew.
Post-harvest
Dip fruits in hot water (55°C for 2–3 min) to kill spores''',

"Rust":'''Cow Urine Spray (1:10 dilution) every 7–10 days.\n
Sulfur Dust (allowed in organic farming): Apply 10–15 kg/acre directly on crops.\n
Neem Oil Spray weekly.\n
Remove affected leaves early.''',

"Mosaic virus":'''Vector Control (same as Yellow Leaf Curl):\n
Neem oil spray.\n
Garlic-Chili spray.\n
Yellow sticky traps.\n
Banana Peel Extract\n
Soak 1 kg banana peels in 5 liters water for 3 days.
Dilute with 20 liters water.
Spray to improve plant immunity.
Remove infected plants immediately.''',

"Leaf miners":'''Neem Seed Extract (5%) Spray every 7 days.\n
Blue Sticky Traps (adult leaf miners are attracted to blue).
Beneficial Insects: Diglyphus isaea (tiny wasp) parasitizes larvae.
Collect and destroy damaged leaves.''',

"Bacterial blight":'''Seed Treatment\n
Soak seeds in Trichoderma solution (10 g/L water) for 30 minutes before sowing.
Neem Cake
Apply 200–250 kg/acre in soil.
Cow Urine Spray (1:10 dilution).
Avoid flood irrigation – water spreads bacteria.'''
    }
    return solutions.get(disease_name, "Maintain soil health, proper watering, and organic compost.")

def generate_report(disease, solution):
    filename = "plant_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold",18)
    c.drawString(200, 750, "🌱 Plant Health Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Disease Detected: {disease.lower}")
    c.drawString(50, 670, "Recommended Organic Solution:")
    text = c.beginText(50, 650)
    text.setFont("Helvetica", 11)
    for line in solution.split(". "):
        text.textLine("- " + line)
    c.drawText(text)
    c.save()
    return filename

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        return res.text if res.status_code == 200 else None
    except:
        return None
