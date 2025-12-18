def plant_chatbot(user_input):
    responses = {
        "hello": "👋 Hi there! How can I help your plants today?",
        "my plant is affected with disease": "🌿 Upload a leaf image for AI-based detection.",
        "provide organic solution for my disease": "🌱 Try neem oil, compost tea, baking soda spray, or crop rotation.",
        "water": "💧 Water plants deeply 2-3 times a week, avoid overwatering.",
        "Powdery mildew": "A fungal disease that causes white, powdery spots on leaves and stems.",
"Yellow leaf curl virus": "A viral infection spread by whiteflies that causes yellowing and curling of leaves.",
"Early blight": "A fungal disease that forms concentric dark spots on leaves, often leading to defoliation.",
"Bacterial leaf spot": "A bacterial infection causing small, dark, water-soaked lesions on leaves.",
"Anthracnose": "A fungal disease that produces dark, sunken spots on leaves, stems, and fruits.",
"Rust": "A fungal disease that causes orange, brown, or reddish pustules on the underside of leaves.",
"Mosaic virus": "A viral disease that creates mottled yellow-green mosaic patterns on leaves.",
"Leaf miner damage": "Caused by insect larvae tunneling inside leaves, leaving winding white trails.",
"Bacterial blight": "A bacterial disease leading to dark, water-soaked lesions that spread rapidly on leaves.",
        "bye": "Goodbye 👋! Keep your plants green & healthy!"
    }
    for key in responses:
        if key in user_input.lower():
            return responses[key]
    return "🤔 Not sure... but try neem oil, compost, or crop rotation!"
