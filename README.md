# Macro-Based Recipe Recommender
Link to the website: [https://macro-based-recipes.onrender.com/]

## Motivation
As a content creator, some of my most viral social media videos revolved around food—specifically, what I ate to maintain my physique. These videos inspired countless questions from followers asking, "What should I eat to hit my macros?" While there are tools out there to track macros, I couldn’t find any platforms that made it easy to **discover recipes tailored to specific macro goals**. Most existing tools were either clunky, hard to use, or simply didn’t deliver good results.

This project is my solution: a simple and intuitive **macro-based recipe recommender**. It allows users to input their daily macro goals, divide them across meals, and instantly find recipes that fit their nutritional needs. Whether you're looking to hit your protein targets or balance your carbs and fats, this tool is designed to make macro-based meal planning effortless.

---

## Technical Details

### The Challenge of Recipe Search
To recommend recipes that match user-defined macros (calories, protein, carbs, and fats), the tool needed a robust search algorithm. Initially, I implemented a **deviation-based algorithm**. This method calculated how far each recipe's macros deviated from the user's target macros. While functional, it had some critical pitfalls.

#### **Example of the Deviation Algorithm's Shortcomings**
Consider a user’s target macros per meal:
- **Calories**: 833
- **Protein**: 58g
- **Carbs**: 67g
- **Fats**: 20g

A dessert recipe with the following macros might rank high using the deviation algorithm:
- **Calories**: 802
- **Protein**: 14g
- **Carbs**: 91g
- **Fats**: 42g

Despite being a poor match (low protein, high fat), it scored well because it matched calories and carbs closely. This exposed the deviation algorithm’s inability to **prioritize critical macros like protein** effectively.

---

### Transition to K-Nearest Neighbors (KNN)

To overcome these limitations, I transitioned to a **K-Nearest Neighbors (KNN)** algorithm. KNN evaluates recipes in a multidimensional space where each dimension corresponds to a macro (calories, protein, carbs, and fats). This approach allows the algorithm to:
- Prioritize critical macros (e.g., protein) by normalizing data and adjusting weights.
- Consider the overall balance of all macros instead of overly favoring individual ones.
- Find the "closest" recipes to the target macros, ensuring recommendations are more relevant.

#### **Why KNN Works Better**
Using the same example above, KNN effectively penalizes recipes like the dessert by:
- Considering protein mismatch as a higher-priority factor.
- Taking all macros into account proportionally.
  
It consistently ranks recipes like "Steak Dinner" or "Grilled Salmon" higher, which are better fits for the user’s macro goals.

---

## Key Features
- **Macro Customization**: Input your daily macro goals (calories, protein, carbs, fats) and divide them across meals.
- **Dynamic Recipe Search**: Find recipes tailored to your macro needs using a sophisticated KNN algorithm.
- **Beautiful Results**: View recipes with images, nutritional details, and links to instructions.
- **Meal Flexibility**: Adjust the number of meals per day to refine your search.

---

## How It Works
1. **Input Your Goals**: Enter your daily macros and the number of meals per day.
2. **Search for Recipes**: The tool divides your macros by meals and searches the recipe database using KNN.
3. **Get Results**: View ranked recipes that closely match your macro targets.

---

## Future Improvements
This project is a work in progress, and there are several exciting features I’d like to add in the future:

1. **Dietary Restrictions**:
   - Allow users to filter recipes based on dietary preferences or restrictions (e.g., vegan, gluten-free, keto).

2. **Meal Types**:
   - Add filters for meal categories such as breakfast, lunch, dinner, or dessert to refine results.

3. **Expand the Recipe Database**:
   - Continuously grow the recipe database to include more diverse and global meal options.

4. **Link Ingredients to Instacart**:
   - Integrate with services like Instacart to allow users to easily shop for ingredients directly from recipe results. This feature would depend on attracting enough user interest.

5. **Enhanced Recommendations**:
   - Incorporate machine learning to offer personalized recipe suggestions based on user history or preferences.

---

This project is not just a tool—it’s an extension of my journey to inspire others to achieve their fitness goals. Whether you're building muscle, cutting weight, or simply eating healthier, I hope this recommender makes your macro-tracking journey easier.
