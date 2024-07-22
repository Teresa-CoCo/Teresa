def bmicalculator(weight,height):
    bmi = weight / (height * height)
    if bmi < 18.5:
        result = "你的BMI是"+bmi+"有点瘦"
        return result
    elif bmi >= 18.5 and bmi < 24:
        result = "你的BMI是"+bmi+"不错"
        return result
    elif bmi >= 24:
        result = "你的BMI是"+bmi+"有点肥胖"
        return result