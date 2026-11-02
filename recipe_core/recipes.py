"""Built-in recipes, all for 2 servings before scaling. Original wording written for this app."""
D = "Lunch or dinner"
RAW = []


def R(title, description, image, prep, cook, items, utensils, steps, addons, healthy, meal=D, ingredient_images=()):
    RAW.append(dict(title=title, description=description, image=image, prep=prep, cook=cook, items=items, utensils=utensils,
                    steps=steps, addons=addons, healthy=healthy, meal=meal, ingredient_images=ingredient_images))


# Local-style dishes
R("Lighter Nasi Goreng", "Brown rice fried with vegetables, egg and a little chilli.", "nasi goreng", 10, 35,
  ["brown rice:150", "water:350", "egg:2", "carrot:1", "cabbage:100", "shallot:3", "garlic:2", "fresh chilli:1", "light soy sauce:2 tsp", "cooking oil:2 tsp"],
  ["pot", "pan"], ["Simmer the rice in the water, covered, until tender, then spread it out to cool.", "Blend or finely chop the shallots, garlic and chilli.", "Fry the paste in the oil for 2 minutes, then add the carrot and cabbage and cook for 3 minutes.", "Push aside, scramble the eggs until set, then add the rice and soy sauce and toss until hot."],
  ["Cucumber and tomato slices", "A wedge of lime", "Grilled chicken strips for extra protein"], ["Uses whole-grain rice", "Plenty of vegetables and little oil"], ingredient_images=("brown rice", "cabbage"))
R("Oven-Baked Nasi Katok-Style Chicken", "A lighter take on the Bruneian favourite: spiced baked chicken with rice and fresh sambal.", "nasi katok", 15, 35,
  ["chicken thigh:300", "ground turmeric:1 tsp", "ground coriander:1 tsp", "garlic:2", "salt:0.25 tsp", "white rice:120", "water:250", "tomato:1", "fresh chilli:2", "shallot:2", "lime:1", "cooking oil:2 tsp"],
  ["oven", "baking tray", "pot"], ["Heat the oven to 200°C. Rub the chicken with turmeric, coriander, half the chopped garlic, the salt and oil.", "Bake on the tray for 25 to 30 minutes until the centre reaches 75°C.", "Simmer the rice in the water, covered, until tender.", "Chop the tomato, chilli, shallots and remaining garlic, then mix with lime juice as a fresh sambal.", "Serve the chicken with rice and sambal."],
  ["Steamed long beans", "Sliced cucumber"], ["Baked, not deep-fried", "Fresh sambal adds flavour with little salt"], ingredient_images=("chicken", "chilli"))
R("Soto Ayam-Style Chicken Soup", "A fragrant turmeric chicken soup with noodles and bean sprouts.", "soto ayam", 10, 30,
  ["chicken breast:250", "water:800", "lemongrass:1", "ginger:15", "garlic:3", "ground turmeric:1 tsp", "salt:0.5 tsp", "rice noodles:80", "bean sprouts:100", "spring onion:2", "lime:1"],
  ["pot"], ["Bruise the lemongrass, chop the ginger and garlic, and simmer with the turmeric, salt, water and chicken for 20 minutes until the chicken reaches 75°C.", "Lift out the chicken, shred it and return it to the pot.", "Remove the lemongrass, add the rice noodles and cook until soft.", "Add the bean sprouts for 1 minute, then serve with spring onion and lime."],
  ["Fresh chilli slices", "Chopped coriander leaves", "A boiled egg for extra protein"], ["A broth-based meal with lean protein", "Low in saturated fat"], ingredient_images=("lemongrass", "bean sprouts"))
R("Ikan Masak Kunyit", "Fish simmered in a light turmeric and lemongrass broth.", "fish curry", 10, 15,
  ["white fish fillet:300", "ground turmeric:1 tsp", "lemongrass:1", "garlic:2", "shallot:3", "fresh chilli:1", "okra:100", "water:300", "tamarind paste:1 tsp", "salt:0.25 tsp"],
  ["pot"], ["Finely chop the garlic, shallots and chilli, and bruise the lemongrass.", "Simmer them with the turmeric, tamarind, salt and water for 5 minutes.", "Add the okra and cook for 5 minutes.", "Add the fish and simmer gently for 5 minutes until it flakes easily."],
  ["Steamed brown rice", "Fresh cucumber slices"], ["Lean fish in a broth with no added oil"], ingredient_images=("turmeric", "okra"))
R("Foil-Baked Ikan Bakar", "Spiced fish baked in foil with a tangy lime and chilli dip.", "ikan bakar", 15, 20,
  ["white fish fillet:320", "ground turmeric:1 tsp", "fresh chilli:2", "garlic:2", "shallot:3", "tamarind paste:1 tsp", "salt:0.25 tsp", "lime:1", "cooking oil:1 tsp", "tomato:1"],
  ["oven", "baking tray", "foil", "blender"], ["Heat the oven to 200°C. Blend or finely chop the chillies, garlic and shallots, then mix with turmeric, tamarind, salt and oil.", "Spread half the paste over the fish and wrap in foil on the tray.", "Bake for 15 to 20 minutes until the fish flakes easily.", "Mix the remaining paste with chopped tomato and lime juice, then cook briefly in the opened foil or serve as a dip."],
  ["Brown rice", "Blanched kangkung", "Cucumber salad"], ["Baked with very little oil", "A flavourful low-fat protein"], ingredient_images=("chilli", "lime"))
R("Sambal Kangkung with Tofu", "Quick-fried water spinach with a lightly spicy sauce and golden tofu.", "water spinach", 10, 10,
  ["kangkung:300", "firm tofu:200", "garlic:2", "shallot:2", "fresh chilli:1", "belacan:0.5 tsp", "cooking oil:2 tsp"],
  ["pan"], ["Cube the tofu and brown it in half the oil, then set aside.", "Finely chop the garlic, shallots and chilli, then fry with the belacan and remaining oil for 2 minutes.", "Add the kangkung stems for 1 minute, then the leaves and tofu, and toss until wilted."],
  ["Steamed brown rice", "A squeeze of lime"], ["Mostly vegetables with plant protein"], ingredient_images=("tofu",))
R("Ayam Masak Kicap Ringan", "Chicken and vegetables in a light soy and ginger sauce.", "chicken stir fry", 10, 20,
  ["chicken thigh:280", "light soy sauce:1 tbsp", "ginger:10", "garlic:2", "onion:1", "potato:1", "tomato:1", "water:150", "cooking oil:2 tsp"],
  ["pan"], ["Cut the chicken and potato into bite-sized pieces. Slice the onion and tomato, and chop the ginger and garlic.", "Fry the onion, ginger and garlic in the oil for 2 minutes.", "Add the chicken and brown it for 4 minutes.", "Add the potato, soy sauce and water, cover and simmer for 12 minutes until tender and the chicken reaches 75°C.", "Stir in the tomato for the last 2 minutes."],
  ["Steamed greens", "Brown rice", "Sliced fresh chilli"], ["A modest amount of soy sauce", "Includes fresh vegetables"], ingredient_images=("potato", "ginger"))
R("Light Sayur Lodeh", "Mixed vegetables simmered in light coconut milk with turmeric.", "sayur lodeh", 15, 20,
  ["cabbage:150", "long beans:100", "carrot:1", "eggplant:0.5", "firm tofu:150", "shallot:3", "garlic:2", "ground turmeric:1 tsp", "light coconut milk:150", "water:250", "salt:0.25 tsp"],
  ["pot"], ["Cut all the vegetables and the tofu into bite-sized pieces, and chop the shallots and garlic.", "Simmer the shallots, garlic, turmeric and water for 3 minutes.", "Add the carrot and long beans for 5 minutes, then the eggplant and cabbage for 5 minutes.", "Add the tofu, coconut milk and salt, and simmer gently for 5 minutes."],
  ["Brown rice", "A boiled egg"], ["Vegetable-rich with light coconut milk"], ingredient_images=("cabbage", "coconut milk"))
R("Baked Tempeh Sambal", "Crisp oven-baked tempeh with long beans and chilli.", "tempeh", 10, 25,
  ["tempeh:200", "long beans:200", "shallot:2", "garlic:2", "fresh chilli:2", "tomato:1", "tamarind paste:1 tsp", "light soy sauce:1 tsp", "cooking oil:2 tsp"],
  ["oven", "baking tray", "pan"], ["Heat the oven to 200°C. Slice the tempeh, toss with half the oil and bake for 15 minutes, turning once.", "Chop the shallots, garlic, chillies and tomato.", "Fry them in the remaining oil for 4 minutes, then add the tamarind and soy sauce.", "Add the long beans with a splash of water, cover for 4 minutes, then toss in the tempeh."],
  ["Brown rice", "Cucumber slices"], ["Plant protein with plenty of fibre", "Baked, not deep-fried"], ingredient_images=("long beans", "chilli"))
R("Gado-Gado Salad", "Lightly cooked vegetables, egg and tofu with a small amount of peanut dressing.", "gado-gado", 15, 12,
  ["potato:1", "long beans:100", "cabbage:100", "bean sprouts:80", "egg:2", "firm tofu:120", "peanuts:30", "garlic:1", "fresh chilli:1", "lime:1", "light soy sauce:2 tsp", "water:60"],
  ["pot", "blender"], ["Boil the cubed potato for 8 minutes, adding the long beans and cabbage for the last 3 minutes and the sprouts for the last minute.", "Boil the eggs for 8 minutes in a separate pot, cool and halve them.", "Blend the peanuts, garlic, chilli, lime juice, soy sauce and water into a dressing.", "Arrange the vegetables, eggs and cubed tofu, then spoon over the dressing."],
  ["Sliced cucumber", "A little fresh coriander leaves"], ["Lots of vegetables with protein from egg and tofu"], ingredient_images=("peanuts", "bean sprouts"))
R("Wholewheat Mee Goreng", "Stir-fried noodles with prawns, greens and a tangy chilli sauce.", "mee goreng", 10, 12,
  ["wholewheat noodles:120", "prawns:180", "cabbage:150", "bean sprouts:80", "tomato:1", "garlic:2", "fresh chilli:1", "light soy sauce:2 tsp", "lime:1", "cooking oil:2 tsp"],
  ["pot", "pan"], ["Boil the noodles according to the pack, then drain.", "Fry the chopped garlic and chilli in the oil for 1 minute.", "Add the prawns and cook for 2 to 3 minutes until pink and firm.", "Add the cabbage and tomato for 2 minutes, then the noodles, sprouts and soy sauce, and toss until hot.", "Finish with lime juice."],
  ["A fried or boiled egg", "Cucumber slices"], ["Whole-grain noodles and lots of vegetables"], ingredient_images=("noodles", "prawns"))
R("Light Prawn Laksa", "A spicy noodle soup with prawns and light coconut milk.", "laksa", 15, 15,
  ["prawns:200", "rice noodles:100", "light coconut milk:150", "water:500", "lemongrass:1", "shallot:3", "garlic:2", "fresh chilli:2", "ground turmeric:1 tsp", "bean sprouts:80", "fish sauce:1 tsp", "lime:1"],
  ["pot", "blender"], ["Blend the shallots, garlic, chillies and turmeric to a paste, then cook in a dry pot for 2 minutes.", "Add the water and bruised lemongrass and simmer for 8 minutes.", "Add the rice noodles, coconut milk, fish sauce and prawns, and simmer for 3 to 4 minutes until the prawns are cooked.", "Add the sprouts and lime juice, remove the lemongrass and serve."],
  ["Sliced cucumber", "Fresh coriander leaves"], ["Light coconut milk keeps it lower in saturated fat"], ingredient_images=("prawns", "lemongrass"))
R("Bubur Ayam", "A gentle chicken and rice porridge with ginger.", "chicken congee", 10, 45,
  ["white rice:90", "water:1000", "chicken breast:200", "ginger:15", "garlic:2", "salt:0.5 tsp", "spring onion:2", "carrot:1"],
  ["pot"], ["Bring the rice, water, sliced ginger, chopped garlic, salt and chicken to the boil, then simmer gently.", "After 20 minutes, lift out the chicken once it reaches 75°C, shred it and set aside.", "Add the diced carrot and simmer the porridge for 25 minutes, stirring often.", "Stir in the chicken and top with spring onion."],
  ["Fresh chilli slices", "A boiled egg", "Steamed spinach"], ["Light, low in fat and high in protein"], "Breakfast", ("ginger", "chicken"))
R("Sweet and Sour Pineapple Fish", "Pan-seared fish with pineapple, tomato and peppers.", "sweet and sour fish", 10, 15,
  ["white fish fillet:300", "pineapple:120", "bell pepper:1", "onion:1", "tomato:1", "vinegar:1 tbsp", "light soy sauce:2 tsp", "water:80", "cooking oil:2 tsp"],
  ["pan"], ["Cut the fish and vegetables into chunks.", "Brown the fish in half the oil for 2 minutes per side and set aside.", "Cook the onion and pepper in the remaining oil for 3 minutes.", "Add the tomato, pineapple, vinegar, soy sauce and water, and simmer for 3 minutes.", "Return the fish and warm through until it flakes easily."],
  ["Brown rice", "Steamed cabbage"], ["Sweetness comes from fruit, not added sugar"], ingredient_images=("pineapple", "bell pepper"))
R("Spiced Pumpkin and Chickpea Curry", "A comforting vegetable curry with warming spices.", "chickpea curry", 10, 25,
  ["pumpkin:250", "canned chickpeas:240", "onion:1", "garlic:2", "ginger:10", "curry powder:2 tsp", "canned chopped tomatoes:150", "water:200", "spinach:100", "cooking oil:2 tsp"],
  ["pot"], ["Cook the chopped onion, garlic and ginger in the oil for 4 minutes.", "Stir in the curry powder for 1 minute.", "Add the cubed pumpkin, drained chickpeas, tomatoes and water, then simmer for 18 minutes until tender.", "Stir in the spinach until wilted."],
  ["Brown rice", "A spoon of plain low-fat yoghurt", "Fresh coriander leaves"], ["High in fibre and plant protein"], ingredient_images=("pumpkin", "chickpea"))
R("Red Lentil Dhal", "A soft, savoury lentil stew with spinach.", "dal", 5, 25,
  ["red lentils:140", "onion:1", "garlic:2", "ginger:10", "ground turmeric:1 tsp", "ground cumin:1 tsp", "tomato:2", "water:700", "spinach:100", "salt:0.25 tsp", "cooking oil:2 tsp"],
  ["pot"], ["Cook the chopped onion, garlic and ginger in the oil for 4 minutes, then stir in the spices.", "Add the rinsed lentils, chopped tomatoes, water and salt.", "Simmer for 18 minutes, stirring now and then, until soft.", "Stir in the spinach until wilted."],
  ["Brown rice or wholemeal bread", "A squeeze of lime", "Cucumber and yoghurt salad"], ["High in fibre and protein", "Low in saturated fat"], ingredient_images=("lentil", "spinach"))
# Rice dishes and bowls
R("Garlic Chicken and Broccoli Rice", "A simple one-wok dinner with brown rice and greens.", "chicken and broccoli", 10, 35,
  ["brown rice:140", "water:350", "chicken breast:260", "broccoli:220", "garlic:3", "light soy sauce:2 tsp", "cooking oil:2 tsp"],
  ["pot", "pan"], ["Simmer the rice in the water, covered, until tender.", "Slice the chicken and fry in the oil for 6 to 8 minutes until it reaches 75°C.", "Add the chopped garlic and broccoli with a splash of water, then cover for 3 minutes.", "Add the soy sauce, toss and serve over the rice."],
  ["Sesame seeds", "Sliced chilli", "Sliced cucumber"], ["Lean protein, whole grains and greens"], ingredient_images=("broccoli", "brown rice"))
R("Steamed Ginger Fish with Rice", "Delicate fish steamed with ginger and spring onion.", "steamed fish", 10, 20,
  ["white fish fillet:300", "ginger:20", "spring onion:3", "light soy sauce:2 tsp", "sesame oil:1 tsp", "white rice:120", "water:250", "cabbage:150"],
  ["steamer", "pot"], ["Simmer the rice in the water, covered, until tender.", "Lay the sliced cabbage on a heatproof plate and top with the fish and sliced ginger.", "Steam for 8 to 10 minutes until the fish flakes easily.", "Top with spring onion, soy sauce and sesame oil."],
  ["Sliced chilli", "Lime wedges"], ["Steaming needs almost no added fat"], ingredient_images=("ginger", "spring onion"))
R("Tuna and Sweet Corn Rice Bowl", "A quick bowl with pantry tuna, sweet corn and crunchy cucumber.", "tuna rice bowl", 10, 30,
  ["brown rice:130", "water:330", "canned tuna in water:160", "sweet corn:100", "cucumber:0.5", "tomato:1", "spring onion:2", "lime:1", "olive oil:2 tsp"],
  ["pot"], ["Simmer the rice in the water, covered, until tender.", "Drain the tuna and chop the cucumber, tomato and spring onion.", "Mix them with the sweet corn, lime juice and oil.", "Spoon over the warm rice."],
  ["Avocado slices", "A boiled egg", "Chopped chilli"], ["Lean protein and whole grains"], ingredient_images=("sweet corn", "tuna"))
R("Rice Cooker Chicken and Mushroom Rice", "A one-pot meal cooked entirely in the rice cooker.", "chicken rice", 10, 35,
  ["brown rice:140", "water:360", "chicken breast:240", "mushrooms:150", "carrot:1", "ginger:10", "garlic:2", "light soy sauce:2 tsp", "sesame oil:1 tsp"],
  ["rice cooker"], ["Rinse the rice and add it to the cooker with the water, soy sauce and sesame oil.", "Add the chopped ginger, garlic, mushrooms and carrot.", "Lay the sliced chicken on top and cook on the rice setting.", "Rest for 5 minutes, check that the chicken has reached 75°C, then fluff and serve."],
  ["Sliced cucumber", "Steamed greens"], ["One pot, whole grains and very little oil"], ingredient_images=("mushroom", "carrot"))
R("Egg and Vegetable Fried Rice", "A quick way to turn leftover-style rice into a balanced meal.", "egg fried rice", 10, 30,
  ["white rice:120", "water:250", "egg:3", "green peas:100", "carrot:1", "spring onion:2", "garlic:2", "light soy sauce:2 tsp", "cooking oil:2 tsp"],
  ["pot", "pan"], ["Simmer the rice in the water, covered, until tender, then spread out to cool.", "Fry the chopped carrot and garlic in the oil for 3 minutes.", "Scramble the eggs in the pan until set.", "Add the rice, peas and soy sauce, then toss until hot and top with spring onion."],
  ["Sliced tomato", "Stir-fried greens"], ["Eggs give filling protein", "Vegetables add fibre"], ingredient_images=("egg", "peas"))
R("Teriyaki-Style Salmon and Greens", "Glazed salmon with a light soy, ginger and honey sauce.", "salmon fillet", 10, 30,
  ["salmon fillet:240", "brown rice:110", "water:280", "broccoli:200", "light soy sauce:2 tsp", "honey:1 tsp", "ginger:10", "garlic:1"],
  ["pot", "pan"], ["Simmer the rice in the water, covered, until tender, adding the broccoli for the final 4 minutes.", "Brown the salmon in a non-stick pan for 3 to 4 minutes per side until it flakes easily.", "Mix the soy sauce, honey, chopped ginger and garlic with a splash of water.", "Add to the pan, bubble for 1 minute, then spoon over the salmon."],
  ["Sesame seeds", "Sliced cucumber"], ["Salmon is rich in omega-3 fats"], ingredient_images=("broccoli", "salmon"))
R("Beef and Pepper Stir-Fry", "Tender strips of lean beef with crisp peppers.", "beef stir fry", 10, 12,
  ["lean beef:220", "bell pepper:2", "onion:1", "garlic:2", "ginger:10", "oyster sauce:2 tsp", "water:50", "cooking oil:2 tsp"],
  ["pan"], ["Slice the beef thinly across the grain, and slice the vegetables.", "Fry the beef in the oil over high heat for 2 minutes, then set aside.", "Fry the onion, peppers, garlic and ginger for 4 minutes.", "Return the beef with the sauce and water, and toss until hot and cooked to your liking."],
  ["Brown rice", "Steamed cabbage"], ["Lean beef with plenty of vitamin-rich peppers"], ingredient_images=("bell pepper", "onion"))
R("Tofu and Mushroom Stir-Fry", "A savoury, meat-free stir-fry that comes together fast.", "tofu stir fry", 10, 12,
  ["firm tofu:300", "mushrooms:200", "broccoli:150", "garlic:2", "ginger:10", "light soy sauce:1 tbsp", "cooking oil:2 tsp"],
  ["pan"], ["Press the tofu dry and cube it, then brown in the oil for 5 minutes.", "Add the sliced mushrooms and cook for 3 minutes.", "Add the broccoli, garlic, ginger and a splash of water, then cover for 3 minutes.", "Add the soy sauce and toss."],
  ["Brown rice", "Sesame seeds", "Sliced chilli"], ["Plant protein and lots of vegetables"], ingredient_images=("tofu", "mushroom"))
R("Chicken Kurma-Style Yoghurt Curry", "A mild, creamy curry using yoghurt in place of heavy cream.", "kurma", 10, 25,
  ["chicken breast:280", "onion:1", "garlic:2", "ginger:10", "curry powder:2 tsp", "potato:1", "water:200", "plain low-fat yoghurt:120", "cooking oil:2 tsp", "salt:0.25 tsp"],
  ["pot"], ["Cook the chopped onion, garlic and ginger in the oil for 4 minutes.", "Add the curry powder, then the cubed chicken and potato, and stir for 2 minutes.", "Add the water and salt, cover and simmer for 15 minutes until the chicken reaches 75°C.", "Off the heat, stir in the yoghurt."],
  ["Brown rice", "Cucumber slices", "Coriander leaves"], ["Yoghurt adds creaminess with less saturated fat"], ingredient_images=("yogurt", "potato"))
R("Spiced Beef and Bean Chilli", "A hearty pot of lean beef, beans and tomatoes.", "chili con carne", 10, 30,
  ["lean minced beef:180", "canned kidney beans:200", "canned chopped tomatoes:300", "onion:1", "garlic:2", "bell pepper:1", "chilli powder:1 tsp", "ground cumin:1 tsp", "water:100"],
  ["pot"], ["Brown the beef in a dry pot for 5 minutes until no pink remains.", "Add the chopped onion, garlic and pepper for 4 minutes.", "Stir in the spices, then add the drained beans, tomatoes and water.", "Simmer gently for 20 minutes."],
  ["Brown rice", "Avocado slices", "Plain low-fat yoghurt"], ["Beans add fibre and stretch the lean beef"], ingredient_images=("kidney bean", "bell pepper"))
R("Tomato and Spinach Egg Shakshuka", "Eggs gently poached in a spiced tomato sauce.", "shakshuka", 5, 20,
  ["egg:4", "canned chopped tomatoes:400", "onion:1", "garlic:2", "bell pepper:1", "spinach:100", "ground cumin:1 tsp", "olive oil:2 tsp"],
  ["pan"], ["Cook the chopped onion and pepper in the oil for 5 minutes, then add the garlic and cumin.", "Add the tomatoes and simmer for 8 minutes, then stir in the spinach.", "Make 4 wells, crack in the eggs, cover and cook for 5 to 7 minutes until the whites are set and the yolks are as firm as you like."],
  ["Toasted wholemeal bread", "Coriander leaves"], ["Packed with vegetables and protein"], "Breakfast", ("tomato", "spinach"))
R("Sardine and Tomato Curry", "A thrifty, omega-3-rich store-cupboard curry.", "sardine", 5, 15,
  ["canned sardines in tomato sauce:180", "onion:1", "garlic:2", "fresh chilli:1", "tomato:2", "curry powder:1 tsp", "okra:120", "water:120"],
  ["pan"], ["Fry the chopped onion, garlic and chilli in a splash of water for 4 minutes.", "Stir in the curry powder, chopped tomatoes and okra, then simmer with the water for 8 minutes.", "Add the sardines and warm through gently for 3 minutes."],
  ["Brown rice", "Sliced cucumber"], ["Canned sardines give protein and omega-3"], ingredient_images=("okra", "tomato"))
R("Lime Chicken with Roast Sweet Potato", "Tray-baked chicken and sweet potato with bright lime.", "roast chicken", 10, 35,
  ["chicken breast:280", "sweet potato:2", "lime:1", "garlic:2", "chilli powder:1 tsp", "cooking oil:1 tbsp", "salt:0.25 tsp", "long beans:150"],
  ["oven", "baking tray"], ["Heat the oven to 200°C. Toss the cubed sweet potato with half the oil and bake for 15 minutes.", "Coat the chicken in the remaining oil, chopped garlic, chilli powder, salt and lime juice.", "Add the chicken and long beans to the tray and bake for 18 to 20 minutes until the chicken reaches 75°C."],
  ["Mixed salad", "A yoghurt and lime dip"], ["Sweet potato adds fibre and vitamin A"], ingredient_images=("sweet potato", "lime"))
R("Baked Salmon with Pumpkin", "A simple tray bake with soft pumpkin and spinach.", "baked salmon", 10, 25,
  ["salmon fillet:240", "pumpkin:350", "spinach:100", "lemon:1", "garlic:2", "olive oil:2 tsp", "salt:0.25 tsp"],
  ["oven", "baking tray"], ["Heat the oven to 200°C. Toss the cubed pumpkin with the oil and salt and bake for 12 minutes.", "Add the salmon and chopped garlic, and bake for 12 minutes until the fish flakes easily.", "Toss in the spinach for the last 2 minutes and finish with lemon juice."],
  ["Brown rice", "Steamed long beans"], ["Rich in omega-3 fats and vitamin A"], ingredient_images=("pumpkin", "lemon"))
R("Stuffed Roast Eggplant", "Eggplant filled with spiced lentils and tomato.", "stuffed eggplant", 15, 40,
  ["eggplant:2", "red lentils:80", "water:300", "onion:1", "garlic:2", "tomato:2", "ground cumin:1 tsp", "olive oil:2 tsp", "salt:0.25 tsp"],
  ["oven", "baking tray", "pot"], ["Heat the oven to 200°C. Halve the eggplants, brush with half the oil and roast for 25 minutes.", "Simmer the lentils in the water for 15 minutes, until soft and thick.", "Cook the chopped onion, garlic and tomatoes in the remaining oil with the cumin and salt, then mix with the lentils.", "Scoop some flesh from the eggplants, mix into the filling, spoon back in and bake for 10 minutes."],
  ["Mixed salad", "Yoghurt dressing"], ["High in fibre and plant protein"], ingredient_images=("lentil", "tomato"))
# Soups and salads
R("Chicken and Vegetable Soup", "A warming clear soup with lots of vegetables.", "chicken soup", 10, 25,
  ["chicken breast:220", "carrot:2", "potato:1", "cabbage:150", "onion:1", "garlic:2", "water:900", "salt:0.5 tsp", "black pepper:0.25 tsp"],
  ["pot"], ["Add the cubed chicken, chopped vegetables, garlic, water, salt and pepper to the pot.", "Bring to the boil, then simmer for 20 to 25 minutes until tender and the chicken reaches 75°C."],
  ["Wholemeal bread", "Fresh chilli and lime"], ["Very low in fat", "Hydrating and filling"], ingredient_images=("carrot", "cabbage"))
R("Pumpkin and Ginger Soup", "A velvety soup with no cream.", "pumpkin soup", 10, 25,
  ["pumpkin:500", "onion:1", "garlic:2", "ginger:15", "water:600", "light coconut milk:60", "salt:0.25 tsp", "cooking oil:1 tsp"],
  ["pot", "blender"], ["Cook the chopped onion, garlic and ginger in the oil for 4 minutes.", "Add the cubed pumpkin, water and salt, and simmer for 18 minutes.", "Blend carefully until smooth, then stir in the coconut milk and reheat."],
  ["Wholemeal toast", "Toasted sesame seeds", "A boiled egg"], ["Rich in vitamin A and low in fat"], ingredient_images=("pumpkin", "ginger"))
R("Tomato and Lentil Soup", "A thick, satisfying soup from pantry staples.", "lentil soup", 5, 25,
  ["red lentils:120", "canned chopped tomatoes:400", "onion:1", "carrot:1", "garlic:2", "ground cumin:1 tsp", "water:700", "lemon:0.5", "cooking oil:2 tsp"],
  ["pot"], ["Cook the chopped onion, carrot and garlic in the oil for 4 minutes.", "Add the cumin, lentils, tomatoes and water.", "Simmer for 20 minutes, then finish with lemon juice."],
  ["Wholemeal toast", "Plain low-fat yoghurt on top"], ["High in fibre and plant protein"], ingredient_images=("lentil", "carrot"))
R("Fish and Tomato Clear Soup", "A light, tangy soup that's ready quickly.", "fish soup", 10, 12,
  ["white fish fillet:280", "tomato:2", "cabbage:150", "ginger:15", "spring onion:2", "water:800", "fish sauce:2 tsp", "lime:1"],
  ["pot"], ["Simmer the sliced tomato, ginger, cabbage and water for 6 minutes.", "Add the fish and fish sauce and cook gently for 5 minutes until it flakes easily.", "Finish with lime juice and spring onion."],
  ["Steamed rice", "Chopped fresh chilli"], ["Lean, low in fat and very light"], ingredient_images=("tomato", "ginger"))
R("Mushroom and Egg Drop Soup", "A silky soup with mushrooms and ribbons of egg.", "egg drop soup", 5, 12,
  ["mushrooms:250", "egg:3", "spinach:100", "garlic:2", "ginger:10", "water:800", "light soy sauce:2 tsp", "sesame oil:1 tsp"],
  ["pot"], ["Simmer the sliced mushrooms, garlic, ginger and water for 6 minutes.", "Add the soy sauce and spinach.", "Slowly pour in the beaten eggs while stirring gently, and cook for 2 minutes until set.", "Finish with the sesame oil."],
  ["Steamed rice", "Wholemeal toast"], ["High in protein and low in carbohydrate"], "Breakfast", ("mushroom", "spinach"))
R("Chickpea and Cucumber Salad", "A fresh no-cook salad with a lime dressing.", "chickpea salad", 10, 0,
  ["canned chickpeas:300", "cucumber:1", "tomato:2", "onion:0.5", "coriander leaves:15", "lime:1", "olive oil:1 tbsp", "salt:0.25 tsp"],
  ["mixing bowl"], ["Drain the chickpeas and chop the vegetables and coriander leaves.", "Whisk the lime juice, oil and salt in a bowl.", "Toss everything together and rest for 5 minutes."],
  ["Wholemeal wrap", "Grilled chicken", "Avocado slices"], ["No cooking, high in fibre"], ingredient_images=("cucumber", "chickpea"))
R("Tuna, Egg and Potato Salad", "A filling warm salad with a mustard-free lemon dressing.", "tuna salad", 10, 15,
  ["canned tuna in water:160", "egg:2", "potato:2", "long beans:120", "tomato:1", "lemon:1", "olive oil:1 tbsp", "lettuce:80"],
  ["pot"], ["Boil the cubed potatoes for 10 minutes, adding the long beans for the last 3 minutes, then drain.", "Boil the eggs for 8 minutes in a separate pot, then cool and quarter them.", "Whisk the lemon juice and oil.", "Toss everything with the drained tuna, tomato and lettuce."],
  ["Wholemeal bread", "Chopped spring onion"], ["High in protein with a light dressing"], ingredient_images=("potato", "lettuce"))
R("Mango and Prawn Salad", "Sweet mango with prawns, cucumber and a chilli-lime dressing.", "mango salad", 15, 5,
  ["prawns:220", "mango:130", "cucumber:1", "lettuce:100", "fresh chilli:1", "lime:2", "fish sauce:1 tsp", "cooking oil:1 tsp"],
  ["pan"], ["Fry the prawns in the oil for 2 to 3 minutes until pink and firm.", "Slice the mango, cucumber and chilli, and tear the lettuce.", "Mix the lime juice and fish sauce, then toss with everything."],
  ["Steamed rice or rice noodles", "Fresh coriander leaves"], ["Light and rich in vitamin C"], ingredient_images=("mango", "cucumber"))
# Noodles, pasta and wraps
R("Rice Noodles with Chicken and Vegetables", "Stir-fried bihun with chicken and crisp vegetables.", "bihun goreng", 10, 12,
  ["rice noodles:110", "chicken breast:220", "cabbage:150", "carrot:1", "bean sprouts:80", "garlic:2", "light soy sauce:2 tsp", "cooking oil:2 tsp"],
  ["pan", "pot"], ["Soak or boil the noodles according to the pack, then drain.", "Fry the sliced chicken in the oil for 6 minutes until it reaches 75°C.", "Add the garlic, shredded cabbage and carrot for 3 minutes.", "Add the noodles, sprouts and soy sauce, and toss until hot."],
  ["Lime wedges", "Sliced chilli"], ["Balanced with protein and vegetables"], ingredient_images=("carrot", "cabbage"))
R("Wholewheat Tomato and Tuna Pasta", "A store-cupboard pasta that's ready in 20 minutes.", "tuna pasta", 5, 15,
  ["wholewheat pasta:140", "canned tuna in water:160", "canned chopped tomatoes:300", "onion:1", "garlic:2", "spinach:80", "olive oil:2 tsp", "water:1000"],
  ["pot", "pan"], ["Boil the pasta in the water according to the pack, then drain.", "Cook the chopped onion and garlic in the oil for 4 minutes.", "Add the tomatoes and simmer for 8 minutes.", "Stir in the tuna, spinach and pasta until hot."],
  ["Mixed salad", "A little grated cheddar cheese"], ["Whole grains with lean protein"], ingredient_images=("tuna", "spinach"))
R("Wholewheat Mushroom Bolognese", "A rich-tasting sauce with lean beef and mushrooms.", "bolognese", 10, 30,
  ["wholewheat pasta:130", "lean minced beef:140", "mushrooms:200", "canned chopped tomatoes:300", "onion:1", "carrot:1", "garlic:2", "water:1000"],
  ["pot", "pan"], ["Brown the beef in a dry pan for 5 minutes until no pink remains.", "Add the chopped onion, carrot, mushrooms and garlic for 6 minutes.", "Add the tomatoes and simmer for 15 minutes.", "Boil the pasta in the water according to the pack, drain and mix with the sauce."],
  ["Green salad", "A little grated cheddar cheese"], ["Mushrooms replace some of the meat"], ingredient_images=("mushroom", "carrot"))
R("Peanut Chicken Noodle Salad", "Cold noodles with chicken and a small amount of peanut sauce.", "noodle salad", 15, 15,
  ["rice noodles:100", "chicken breast:200", "cucumber:1", "carrot:1", "peanuts:25", "lime:1", "light soy sauce:2 tsp", "fresh chilli:1", "water:900"],
  ["pot", "blender"], ["Poach the chicken in the simmering water for 12 minutes until it reaches 75°C, then shred.", "Cook the noodles in the same water, then drain and cool.", "Blend the peanuts, lime juice, soy sauce and chilli with a splash of water.", "Toss with the shredded cucumber and carrot."],
  ["Coriander leaves", "Bean sprouts"], ["Lots of raw vegetables and lean protein"], ingredient_images=("peanuts", "cucumber"))
R("Chicken and Avocado Wrap", "A quick no-mess lunch with yoghurt dressing.", "chicken wrap", 10, 10,
  ["wholemeal tortilla wrap:2", "chicken breast:180", "avocado:0.5", "lettuce:60", "tomato:1", "plain low-fat yoghurt:40", "lime:0.5", "cooking oil:1 tsp"],
  ["pan"], ["Fry the sliced chicken in the oil for 6 to 8 minutes until it reaches 75°C.", "Mix the yoghurt and lime juice.", "Fill the wraps with lettuce, tomato, avocado and chicken, then add the dressing and roll."],
  ["Apple slices", "Sliced cucumber"], ["Avocado gives unsaturated fat"], ingredient_images=("avocado", "lettuce"))
R("Egg and Spinach Breakfast Wrap", "A protein-rich wrap you can eat on the go.", "breakfast burrito", 5, 8,
  ["wholemeal tortilla wrap:2", "egg:3", "spinach:100", "tomato:1", "fresh chilli:1", "cooking oil:1 tsp"],
  ["pan"], ["Wilt the spinach with the chopped tomato and chilli in the oil for 2 minutes.", "Add the beaten eggs and scramble until set.", "Divide between the wraps and roll."],
  ["Banana", "Plain low-fat yoghurt"], ["Protein and greens for breakfast"], "Breakfast", ("spinach", "egg"))
R("Sardine Toast with Tomato and Cucumber", "A fast, omega-3-rich open sandwich.", "sardine toast", 5, 5,
  ["wholemeal bread:4", "canned sardines in tomato sauce:120", "tomato:1", "cucumber:0.5", "lime:0.5"],
  ["pan"], ["Toast the bread in a dry pan until golden.", "Mash the sardines lightly with the lime juice.", "Spread on the toast and top with sliced tomato and cucumber."],
  ["Fresh fruit", "Sliced chilli"], ["Whole grains with omega-3 fats"], "Breakfast", ("cucumber", "tomato"))
# Breakfasts and snacks
R("Banana Cinnamon Oats", "Warm porridge sweetened with fruit.", "oatmeal", 2, 8,
  ["rolled oats:100", "low-fat milk:300", "water:150", "banana:1", "ground cinnamon:0.5 tsp"],
  ["pot"], ["Simmer the oats, milk and water for 5 minutes, stirring often.", "Stir in the cinnamon and half the sliced banana.", "Top with the remaining banana."],
  ["Toasted almonds", "A spoon of plain low-fat yoghurt"], ["No added sugar", "High in fibre"], "Breakfast", ("banana", "oat"))
R("Overnight Apple Oats", "A no-cook breakfast you prepare the night before.", "overnight oats", 5, 0,
  ["rolled oats:90", "plain low-fat yoghurt:150", "low-fat milk:180", "apple:0.75", "ground cinnamon:0.5 tsp"],
  ["mixing bowl"], ["Mix the oats, yoghurt, milk and cinnamon in a bowl.", "Cover and refrigerate overnight.", "Top with the chopped apple before serving."],
  ["Sliced banana", "Toasted sesame seeds"], ["High in fibre and protein", "No added sugar"], "Breakfast", ("apple", "oat"))
R("Vegetable Omelette", "A fluffy omelette packed with vegetables.", "omelette", 5, 8,
  ["egg:4", "mushrooms:100", "tomato:1", "spring onion:2", "bell pepper:0.5", "cooking oil:1 tsp", "black pepper:0.25 tsp"],
  ["pan"], ["Fry the chopped mushrooms and pepper in the oil for 3 minutes.", "Add the tomato and spring onion for 1 minute.", "Pour in the eggs beaten with black pepper, and cook gently until set."],
  ["Wholemeal toast", "Sliced avocado"], ["High in protein with lots of vegetables"], "Breakfast", ("egg", "mushroom"))
R("Banana Oat Pancakes", "Simple pancakes with no added sugar or wheat flour.", "banana pancakes", 5, 10,
  ["banana:2", "egg:2", "rolled oats:80", "ground cinnamon:0.5 tsp", "cooking oil:1 tsp"],
  ["pan", "blender"], ["Blend the bananas, eggs, oats and cinnamon until smooth.", "Lightly oil a non-stick pan and cook small pancakes for 2 minutes per side until set."],
  ["Plain low-fat yoghurt", "Fresh mango"], ["Sweetened with fruit only"], "Breakfast", ("banana", "oat"))
R("Mango Yoghurt Smoothie", "A cooling, protein-rich drink.", "mango smoothie", 5, 0,
  ["mango:100", "rolled oats:40", "plain low-fat yoghurt:200", "low-fat milk:120"],
  ["blender"], ["Add everything to the blender.", "Blend until smooth and serve cold."],
  ["Toasted sesame seeds", "A little lime juice"], ["No added sugar", "Oats add fibre to this protein-rich drink"], "Breakfast", ("mango", "yogurt"))
R("Sweet Potato and Tomato Hash", "A savoury pan of sweet potato topped with eggs.", "sweet potato hash", 10, 20,
  ["sweet potato:2", "onion:1", "bell pepper:1", "egg:2", "chilli powder:0.5 tsp", "cooking oil:2 tsp"],
  ["pan"], ["Fry the small cubes of sweet potato in the oil, covered, for 10 minutes.", "Add the chopped onion, pepper and chilli powder and cook for 5 minutes.", "Make 2 wells, crack in the eggs, cover and cook until the whites are set."],
  ["Fresh tomato salad", "Chopped coriander leaves"], ["Rich in fibre and vitamin A"], "Breakfast", ("sweet potato", "bell pepper"))
