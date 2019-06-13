def readNumber(line, index): 
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  return number, index


def readPlus(line, index, p):
  operator = {'type': 'PLUS'}
  priority = p + 1
  return operator, index + 1, priority


def readMinus(line, index, p):
  operator = {'type': 'MINUS'}
  priority = p + 1
  return operator, index + 1, priority


def readMultipled(line, index, p):
  operator = {'type': 'MULTI'}
  priority = p + 2
  return operator, index + 1, priority


def readDevided(line, index, p):
  operator = {'type': 'DEVIDED'}
  priority = p + 2
  return operator, index + 1, priority


def readParentheses1(line, index, p):
  p += 10
  return index + 1, p


def readParentheses2(line, index, p):
  p -= 10
  return index + 1, p


def tokenize(line):
  Priority = []
  Number = []
  Operator = []
  index = 0
  p = 0
  while index < len(line):
    if line[index].isdigit():
      (number, index) = readNumber(line, index)
      Number.append(number) #数字は配列Numberに入れる
    elif line[index] == '+' or line[index] =='-' or line[index] =='*' or line[index] == '/':
        if line[index] == '+':
            (operator, index, priority) = readPlus(line, index, p)
        elif line[index] == '-':
            (operator, index, priority) = readMinus(line, index, p)
        elif line[index] == '*':
            (operator, index, priority) = readMultipled(line, index, p)
        elif line[index] == '/':
            (operator, index, priority) = readDevided(line, index, p)
        Priority.append(priority) #演算子の優先度を配列Priorityに入れる
        Operator.append(operator) #演算子は配列Operatorに入れる
    elif line[index] == '(':
      (index, p) = readParentheses1(line, index, p)
    elif line[index] == ')':
      (index, p) = readParentheses2(line, index, p)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
  return Number, Operator, Priority


def maxpriority(Priority, count):
  i = 1
  imax = 0
  while len(Priority) - count > i:
    if Priority[imax] < int(Priority[i]):
      imax = i
    i += 1
  return imax, Priority, count

def organize(Number, Operator, Priority, imax, count):
  j = imax + 1
  while j < len(Priority) - count:
    Number[j] = Number[j + 1]
    Operator[j - 1] = Operator[j]
    Priority[j - 1] = Priority[j]
    j += 1
  return Number, Operator, Priority, count


def evaluate(Number, Operator, Priority):
  answer = 0
  count = 0
  while len(Operator) - count > 0:
    (imax, Priority, count) = maxpriority(Priority, count) #最も優先度の高い演算子を見つける
    if Operator[imax]['type'] == 'PLUS':
      Number[imax] += Number[imax + 1]
    elif Operator[imax]['type'] == 'MINUS':
      Number[imax] -= Number[imax + 1]
    elif Operator[imax]['type'] == 'MULTI':
      Number[imax] *= Number[imax + 1]
    elif Operator[imax]['type'] == 'DEVIDED':
      Number[imax] /= Number[imax + 1]
    (Number, Operator, Priority, count) = organize(Number, Operator, Priority, imax, count) #数字、演算子を１つずつずらし、配列を整理
    count += 1
  answer = Number[imax]   
  return answer  


def test(line):
  (Number, Operator, Priority) = tokenize(line)
  actualAnswer = evaluate(Number, Operator, Priority)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("3*4+4*6-9/3") #整数のみの加減乗除
  test("2.5*4+12.25*8.0-120/2.5") #小数を含む加減乗除
  test("1.25*8*5/30-3.3*2.2/8*5+2.8/3*1.35") #無限小数を含む加減乗除
  test("10*(3+6)/3") #カッコを含む数式
  test("10*(2.5+7.5-9/3.0/2*10+5)") #カッコ内に加減乗除をすべて含む数式
  test("2.6*(5.9+1.6*(75+15)/8)-5") #２重カッコ
  test("10*(5+5)/(1+1)") #カッコ/カッコ
  test("(6*(5+(6-3.5)*2)-10)/1.8*10+2") #３重カッコ
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  (Number, Operator, Priority) = tokenize(line) #入力された文字列を解析し、Number、Operaterに振り分け
  answer = evaluate(Number, Operator, Priority) #Priorityにて計算優先度を参照しながら計算
  print("answer = %f\n" % answer)
