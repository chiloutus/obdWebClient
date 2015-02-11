__author__ = 'GaryPC'
import os,random
def get_random_line():
    total_bytes = os.stat('longWords.txt').st_size
    random_point = random.randint(0, total_bytes)
    file = open('longWords.txt')
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    return file.readline()#variables

def checkWords(words):
    shortWord = open("shortWords.txt", "r")

    count = 0
    line = ""
    #print(l[2])
    usrin = input("Your word is:" + line + " Please find words that are contained within!")
    count = len(usrin)
    for usrin in words:
        if usrin in shortWord:
            print("Hey!")
            for i in usrin:
                if i in line:
                    count -= 1
                    print("I'm over here now")
            if count == 0:
                print("Good Job")
                print(count)


print(get_random_line())


def savegamedata():
    words = request.form['word1'],request.form['word2'],request.form['word3'],request.form['word4'],request.form['word5'],request.form['word6'],request.form['word7']
    t = Thread(target=update_log, args=(request.form['user_name'], request.form['the_comment']))
    t.start()
    if checkWords(request.form(the_word),words):
        return render_template("thanks.html",
                               the_title="Thanks!",
                               the_user=request.form['user_name'],
                               home_link=url_for("display_home"), )
    else:
        return redirect(url_for("getacomment"))

