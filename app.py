import random
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        weight = float(request.form.get("weight"))
        raw_height = float(request.form.get("height"))

        if raw_height < 3.0:
            height_m = raw_height
            height_cm = raw_height * 100
        else:
            height_m = raw_height / 100
            height_cm = raw_height

        # --- TROLL EKRANI YÖNLENDİRMELERİ ---

        # 1. Hata / Negatif Giriş -> ERROR (error.jpeg)
        if height_m <= 0 or weight <= 0:
             return render_template("troll.html",
                                    title="MATH ERROR",
                                    msg="You broke the physics engine. Negative mass?",
                                    image_url=url_for('static', filename='bmi-photos/error.jpeg'))

        # 2. HOBBIT KONTROLÜ (<150cm) -> FRODO (frodo.jpg)
        if height_cm < 150:
            return render_template("troll.html",
                                   title="HOBBIT DETECTED",
                                   msg="Straight from the Shire? We don't calculate BMI here, we give directions to Mordor.",
                                   image_url=url_for('static', filename='bmi-photos/frodo.jpg'))

        # 3. DEV KONTROLÜ (>210cm) -> GIANT (giant.jpeg)
        if height_cm > 210:
            return render_template("troll.html",
                                   title="TITAN DETECTED",
                                   msg="Is the oxygen cleaner up there? If you aren't in the NBA, it's a waste.",
                                   image_url=url_for('static', filename='bmi-photos/giant.jpeg'))

        # BMI Hesabı
        bmi = round(weight / (height_m * height_m), 1)

        # 4. İnsanlık dışı sınırlar -> ERROR (error.jpeg)
        if bmi < 5.0 or bmi > 200.0:
            return render_template("troll.html",
                                   title="SYSTEM GLITCH",
                                   msg="These numbers are out of this world. Literally.",
                                   image_url=url_for('static', filename='bmi-photos/error.jpeg'))

        # --- NORMAL HESAPLAMA ---
        water_intake = round(weight * 0.033, 1)
        ideal_min_weight = round(18.5 * (height_m * height_m), 1)
        ideal_max_weight = round(24.9 * (height_m * height_m), 1)
        ideal_range = f"{ideal_min_weight}kg - {ideal_max_weight}kg"

        weight_diff = 0
        diff_msg = "You are right on track!"
        if weight < ideal_min_weight:
            weight_diff = round(ideal_min_weight - weight, 1)
            diff_msg = f"You need to gain ~{weight_diff}kg."
        elif weight > ideal_max_weight:
            weight_diff = round(weight - ideal_max_weight, 1)
            diff_msg = f"You need to lose ~{weight_diff}kg."

        analysis = get_detailed_analysis(bmi)

        return render_template("result.html",
                               bmi=bmi,
                               result=analysis,
                               water=water_intake,
                               ideal_range=ideal_range,
                               diff_msg=diff_msg)

    except ValueError:
        return render_template("troll.html",
                               title="INPUT ERROR",
                               msg="Please enter numbers, not philosophical concepts.",
                               image_url=url_for('static', filename='bmi-photos/error.jpeg'))

def get_detailed_analysis(bmi):
    # Varsayılan Resim: thinking.jpeg
    data = {
        "category": "Analyzing...",
        "color": "secondary",
        "message": "Calculation complete.",
        "advice": "Check your results.",
        "image": url_for('static', filename='bmi-photos/thinking.jpeg'),
        "link_text": "Health Info",
        "link_url": "https://www.who.int/news-room/fact-sheets/detail/healthy-diet",
    }

    if bmi < 16.0:
        data["category"] = "Severe Thinness"
        data["color"] = "danger"
        # Skeleton -> skeleton.jpeg
        data["image"] = url_for('static', filename='bmi-photos/skeleton.jpeg')
        data["message"] = "I've seen ghosts with more body mass."
        data["advice"] = "Critical range. Eat a burger ASAP!"
        data["link_text"] = "🚑 Medical: Malnutrition"
        data["link_url"] = "https://www.nhs.uk/conditions/malnutrition/"

    elif 16.0 <= bmi < 18.5:
        data["category"] = "Underweight"
        data["color"] = "warning"
        # Sonic resmi listede 'images-1.jpeg' olarak görünüyor olabilir, onu kullandım.
        data["image"] = url_for('static', filename='bmi-photos/images-1.jpeg')
        data["message"] = "Aerodynamic build. Great for marathons."
        data["advice"] = "Fuel up! Protein is your friend."
        data["link_text"] = "🥑 Diet: Weight Gain"
        data["link_url"] = "https://www.healthline.com/nutrition/how-to-gain-weight"

    elif 18.5 <= bmi < 19.5:
        data["category"] = "Normal (Borderline)"
        data["color"] = "success"
        # Wind -> wind.jpeg
        data["image"] = url_for('static', filename='bmi-photos/wind.jpeg')
        data["message"] = "Technically normal, but don't fly away!"
        data["advice"] = "Safe zone, but keep an eye on it."

    elif 19.5 <= bmi < 20.5:
        data["category"] = "Standard Human"
        data["color"] = "success"
        # Jim -> jim.jpeg
        data["image"] = url_for('static', filename='bmi-photos/jim.jpeg')
        data["message"] = "Factory settings human. Statistics love you."
        data["advice"] = "Whatever you're doing, keep doing it."

    elif 20.5 <= bmi < 21.5:
        data["category"] = "Golden Ratio"
        data["color"] = "success"
        # Balance -> balance.jpeg
        data["image"] = url_for('static', filename='bmi-photos/balance.jpeg')
        data["message"] = "Perfectly balanced, as all things should be."
        data["advice"] = "You nailed it."

    elif 21.5 <= bmi < 22.5:
        data["category"] = "The Perfectionist"
        data["color"] = "success"
        # Chef -> chef.jpeg
        data["image"] = url_for('static', filename='bmi-photos/chef.jpeg')
        data["message"] = "Doctors dream of patients like you."
        data["advice"] = "Treat yourself today."

    elif 22.5 <= bmi < 23.5:
        data["category"] = "Normal (Watch Out)"
        data["color"] = "warning"
        # Traffic -> traffic.jpeg
        data["image"] = url_for('static', filename='bmi-photos/traffic.jpeg')
        data["message"] = "Last exit before the 'Curvy' zone."
        data["advice"] = "Still great, just be mindful."

    elif 23.5 <= bmi < 25.0:
        data["category"] = "Pre-Dad Bod"
        data["color"] = "warning"
        # Homer -> homer.png (Dikkat: PNG formatında)
        data["image"] = url_for('static', filename='bmi-photos/homer.png')
        data["message"] = "Loading dad bod... 20%."
        data["advice"] = "Time to switch gym mode to 'Active'."

    elif 25.0 <= bmi < 30.0:
        data["category"] = "Overweight"
        data["color"] = "warning"
        # Joey -> joey.jpeg
        data["image"] = url_for('static', filename='bmi-photos/joey.jpeg')
        data["message"] = "Gourmet lifestyle detected."
        data["advice"] = "Cardio is your new best friend."
        data["link_text"] = "👟 Cardio: Couch to 5K"
        data["link_url"] = "https://www.nhs.uk/better-health/get-active/get-running-with-couch-to-5k/"

    elif 30.0 <= bmi:
        data["category"] = "Obesity"
        data["color"] = "danger"
        # Baymax -> baymax.jpeg
        data["image"] = url_for('static', filename='bmi-photos/baymax.jpeg')
        data["message"] = "Gravity is working overtime."
        data["advice"] = "High health risk. Small changes start today."
        data["link_text"] = "👨‍⚕️ Medical: Obesity Help"
        data["link_url"] = "https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight"

    return data
