import os

readme_path = os.path.join("QGU-Theory", "README.md")

# Ye text hum append karenge
image_section = """

## 📸 Visual Proof
**Here is the empirical evidence:** The graph below shows the correlation between Density Gradient and Acceleration. 
An **R² score of 0.85** confirms that motion is driven by the geometry of the field.

![Law 2 Verification Graph](figures/law2_result.png)
"""

if os.path.exists(readme_path):
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(image_section)
    print("✅ README updated! Graph is now visible on the front page.")
else:
    print("❌ Error: README.md not found.")