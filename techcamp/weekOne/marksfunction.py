maths = int(input("Enter maths: "))
english = int(input("Enter English: "))
kiswahili = int(input("Enter Kiswahili: "))
science = int(input("Enter Science: "))
social = int(input("Enter Social: "))


def calculateTotalMarks(maths, english, kiswahili, science, social):
    total = maths + english + kiswahili + science + social
    print("total marks is: ", total)
    return total


def calculateAverageMarks(total):
    average = total/5
    print("Average marks is: ", average)
    return average


def calculateGrade(average):
    if average > 0 and average <= 40:
        print("Grade E")
    elif average > 40 and average <= 51:
        print("Grade C")
    elif average > 50 and average <= 61:
        print("Grade B")
    else:
        print("Grade is A")


calculateTotalMarks(maths, english, kiswahili, science, social)
calculateAverageMarks(calculateTotalMarks)
calculateGrade(calculateAverageMarks)
