
questions = ["What is our name?", "What is your Age?", "Are you tired?"]
answerSet = ["Bharat", "25", "no"]


def setQuestion():
    questions = []
    more = "y"
    while more == "y":
        question = input("Ask a question: \n")
        questions.append(question)
        print("Cool, saved \n")
        print("\n")
        more = input("Do you have new questions ? \n")
        if more != "y":
            break


def askQuestion():
    for question in questions:
        answer = input(question)
        answerSet.append(answer)
    print(answerSet)
    print("\n")
    print("\n")



def countList(lst1, lst2): 
    return [sub[item] for item in range(len(lst2)) for sub in [lst1, lst2]] 


def publishQuiz():
    print(countList(questions, answerSet))
    print("\n")
    print("\n")


def main():
    print("Welcome to Quiz Master \n")
    print("\n")
    rew = "0"
    while rew != "x":
        print("What do you want to do?")
        rew = input(" 1: Publish Answers, 2: ask Questions, 3: setQuestion, x: to exit \n")
        print("\n")
        print("\n")
        if rew == "1":
            publishQuiz()
        elif rew =="2":
            askQuestion()
        elif rew =="3":
            setQuestion()
        elif rew == "x":
            print("Thank you")
            exit()
        else:
            print("Invalid Key \n")



if __name__ == "__main__":
    main()