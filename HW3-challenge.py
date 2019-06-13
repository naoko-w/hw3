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
  operater = {'type': 'PLUS'}
  priority = p + 1
  return operater, index + 1, priority


def readMinus(line, index, p):
  operater = {'type': 'MINUS'}
  priority = p + 1
  return operater, index + 1, priority


def readMultipled(line, index, p):
  operater = {'type': 'MULTI'}
  priority = p + 2
  return operater, index + 1, priority


def readDevided(line, index, p):
  operater = {'type': 'DEVIDED'}
  priority = p + 2
  return operater, index + 1, priority


def readParentheses1(line, index, p):
  p += 10
  return index + 1, p


def readParentheses2(line, index, p):
  p -= 10
  return index + 1, p


def tokenize(line):
  Priority = []
  Number = []
  Operater = []
  index = 0
  p = 0
  while index < len(line):
    if line[index].isdigit():
      (number, index) = readNumber(line, index)
      Number.append(number)
    elif line[index] == '+' or line[index] =='-' or line[index] =='*' or line[index] == '/':
        if line[index] == '+':
            (operater, index, priority) = readPlus(line, index, p)
        elif line[index] == '-':
            (operater, index, priority) = readMinus(line, index, p)
        elif line[index] == '*':
            (operater, index, priority) = readMultipled(line, index, p)
        elif line[index] == '/':
            (operater, index, priority) = readDevided(line, index, p)
        Priority.append(priority)
        Operater.append(operater)
    elif line[index] == '(':
      (index, p) = readParentheses1(line, index, p)
    elif line[index] == ')':
      (index, p) = readParentheses2(line, index, p)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
  return Number, Operater, Priority


def evaluate(Number, Operater, Priority):
  answer = 0
  count = 0
  Operater.insert(len(Operater)+1, "+") #dammy
  Priority.insert(len(Priority)+1, "0") #dammy
  Number.insert(len(Number)+1, "0") #dammy
  while len(Operater) - count > 1: #insert分だけ+1
    imax = 0
    i = 1
    while len(Priority) - count > i + 1: #insert分だけ+1
      if Priority[imax] < int(Priority[i]):
        imax = i
      i += 1
    if Operater[imax]['type'] == 'PLUS':
      Number[imax] += Number[imax + 1]
    elif Operater[imax]['type'] == 'MINUS':
      Number[imax] -= Number[imax + 1]
    elif Operater[imax]['type'] == 'MULTI':
      Number[imax] *= Number[imax + 1]
    elif Operater[imax]['type'] == 'DEVIDED':
      Number[imax] /= Number[imax + 1]
    j = imax + 1
    while j < len(Priority):
      Number[j] = Number[j + 1]
      Operater[j - 1] = Operater[j]
      Priority[j - 1] = Priority[j]
      j += 1
    count += 1
  answer = Number[imax]   
  return answer  
   
def test(line):
  (Number, Operater, Priority) = tokenize(line)
  actualAnswer = evaluate(Number, Operater, Priority)
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
  (Number, Operater, Priority) = tokenize(line)
  answer = evaluate(Number, Operater, Priority)
  print("answer = %f\n" % answer)
